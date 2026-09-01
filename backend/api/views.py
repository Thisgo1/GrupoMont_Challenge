import calendar
from datetime import date, datetime
from decimal import Decimal
from django.db.models import Avg
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics


from .models import (
    MontseguroLead, MontseguroFunil, MontseguroClienteAtivo,
    Prop5Lead, Prop5Oportunidade,
    TechbraboLead, TechbraboOportunidade, TechbraboProjeto,
    Marketing, MetaEmpresa, Empresa,
)
from .serializers import (
    MontseguroFunilSerializer, MontseguroClienteAtivoSerializer,
    Prop5OportunidadeSerializer,
    TechbraboOportunidadeSerializer, TechbraboProjetoSerializer,
    MarketingSerializer, MetaEmpresaSerializer,
)

COMISSAO_MONTSEGURO = Decimal("0.15")


def limites_do_mes(mes_str):
    """'2026-08' -> (date(2026,8,1), date(2026,8,31))"""
    ano, mes = map(int, mes_str.split("-"))
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    return date(ano, mes, 1), date(ano, mes, ultimo_dia)


def mes_mais_recente(queryset, campo="mes_referencia"):
    """Pega o mês mais recente presente nos dados, caso o front não passe ?mes=."""
    valor = queryset.order_by(f"-{campo}").values_list(campo, flat=True).first()
    return valor


# ---------------------------------------------------------------
# MONTSEGURO — endpoint de KPIs COMPLETO (padrão de referência).
# Cada bloco abaixo corresponde a um KPI documentado em kpis-grupo-mont.md.
# ---------------------------------------------------------------
class MontseguroKpisView(APIView):
    def get(self, request):
        mes = request.query_params.get("mes") or mes_mais_recente(MontseguroLead.objects.all())
        if mes is None:
            return Response({"detail": "Sem dados carregados."}, status=404)

        inicio_mes, fim_mes = limites_do_mes(mes)

        leads_no_mes = MontseguroLead.objects.filter(mes_referencia=mes).count()

        funil_mes = MontseguroFunil.objects.filter(
            data_contratacao__gte=inicio_mes, data_contratacao__lte=fim_mes
        )
        contratacoes_no_mes = funil_mes.count()

        implantacoes_no_mes = MontseguroFunil.objects.filter(
            data_implantacao__gte=inicio_mes, data_implantacao__lte=fim_mes
        ).count()

        # --- Taxa de conversão lead -> contratação ---
        # Aproximação de mês corrido: contratações fechadas no mês / leads
        # criados no mesmo mês. Não é uma leitura por coorte (uma contratação
        # de agosto pode ter vindo de um lead de julho), mas é a leitura
        # padrão de "ritmo do mês" usada em dashboards executivos.
        taxa_conversao_lead_contratacao = (
            round(contratacoes_no_mes / leads_no_mes * 100, 1) if leads_no_mes else None
        )

        # --- Taxa de implantação ---
        taxa_implantacao = (
            round(implantacoes_no_mes / contratacoes_no_mes * 100, 1) if contratacoes_no_mes else None
        )

        # --- Vidas ativas e receita de comissão (base ativa no fim do mês) ---
        clientes_ativos_no_mes = MontseguroClienteAtivo.objects.filter(
            data_ativacao__lte=fim_mes
        ).exclude(cancelado=True, data_cancelamento__lte=fim_mes)

        vidas_ativas = clientes_ativos_no_mes.aggregate(total=Sum("vidas_ativas"))["total"] or 0
        premio_total = clientes_ativos_no_mes.aggregate(total=Sum("premio_mensal"))["total"] or Decimal("0")
        receita_comissao_mes = round(premio_total * COMISSAO_MONTSEGURO, 2)

        # --- Ticket médio (prêmio mensal médio dos contratos implantados no mês) ---
        implantados_no_mes = MontseguroFunil.objects.filter(
            data_implantacao__gte=inicio_mes, data_implantacao__lte=fim_mes
        )
        ticket_medio = None
        if implantados_no_mes.exists():
            soma = implantados_no_mes.aggregate(total=Sum("premio_mensal_estimado"))["total"]
            ticket_medio = round(soma / implantados_no_mes.count(), 2)

        # --- CAC ---
        investimento_mkt = Marketing.objects.filter(
            empresa=Empresa.MONTSEGURO, mes=mes
        ).aggregate(total=Sum("investimento"))["total"] or Decimal("0")
        cac = round(investimento_mkt / implantacoes_no_mes, 2) if implantacoes_no_mes else None

        # --- Churn (cancelamentos no mês / ativos no início do mês) ---
        ativos_inicio_mes = MontseguroClienteAtivo.objects.filter(
            data_ativacao__lt=inicio_mes
        ).exclude(cancelado=True, data_cancelamento__lt=inicio_mes).count()
        cancelamentos_no_mes = MontseguroClienteAtivo.objects.filter(
            cancelado=True, data_cancelamento__gte=inicio_mes, data_cancelamento__lte=fim_mes
        ).count()
        taxa_churn = (
            round(cancelamentos_no_mes / ativos_inicio_mes * 100, 1) if ativos_inicio_mes else None
        )

        # --- Atingimento de meta ---
        meta = MetaEmpresa.objects.filter(empresa=Empresa.MONTSEGURO, mes=mes).first()
        atingimento_meta = (
            round(float(receita_comissao_mes) / float(meta.meta_receita) * 100, 1)
            if meta and meta.meta_receita else None
        )

        return Response({
            "mes": mes,
            "leads_no_mes": leads_no_mes,
            "contratacoes_no_mes": contratacoes_no_mes,
            "implantacoes_no_mes": implantacoes_no_mes,
            "taxa_conversao_lead_contratacao_pct": taxa_conversao_lead_contratacao,
            "taxa_implantacao_pct": taxa_implantacao,
            "vidas_ativas": vidas_ativas,
            "receita_comissao_mes": receita_comissao_mes,
            "ticket_medio_premio_mensal": ticket_medio,
            "cac": cac,
            "taxa_churn_pct": taxa_churn,
            "meta_receita": meta.meta_receita if meta else None,
            "atingimento_meta_pct": atingimento_meta,
        })

# ---------------------------------------------------------------
# PROP5 — pipeline consultivo de alto valor: valor de imóvel != receita,
# pipeline != venda fechada, ciclo longo
# ---------------------------------------------------------------
class Prop5KpisView(APIView):
    def get(self, request):
        mes = request.query_params.get("mes") or mes_mais_recente(Prop5Lead.objects.all())
        if mes is None:
            return Response({"detail": "Sem dados carregados."}, status=404)

        inicio_mes, fim_mes = limites_do_mes(mes)

        leads_no_mes = Prop5Lead.objects.filter(mes_referencia=mes).count()

        # --- Fechamentos e receita realizada (comissão, não valor do imóvel) ---
        fechamentos_no_mes = Prop5Oportunidade.objects.filter(
            estagio="Fechado", data_fechamento__gte=inicio_mes, data_fechamento__lte=fim_mes
        )
        n_fechamentos = fechamentos_no_mes.count()
        receita_comissao_mes = fechamentos_no_mes.aggregate(total=Sum("comissao"))["total"] or Decimal("0")

        # --- Pipeline ponderado ---
        # Limitação assumida: não guardamos histórico de mudança de estágio,
        # então isto é uma fotografia do estado ATUAL das oportunidades abertas
        # criadas até o fim do mês consultado — não "como o pipeline estava"
        # naquele momento passado. Pra rastrear isso de verdade seria preciso
        # uma tabela de histórico de estágio por oportunidade.
        pipeline_aberto = Prop5Oportunidade.objects.filter(
            lead__data_criacao__lte=fim_mes
        ).exclude(estagio__in=["Fechado", "Perdido"]).select_related("lead")
        pipeline_ponderado = sum(
            (op.valor_estimado * (op.probabilidade or Decimal("0"))) for op in pipeline_aberto
        )
        pipeline_ponderado = round(pipeline_ponderado, 2)

        # --- Taxa de conversão lead -> fechamento (mesma aproximação de mês
        # corrido já documentada na MontseguroKpisView) ---
        taxa_conversao = round(n_fechamentos / leads_no_mes * 100, 1) if leads_no_mes else None

        # --- Ciclo médio de venda (dias entre criação do lead e fechamento) ---
        dias_ciclo = [
            (op.data_fechamento - op.lead.data_criacao).days
            for op in fechamentos_no_mes.select_related("lead")
            if op.data_fechamento and op.lead.data_criacao
        ]
        ciclo_medio_dias = round(sum(dias_ciclo) / len(dias_ciclo), 1) if dias_ciclo else None

        # --- Ticket médio por operação fechada ---
        ticket_medio = None
        if n_fechamentos:
            soma_valor_fechado = fechamentos_no_mes.aggregate(total=Sum("valor_fechado"))["total"] or Decimal("0")
            ticket_medio = round(soma_valor_fechado / n_fechamentos, 2)

        # --- CAC ---
        investimento_mkt = Marketing.objects.filter(
            empresa=Empresa.PROP5, mes=mes
        ).aggregate(total=Sum("investimento"))["total"] or Decimal("0")
        cac = round(investimento_mkt / n_fechamentos, 2) if n_fechamentos else None

        # --- Atingimento de meta ---
        meta = MetaEmpresa.objects.filter(empresa=Empresa.PROP5, mes=mes).first()
        atingimento_meta = (
            round(float(receita_comissao_mes) / float(meta.meta_receita) * 100, 1)
            if meta and meta.meta_receita else None
        )

        return Response({
            "mes": mes,
            "leads_no_mes": leads_no_mes,
            "fechamentos_no_mes": n_fechamentos,
            "receita_comissao_mes": receita_comissao_mes,
            "pipeline_ponderado": pipeline_ponderado,
            "taxa_conversao_lead_fechamento_pct": taxa_conversao,
            "ciclo_medio_dias": ciclo_medio_dias,
            "ticket_medio_fechado": ticket_medio,
            "cac": cac,
            "meta_receita": meta.meta_receita if meta else None,
            "atingimento_meta_pct": atingimento_meta,
        })


def _mrr_ate(fim_mes):
    """Soma o MRR de todos os contratos recorrentes/híbridos assinados até
    a data informada. Limitação assumida: a base não guarda data de
    encerramento de contrato recorrente (churn) da TechBrabo, então tratamos
    todo contrato com mrr preenchido como ainda ativo indefinidamente. Isso
    tende a superestimar o MRR em bases reais — vale apontar isso como
    'dado faltante' na apresentação, igual foi feito pro churn da Montseguro.
    """
    return TechbraboOportunidade.objects.filter(
        mrr__isnull=False, data_contrato__lte=fim_mes
    ).aggregate(total=Sum("mrr"))["total"] or Decimal("0")


def _mes_anterior(mes_str):
    ano, mes = map(int, mes_str.split("-"))
    if mes == 1:
        return f"{ano - 1}-12"
    return f"{ano}-{mes - 1:02d}"

# ---------------------------------------------------------------
# TECHBRABO
# ---------------------------------------------------------------
class TechbraboKpisView(APIView):
    def get(self, request):
        mes = request.query_params.get("mes") or mes_mais_recente(TechbraboLead.objects.all())
        if mes is None:
            return Response({"detail": "Sem dados carregados."}, status=404)

        inicio_mes, fim_mes = limites_do_mes(mes)

        # --- MRR e crescimento MoM ---
        mrr_atual = _mrr_ate(fim_mes)
        _, fim_mes_anterior = limites_do_mes(_mes_anterior(mes))
        mrr_anterior = _mrr_ate(fim_mes_anterior)
        crescimento_mrr_mom = (
            round(float(mrr_atual - mrr_anterior) / float(mrr_anterior) * 100, 1)
            if mrr_anterior else None
        )

        # --- Contratos assinados no mês (comercial) ---
        contratos_no_mes = TechbraboOportunidade.objects.filter(
            estagio="Contrato assinado", data_contrato__gte=inicio_mes, data_contrato__lte=fim_mes
        )
        n_contratos = contratos_no_mes.count()

        receita_pontual_mes = contratos_no_mes.filter(
            tipo_receita="Pontual"
        ).aggregate(total=Sum("valor_contrato"))["total"] or Decimal("0")

        receita_total_mes = mrr_atual + receita_pontual_mes

        ticket_medio = None
        if n_contratos:
            soma = contratos_no_mes.aggregate(total=Sum("valor_contrato"))["total"] or Decimal("0")
            ticket_medio = round(soma / n_contratos, 2)

        # --- Pipeline/forecast (mesma limitação de "estado atual" do Prop5) ---
        propostas_abertas = TechbraboOportunidade.objects.filter(
            estagio="Proposta enviada", lead__data_criacao__lte=fim_mes
        )
        pipeline_forecast = propostas_abertas.aggregate(total=Sum("valor_proposta"))["total"] or Decimal("0")

        # --- Operação: margem e prazo ---
        projetos_concluidos = TechbraboProjeto.objects.filter(
            status="Concluído", data_entrega_real__lte=fim_mes
        )
        n_concluidos = projetos_concluidos.count()
        margem_media_pct = None
        if n_concluidos:
            soma_margem = projetos_concluidos.aggregate(total=Sum("margem_percentual"))["total"]
            margem_media_pct = round(soma_margem / n_concluidos, 1)

        # % no prazo = concluídos (por definição, no mock, "Concluído" só
        # acontece quando NÃO houve atraso) / (concluídos + atrasados em curso).
        projetos_atrasados = TechbraboProjeto.objects.filter(status="Atrasado").count()
        total_avaliavel = n_concluidos + projetos_atrasados
        pct_no_prazo = round(n_concluidos / total_avaliavel * 100, 1) if total_avaliavel else None

        # --- Expansão vs. cliente novo ---
        valor_total_contratado_mes = contratos_no_mes.aggregate(total=Sum("valor_contrato"))["total"] or Decimal("0")
        valor_clientes_existentes = contratos_no_mes.filter(
            cliente_existente=True
        ).aggregate(total=Sum("valor_contrato"))["total"] or Decimal("0")
        pct_expansao = (
            round(float(valor_clientes_existentes) / float(valor_total_contratado_mes) * 100, 1)
            if valor_total_contratado_mes else None
        )

        # --- CAC ---
        investimento_mkt = Marketing.objects.filter(
            empresa=Empresa.TECHBRABO, mes=mes
        ).aggregate(total=Sum("investimento"))["total"] or Decimal("0")
        cac = round(investimento_mkt / n_contratos, 2) if n_contratos else None

        # --- Atingimento de meta ---
        meta = MetaEmpresa.objects.filter(empresa=Empresa.TECHBRABO, mes=mes).first()
        atingimento_meta = (
            round(float(receita_total_mes) / float(meta.meta_receita) * 100, 1)
            if meta and meta.meta_receita else None
        )

        return Response({
            "mes": mes,
            "mrr_atual": mrr_atual,
            "crescimento_mrr_mom_pct": crescimento_mrr_mom,
            "receita_pontual_mes": receita_pontual_mes,
            "receita_total_mes": receita_total_mes,
            "novos_contratos_no_mes": n_contratos,
            "ticket_medio_contrato": ticket_medio,
            "pipeline_forecast": pipeline_forecast,
            "margem_media_pct": margem_media_pct,
            "pct_projetos_no_prazo": pct_no_prazo,
            "pct_expansao_clientes_existentes": pct_expansao,
            "cac": cac,
            "meta_receita": meta.meta_receita if meta else None,
            "atingimento_meta_pct": atingimento_meta,
        })

# ---------------------------------------------------------------
# Endpoints de listagem "crua" — usados pelos gráficos de funil e
# marketing no front. Aceitam filtro opcional ?mes=YYYY-MM.
# ---------------------------------------------------------------
class MontseguroFunilListView(generics.ListAPIView):
    serializer_class = MontseguroFunilSerializer

    def get_queryset(self):
        qs = MontseguroFunil.objects.select_related("lead").all()
        mes = self.request.query_params.get("mes")
        vendedor = self.request.query_params.get("vendedor")
        canal = self.request.query_params.get("canal")

        if mes:
            qs = qs.filter(lead__mes_referencia=mes)
        if vendedor:
            qs = qs.filter(vendedor=vendedor)
        if canal:
            qs = qs.filter(lead__canal=canal)
        return qs


class MontseguroClienteAtivoListView(generics.ListAPIView):
    queryset = MontseguroClienteAtivo.objects.all()
    serializer_class = MontseguroClienteAtivoSerializer


class Prop5OportunidadeListView(generics.ListAPIView):
    serializer_class = Prop5OportunidadeSerializer

    def get_queryset(self):
        qs = Prop5Oportunidade.objects.select_related("lead").all()
        mes = self.request.query_params.get("mes")
        vendedor = self.request.query_params.get("vendedor")
        canal = self.request.query_params.get("canal")

        if mes:
            qs = qs.filter(lead__mes_referencia=mes)
        if vendedor:
            qs = qs.filter(vendedor=vendedor)
        if canal:
            qs = qs.filter(lead__canal=canal)
        return qs



class TechbraboOportunidadeListView(generics.ListAPIView):
    serializer_class = TechbraboOportunidadeSerializer

    def get_queryset(self):
        qs = TechbraboOportunidade.objects.select_related("lead").all()
        mes = self.request.query_params.get("mes")
        vendedor = self.request.query_params.get("vendedor")
        canal = self.request.query_params.get("canal")

        if mes:
            qs = qs.filter(lead__mes_referencia=mes)
        if vendedor:
            qs = qs.filter(vendedor=vendedor)
        if canal:
            qs = qs.filter(lead__canal=canal)
        return qs


class TechbraboProjetoListView(generics.ListAPIView):
    queryset = TechbraboProjeto.objects.all()
    serializer_class = TechbraboProjetoSerializer


class MarketingListView(generics.ListAPIView):
    serializer_class = MarketingSerializer

    def get_queryset(self):
        qs = Marketing.objects.all()
        empresa = self.request.query_params.get("empresa")
        if empresa:
            qs = qs.filter(empresa=empresa)
        return qs


class MetaEmpresaListView(generics.ListAPIView):
    serializer_class = MetaEmpresaSerializer

    def get_queryset(self):
        qs = MetaEmpresa.objects.all()
        empresa = self.request.query_params.get("empresa")
        if empresa:
            qs = qs.filter(empresa=empresa)
        return qs

# ---------------------------------------------------------------
# COMPARATIVOS ENTRE EMPRESAS (item 11 do briefing)
# ---------------------------------------------------------------
class ComparativosView(APIView):
    def get(self, request):
        mes = request.query_params.get("mes") or mes_mais_recente(MontseguroLead.objects.all())
        if mes is None:
            return Response({"detail": "Sem dados carregados."}, status=404)

        inicio_mes, fim_mes = limites_do_mes(mes)

        # Helper para contar vendedores únicos por empresa (usando os dados do mês)
        # Montseguro: vendedores no funil do mês
        vendedores_mont = MontseguroFunil.objects.filter(
            lead__mes_referencia=mes
        ).values_list("vendedor", flat=True).distinct().count()

        # Prop5: vendedores em oportunidades do mês
        vendedores_prop5 = Prop5Oportunidade.objects.filter(
            lead__mes_referencia=mes
        ).values_list("vendedor", flat=True).distinct().count()

        # TechBrabo: vendedores em oportunidades do mês
        vendedores_tech = TechbraboOportunidade.objects.filter(
            lead__mes_referencia=mes
        ).values_list("vendedor", flat=True).distinct().count()

        # ---- 1. Montseguro ----
        # Leads qualificados = leads criados no mês (simplificação)
        leads_qtd_mont = MontseguroLead.objects.filter(mes_referencia=mes).count()

        # Fechamentos no mês = contratados
        fechamentos_mont = MontseguroFunil.objects.filter(
            data_contratacao__gte=inicio_mes,
            data_contratacao__lte=fim_mes
        ).count()

        # Receita = comissão sobre clientes ativos no fim do mês
        ativos_mont = MontseguroClienteAtivo.objects.filter(
            data_ativacao__lte=fim_mes
        ).exclude(cancelado=True, data_cancelamento__lte=fim_mes)
        premio_total_mont = ativos_mont.aggregate(total=Sum("premio_mensal"))["total"] or Decimal("0")
        receita_mont = round(premio_total_mont * COMISSAO_MONTSEGURO, 2)

        # Ticket médio (prêmio mensal médio de clientes ativos)
        ticket_medio_mont = ativos_mont.aggregate(avg=Avg("premio_mensal"))["avg"] or Decimal("1")

        # Investimento marketing
        invest_mont = Marketing.objects.filter(
            empresa=Empresa.MONTSEGURO, mes=mes
        ).aggregate(total=Sum("investimento"))["total"] or Decimal("0")

        # ---- 2. Prop5 ----
        leads_qtd_prop5 = Prop5Lead.objects.filter(mes_referencia=mes).count()

        fechamentos_prop5 = Prop5Oportunidade.objects.filter(
            estagio="Fechado",
            data_fechamento__gte=inicio_mes,
            data_fechamento__lte=fim_mes
        ).count()

        receita_prop5 = Prop5Oportunidade.objects.filter(
            estagio="Fechado",
            data_fechamento__gte=inicio_mes,
            data_fechamento__lte=fim_mes
        ).aggregate(total=Sum("comissao"))["total"] or Decimal("0")

        ticket_medio_prop5 = Prop5Oportunidade.objects.filter(
            estagio="Fechado"
        ).aggregate(avg=Avg("valor_fechado"))["avg"] or Decimal("1")

        invest_prop5 = Marketing.objects.filter(
            empresa=Empresa.PROP5, mes=mes
        ).aggregate(total=Sum("investimento"))["total"] or Decimal("0")

        # ---- 3. TechBrabo ----
        leads_qtd_tech = TechbraboLead.objects.filter(mes_referencia=mes).count()

        fechamentos_tech = TechbraboOportunidade.objects.filter(
            estagio="Contrato assinado",
            data_contrato__gte=inicio_mes,
            data_contrato__lte=fim_mes
        ).count()

        mrr_atual = _mrr_ate(fim_mes)
        receita_pontual_tech = TechbraboOportunidade.objects.filter(
            estagio="Contrato assinado",
            tipo_receita="Pontual",
            data_contrato__gte=inicio_mes,
            data_contrato__lte=fim_mes
        ).aggregate(total=Sum("valor_contrato"))["total"] or Decimal("0")
        receita_tech = mrr_atual + receita_pontual_tech

        ticket_medio_tech = TechbraboOportunidade.objects.filter(
            estagio="Contrato assinado"
        ).aggregate(avg=Avg("valor_contrato"))["avg"] or Decimal("1")

        invest_tech = Marketing.objects.filter(
            empresa=Empresa.TECHBRABO, mes=mes
        ).aggregate(total=Sum("investimento"))["total"] or Decimal("0")

        # ---- Montar resultado com os 3 indicadores comparativos ----
        resultado = []

        # Montseguro
        produtividade_ajustada_mont = (receita_mont / vendedores_mont) / ticket_medio_mont if vendedores_mont and ticket_medio_mont else 0
        cplq_mont = invest_mont / leads_qtd_mont if leads_qtd_mont else 0
        conversao_ajustada_mont = (fechamentos_mont / leads_qtd_mont * 100) if leads_qtd_mont else 0

        resultado.append({
            "empresa": "Montseguro",
            "produtividade_ajustada": round(produtividade_ajustada_mont, 2),
            "cplq": round(cplq_mont, 2),
            "conversao_ajustada_pct": round(conversao_ajustada_mont, 1),
            "leads_qualificados": leads_qtd_mont,
            "fechamentos": fechamentos_mont,
            "receita": receita_mont,
            "num_vendedores": vendedores_mont,
            "ticket_medio": ticket_medio_mont,
        })

        # Prop5
        produtividade_ajustada_prop5 = (receita_prop5 / vendedores_prop5) / ticket_medio_prop5 if vendedores_prop5 and ticket_medio_prop5 else 0
        cplq_prop5 = invest_prop5 / leads_qtd_prop5 if leads_qtd_prop5 else 0
        conversao_ajustada_prop5 = (fechamentos_prop5 / leads_qtd_prop5 * 100) if leads_qtd_prop5 else 0

        resultado.append({
            "empresa": "Prop5",
            "produtividade_ajustada": round(produtividade_ajustada_prop5, 2),
            "cplq": round(cplq_prop5, 2),
            "conversao_ajustada_pct": round(conversao_ajustada_prop5, 1),
            "leads_qualificados": leads_qtd_prop5,
            "fechamentos": fechamentos_prop5,
            "receita": receita_prop5,
            "num_vendedores": vendedores_prop5,
            "ticket_medio": ticket_medio_prop5,
        })

        # TechBrabo
        produtividade_ajustada_tech = (receita_tech / vendedores_tech) / ticket_medio_tech if vendedores_tech and ticket_medio_tech else 0
        cplq_tech = invest_tech / leads_qtd_tech if leads_qtd_tech else 0
        conversao_ajustada_tech = (fechamentos_tech / leads_qtd_tech * 100) if leads_qtd_tech else 0

        resultado.append({
            "empresa": "TechBrabo",
            "produtividade_ajustada": round(produtividade_ajustada_tech, 2),
            "cplq": round(cplq_tech, 2),
            "conversao_ajustada_pct": round(conversao_ajustada_tech, 1),
            "leads_qualificados": leads_qtd_tech,
            "fechamentos": fechamentos_tech,
            "receita": receita_tech,
            "num_vendedores": vendedores_tech,
            "ticket_medio": ticket_medio_tech,
        })

        return Response({
            "mes": mes,
            "comparativos": resultado,
        })

# ================================================================
# EVOLUÇÃO DA RECEITA — últimos N meses (padrão: 6)
# ================================================================
class EvolucaoReceitaView(APIView):
    def get(self, request):
        meses = int(request.query_params.get("meses", 6))
        mes_fim = request.query_params.get("mes") or mes_mais_recente(MontseguroLead.objects.all())
        if mes_fim is None:
            return Response({"detail": "Sem dados carregados."}, status=404)

        # Lista de meses (do mais antigo para o mais recente)
        lista_meses = []
        mes_atual = mes_fim
        for _ in range(meses):
            lista_meses.insert(0, mes_atual)
            mes_atual = _mes_anterior(mes_atual)

        resultado = []
        empresas_config = [
            {"nome": "Montseguro", "choice": Empresa.MONTSEGURO, "comissao": COMISSAO_MONTSEGURO},
            {"nome": "Prop5", "choice": Empresa.PROP5},
            {"nome": "TechBrabo", "choice": Empresa.TECHBRABO},
        ]

        for mes in lista_meses:
            inicio_mes, fim_mes = limites_do_mes(mes)
            entrada = {"mes": mes}

            receita_total_mes = Decimal("0")

            for emp in empresas_config:
                nome = emp["nome"]

                if nome == "Montseguro":
                    ativos = MontseguroClienteAtivo.objects.filter(
                        data_ativacao__lte=fim_mes
                    ).exclude(cancelado=True, data_cancelamento__lte=fim_mes)
                    premio = ativos.aggregate(total=Sum("premio_mensal"))["total"] or Decimal("0")
                    receita = round(premio * emp["comissao"], 2)

                elif nome == "Prop5":
                    fechamentos = Prop5Oportunidade.objects.filter(
                        estagio="Fechado",
                        data_fechamento__gte=inicio_mes,
                        data_fechamento__lte=fim_mes
                    )
                    receita = fechamentos.aggregate(total=Sum("comissao"))["total"] or Decimal("0")

                else:  # TechBrabo
                    mrr = _mrr_ate(fim_mes)
                    receita_pontual = TechbraboOportunidade.objects.filter(
                        estagio="Contrato assinado",
                        tipo_receita="Pontual",
                        data_contrato__gte=inicio_mes,
                        data_contrato__lte=fim_mes
                    ).aggregate(total=Sum("valor_contrato"))["total"] or Decimal("0")
                    receita = mrr + receita_pontual

                # Chave normalizada para o frontend (ex: "receita_montseguro")
                entrada[f"receita_{nome.lower()}"] = receita
                receita_total_mes += receita

            entrada["receita_total"] = receita_total_mes
            resultado.append(entrada)

        return Response({
            "meses": resultado,
            "labels": [e["mes"] for e in resultado],
        })

# ================================================================
# METAS E PROJEÇÃO — ritmo de meta, gap e necessidade diária
# ================================================================
class MetasProjecaoView(APIView):
    def get(self, request):
        mes = request.query_params.get("mes") or mes_mais_recente(MontseguroLead.objects.all())
        if mes is None:
            return Response({"detail": "Sem dados carregados."}, status=404)

        inicio_mes, fim_mes = limites_do_mes(mes)

        # Dias úteis (simplificado para 22 dias úteis por mês)
        dias_uteis_mes = 22
        # Dia atual (usamos a data de hoje para simular o progresso do mês)
        dia_atual = datetime.now().day
        dia_corrido = min(dia_atual, dias_uteis_mes)
        dias_restantes = max(dias_uteis_mes - dia_corrido, 1)

        empresas_config = [
            {"nome": "Montseguro", "choice": Empresa.MONTSEGURO, "comissao": COMISSAO_MONTSEGURO},
            {"nome": "Prop5", "choice": Empresa.PROP5},
            {"nome": "TechBrabo", "choice": Empresa.TECHBRABO},
        ]

        resultado = []

        for emp in empresas_config:
            nome = emp["nome"]
            empresa_choice = emp["choice"]

            # ---- 1. Receita realizada (mesmo cálculo do CEOOverview) ----
            if nome == "Montseguro":
                ativos = MontseguroClienteAtivo.objects.filter(
                    data_ativacao__lte=fim_mes
                ).exclude(cancelado=True, data_cancelamento__lte=fim_mes)
                premio_total = ativos.aggregate(total=Sum("premio_mensal"))["total"] or Decimal("0")
                receita = round(premio_total * emp["comissao"], 2)

            elif nome == "Prop5":
                fechamentos = Prop5Oportunidade.objects.filter(
                    estagio="Fechado",
                    data_fechamento__gte=inicio_mes,
                    data_fechamento__lte=fim_mes
                )
                receita = fechamentos.aggregate(total=Sum("comissao"))["total"] or Decimal("0")

            else:  # TechBrabo
                mrr = _mrr_ate(fim_mes)
                receita_pontual = TechbraboOportunidade.objects.filter(
                    estagio="Contrato assinado",
                    tipo_receita="Pontual",
                    data_contrato__gte=inicio_mes,
                    data_contrato__lte=fim_mes
                ).aggregate(total=Sum("valor_contrato"))["total"] or Decimal("0")
                receita = mrr + receita_pontual

            # ---- 2. Meta do mês ----
            meta_obj = MetaEmpresa.objects.filter(empresa=empresa_choice, mes=mes).first()
            meta = meta_obj.meta_receita if meta_obj else Decimal("0")

            # ---- 3. Meta esperada até hoje (proporcional aos dias úteis) ----
            meta_esperada = meta * Decimal(str(dia_corrido / dias_uteis_mes))

            # ---- 4. Gap de ritmo (realizado - meta esperada) ----
            gap_ritmo = receita - meta_esperada

            # ---- 5. Necessidade diária (quanto precisa ser produzido por dia para bater a meta) ----
            restante_para_meta = max(meta - receita, Decimal("0"))
            necessidade_diaria = restante_para_meta / Decimal(str(dias_restantes))

            # ---- 6. Atingimento da meta (realizado / meta total) ----
            atingimento = round(float(receita) / float(meta) * 100, 1) if meta else None

            # ---- 7. Quantidade de negócios (para contexto) ----
            if nome == "Montseguro":
                qtd_negocios = MontseguroFunil.objects.filter(
                    data_contratacao__gte=inicio_mes,
                    data_contratacao__lte=fim_mes
                ).count()
            elif nome == "Prop5":
                qtd_negocios = fechamentos.count()
            else:
                qtd_negocios = TechbraboOportunidade.objects.filter(
                    estagio="Contrato assinado",
                    data_contrato__gte=inicio_mes,
                    data_contrato__lte=fim_mes
                ).count()

            resultado.append({
                "empresa": nome,
                "receita": receita,
                "meta": meta,
                "atingimento_pct": atingimento,
                "meta_esperada_ate_hoje": round(meta_esperada, 2),
                "gap_ritmo": round(gap_ritmo, 2),
                "necessidade_diaria": round(necessidade_diaria, 2),
                "dias_uteis_restantes": dias_restantes,
                "qtd_negocios": qtd_negocios,
                "dia_corrido": dia_corrido,
            })

        return Response({
            "mes": mes,
            "dias_uteis_mes": dias_uteis_mes,
            "dia_corrido": dia_corrido,
            "empresas": resultado,
        })


class CEOOverviewView(APIView):
    def get(self, request):
        mes = request.query_params.get("mes") or mes_mais_recente(MontseguroLead.objects.all())
        if mes is None:
            return Response({"detail": "Sem dados carregados."}, status=404)

        inicio_mes, fim_mes = limites_do_mes(mes)

        # --- Dias úteis (simplificado para 22 dias úteis) ---
        dias_uteis_mes = 22
        # Dia atual dentro do mês (usamos a data atual para simular "hoje")
        dia_corrido = min(datetime.now().day, dias_uteis_mes)

        # --- Configuração das empresas ---
        empresas_config = [
            {
                "nome": "Montseguro",
                "empresa_choice": Empresa.MONTSEGURO,
                "comissao": COMISSAO_MONTSEGURO,
                "model_lead": MontseguroLead,
                "model_funil": MontseguroFunil,
                "model_cliente": MontseguroClienteAtivo,
            },
            {
                "nome": "Prop5",
                "empresa_choice": Empresa.PROP5,
                "model_lead": Prop5Lead,
                "model_op": Prop5Oportunidade,
            },
            {
                "nome": "TechBrabo",
                "empresa_choice": Empresa.TECHBRABO,
                "model_lead": TechbraboLead,
                "model_op": TechbraboOportunidade,
            },
        ]

        resultado = []
        receita_total = Decimal("0")
        meta_total = Decimal("0")
        forecast_total = Decimal("0")
        investimento_total = Decimal("0")
        qtd_negocios_total = 0
        meta_esperada_total = Decimal("0")
        gap_ritmo_total = Decimal("0")
        leads_total = 0  # <-- NOVO: acumular leads

        # --- Variáveis para evolução da receita (últimos 6 meses) ---
        evolucao_receita = []
        for i in range(6):
            mes_hist = mes
            for _ in range(i):
                mes_hist = _mes_anterior(mes_hist)
            # Calcular receita total daquele mês (simplificado)
            _, fim_mes_hist = limites_do_mes(mes_hist)
            receita_hist = Decimal("0")
            for emp in empresas_config:
                nome = emp["nome"]
                if nome == "Montseguro":
                    ativos_hist = MontseguroClienteAtivo.objects.filter(
                        data_ativacao__lte=fim_mes_hist
                    ).exclude(cancelado=True, data_cancelamento__lte=fim_mes_hist)
                    premio_hist = ativos_hist.aggregate(total=Sum("premio_mensal"))["total"] or Decimal("0")
                    receita_hist += round(premio_hist * emp["comissao"], 2)
                elif nome == "Prop5":
                    fechamentos_hist = Prop5Oportunidade.objects.filter(
                        estagio="Fechado",
                        data_fechamento__gte=limites_do_mes(mes_hist)[0],
                        data_fechamento__lte=fim_mes_hist
                    )
                    receita_hist += fechamentos_hist.aggregate(total=Sum("comissao"))["total"] or Decimal("0")
                else:
                    mrr_hist = _mrr_ate(fim_mes_hist)
                    receita_pontual_hist = TechbraboOportunidade.objects.filter(
                        estagio="Contrato assinado",
                        tipo_receita="Pontual",
                        data_contrato__gte=limites_do_mes(mes_hist)[0],
                        data_contrato__lte=fim_mes_hist
                    ).aggregate(total=Sum("valor_contrato"))["total"] or Decimal("0")
                    receita_hist += mrr_hist + receita_pontual_hist
            evolucao_receita.append({
                "mes": mes_hist,
                "receita": receita_hist,
            })
        evolucao_receita = sorted(evolucao_receita, key=lambda x: x["mes"])

        # --- Loop por empresa ---
        for emp in empresas_config:
            nome = emp["nome"]
            empresa_choice = emp["empresa_choice"]

            # --- 1. Receita, Meta, Forecast e Quantidade de Negócios ---
            if nome == "Montseguro":
                ativos = MontseguroClienteAtivo.objects.filter(
                    data_ativacao__lte=fim_mes
                ).exclude(cancelado=True, data_cancelamento__lte=fim_mes)
                premio_total = ativos.aggregate(total=Sum("premio_mensal"))["total"] or Decimal("0")
                receita = round(premio_total * emp["comissao"], 2)

                meta_obj = MetaEmpresa.objects.filter(empresa=empresa_choice, mes=mes).first()
                meta = meta_obj.meta_receita if meta_obj else Decimal("0")

                # Forecast: receita + pipeline (propostas em aberto com taxa de conversão estimada)
                propostas_abertas = MontseguroFunil.objects.filter(
                    data_proposta__isnull=False,
                    data_contratacao__isnull=True,
                    data_implantacao__isnull=True,
                )
                pipeline = sum(
                    (p.premio_mensal_estimado * 12 * Decimal("0.4") * emp["comissao"])
                    for p in propostas_abertas
                )
                forecast = receita + pipeline

                # Quantidade de negócios (contratações no mês)
                qtd_negocios = MontseguroFunil.objects.filter(
                    data_contratacao__gte=inicio_mes,
                    data_contratacao__lte=fim_mes
                ).count()

                # Ticket médio = receita / qtd_negocios (se houver)
                ticket_medio = round(receita / qtd_negocios, 2) if qtd_negocios else Decimal("0")

                # Leads do mês
                leads_empresa = MontseguroLead.objects.filter(mes_referencia=mes).count()

            elif nome == "Prop5":
                fechamentos = Prop5Oportunidade.objects.filter(
                    estagio="Fechado",
                    data_fechamento__gte=inicio_mes,
                    data_fechamento__lte=fim_mes
                )
                receita = fechamentos.aggregate(total=Sum("comissao"))["total"] or Decimal("0")

                meta_obj = MetaEmpresa.objects.filter(empresa=empresa_choice, mes=mes).first()
                meta = meta_obj.meta_receita if meta_obj else Decimal("0")

                pipeline_aberto = Prop5Oportunidade.objects.filter(
                    lead__data_criacao__lte=fim_mes
                ).exclude(estagio__in=["Fechado", "Perdido"])
                pipeline = sum(
                    (op.valor_estimado * (op.probabilidade or Decimal("0"))) for op in pipeline_aberto
                )
                forecast = receita + pipeline
                qtd_negocios = fechamentos.count()
                ticket_medio = round(receita / qtd_negocios, 2) if qtd_negocios else Decimal("0")
                leads_empresa = Prop5Lead.objects.filter(mes_referencia=mes).count()

            else:  # TechBrabo
                mrr = _mrr_ate(fim_mes)
                receita_pontual = TechbraboOportunidade.objects.filter(
                    estagio="Contrato assinado",
                    tipo_receita="Pontual",
                    data_contrato__gte=inicio_mes,
                    data_contrato__lte=fim_mes
                ).aggregate(total=Sum("valor_contrato"))["total"] or Decimal("0")
                receita = mrr + receita_pontual

                meta_obj = MetaEmpresa.objects.filter(empresa=empresa_choice, mes=mes).first()
                meta = meta_obj.meta_receita if meta_obj else Decimal("0")

                pipeline = TechbraboOportunidade.objects.filter(
                    estagio="Proposta enviada",
                    lead__data_criacao__lte=fim_mes
                ).aggregate(total=Sum("valor_proposta"))["total"] or Decimal("0")
                forecast = receita + pipeline

                qtd_negocios = TechbraboOportunidade.objects.filter(
                    estagio="Contrato assinado",
                    data_contrato__gte=inicio_mes,
                    data_contrato__lte=fim_mes
                ).count()
                ticket_medio = round(receita / qtd_negocios, 2) if qtd_negocios else Decimal("0")
                leads_empresa = TechbraboLead.objects.filter(mes_referencia=mes).count()

            # Acumular leads totais
            leads_total += leads_empresa

            # --- 2. Metas e ritmo ---
            meta_esperada = meta * Decimal(str(dia_corrido / dias_uteis_mes))
            gap_ritmo = receita - meta_esperada
            necessidade_diaria = (meta - receita) / Decimal(str(max(dias_uteis_mes - dia_corrido, 1)))
            dias_uteis_restantes = dias_uteis_mes - dia_corrido

            # --- 3. Marketing ---
            investimento = Marketing.objects.filter(
                empresa=empresa_choice, mes=mes
            ).aggregate(total=Sum("investimento"))["total"] or Decimal("0")
            cac = round(investimento / qtd_negocios, 2) if qtd_negocios else None
            roi_marketing = round((receita - investimento) / investimento * 100, 1) if investimento else None

            # --- 4. Crescimento MoM ---
            mes_anterior = _mes_anterior(mes)
            _, fim_mes_anterior = limites_do_mes(mes_anterior)
            if nome == "Montseguro":
                ativos_ant = MontseguroClienteAtivo.objects.filter(
                    data_ativacao__lte=fim_mes_anterior
                ).exclude(cancelado=True, data_cancelamento__lte=fim_mes_anterior)
                premio_ant = ativos_ant.aggregate(total=Sum("premio_mensal"))["total"] or Decimal("0")
                receita_anterior = round(premio_ant * emp["comissao"], 2)
            elif nome == "Prop5":
                fechamentos_ant = Prop5Oportunidade.objects.filter(
                    estagio="Fechado",
                    data_fechamento__gte=limites_do_mes(mes_anterior)[0],
                    data_fechamento__lte=fim_mes_anterior
                )
                receita_anterior = fechamentos_ant.aggregate(total=Sum("comissao"))["total"] or Decimal("0")
            else:
                mrr_ant = _mrr_ate(fim_mes_anterior)
                receita_pontual_ant = TechbraboOportunidade.objects.filter(
                    estagio="Contrato assinado",
                    tipo_receita="Pontual",
                    data_contrato__gte=limites_do_mes(mes_anterior)[0],
                    data_contrato__lte=fim_mes_anterior
                ).aggregate(total=Sum("valor_contrato"))["total"] or Decimal("0")
                receita_anterior = mrr_ant + receita_pontual_ant

            crescimento_mom = round((receita - receita_anterior) / receita_anterior * 100, 1) if receita_anterior else None

            # --- 5. Montar resultado por empresa ---
            resultado.append({
                "empresa": nome,
                "receita": receita,
                "meta": meta,
                "atingimento_pct": round(float(receita) / float(meta) * 100, 1) if meta else None,
                "forecast": forecast,
                "gap": forecast - meta,
                "meta_esperada_ate_hoje": meta_esperada,
                "gap_ritmo": gap_ritmo,
                "necessidade_diaria": necessidade_diaria,
                "dias_uteis_restantes": dias_uteis_restantes,
                "crescimento_mom_pct": crescimento_mom,
                "investimento_marketing": investimento,
                "cac": cac,
                "roi_marketing_pct": roi_marketing,
                "qtd_negocios": qtd_negocios,
                "ticket_medio": ticket_medio,
                "leads": leads_empresa,  # <-- NOVO: leads por empresa
            })

            # Acumular totais
            receita_total += receita
            meta_total += meta
            forecast_total += forecast
            investimento_total += investimento
            qtd_negocios_total += qtd_negocios
            meta_esperada_total += meta_esperada
            gap_ritmo_total += gap_ritmo

        # --- Totais do grupo ---
        atingimento_geral = round(float(receita_total) / float(meta_total) * 100, 1) if meta_total else None
        ticket_medio_consolidado = round(receita_total / qtd_negocios_total, 2) if qtd_negocios_total else Decimal("0")
        cac_medio = round(investimento_total / qtd_negocios_total, 2) if qtd_negocios_total else None
        roi_marketing_geral = round((receita_total - investimento_total) / investimento_total * 100, 1) if investimento_total else None

        # Taxa de conversão geral (negócios / leads)
        taxa_conversao_geral = round(qtd_negocios_total / leads_total * 100, 1) if leads_total else None

        # Crescimento MoM do grupo (já calculado? vamos refazer com base na receita anterior total)
        mes_anterior = _mes_anterior(mes)
        _, fim_mes_ant = limites_do_mes(mes_anterior)
        receita_anterior_total = Decimal("0")
        for emp in empresas_config:
            nome = emp["nome"]
            if nome == "Montseguro":
                ativos_ant = MontseguroClienteAtivo.objects.filter(
                    data_ativacao__lte=fim_mes_ant
                ).exclude(cancelado=True, data_cancelamento__lte=fim_mes_ant)
                premio_ant = ativos_ant.aggregate(total=Sum("premio_mensal"))["total"] or Decimal("0")
                receita_anterior_total += round(premio_ant * emp["comissao"], 2)
            elif nome == "Prop5":
                fechamentos_ant = Prop5Oportunidade.objects.filter(
                    estagio="Fechado",
                    data_fechamento__gte=limites_do_mes(mes_anterior)[0],
                    data_fechamento__lte=fim_mes_ant
                )
                receita_anterior_total += fechamentos_ant.aggregate(total=Sum("comissao"))["total"] or Decimal("0")
            else:
                mrr_ant = _mrr_ate(fim_mes_ant)
                receita_pontual_ant = TechbraboOportunidade.objects.filter(
                    estagio="Contrato assinado",
                    tipo_receita="Pontual",
                    data_contrato__gte=limites_do_mes(mes_anterior)[0],
                    data_contrato__lte=fim_mes_ant
                ).aggregate(total=Sum("valor_contrato"))["total"] or Decimal("0")
                receita_anterior_total += mrr_ant + receita_pontual_ant

        crescimento_mom_geral = round((receita_total - receita_anterior_total) / receita_anterior_total * 100, 1) if receita_anterior_total else None

        # Necessidade diária total
        necessidade_diaria_total = round((meta_total - receita_total) / Decimal(str(max(dias_uteis_mes - dia_corrido, 1))), 2) if meta_total else Decimal("0")
        dias_uteis_restantes = dias_uteis_mes - dia_corrido

        return Response({
            "mes": mes,
            "empresas": resultado,
            "total": {
                "receita_total": receita_total,
                "meta_total": meta_total,
                "atingimento_geral_pct": atingimento_geral,
                "forecast_total": forecast_total,
                "gap_total": forecast_total - meta_total,
                "meta_esperada_ate_hoje": meta_esperada_total,
                "gap_ritmo_total": gap_ritmo_total,
                "necessidade_diaria_total": necessidade_diaria_total,
                "dias_uteis_restantes": dias_uteis_restantes,
                "crescimento_mom_pct": crescimento_mom_geral,
                "investimento_marketing_total": investimento_total,
                "cac_medio": cac_medio,
                "roi_marketing_geral_pct": roi_marketing_geral,
                "qtd_negocios_total": qtd_negocios_total,
                "ticket_medio_consolidado": ticket_medio_consolidado,
                # NOVOS campos
                "leads_total": leads_total,
                "taxa_conversao_geral_pct": taxa_conversao_geral,
                "evolucao_receita": evolucao_receita,  # lista de {mes, receita}
            }
        })


