import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from api.models import (
    MontseguroLead, MontseguroFunil, MontseguroClienteAtivo,
    Prop5Lead, Prop5Oportunidade,
    TechbraboLead, TechbraboOportunidade, TechbraboProjeto,
    Marketing, MetaEmpresa, Empresa,
)

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "mock-data-grupo-mont.json"


class Command(BaseCommand):
    help = "Carrega o dataset mockado do Grupo Mont (mock-data-grupo-mont.json) no banco."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Apaga os dados existentes das tabelas antes de recarregar.",
        )

    def handle(self, *args, **options):
        with open(DATA_PATH, encoding="utf-8") as f:
            data = json.load(f)

        if options["reset"]:
            self.stdout.write("Limpando dados existentes...")
            for model in [
                MontseguroClienteAtivo, MontseguroFunil, MontseguroLead,
                Prop5Oportunidade, Prop5Lead,
                TechbraboProjeto, TechbraboOportunidade, TechbraboLead,
                Marketing, MetaEmpresa,
            ]:
                model.objects.all().delete()

        with transaction.atomic():
            self._carregar_montseguro(data["montseguro"])
            self._carregar_prop5(data["prop5"])
            self._carregar_techbrabo(data["techbrabo"])
            self._carregar_marketing_e_metas(data)

        self.stdout.write(self.style.SUCCESS("Dataset mockado carregado com sucesso."))

    def _carregar_montseguro(self, bloco):
        leads_por_id = {}
        for l in bloco["leads"]:
            obj = MontseguroLead.objects.create(
                data_criacao=l["data_criacao"],
                mes_referencia=l["mes_referencia"],
                canal=l["canal"],
                porte_empresa=l["porte_empresa"],
                vidas_estimadas=l["vidas_estimadas"],
            )
            leads_por_id[l["lead_id"]] = obj
        self.stdout.write(f"  Montseguro: {len(leads_por_id)} leads")

        funil_por_lead = {}
        for reg in bloco["funil"]:
            lead = leads_por_id[reg["lead_id"]]
            obj = MontseguroFunil.objects.create(
                lead=lead,
                vendedor=reg["vendedor"],
                operadora=reg["operadora"],
                vidas=reg["vidas"],
                premio_mensal_estimado=reg["premio_mensal_estimado"],
                data_cotacao=reg["data_cotacao"],
                data_proposta=reg["data_proposta"],
                data_contratacao=reg["data_contratacao"],
                data_implantacao=reg["data_implantacao"],
                status=reg["status"],
                motivo_perda=reg["motivo_perda"],
            )
            funil_por_lead[reg["lead_id"]] = obj
        self.stdout.write(f"  Montseguro: {len(funil_por_lead)} registros de funil")

        n_clientes = 0
        for c in bloco["clientes_ativos"]:
            lead = leads_por_id[c["lead_id"]]
            MontseguroClienteAtivo.objects.create(
                lead=lead,
                operadora=c["operadora"],
                vidas_ativas=c["vidas_ativas"],
                premio_mensal=c["premio_mensal"],
                data_ativacao=c["data_ativacao"],
                cancelado=c["cancelado"],
                data_cancelamento=c["data_cancelamento"],
            )
            n_clientes += 1
        self.stdout.write(f"  Montseguro: {n_clientes} clientes ativos")

    def _carregar_prop5(self, bloco):
        leads_por_id = {}
        for l in bloco["leads"]:
            obj = Prop5Lead.objects.create(
                data_criacao=l["data_criacao"],
                mes_referencia=l["mes_referencia"],
                canal=l["canal"],
                pais_residencia=l["pais_residencia"],
            )
            leads_por_id[l["lead_id"]] = obj
        self.stdout.write(f"  Prop5: {len(leads_por_id)} leads")

        n_op = 0
        for reg in bloco["oportunidades"]:
            lead = leads_por_id[reg["lead_id"]]
            Prop5Oportunidade.objects.create(
                lead=lead,
                vendedor=reg["vendedor"],
                valor_estimado=reg["valor_estimado"],
                probabilidade=reg["probabilidade"],
                estagio=reg["estagio"],
                data_diagnostico=reg["data_diagnostico"],
                data_reuniao_consultiva=reg["data_reuniao_consultiva"],
                data_fechamento=reg["data_fechamento"],
                valor_fechado=reg["valor_fechado"],
                comissao=reg["comissao"],
            )
            n_op += 1
        self.stdout.write(f"  Prop5: {n_op} oportunidades")

    def _carregar_techbrabo(self, bloco):
        leads_por_id = {}
        for l in bloco["leads"]:
            obj = TechbraboLead.objects.create(
                data_criacao=l["data_criacao"],
                mes_referencia=l["mes_referencia"],
                canal=l["canal"],
                tipo_solucao=l["tipo_solucao"],
            )
            leads_por_id[l["lead_id"]] = obj
        self.stdout.write(f"  TechBrabo: {len(leads_por_id)} leads")

        oportunidades_por_lead = {}
        for reg in bloco["oportunidades"]:
            lead = leads_por_id[reg["lead_id"]]
            obj = TechbraboOportunidade.objects.create(
                lead=lead,
                vendedor=reg["vendedor"],
                tipo_solucao=reg["tipo_solucao"],
                tipo_receita=reg["tipo_receita"],
                valor_proposta=reg["valor_proposta"],
                estagio=reg["estagio"],
                cliente_existente=reg["cliente_existente"],
                data_proposta=reg["data_proposta"],
                data_contrato=reg["data_contrato"],
                valor_contrato=reg["valor_contrato"],
                mrr=reg["mrr"],
            )
            oportunidades_por_lead[reg["lead_id"]] = obj
        self.stdout.write(f"  TechBrabo: {len(oportunidades_por_lead)} oportunidades")

        n_proj = 0
        for p in bloco["projetos"]:
            oportunidade = oportunidades_por_lead[p["lead_id"]]
            TechbraboProjeto.objects.create(
                oportunidade=oportunidade,
                tipo_solucao=p["tipo_solucao"],
                valor_contrato=p["valor_contrato"],
                custo_estimado=p["custo_estimado"],
                margem=p["margem"],
                margem_percentual=p["margem_percentual"],
                status=p["status"],
                data_inicio=p["data_inicio"],
                data_entrega_prevista=p["data_entrega_prevista"],
                data_entrega_real=p["data_entrega_real"],
                mrr=p["mrr"],
            )
            n_proj += 1
        self.stdout.write(f"  TechBrabo: {n_proj} projetos")

    def _carregar_marketing_e_metas(self, data):
        empresa_map = {
            "montseguro": Empresa.MONTSEGURO,
            "prop5": Empresa.PROP5,
            "techbrabo": Empresa.TECHBRABO,
        }

        campo_receita_por_empresa = {
            "montseguro": "meta_receita_comissao",
            "prop5": "meta_comissao",
            "techbrabo": "meta_receita_total",
        }
        campo_quantidade_por_empresa = {
            "montseguro": "meta_novos_contratos",
            "prop5": "meta_fechamentos",
            "techbrabo": "meta_novos_contratos",
        }

        n_mkt = 0
        n_metas = 0
        for empresa_key, bloco in data.items():
            if empresa_key == "periodo":
                continue
            empresa_choice = empresa_map[empresa_key]

            for m in bloco["marketing"]:
                Marketing.objects.create(
                    empresa=empresa_choice,
                    mes=m["mes"],
                    canal=m["canal"],
                    investimento=m["investimento"],
                    leads_gerados=m["leads_gerados"],
                )
                n_mkt += 1

            campo_receita = campo_receita_por_empresa[empresa_key]
            campo_qtd = campo_quantidade_por_empresa[empresa_key]
            for meta in bloco["metas"]:
                MetaEmpresa.objects.create(
                    empresa=empresa_choice,
                    mes=meta["mes"],
                    meta_receita=meta[campo_receita],
                    meta_quantidade=meta[campo_qtd],
                )
                n_metas += 1

        self.stdout.write(f"  Marketing: {n_mkt} registros | Metas: {n_metas} registros")
