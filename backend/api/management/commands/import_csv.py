import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import (
    Empresa, Vendedor, Canal, Campanha,
    Oportunidade, Meta, MarketingInvestimento
)

class Command(BaseCommand):
    help = 'Importa dados dos CSVs para o banco de dados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='Caminho para a pasta com os CSVs (padrão: ../dados/)',
            default='../dados/'
        )

    def handle(self, *args, **options):
        base_path = options['path']
        self.stdout.write(f"Importando dados de: {base_path}")

        # 1. Importar dimensões (ordem importa por causa das FKs)
        self.import_empresas(base_path)
        self.import_vendedores(base_path)
        self.import_canais(base_path)
        self.import_campanhas(base_path)

        # 2. Importar tabelas fato
        self.import_oportunidades(base_path)
        self.import_metas(base_path)
        self.import_marketing_investimento(base_path)

        self.stdout.write(self.style.SUCCESS('Importação concluída com sucesso!'))

    @transaction.atomic
    def import_empresas(self, path):
        filename = os.path.join(path, 'dim_empresa.csv')
        if not os.path.exists(filename):
            self.stdout.write(self.style.WARNING(f'Arquivo {filename} não encontrado, pulando...'))
            return
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Empresa.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'nome': row['nome'],
                        'ticket_medio': row['ticket_medio'],
                        'ciclo_dias': row['ciclo_dias'],
                    }
                )
        self.stdout.write(f'✅ Empresas importadas: {Empresa.objects.count()}')

    @transaction.atomic
    def import_vendedores(self, path):
        filename = os.path.join(path, 'dim_vendedor.csv')
        if not os.path.exists(filename):
            self.stdout.write(self.style.WARNING(f'Arquivo {filename} não encontrado, pulando...'))
            return
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                empresa = Empresa.objects.get(id=row['empresa_principal']) if row['empresa_principal'] else None
                Vendedor.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'nome': row['nome'],
                        'equipe': row['equipe'],
                        'empresa_principal': empresa,
                    }
                )
        self.stdout.write(f'✅ Vendedores importados: {Vendedor.objects.count()}')

    @transaction.atomic
    def import_canais(self, path):
        filename = os.path.join(path, 'dim_canal.csv')
        if not os.path.exists(filename):
            self.stdout.write(self.style.WARNING(f'Arquivo {filename} não encontrado, pulando...'))
            return
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Canal.objects.update_or_create(
                    id=row['id'],
                    defaults={'nome': row['nome']}
                )
        self.stdout.write(f'✅ Canais importados: {Canal.objects.count()}')

    @transaction.atomic
    def import_campanhas(self, path):
        filename = os.path.join(path, 'dim_campanha.csv')
        if not os.path.exists(filename):
            self.stdout.write(self.style.WARNING(f'Arquivo {filename} não encontrado, pulando...'))
            return
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Campanha.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'nome': row['nome'],
                        'investimento_total': row.get('investimento_total', 0),
                    }
                )
        self.stdout.write(f'✅ Campanhas importadas: {Campanha.objects.count()}')

    @transaction.atomic
    def import_oportunidades(self, path):
        filename = os.path.join(path, 'oportunidades.csv')
        if not os.path.exists(filename):
            self.stdout.write(self.style.WARNING(f'Arquivo {filename} não encontrado, pulando...'))
            return
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                empresa = Empresa.objects.get(id=row['id_empresa'])
                vendedor = Vendedor.objects.filter(id=row['id_vendedor']).first()
                canal = Canal.objects.filter(id=row['id_canal']).first()
                campanha = Campanha.objects.filter(id=row['id_campanha']).first()

                Oportunidade.objects.update_or_create(
                    id=row['id_oportunidade'],
                    defaults={
                        'empresa': empresa,
                        'data_criacao': row['data_criacao'],
                        'vendedor': vendedor,
                        'canal': canal,
                        'campanha': campanha,
                        'estagio': row['estagio'],
                        'probabilidade': row.get('probabilidade', 0),
                        'data_previsao_fechamento': row.get('data_previsao_fechamento') or None,
                        'valor_potencial': row.get('valor_potencial', 0),
                        'receita_reconhecida': row.get('receita_reconhecida', 0),
                        'custo_investimento': row.get('custo_investimento', 0),
                        'status': row.get('status', 'Aberta'),
                        'vidas_contratadas': row.get('vidas_contratadas') or None,
                        'pais_cliente': row.get('pais_cliente') or None,
                        'tipo_receita': row.get('tipo_receita') or None,
                        'mrr_mensal': row.get('mrr_mensal') or None,
                    }
                )
        self.stdout.write(f'✅ Oportunidades importadas: {Oportunidade.objects.count()}')

    @transaction.atomic
    def import_metas(self, path):
        filename = os.path.join(path, 'metas.csv')
        if not os.path.exists(filename):
            self.stdout.write(self.style.WARNING(f'Arquivo {filename} não encontrado, pulando...'))
            return
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                empresa = Empresa.objects.get(id=row['id_empresa'])
                Meta.objects.update_or_create(
                    ano_mes=row['ano_mes'],
                    empresa=empresa,
                    defaults={'meta_receita': row['meta_receita']}
                )
        self.stdout.write(f'✅ Metas importadas: {Meta.objects.count()}')

    @transaction.atomic
    def import_marketing_investimento(self, path):
        filename = os.path.join(path, 'marketing_investimento.csv')
        if not os.path.exists(filename):
            self.stdout.write(self.style.WARNING(f'Arquivo {filename} não encontrado, pulando...'))
            return
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                canal = Canal.objects.get(id=row['id_canal'])
                MarketingInvestimento.objects.update_or_create(
                    ano_mes=row['ano_mes'],
                    canal=canal,
                    defaults={'investimento': row['investimento']}
                )
        self.stdout.write(f'✅ Marketing Investimento importados: {MarketingInvestimento.objects.count()}')
