from django.urls import path
from . import views

urlpatterns = [
    # KPIs (visão executiva por empresa)
    path("montseguro/kpis/", views.MontseguroKpisView.as_view(), name="montseguro-kpis"),
    path("prop5/kpis/", views.Prop5KpisView.as_view(), name="prop5-kpis"),
    path("techbrabo/kpis/", views.TechbraboKpisView.as_view(), name="techbrabo-kpis"),

    # Dados brutos (funis, projetos, marketing, metas) pra gráficos e drill-down
    path("montseguro/funil/", views.MontseguroFunilListView.as_view(), name="montseguro-funil"),
    path("montseguro/clientes-ativos/", views.MontseguroClienteAtivoListView.as_view(), name="montseguro-clientes"),
    path("prop5/oportunidades/", views.Prop5OportunidadeListView.as_view(), name="prop5-oportunidades"),
    path("techbrabo/oportunidades/", views.TechbraboOportunidadeListView.as_view(), name="techbrabo-oportunidades"),
    path("techbrabo/projetos/", views.TechbraboProjetoListView.as_view(), name="techbrabo-projetos"),
    path("marketing/", views.MarketingListView.as_view(), name="marketing"),
    path("metas/", views.MetaEmpresaListView.as_view(), name="metas"),
    path("kpis/ceo-overview/", views.CEOOverviewView.as_view(), name="ceo-overview"),
    path("kpis/comparativos/", views.ComparativosView.as_view(), name="comparativos"),
    path("kpis/evolucao-receita/", views.EvolucaoReceitaView.as_view(), name="evolucao-receita"),
    path("kpis/metas-projecao/", views.MetasProjecaoView.as_view(), name="metas-projecao"),
]
