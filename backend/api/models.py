from django.db import models

class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    ticket_medio = models.DecimalField(max_digits=15, decimal_places=2)
    ciclo_dias = models.IntegerField()

    def __str__(self):
        return self.nome

class Vendedor(models.Model):
    nome = models.CharField(max_length=100)
    equipe = models.CharField(max_length=50)
    empresa_principal = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome

class Canal(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Campanha(models.Model):
    nome = models.CharField(max_length=100)
    investimento_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.nome

class Oportunidade(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    data_criacao = models.DateField()
    vendedor = models.ForeignKey(Vendedor, on_delete=models.SET_NULL, null=True, blank=True)
    canal = models.ForeignKey(Canal, on_delete=models.SET_NULL, null=True, blank=True)
    campanha = models.ForeignKey(Campanha, on_delete=models.SET_NULL, null=True, blank=True)
    estagio = models.CharField(max_length=50)
    probabilidade = models.FloatField(default=0.0)
    data_previsao_fechamento = models.DateField(null=True, blank=True)
    valor_potencial = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    receita_reconhecida = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    custo_investimento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[
        ('Aberta', 'Aberta'),
        ('Ganha', 'Ganha'),
        ('Perdida', 'Perdida'),
    ], default='Aberta')
    # Campos específicos
    vidas_contratadas = models.IntegerField(null=True, blank=True)
    pais_cliente = models.CharField(max_length=50, null=True, blank=True)
    tipo_receita = models.CharField(max_length=20, null=True, blank=True)
    mrr_mensal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.empresa.nome} - {self.id}"

class Meta(models.Model):
    ano_mes = models.CharField(max_length=7)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    meta_receita = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        unique_together = ('ano_mes', 'empresa')

class MarketingInvestimento(models.Model):
    ano_mes = models.CharField(max_length=7)
    canal = models.ForeignKey(Canal, on_delete=models.CASCADE)
    investimento = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ('ano_mes', 'canal')
