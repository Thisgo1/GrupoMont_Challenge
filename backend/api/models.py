from django.db import models


class Empresa(models.TextChoices):
    MONTSEGURO = "montseguro", "Montseguro"
    PROP5 = "prop5", "Prop5"
    TECHBRABO = "techbrabo", "TechBrabo"


# ---------------------------------------------------------------
# MONTSEGURO — planos de saúde empresariais
# ---------------------------------------------------------------
class MontseguroLead(models.Model):
    data_criacao = models.DateField()
    mes_referencia = models.CharField(max_length=7)  # "2026-03"
    canal = models.CharField(max_length=50)
    porte_empresa = models.CharField(max_length=30)
    vidas_estimadas = models.PositiveIntegerField()

    def __str__(self):
        return f"Lead #{self.id} ({self.canal})"


class MontseguroFunil(models.Model):
    """
    Uma linha por lead, com o avanço no funil: cotação -> proposta ->
    contratação -> implantação. Campos nulos = etapa não alcançada.
    """
    lead = models.OneToOneField(MontseguroLead, on_delete=models.CASCADE, related_name="funil")
    vendedor = models.CharField(max_length=100)
    operadora = models.CharField(max_length=50, blank=True, null=True)
    vidas = models.PositiveIntegerField()
    premio_mensal_estimado = models.DecimalField(max_digits=12, decimal_places=2)

    data_cotacao = models.DateField(blank=True, null=True)
    data_proposta = models.DateField(blank=True, null=True)
    data_contratacao = models.DateField(blank=True, null=True)
    data_implantacao = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=40)
    motivo_perda = models.CharField(max_length=100, blank=True, null=True)


class MontseguroClienteAtivo(models.Model):
    lead = models.OneToOneField(MontseguroLead, on_delete=models.CASCADE, related_name="cliente_ativo")
    operadora = models.CharField(max_length=50)
    vidas_ativas = models.PositiveIntegerField()
    premio_mensal = models.DecimalField(max_digits=12, decimal_places=2)
    data_ativacao = models.DateField()
    cancelado = models.BooleanField(default=False)
    data_cancelamento = models.DateField(blank=True, null=True)


# ---------------------------------------------------------------
# PROP5 — consultoria e estruturação patrimonial
# ---------------------------------------------------------------
class Prop5Lead(models.Model):
    data_criacao = models.DateField()
    mes_referencia = models.CharField(max_length=7)
    canal = models.CharField(max_length=50)
    pais_residencia = models.CharField(max_length=50)

    def __str__(self):
        return f"Lead #{self.id} ({self.pais_residencia})"


class Prop5Oportunidade(models.Model):
    lead = models.OneToOneField(Prop5Lead, on_delete=models.CASCADE, related_name="oportunidade")
    vendedor = models.CharField(max_length=100)
    valor_estimado = models.DecimalField(max_digits=14, decimal_places=2)
    probabilidade = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    estagio = models.CharField(max_length=50)

    data_diagnostico = models.DateField(blank=True, null=True)
    data_reuniao_consultiva = models.DateField(blank=True, null=True)
    data_fechamento = models.DateField(blank=True, null=True)
    valor_fechado = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    comissao = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)


# ---------------------------------------------------------------
# TECHBRABO — tecnologia B2B
# ---------------------------------------------------------------
class TechbraboLead(models.Model):
    data_criacao = models.DateField()
    mes_referencia = models.CharField(max_length=7)
    canal = models.CharField(max_length=50)
    tipo_solucao = models.CharField(max_length=50)

    def __str__(self):
        return f"Lead #{self.id} ({self.tipo_solucao})"


class TechbraboOportunidade(models.Model):
    lead = models.OneToOneField(TechbraboLead, on_delete=models.CASCADE, related_name="oportunidade")
    vendedor = models.CharField(max_length=100)
    tipo_solucao = models.CharField(max_length=50)
    tipo_receita = models.CharField(max_length=20)  # Pontual / Recorrente / Híbrido
    valor_proposta = models.DecimalField(max_digits=14, decimal_places=2)
    estagio = models.CharField(max_length=50)
    cliente_existente = models.BooleanField(default=False)

    data_proposta = models.DateField(blank=True, null=True)
    data_contrato = models.DateField(blank=True, null=True)
    valor_contrato = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    mrr = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)


class TechbraboProjeto(models.Model):
    oportunidade = models.OneToOneField(TechbraboOportunidade, on_delete=models.CASCADE, related_name="projeto")
    tipo_solucao = models.CharField(max_length=50)
    valor_contrato = models.DecimalField(max_digits=14, decimal_places=2)
    custo_estimado = models.DecimalField(max_digits=14, decimal_places=2)
    margem = models.DecimalField(max_digits=14, decimal_places=2)
    margem_percentual = models.DecimalField(max_digits=5, decimal_places=1)
    status = models.CharField(max_length=30)  # Em andamento / Concluído / Atrasado

    data_inicio = models.DateField()
    data_entrega_prevista = models.DateField()
    data_entrega_real = models.DateField(blank=True, null=True)
    mrr = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)


# ---------------------------------------------------------------
# COMUM ÀS TRÊS EMPRESAS
# ---------------------------------------------------------------
class Marketing(models.Model):
    empresa = models.CharField(max_length=20, choices=Empresa.choices)
    mes = models.CharField(max_length=7)
    canal = models.CharField(max_length=50)
    investimento = models.DecimalField(max_digits=12, decimal_places=2)
    leads_gerados = models.PositiveIntegerField()

    class Meta:
        indexes = [models.Index(fields=["empresa", "mes"])]


class MetaEmpresa(models.Model):
    """
    Nomeada 'MetaEmpresa' (e não 'Meta') pra não colidir com a classe
    interna Meta que o Django usa em todo model pra opções (Meta.indexes etc).
    """
    empresa = models.CharField(max_length=20, choices=Empresa.choices)
    mes = models.CharField(max_length=7)
    # nomes de campo variavam por empresa no JSON original (meta_receita_comissao,
    # meta_comissao, meta_receita_total) — aqui padronizamos em um único campo
    # de valor-alvo pra simplificar consultas comparativas entre empresas.
    meta_receita = models.DecimalField(max_digits=14, decimal_places=2)
    meta_quantidade = models.PositiveIntegerField(help_text="novos contratos/fechamentos esperados no mês")

    class Meta:
        indexes = [models.Index(fields=["empresa", "mes"])]
