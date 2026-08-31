from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmpresaViewSet, VendedorViewSet, CanalViewSet,
    CampanhaViewSet, OportunidadeViewSet, MetaViewSet,
    MarketingInvestimentoViewSet,
    CEOOverviewAPIView, MontseguroKPIAPIView,
    Prop5KPIAPIView, TechBraboKPIAPIView,
    ComparativosKPIAPIView
)

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'vendedores', VendedorViewSet)
router.register(r'canais', CanalViewSet)
router.register(r'campanhas', CampanhaViewSet)
router.register(r'oportunidades', OportunidadeViewSet)
router.register(r'metas', MetaViewSet)
router.register(r'marketing-investimentos', MarketingInvestimentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('kpis/ceo-overview/', CEOOverviewAPIView.as_view(), name='ceo-overview'),
    path('kpis/montseguro/', MontseguroKPIAPIView.as_view(), name='montseguro'),
    # path('kpis/prop5/', Prop5KPIAPIView.as_view(), name='prop5'),
    # path('kpis/techbrabo/', TechBraboKPIAPIView.as_view(), name='techbrabo'),
    # path('kpis/comparativos/', ComparativosKPIAPIView.as_view(), name='comparativos'),
]
