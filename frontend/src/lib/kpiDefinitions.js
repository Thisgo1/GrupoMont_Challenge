// src/lib/kpiDefinitions.js

export const kpiDefinitions = {
  // ============================================================
  // 1. KPIs CONSOLIDADOS DO GRUPO (CEO Overview)
  // ============================================================
  receita_total: {
    label: "Receita Total do Grupo",
    description: "Resultado financeiro agregado do período, somando a receita reconhecida das três empresas.",
    formula: "Σ (receita Montseguro + comissão Prop5 + receita TechBrabo)"
  },
  meta_total: {
    label: "Meta Total do Grupo",
    description: "Soma das metas de receita das três empresas para o período.",
    formula: "Σ meta_receita de Montseguro, Prop5 e TechBrabo"
  },
  atingimento_meta: {
    label: "Atingimento de Meta",
    description: "Percentual da meta já realizado. Valores abaixo de 100% indicam necessidade de aceleração.",
    formula: "(receita realizada / meta do período) × 100"
  },
  forecast: {
    label: "Forecast",
    description: "Projeção de receita para o período, considerando o ritmo atual e o pipeline em aberto.",
    formula: "Receita realizada + pipeline ponderado"
  },
  gap: {
    label: "Gap",
    description: "Diferença entre o forecast e a meta. Gap negativo indica risco de não atingir a meta.",
    formula: "Forecast − Meta"
  },
  ticket_medio: {
    label: "Ticket Médio",
    description: "Valor médio por negócio fechado no período. Ajuda a entender o perfil dos clientes.",
    formula: "Receita total / número de negócios"
  },
  leads_total: {
    label: "Leads Totais",
    description: "Total de leads gerados no período, somando as três empresas.",
    formula: "Σ leads de Montseguro, Prop5 e TechBrabo"
  },
  taxa_conversao: {
    label: "Taxa de Conversão Geral",
    description: "Percentual de leads que se tornaram negócios fechados (contratos, vendas, etc.).",
    formula: "(negócios fechados / leads totais) × 100"
  },
  crescimento_mom: {
    label: "Crescimento Mês a Mês",
    description: "Variação percentual da receita em relação ao mês anterior. Crescimento negativo por 2 meses seguidos é alerta.",
    formula: "((Receita atual − Receita anterior) / Receita anterior) × 100"
  },
  investimento_marketing: {
    label: "Investimento em Marketing",
    description: "Total investido em Marketing no período, somando as três empresas.",
    formula: "Σ investimento de Montseguro, Prop5 e TechBrabo"
  },
  roi_marketing: {
    label: "ROI de Marketing",
    description: "Retorno sobre o investimento em Marketing. Indica se o investimento está gerando resultado.",
    formula: "((Receita − Investimento) / Investimento) × 100"
  },
  meta_esperada: {
    label: "Meta esperada até hoje",
    description: "Quanto da meta deveria ter sido realizado considerando o dia do mês (ritmo linear).",
    formula: "Meta × (dias corridos / dias úteis do mês)"
  },
  gap_ritmo: {
    label: "Gap de ritmo",
    description: "Diferença entre o realizado e a meta esperada até hoje. Negativo indica que está abaixo do ritmo necessário.",
    formula: "Realizado − Meta esperada"
  },
  necessidade_diaria: {
    label: "Necessidade diária",
    description: "Quanto precisa ser produzido por dia útil para atingir a meta até o fim do mês.",
    formula: "(Meta − Realizado) / dias úteis restantes"
  },
  dias_uteis: {
    label: "Dias úteis restantes",
    description: "Quantos dias úteis ainda restam no mês para correr atrás da meta.",
    formula: "dias úteis totais − dias corridos"
  },

  // ============================================================
  // 2. MONTSEGURO
  // ============================================================
  receita_comissao: {
    label: "Receita de Comissão",
    description: "Resultado financeiro efetivo do mês, calculado sobre o prêmio dos contratos já implantados e ativos.",
    formula: "Σ prêmio_mensal dos contratos implantados e ativos × % de comissão média"
  },
  taxa_implantacao: {
    label: "Taxa de Implantação",
    description: "Percentual de contratos que efetivamente se tornaram clientes ativos. Implantação baixa com contratação alta indica gargalo pós-venda.",
    formula: "(implantados / contratados no período) × 100"
  },
  vidas_ativas: {
    label: "Vidas Ativas",
    description: "Total de beneficiários cobertos por planos de saúde ativos. Reflete o tamanho real da carteira.",
    formula: "Σ vidas_ativas dos contratos não cancelados"
  },
  churn: {
    label: "Taxa de Churn",
    description: "Percentual de clientes que cancelaram no período. Churn alto anula o esforço comercial.",
    formula: "(cancelamentos no mês / clientes ativos no início do mês) × 100"
  },
  cac: {
    label: "CAC (Custo de Aquisição)",
    description: "Custo médio para adquirir um novo cliente. Comparar com ticket médio e margem para avaliar payback.",
    formula: "investimento em Marketing / novos clientes no período"
  },
  taxa_conversao_lead_contratacao: {
    label: "Taxa de Conversão Lead → Contratação",
    description: "Eficiência ponta a ponta do funil comercial. Separar por canal revela se o problema é qualidade de lead ou execução comercial.",
    formula: "(contratações no período / leads no período) × 100"
  },
  ticket_medio_premio: {
    label: "Ticket Médio (Prêmio Mensal)",
    description: "Valor médio do prêmio mensal por contrato fechado. Cruzar com porte da empresa (MEI/pequena/média) explica variação.",
    formula: "Σ prêmio_mensal implantado / nº contratos implantados"
  },

  // ============================================================
  // 3. PROP5
  // ============================================================
  pipeline_ponderado: {
    label: "Pipeline Ponderado",
    description: "Valor estimado das oportunidades em aberto, ajustado pela probabilidade de fechamento. Mais realista que pipeline bruto.",
    formula: "Σ (valor_estimado × probabilidade) das oportunidades em aberto"
  },
  ciclo_medio: {
    label: "Ciclo Médio de Venda",
    description: "Tempo médio entre a entrada do lead e o fechamento da oportunidade. Ciclo muito longo pode indicar objeções não tratadas.",
    formula: "média (data_fechamento − data_criação do lead)"
  },
  ticket_medio_fechado: {
    label: "Ticket Médio por Operação Fechada",
    description: "Valor médio de cada operação estruturada. Cruzar com país de origem e canal para achar o perfil mais valioso.",
    formula: "Σ valor_fechado / nº de fechamentos"
  },
  taxa_conversao_lead_fechamento: {
    label: "Taxa de Conversão Lead → Fechamento",
    description: "Eficiência do funil consultivo. Ciclo longo exige olhar por coorte de entrada, não só pelo mês do fechamento.",
    formula: "(oportunidades fechadas / leads do período) × 100"
  },

  // ============================================================
  // 4. TECHBRABO
  // ============================================================
  mrr: {
    label: "MRR (Receita Recorrente Mensal)",
    description: "Base de receita previsível da TechBrabo. MRR crescente indica negócio mais sustentável e menos dependente de projetos pontuais.",
    formula: "Σ mrr de todos os contratos recorrentes ativos"
  },
  margem_media: {
    label: "Margem Média dos Projetos",
    description: "Margem de lucro média dos projetos concluídos. Receita subindo com margem caindo é um alerta silencioso.",
    formula: "Σ margem / Σ valor_contrato dos projetos concluídos"
  },
  projetos_prazo: {
    label: "% de Projetos no Prazo",
    description: "Percentual de projetos entregues dentro do prazo. Conecta vendas com capacidade de entrega.",
    formula: "(projetos concluídos sem atraso / total de concluídos) × 100"
  },
  expansao_clientes: {
    label: "Expansão vs. Novo Cliente",
    description: "Percentual da receita que vem de clientes existentes (upsell/cross-sell). Um mix saudável reduz dependência de aquisição constante.",
    formula: "Σ valor_contrato com cliente_existente / receita total do período"
  },
  receita_pontual: {
    label: "Receita Pontual do Período",
    description: "Receita de projetos únicos (não recorrentes). Complementa o MRR sem misturar naturezas de receita diferentes.",
    formula: "Σ valor_contrato de contratos com tipo_receita = 'Pontual' fechados no período"
  },
  ticket_medio_contrato: {
    label: "Ticket Médio por Contrato",
    description: "Valor médio negociado por contrato. Separar por tipo_solucao mostra onde está o maior valor agregado.",
    formula: "Σ valor_contrato / nº de contratos assinados"
  },
  pipeline_forecast: {
    label: "Pipeline / Forecast Comercial",
    description: "Projeção de novos contratos com base nas propostas enviadas, ponderada por taxa histórica de fechamento.",
    formula: "Σ valor_proposta das propostas enviadas × taxa histórica"
  },

  // ============================================================
  // 5. MÉTRICAS DE MARKETING (usadas na página Marketing)
  // ============================================================
  investimento_total: {
    label: "Investimento Total",
    description: "Soma de todo o investimento em Marketing no período, independente do canal.",
    formula: "Σ investimento de todos os canais"
  },
  leads_gerados: {
    label: "Leads Gerados",
    description: "Total de leads gerados por todos os canais no período.",
    formula: "Σ leads_gerados de todos os canais"
  },
  receita_estimada: {
    label: "Receita Estimada",
    description: "Receita atribuída aos leads gerados pelo Marketing, considerando o estágio de conversão de cada um.",
    formula: "Σ receita dos leads que avançaram no funil"
  },
  roi_geral: {
    label: "ROI Geral",
    description: "Retorno sobre o investimento total em Marketing. ROI positivo indica que o investimento está gerando resultado.",
    formula: "((Receita Estimada − Investimento) / Investimento) × 100"
  },
  cpl: {
    label: "CPL (Custo por Lead)",
    description: "Custo médio para gerar um lead. Ajuda a comparar a eficiência entre canais.",
    formula: "investimento do canal / leads gerados pelo canal"
  },

  // ============================================================
  // 6. GENÉRICOS / POR EMPRESA (usados em detalhes)
  // ============================================================
  receita_empresa: {
    label: "Receita da Empresa",
    description: "Receita reconhecida pela empresa no período, conforme seu modelo de negócio (comissão, MRR, etc.).",
    formula: "Varia conforme a empresa – veja KPIs específicos."
  },
  meta_empresa: {
    label: "Meta da Empresa",
    description: "Meta de receita estabelecida para a empresa no período.",
    formula: "Definida no planejamento estratégico."
  }
};

// Helper para acessar definições com fallback
export function getKpiDefinition(key) {
  return kpiDefinitions[key] || {
    label: key.replace(/_/g, " ").toUpperCase(),
    description: "Descrição não disponível para este indicador.",
    formula: "—"
  };
}
