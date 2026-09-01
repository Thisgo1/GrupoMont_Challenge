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


class CEOOverviewAPIView(APIView):
    def get(self, request):
        ano = request.query_params.get('ano', datetime.now().year)
        mes = request.query_params.get('mes', datetime.now().month)
        empresas = Empresa.objects.all()
        resultado = []
        for emp in empresas:
            receita = Oportunidade.objects.filter(
                empresa=emp, status='Ganha',
                data_previsao_fechamento__year=ano,
                data_previsao_fechamento__month=mes
            ).aggregate(total=Sum('receita_reconhecida'))['total'] or 0

            meta_obj = Meta.objects.filter(
                empresa=emp, ano_mes=f"{ano}-{str(mes).zfill(2)}"
            ).first()
            meta_valor = meta_obj.meta_receita if meta_obj else 0

            pipeline = Oportunidade.objects.filter(
                empresa=emp, status='Aberta',
                data_previsao_fechamento__year=ano,
                data_previsao_fechamento__month=mes
            ).aggregate(
                total=Sum(ExpressionWrapper(F('valor_potencial') * F('probabilidade'), output_field=FloatField()))
            )['total'] or 0

            forecast = receita + pipeline
            atingimento = round(receita / meta_valor * 100, 2) if meta_valor else 0

            resultado.append({
                'empresa': emp.nome,
                'receita': receita,
                'meta': meta_valor,
                'atingimento': atingimento,
                'forecast': forecast,
                'gap': forecast - meta_valor,
            })
        return Response(resultado)

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer

class CanalViewSet(viewsets.ModelViewSet):
    queryset = Canal.objects.all()
    serializer_class = CanalSerializer

class CampanhaViewSet(viewsets.ModelViewSet):
    queryset = Campanha.objects.all()
    serializer_class = CampanhaSerializer

class OportunidadeViewSet(viewsets.ModelViewSet):
    queryset = Oportunidade.objects.all()
    serializer_class = OportunidadeSerializer
    filterset_fields = ['empresa', 'status', 'canal', 'vendedor', 'estagio']
    search_fields = ['empresa__nome']

class MetaViewSet(viewsets.ModelViewSet):
    queryset = Meta.objects.all()
    serializer_class = MetaSerializer

class MarketingInvestimentoViewSet(viewsets.ModelViewSet):
    queryset = MarketingInvestimento.objects.all()
    serializer_class = MarketingInvestimentoSerializer

