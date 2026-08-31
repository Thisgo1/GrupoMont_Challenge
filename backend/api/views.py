from django.shortcuts import render
from rest_framework import viewsets
from .models import Empresa, Vendedor, Canal, Campanha, Oportunidade, Meta, MarketingInvestimento
from .serializers import (
    EmpresaSerializer, VendedorSerializer, CanalSerializer,
    CampanhaSerializer, OportunidadeSerializer, MetaSerializer,
    MarketingInvestimentoSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg, Q, F, ExpressionWrapper, FloatField
from datetime import datetime
from .models import Oportunidade, Empresa, Meta, MarketingInvestimento


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

class MontseguroKPIAPIView(APIView):
    def get(self, request):
        ano = request.query_params.get('ano', datetime.now().year)
        mes = request.query_params.get('mes', datetime.now().month)
        empresa = Empresa.objects.get(nome='Montseguro')

        ops_mes = Oportunidade.objects.filter(empresa=empresa, data_criacao__year=ano, data_criacao__month=mes)
        leads = ops_mes.count()
        contratacoes = Oportunidade.objects.filter(
            empresa=empresa, status='Ganha',
            data_previsao_fechamento__year=ano,
            data_previsao_fechamento__month=mes,
            estagio__in=['Contratação', 'Implantado', 'Ativo']
        ).count()
        implantados = Oportunidade.objects.filter(
            empresa=empresa, status='Ganha',
            data_previsao_fechamento__year=ano,
            data_previsao_fechamento__month=mes,
            estagio__in=['Implantado', 'Ativo']
        ).count()

        taxa_conversao = round(contratacoes / leads * 100, 2) if leads else 0
        taxa_implantacao = round(implantados / contratacoes * 100, 2) if contratacoes else 0
        ticket_medio = Oportunidade.objects.filter(
            empresa=empresa, status='Ganha',
            estagio__in=['Implantado', 'Ativo']
        ).aggregate(avg=Avg('valor_potencial'))['avg'] or 0

        vidas_ativas = Oportunidade.objects.filter(
            empresa=empresa, status='Ganha',
            estagio__in=['Implantado', 'Ativo']
        ).aggregate(total=Sum('vidas_contratadas'))['total'] or 0

        investimento = MarketingInvestimento.objects.filter(
            ano_mes=f"{ano}-{str(mes).zfill(2)}"
        ).aggregate(total=Sum('investimento'))['total'] or 0
        cac = round(investimento / implantados, 2) if implantados else 0

        return Response({
            'taxa_conversao_lead_contratacao': taxa_conversao,
            'taxa_implantacao': taxa_implantacao,
            'ticket_medio': ticket_medio,
            'vidas_ativas': vidas_ativas,
            'cac': cac,
            'contratacoes': contratacoes,
            'implantados': implantados,
        })

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

