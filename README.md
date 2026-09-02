formata esse .md pra mim porfavor
markdown
# 🚀 Dashboard Executivo — Grupo Mont

**Desafio técnico** | Montseguro · Prop5 · TechBrabo

---

## 📋 Sobre o desafio

O Grupo Mont tem três operações com modelos de negócio completamente diferentes. O desafio era construir uma **visão executiva** que permitisse ao CEO entender rapidamente a saúde do grupo, sem perder as particularidades de cada empresa.

O briefing deixou claro: não era só sobre fazer gráficos bonitos. Era sobre **entender o negócio, modelar dados, definir KPIs relevantes e construir uma ferramenta que realmente ajude a tomar decisões**.

Foi isso que eu tentei fazer.

---

## 🧠 O que eu entendi sobre as empresas

### Montseguro
Corretora de planos de saúde empresariais. O funil é: **Lead → Cotação → Proposta → Contratação → Implantação → Ativo**. O ponto crítico aqui é que **contratação não é implantação** — se o contrato não vira cliente ativo, a receita não chega. Por isso, a **taxa de implantação** é um dos KPIs mais importantes pra essa empresa.

### Prop5
Consultoria de investimentos para brasileiros no exterior. Aqui, **valor do imóvel não é receita** — a receita é a comissão sobre a operação. O ciclo é longo e consultivo, então o **pipeline ponderado** (valor × probabilidade) é mais honesto do que pipeline bruto.

### TechBrabo
Tecnologia B2B. O grande desafio é separar **receita pontual** de **receita recorrente (MRR)**. O MRR é o KPI mais importante pra entender se o negócio tem base previsível ou depende de vender projeto novo todo mês. E o **% de projetos no prazo** conecta vendas com capacidade de entrega.

---

## 🏗️ Como eu estruturei a solução

### Backend (Django + DRF)

Modelos separados por empresa:

- `MontseguroLead`, `MontseguroFunil`, `MontseguroClienteAtivo`
- `Prop5Lead`, `Prop5Oportunidade`
- `TechbraboLead`, `TechbraboOportunidade`, `TechbraboProjeto`
- `Marketing` e `MetaEmpresa` (comuns)

**Decisão**: Modelos separados permitem que cada empresa tenha campos específicos (ex: `vidas_ativas` na Montseguro, `mrr` na TechBrabo) sem poluir a estrutura das outras. Isso respeita as particularidades do negócio.

### Endpoints de KPI

| Endpoint | Descrição |
|----------|-----------|
| `/api/montseguro/kpis/` | KPIs específicos da Montseguro (receita de comissão, churn, CAC, vidas ativas, taxas de conversão e implantação) |
| `/api/prop5/kpis/` | KPIs da Prop5 (comissão realizada, pipeline ponderado, ciclo médio, CAC) |
| `/api/techbrabo/kpis/` | KPIs da TechBrabo (MRR, crescimento, margem, SLA, receita pontual) |
| `/api/kpis/ceo-overview/` | Visão consolidada do grupo (receita total, meta, atingimento, forecast, gap) |
| `/api/kpis/comparativos/` | Indicadores comparáveis entre empresas (produtividade ajustada, CPLQ, conversão ajustada) |
| `/api/kpis/evolucao-receita/` | Série histórica de receita (últimos N meses) |
| `/api/kpis/metas-projecao/` | Ritmo de meta, necessidade diária e gap de ritmo |
| `/api/marketing/` | Dados de investimento e leads por canal |
| `/api/metas/` | Metas por empresa/mês |

### Frontend (React + shadcn/ui + Tailwind)

**Páginas implementadas**:

1. **CEO Overview** — consolidado do grupo com cards de totais, gráfico comparativo, banner de insights e detalhamento por empresa. É a primeira tela que o CEO vê.
2. **Comercial** — funil com conversões por etapa e ranking de vendedores. Configuração centralizada em `funilConfig.js`, então cada empresa define o que é uma etapa e o que é "resultado".
3. **Marketing** — investimento por canal, evolução mensal e CPL (custo por lead). Cada empresa tem sua própria aba.
4. **Empresas** — drill-down individual com KPIs específicos, gráficos de funil e análise de carteira.
5. **Insights** — alertas baseados em limiares (churn alto, meta baixa, projetos atrasados, etc.). As regras estão centralizadas em `rules.js`.
6. **Comparativos** — indicadores padronizados entre empresas, com tabela e cards de destaque.
7. **Metas e Projeção** — acompanhamento de ritmo de meta com meta esperada até hoje, gap de ritmo e necessidade diária.

---

## 📊 KPIs que eu escolhi e por quê

### Montseguro

| KPI | Finalidade | Fórmula |
|-----|------------|---------|
| **Receita de Comissão Mensal** | Resultado financeiro efetivo do mês | Σ prêmio_mensal dos contratos implantados e ativos × % de comissão média |
| **Atingimento de Meta** | Ritmo frente ao objetivo do mês | Receita do mês / meta_receita_comissao |
| **Taxa de Conversão Lead → Contratação** | Eficiência ponta a ponta do funil comercial | contratações no período / leads no período |
| **Taxa de Implantação** | Mede se o vendido está virando cliente ativo | implantados / contratados no período |
| **Vidas Ativas sob Gestão** | Tamanho real da carteira | Σ vidas_ativas dos contratos não cancelados |
| **Ticket Médio (Prêmio Mensal)** | Valor médio por contrato fechado | Σ prêmio_mensal implantado / nº contratos implantados |
| **CAC** | Custo de aquisição por novo contrato implantado | investimento total em Marketing / novos contratos implantados |
| **Taxa de Churn** | Saúde da base já conquistada | contratos cancelados / contratos ativos no início do período |

### Prop5

| KPI | Finalidade | Fórmula |
|-----|------------|---------|
| **Receita/Comissão Realizada** | Resultado financeiro efetivo | Σ comissão das oportunidades fechadas no período |
| **Pipeline Ponderado** | Estimativa realista do pipeline | Σ (valor_estimado × probabilidade) das oportunidades em aberto |
| **Taxa de Conversão Lead → Fechamento** | Eficiência do funil consultivo | oportunidades fechadas / leads do período |
| **Ciclo Médio de Venda** | Tempo entre entrada e fechamento | média (data_fechamento − data_criacao) |
| **Ticket Médio por Operação** | Valor médio de cada operação estruturada | Σ valor_fechado / nº de fechamentos |
| **CAC** | Custo de aquisição por cliente fechado | investimento de Marketing / fechamentos |
| **Atingimento de Meta** | Ritmo frente ao objetivo | comissão realizada / meta_comissao |

### TechBrabo

| KPI | Finalidade | Fórmula |
|-----|------------|---------|
| **MRR** | Base de receita previsível | Σ mrr de todos os projetos recorrentes ativos |
| **Crescimento de MRR (MoM)** | Expansão da base recorrente | (MRR atual − MRR anterior) / MRR anterior |
| **Receita Pontual do Período** | Projetos únicos (não recorrentes) | Σ valor_contrato com tipo_receita = "Pontual" |
| **Ticket Médio por Contrato** | Valor médio negociado | Σ valor_contrato / nº contratos assinados |
| **Pipeline/Forecast** | Projeção de novos contratos | Σ valor_proposta das propostas enviadas × taxa histórica |
| **Margem Média dos Projetos** | Sustentabilidade do crescimento | Σ margem / Σ valor_contrato dos projetos concluídos |
| **% de Projetos no Prazo** | Capacidade de entrega | projetos concluídos sem atraso / total de concluídos |
| **Expansão vs. Novo Cliente** | Origem do crescimento | Σ valor_contrato com cliente_existente / receita total |
| **CAC** | Custo de aquisição por contrato | investimento de Marketing / novos contratos |

---

## 🔍 Dados faltantes (e o que eu fiz sobre isso)

Identifiquei campos que seriam necessários para uma análise mais precisa, mas que não estavam disponíveis:

- **Montseguro**: % de comissão por operadora (usei uma média fixa de 15%)
- **Prop5**: data de renovação de contratos (não temos churn real)
- **TechBrabo**: horas apontadas por projeto (margem é estimada)

Documentei essas limitações e, para demonstrar como seria com dados completos, criei um script de enriquecimento que gera uma versão estendida do JSON com campos extras.

---
## Acesse o projeto em
https://montdashboard.vercel.app

## 🛠️ Como rodar o projeto localmente

### Pré-requisitos

- **Python 3.12+** (com `venv` e `pip`)
- **Node.js 18+** (com `npm`)
- **Git** (opcional, para clonar)

### Passo a passo (Windows / Linux / Mac)

#### 1. Clone o repositório (ou baixe os arquivos)

```bash
git clone https://github.com/seu-usuario/grupo-mont-challenge.git
cd grupo-mont-challenge
2. Execute o script de automação (backend + frontend)
Na raiz do projeto (onde está o run.py), execute:
```
```bash
python run.py
```
Esse script vai:

Criar um ambiente virtual Python (venv/)

Instalar todas as dependências do backend (a partir de backend/requirements.txt)

Rodar as migrações do Django

Carregar os dados de mock (gerando um banco SQLite populado)

Iniciar o servidor Django em http://localhost:8000

Para instalar também as dependências do frontend, use a flag --frontend:

```bash
python run.py --frontend
```

Para pular o carregamento dos dados mock (se já tiver um banco com dados):

```bash
python run.py --no-mock
```
Para mudar a porta do backend:

```bash
python run.py --port 8001
```
### 3. Rode o frontend separadamente (em outro terminal)
```bash
cd frontend
npm install   # se não tiver rodado com --frontend
npm run dev
```
O frontend estará disponível em http://localhost:5173 (ou a porta que o Vite indicar).

### 4. Acesse a aplicação
Frontend: http://localhost:5173

API: http://localhost:8000/api/...

Rodando sem o script automático (passo a passo manual)
Se preferir fazer manualmente:

Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Linux/Mac
# ou venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py load_mock_data --reset
python manage.py runserver
```
Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📂 Estrutura de dados
Montseguro
MontseguroLead: lead gerado (canal, porte da empresa, vidas estimadas)

MontseguroFunil: evolução do lead (cotação, proposta, contratação, implantação)

MontseguroClienteAtivo: contratos implantados e ativos

Prop5
Prop5Lead: lead com país de residência e canal

Prop5Oportunidade: oportunidade com estágio, probabilidade, valor, comissão

TechBrabo
TechbraboLead: lead com tipo de solução e canal

TechbraboOportunidade: oportunidade com tipo de receita, valor, MRR

TechbraboProjeto: projeto vinculado à oportunidade, com custo, margem, status

Comuns
Marketing: investimento e leads por canal/mês/empresa

MetaEmpresa: metas de receita e quantidade por mês/empresa

## 🎨 Extras que adicionei
Dark mode — toggle na sidebar, com persistência via localStorage

Tipografia refinada — Geist Variable, com hierarquia clara e tabular-nums pra números

Gráfico de evolução da receita — últimos 6 meses, com linhas por empresa e total do grupo

Banner de insights na página CEO Overview — os 3 alertas mais importantes ficam visíveis imediatamente

Página de Metas e Projeção — ritmo de meta, gap e necessidade diária

Logos das empresas — iniciais estilizadas (ou imagens, se disponíveis)

Responsividade — sidebar colapsável em mobile e grids adaptáveis

## 🚧 Limitações conhecidas
Churn da Prop5 e TechBrabo: não calculado por falta de dados de cancelamento/renovação.

Margem da TechBrabo: estimada com base em custo_hora fixo, sem apontamento real de horas.

Comissão da Montseguro: fixa em 15% (não varia por operadora).

Persistência de filtros: o seletor de mês não é mantido entre telas.

Desempenho: para volumes muito grandes (milhares de leads), seria necessário cache ou otimização de queries.

## 📈 Evoluções futuras (se tivesse mais tempo)
Inclusão de autenticação e perfis de usuário (CEO, Comercial, Marketing).

Alertas em tempo real via WebSocket.

Forecast mais sofisticado (regressão linear, machine learning).

Integração com dados reais via API externa (ou leitura de planilhas).

Testes automatizados (unitários e de integração).

Deploy automatizado com GitHub Actions.

## 🧪 Tecnologias utilizadas
Backend: Python 3.12, Django 6.1, Django REST Framework, SQLite3

Frontend: React 19, Vite 8, shadcn/ui, Tailwind CSS 4, Recharts

Ferramentas: Git, npm, pip, venv

## 📄 Licença
Este projeto foi desenvolvido como parte de um desafio técnico para o Grupo Mont. Todos os direitos reservados.

Desenvolvido por — Thiago Silva Ribeiro
Data — Setembro de 2026
