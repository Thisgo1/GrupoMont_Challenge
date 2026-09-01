# KPIs Executivos — Grupo Mont
### Montseguro | Prop5 | TechBrabo

Critério de seleção: cada KPI abaixo responde a uma das perguntas executivas listadas no briefing (o que Marketing está trazendo, o que o Comercial está convertendo, o que a Operação está entregando, quanto o Financeiro está gerando, se o ritmo bate a meta). KPIs de vaidade (ex.: "total de leads" isolado, "número de contratos" sem valor associado) foram deixados de fora do nível de CEO — eles aparecem no dashboard Comercial/Marketing, não no CEO Overview.

Os campos de "Fonte" referenciam as tabelas do `mock-data-grupo-mont.json`.

---

## 1. KPIs consolidados do Grupo (CEO Overview)

| Nome | Finalidade | Fórmula | Fonte | Interpretação |
|---|---|---|---|---|
| Receita Total do Grupo | Entender o resultado financeiro agregado no período | Σ (receita reconhecida de Montseguro + comissão Prop5 + receita TechBrabo) | `montseguro.clientes_ativos` (prêmio × meses ativos), `prop5.oportunidades.comissao`, `techbrabo.projetos` + `mrr` | Base para todas as demais leituras comparativas; sempre exibida ao lado da meta consolidada |
| Atingimento de Meta Consolidado | Saber se o grupo está no ritmo do período | Receita Total do Grupo / Σ metas das 3 empresas | `*.metas` de cada empresa | < 90% do "esperado até hoje" liga o alerta amarelo/vermelho |
| Crescimento MoM do Grupo | Detectar tendência de curto prazo | (Receita mês atual − Receita mês anterior) / Receita mês anterior | Receita Total do Grupo por mês | Crescimento negativo por 2 meses seguidos é gatilho de alerta |
| Eficiência de Aquisição (CPO Comparável) | Comparar Marketing entre negócios com tickets muito diferentes | Investimento em Marketing / Oportunidades Qualificadas geradas (não leads brutos) | `*.marketing` + eventos de qualificação do funil de cada empresa | Permite comparar Montseguro, Prop5 e TechBrabo sem distorcer pelo ticket médio |
| Forecast de Fechamento do Grupo | Antecipar se a meta do período será batida | Σ forecast individual de cada empresa (ver KPIs de forecast abaixo) | Pipeline ponderado por estágio de cada empresa | Municia a decisão de "onde investir/corrigir nas próximas semanas" |

---

## 2. Montseguro — planos de saúde empresariais

Lógica: cotação ≠ proposta ≠ contratação ≠ implantação. O CEO precisa ver receita e qualidade de funil, não volume bruto de contratos.

| Nome | Finalidade | Fórmula | Fonte | Interpretação |
|---|---|---|---|---|
| Receita de Comissão Mensal | Resultado financeiro efetivo do mês | Σ prêmio_mensal dos contratos implantados e ativos no mês × % de comissão média | `clientes_ativos` | Só conta receita de contrato **implantado**, não apenas contratado |
| Atingimento de Meta | Ritmo frente ao objetivo do mês | Receita do mês / meta_receita_comissao | `metas` | Cruza com "meta esperada até hoje" (dia do mês / dias do mês × meta) |
| Taxa de Conversão Lead → Contratação | Eficiência ponta a ponta do funil comercial | contratações no período / leads no período | `funil` | Separado por canal revela se o problema é qualidade de lead ou execução comercial |
| Taxa de Implantação | Mede se o vendido está virando cliente ativo (gargalo de operação) | implantados / contratados no período | `funil` (status = "Contratado…" vs "Implantado") | Contratação alta com implantação baixa = gargalo pós-venda, não comercial |
| Ticket Médio (Prêmio Mensal) | Entender o valor médio por contrato fechado | Σ prêmio_mensal implantado / nº contratos implantados | `clientes_ativos` | Cruzar com porte de empresa (MEI/pequena/média) explica variação |
| CAC | Custo de aquisição de cada novo contrato implantado | investimento total em Marketing do mês / novos contratos implantados no mês | `marketing` + `funil` | Comparar com ticket médio × tempo médio de retenção para checar payback |
| Vidas Ativas sob Gestão | Tamanho real da carteira (não só nº de contratos) | Σ vidas_ativas dos contratos não cancelados | `clientes_ativos` | Cresce com novos contratos e cai com churn — é a base recorrente do negócio |
| Taxa de Churn | Saúde da base já conquistada | contratos cancelados no período / contratos ativos no início do período | `clientes_ativos` (campo `cancelado`) | Churn alto anula o esforço comercial do mês |

---

## 3. Prop5 — consultoria e estruturação patrimonial

Lógica: valor de imóvel ≠ receita; pipeline ≠ venda fechada. O CEO precisa distinguir volume estruturado de comissão efetiva.

| Nome | Finalidade | Fórmula | Fonte | Interpretação |
|---|---|---|---|---|
| Receita/Comissão Realizada | Resultado financeiro efetivo do período | Σ comissao das oportunidades com estágio = "Fechado" no período | `oportunidades` | É o único número que deve ser tratado como "faturamento" — não o valor_fechado bruto |
| Volume de Pipeline Ponderado | Estimar quanto do pipeline em aberto tende a virar receita | Σ (valor_estimado × probabilidade) das oportunidades em aberto | `oportunidades` | Mais útil que "pipeline total" puro, que superestima o que vai fechar |
| Taxa de Conversão Lead → Fechamento | Eficiência do funil consultivo (ciclo longo) | oportunidades fechadas / leads que entraram no período de referência | `leads` + `oportunidades` | Ciclo longo exige olhar por coorte de entrada, não só pelo mês do fechamento |
| Ciclo Médio de Venda | Entender o tempo entre entrada e fechamento | média (data_fechamento − data_criacao do lead) | `oportunidades` + `leads` | Ciclo maior que o normal do país/canal pode indicar objeção não tratada |
| Ticket Médio por Operação Fechada | Valor médio de cada operação estruturada | Σ valor_fechado / nº de fechamentos | `oportunidades` | Cruzar com país de origem e canal para achar o perfil mais valioso |
| CAC | Custo de aquisição por cliente fechado | investimento de Marketing / fechamentos no período | `marketing` + `oportunidades` | Ciclo longo → olhar CAC por coorte, não por mês corrido |
| Atingimento de Meta | Ritmo frente ao objetivo do mês | comissão realizada / meta_comissao | `metas` | Junto com o forecast, indica se vale acelerar negociações em andamento |
| Forecast de Fechamento | Projeção de receita do período | pipeline ponderado das oportunidades com data prevista no período + receita já realizada | `oportunidades` | Metodologia simples de "ritmo mantido"; pode evoluir para regressão por estágio |

---

## 4. TechBrabo — tecnologia B2B

Lógica: contrato assinado ≠ receita reconhecida; receita pontual e recorrente precisam ser lidas separadamente; pipeline precisa ser cruzado com capacidade de entrega.

| Nome | Finalidade | Fórmula | Fonte | Interpretação |
|---|---|---|---|---|
| MRR (Receita Recorrente Mensal) | Medir a base de receita previsível do negócio | Σ mrr de todos os projetos/contratos recorrentes ativos | `projetos` | É o indicador mais importante para um CEO de tech — mostra se o negócio depende de vender projeto novo todo mês |
| Crescimento de MRR (MoM) | Ver se a base recorrente está expandindo | (MRR mês atual − MRR mês anterior) / MRR mês anterior | `projetos` por mês | MRR estagnado com muitos projetos pontuais = dependência de vendas pontuais |
| Receita Pontual do Período | Entender o quanto do resultado é projeto único (não recorrente) | Σ valor_contrato de contratos com tipo_receita = "Pontual" fechados no período | `oportunidades` | Complementa o MRR sem misturar naturezas de receita diferentes |
| Pipeline / Forecast Comercial | Antecipar novos contratos do próximo período | Σ valor_proposta das oportunidades em "Proposta enviada", ponderado por taxa histórica de fechamento | `oportunidades` | Cruzar com capacidade de entrega antes de "empurrar" mais vendas |
| Ticket Médio por Contrato | Entender o valor médio negociado | Σ valor_contrato / nº de contratos assinados | `oportunidades` | Separar por tipo_solucao mostra onde está o maior valor agregado |
| Margem Média dos Projetos | Saber se o crescimento em receita está gerando lucro | Σ margem / Σ valor_contrato dos projetos concluídos | `projetos` | Receita subindo com margem caindo é um alerta silencioso |
| % de Projetos no Prazo (SLA de Entrega) | Medir se a operação sustenta o que foi vendido | projetos com status "Concluído" e sem atraso / total de projetos concluídos | `projetos` | Vendido crescendo + atraso subindo = gargalo de capacidade operacional |
| Expansão vs. Novo Cliente | Ver se o crescimento vem de upsell ou aquisição | Σ valor_contrato com cliente_existente = true / receita total do período | `oportunidades` (campo `cliente_existente`) | Um mix saudável reduz dependência de aquisição constante |
| CAC | Custo de aquisição por novo contrato | investimento em Marketing / novos contratos assinados no período | `marketing` + `oportunidades` | Comparar com ticket médio e margem, não só com receita bruta |

---

## 5. Semáforo executivo sugerido (aplicável aos três negócios)

| Status | Regra proposta |
|---|---|
| 🟢 Verde | Atingimento de meta (real vs. esperado até hoje) ≥ 95% **e** forecast de fechamento ≥ meta do período |
| 🟡 Amarelo | Atingimento entre 80% e 95% **ou** forecast entre 90% e 100% da meta |
| 🔴 Vermelho | Atingimento < 80% **ou** forecast < 90% da meta **ou** churn/atraso acima do limite definido por empresa |

---

## 6. Dados que faltariam numa base real (achado a documentar no README)

Mesmo com o mock cobrindo os KPIs acima, numa base real do Grupo Mont provavelmente faltariam:
- **% de comissão efetiva por operadora** (Montseguro) — sem isso, a receita de comissão é uma estimativa, não um valor exato.
- **Motivo de perda padronizado** em todas as etapas (hoje só existe no funil da Montseguro) — necessário para os três negócios para gerar insights de gargalo confiáveis.
- **Custo de entrega por projeto detalhado por hora/recurso** (TechBrabo) — a margem calculada aqui é estimada; margem real exigiria apontamento de horas.
- **Data de renovação/cancelamento contratual** (Prop5 e TechBrabo recorrente) — sem isso, não dá para calcular churn real desses dois negócios, só da Montseguro.
