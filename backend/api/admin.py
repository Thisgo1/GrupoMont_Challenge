from django.contrib import admin
from .models import (
    MontseguroLead, MontseguroFunil, MontseguroClienteAtivo,
    Prop5Lead, Prop5Oportunidade,
    TechbraboLead, TechbraboOportunidade, TechbraboProjeto,
    Marketing, MetaEmpresa,
)


@admin.register(MontseguroLead)
class MontseguroLeadAdmin(admin.ModelAdmin):
    list_display = ("id", "data_criacao", "canal", "porte_empresa", "vidas_estimadas")
    list_filter = ("canal", "porte_empresa", "mes_referencia")


@admin.register(MontseguroFunil)
class MontseguroFunilAdmin(admin.ModelAdmin):
    list_display = ("id", "lead", "status", "vendedor", "operadora", "premio_mensal_estimado")
    list_filter = ("status", "operadora", "vendedor")


@admin.register(MontseguroClienteAtivo)
class MontseguroClienteAtivoAdmin(admin.ModelAdmin):
    list_display = ("id", "lead", "operadora", "vidas_ativas", "premio_mensal", "cancelado")
    list_filter = ("operadora", "cancelado")


@admin.register(Prop5Lead)
class Prop5LeadAdmin(admin.ModelAdmin):
    list_display = ("id", "data_criacao", "canal", "pais_residencia")
    list_filter = ("canal", "pais_residencia", "mes_referencia")


@admin.register(Prop5Oportunidade)
class Prop5OportunidadeAdmin(admin.ModelAdmin):
    list_display = ("id", "lead", "estagio", "valor_estimado", "valor_fechado", "comissao")
    list_filter = ("estagio", "vendedor")


@admin.register(TechbraboLead)
class TechbraboLeadAdmin(admin.ModelAdmin):
    list_display = ("id", "data_criacao", "canal", "tipo_solucao")
    list_filter = ("canal", "tipo_solucao", "mes_referencia")


@admin.register(TechbraboOportunidade)
class TechbraboOportunidadeAdmin(admin.ModelAdmin):
    list_display = ("id", "lead", "estagio", "tipo_receita", "valor_contrato", "mrr", "cliente_existente")
    list_filter = ("estagio", "tipo_receita", "cliente_existente")


@admin.register(TechbraboProjeto)
class TechbraboProjetoAdmin(admin.ModelAdmin):
    list_display = ("id", "oportunidade", "status", "valor_contrato", "margem_percentual")
    list_filter = ("status",)


@admin.register(Marketing)
class MarketingAdmin(admin.ModelAdmin):
    list_display = ("id", "empresa", "mes", "canal", "investimento", "leads_gerados")
    list_filter = ("empresa", "mes", "canal")


@admin.register(MetaEmpresa)
class MetaEmpresaAdmin(admin.ModelAdmin):
    list_display = ("id", "empresa", "mes", "meta_receita", "meta_quantidade")
    list_filter = ("empresa", "mes")
