from rest_framework import serializers
from .models import Empresa, Vendedor, Canal, Campanha, Oportunidade, Meta, MarketingInvestimento

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'

class CanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canal
        fields = '__all__'

class CampanhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campanha
        fields = '__all__'

class OportunidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oportunidade
        fields = '__all__'
        depth = 1

class MetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meta
        fields = '__all__'

class MarketingInvestimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingInvestimento
        fields = '__all__'
