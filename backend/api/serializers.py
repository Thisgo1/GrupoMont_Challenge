from rest_framework import serializers
from .models import (
    MontseguroFunil, MontseguroClienteAtivo,
    Prop5Oportunidade,
    TechbraboOportunidade, TechbraboProjeto,
    Marketing, MetaEmpresa,
)
from django.urls import path, include



class MontseguroFunilSerializer(serializers.ModelSerializer):
    canal = serializers.CharField(source="lead.canal", read_only=True)
    mes_referencia = serializers.CharField(source="lead.mes_referencia", read_only=True)

    class Meta:
        model = MontseguroFunil
        fields = [
            "id", "status", "vendedor", "operadora", "vidas",
            "premio_mensal_estimado", "data_cotacao", "data_proposta",
            "data_contratacao", "data_implantacao", "motivo_perda",
            "canal", "mes_referencia",
        ]


class MontseguroClienteAtivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MontseguroClienteAtivo
        fields = "__all__"


class Prop5OportunidadeSerializer(serializers.ModelSerializer):
    canal = serializers.CharField(source="lead.canal", read_only=True)
    pais_residencia = serializers.CharField(source="lead.pais_residencia", read_only=True)
    mes_referencia = serializers.CharField(source="lead.mes_referencia", read_only=True)

    class Meta:
        model = Prop5Oportunidade
        fields = "__all__"


class TechbraboOportunidadeSerializer(serializers.ModelSerializer):
    canal = serializers.CharField(source="lead.canal", read_only=True)
    mes_referencia = serializers.CharField(source="lead.mes_referencia", read_only=True)

    class Meta:
        model = TechbraboOportunidade
        fields = "__all__"


class TechbraboProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechbraboProjeto
        fields = "__all__"


class MarketingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketing
        fields = "__all__"


class MetaEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaEmpresa
        fields = "__all__"
