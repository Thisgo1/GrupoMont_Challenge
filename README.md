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

Cada empresa tem seu próprio endpoint com KPIs específicos:

| Endpoint | O que retorna |
|----------|---------------|
| `/montseguro/kpis/` | Receita de comissão, churn, CAC, vidas ativas, taxas de conversão e implantação |
| `/prop5/kpis/` | Comissão realizada, pipeline ponderado, ciclo médio, CAC |
| `/techbrabo/kpis/` | MRR, crescimento, margem, SLA, receita pontual |

Além disso, criei endpoints consolidados:

- `/kpis/ceo-overview/` — visão de grupo com receita, meta, atingimento, forecast e gap
- `/kpis/comparativos/` — produtividade ajustada, CPLQ e conversão ajustada (indicadores comparáveis entre empresas)
- `/kpis/evolucao-receita/` — série histórica de 6 meses
- `/kpis/metas-projecao/` — ritmo de meta, necessidade diária e gap de ritmo

### Frontend (React + shadcn/ui + Tailwind)

Decidi usar shadcn/ui porque ele já entrega componentes acessíveis e estilizados com Tailwind, o que me permitiu focar na lógica de negócio em vez de ficar ajustando CSS. A experiência ficou limpa, consistente e responsiva.

**Páginas implementadas**:

1. **CEO Overview** — consolidado do grupo com cards de totais, gráfico comparativo, banner de insights e detalhamento por empresa. É a primeira tela que o CEO vê.
2. **Comercial** — funil com conversões por etapa e ranking de vendedores. Configuração centralizada em `funilConfig.js`, então cada empresa define o que é uma etapa e o que é "resultado".
3. **Marketing** — investimento por canal, evolução mensal e CPL (custo por lead). Cada empresa tem sua própria aba.
4. **Empresas** — drill-down individual com KPIs específicos, gráficos de funil e análise de carteira.
5. **Insights** — alertas baseados em limiares (churn alto, meta baixa, projetos atrasados, etc.). As regras estão centralizadas em `rules.js`.
6. **Comparativos** — indicadores padronizados entre empresas, com tabela e cards de destaque.
7. **Metas e Projeção** — acompanhamento de ritmo de meta com meta esperada até hoje, gap de ritmo e necessidade diária.

### Componentes reutilizáveis

- `KpiCard` — exibe valor com formatação (moeda, percentual, dias) e status de semáforo
- `BarList` — barras horizontais para funis e rankings
- `RankingTable` — performance de vendedores
- `StatusTable` — distribuição de status
- `MesSelector` — seletor de mês (acumulado ou mês específico)
- `EmpresaLogo` — logo ou iniciais estilizadas

---

## 📊 KPIs que eu escolhi e por quê

O briefing não entregou uma lista fechada de KPIs — e isso foi proposital. A ideia era justamente avaliar se eu sabia identificar o que realmente importa. Esses foram os meus critérios:

- **Montseguro**: receita de comissão (não prêmio bruto), taxa de implantação (gargalo operacional), vidas ativas (tamanho da carteira) e churn.
- **Prop5**: comissão realizada (não valor do imóvel), pipeline ponderado (não bruto), ciclo médio de venda e CAC.
- **TechBrabo**: MRR (base previsível), margem média (sustentabilidade), % de projetos no prazo (capacidade operacional) e expansão vs. cliente novo.

A escolha de cada KPI está documentada em `kpis-grupo-mont.md`, com nome, fórmula, fonte e interpretação.

---

## 🔍 Dados faltantes (e o que eu fiz sobre isso)

O briefing diz: *"Dados faltantes também são um achado"*. Isso me chamou atenção.

Identifiquei campos que seriam necessários para uma análise mais precisa, mas que não estavam disponíveis:

- **Montseguro**: % de comissão por operadora (usei uma média fixa de 15%)
- **Prop5**: data de renovação de contratos (não temos churn real)
- **TechBrabo**: horas apontadas por projeto (margem é estimada)

Documentei essas limitações em `docs/dados-faltantes.md` e, para demonstrar como seria com dados completos, criei um script (`enrich_mock_data.py`) que gera uma versão enriquecida do JSON com campos extras.

---

## 🎨 Extras que adicionei

Além do escopo mínimo, adicionei alguns diferenciais:

- **Dark mode** — toggle na sidebar, com persistência via localStorage
- **Tipografia refinada** — Geist Variable, com hierarquia clara e `tabular-nums` pra números
- **Gráfico de evolução da receita** — últimos 6 meses, com linhas por empresa e total do grupo
- **Banner de insights** na página CEO Overview — os 3 alertas mais importantes ficam visíveis imediatamente
- **Página de Metas e Projeção** — ritmo de meta, gap e necessidade diária
- **Logos das empresas** — iniciais estilizadas (ou imagens, se disponíveis)
- **Responsividade** — sidebar colapsável em mobile e grids adaptáveis

---

## 🛠️ Como rodar o projeto

### Backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py load_mock_data --path ../mock-data-grupo-mont.json
python manage.py runserver
