// src/lib/kpiDefinitions.js
export const kpiDefinitions = {
  // ===== Montseguro =====
  receita_comissao: {
    label: "Receita de Comissão",
    description: "Receita efetiva gerada pela Montseguro no mês, calculada sobre o prêmio dos clientes ativos.",
    formula: "Σ prêmio_mensal × 15% (comissão média)"
  },
  taxa_implantacao: {
    label: "Taxa de Implantação",
    description: "Percentual de contratos que se tornaram clientes ativos. Se baixa, indica gargalo pós-venda.",
    formula: "(implantados / contratados) × 100"
  },
  vidas_ativas: {
    label: "Vidas Ativas",
    description: "Total de beneficiários cobertos por planos de saúde ativos. Reflete o tamanho real da carteira.",
    formula: "Σ vidas_ativas dos contratos não cancelados"
  },
  churn: {
    label: "Taxa de Churn",
    description: "Percentual de clientes que cancelaram no período. Churn alto anula o esforço de aquisição.",
    formula: "(cancelamentos no mês / clientes ativos no início do mês) × 100"
  },
  cac: {
    label: "CAC (Custo de Aquisição)",
    description: "Custo médio para adquirir um novo cliente. Comparar com ticket médio e margem para avaliar payback.",
    formula: "investimento em Marketing / novos clientes no período"
  },

  // ===== Prop5 =====
  pipeline_ponderado: {
    label: "Pipeline Ponderado",
    description: "Valor estimado das oportunidades em aberto, ajustado pela probabilidade de fechamento. Mais realista que pipeline bruto.",
    formula: "Σ (valor_estimado × probabilidade)"
  },
  ciclo_medio: {
    label: "Ciclo Médio de Venda",
    description: "Tempo médio entre a entrada do lead e o fechamento da oportunidade. Ciclo muito longo pode indicar objeções não tratadas.",
    formula: "média (data_fechamento − data_criação do lead)"
  },

  // ===== TechBrabo =====
  mrr: {
    label: "MRR (Receita Recorrente Mensal)",
    description: "Base de receita previsível da TechBrabo. MRR crescente indica negócio mais sustentável.",
    formula: "Σ mrr de todos os contratos recorrentes ativos"
  },
  margem_media: {
    label: "Margem Média",
    description: "Margem de lucro média dos projetos concluídos. Margem caindo com receita subindo é alerta.",
    formula: "Σ margem / Σ valor_contrato dos projetos concluídos"
  },
  projetos_prazo: {
    label: "% Projetos no Prazo",
    description: "Percentual de projetos entregues dentro do prazo. Conecta vendas com capacidade de entrega.",
    formula: "(projetos concluídos sem atraso / total de concluídos) × 100"
  },

  // ===== Comuns / CEO Overview =====
  receita_total: {
    label: "Receita Total do Grupo",
    description: "Soma da receita reconhecida das três empresas. É a base para avaliar o desempenho consolidado.",
    formula: "Σ (receita Montseguro + comissão Prop5 + receita TechBrabo)"
  },
  meta_total: {
    label: "Meta Total do Grupo",
    description: "Soma das metas de receita das três empresas para o período.",
    formula: "Σ meta_receita de Montseguro, Prop5 e TechBrabo"
  },
  atingimento_meta: {
    label: "Atingimento da Meta",
    description: "Percentual da meta já realizado no período. Valor abaixo de 100% indica necessidade de aceleração.",
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
   receita_empresa: {
    label: "Receita da Empresa",
    description: "Receita reconhecida pela empresa no período, conforme seu modelo de negócio (comissão, MRR, etc.).",
    formula: "Varia conforme a empresa"
  },
  meta_empresa: {
    label: "Meta da Empresa",
    description: "Meta de receita estabelecida para a empresa no período.",
    formula: "Definida no planejamento"
  },
  investimento_total: {
    label: "Investimento Total",
    description: "Soma de todo o investimento em marketing no período, em todos os canais.",
    formula: "Σ investimento por canal"
  },
  leads_gerados: {
    label: "Leads Gerados",
    description: "Total de leads gerados pelos esforços de marketing no período.",
    formula: "Σ leads por canal"
  },
  receita_estimada: {
    label: "Receita Estimada",
    description: "Receita gerada a partir dos leads adquiridos pelo marketing (atribuição por canal).",
    formula: "Σ receita atribuída a cada canal"
  },
  roi_geral: {
    label: "ROI Geral do Marketing",
    description: "Retorno sobre o investimento total em marketing. ROI positivo indica que o marketing está gerando mais receita do que custa.",
    formula: "(Receita - Investimento) / Investimento"
  },
  cpl: {
    label: "CPL (Custo por Lead)",
    description: "Custo médio para gerar cada lead. Útil para comparar eficiência entre canais.",
    formula: "Investimento / Leads"
  },
  roi_canal: {
    label: "ROI por Canal",
    description: "Retorno sobre o investimento em um canal específico. Ajuda a identificar quais canais são mais eficientes.",
    formula: "(Receita do canal - Investimento do canal) / Investimento do canal"
  },
  crescimento_mom: {
    label: "Crescimento Mês a Mês",
    description: "Variação percentual do MRR em relação ao mês anterior.",
    formula: "((MRR atual − MRR anterior) / MRR anterior) × 100"
  },
  churn: {
    label: "Taxa de Churn",
    description: "Percentual de clientes que cancelaram no período.",
    formula: "(cancelamentos no mês / clientes ativos no início do mês) × 100"
  },
  negocios_mes: {
    label: "Negócios no mês",
    description: "Quantidade total de negócios (contratos/vendas) fechados no mês.",
    formula: "Σ contratos/vendas com data de fechamento no período"
  },

};

const empresas = ['montseguro', 'prop5', 'techbrabo'];

empresas.forEach((emp) => {
  kpiDefinitions[`${emp}_total_leads`] = {
    label: 'Total de Leads',
    description: `Total de leads gerados para a ${emp === 'montseguro' ? 'Montseguro' : emp === 'prop5' ? 'Prop5' : 'TechBrabo'} no período.`,
    formula: 'Σ leads criados no período'
  };
  kpiDefinitions[`${emp}_negocios_fechados`] = {
    label: 'Negócios Fechados',
    description: `Total de negócios (contratos/vendas) fechados pela ${emp === 'montseguro' ? 'Montseguro' : emp === 'prop5' ? 'Prop5' : 'TechBrabo'} no período.`,
    formula: 'Varia conforme o funil de cada empresa'
  };
  kpiDefinitions[`${emp}_taxa_conversao`] = {
    label: 'Taxa de Conversão',
    description: `Percentual de leads que se tornaram negócios fechados na ${emp === 'montseguro' ? 'Montseguro' : emp === 'prop5' ? 'Prop5' : 'TechBrabo'}.`,
    formula: '(Negócios Fechados / Total de Leads) × 100'
  };
  kpiDefinitions[`${emp}_receita_empresa`] = {
    label: 'Receita da Empresa',
    description: `Receita reconhecida pela ${emp === 'montseguro' ? 'Montseguro' : emp === 'prop5' ? 'Prop5' : 'TechBrabo'} no período, conforme seu modelo de negócio.`,
    formula: 'Varia conforme a empresa (comissão, MRR, etc.)'
  };
  kpiDefinitions[`${emp}_pipeline_ponderado`] = {
    label: 'Pipeline Ponderado',
    description: `Valor estimado das oportunidades em aberto na ${emp === 'montseguro' ? 'Montseguro' : emp === 'prop5' ? 'Prop5' : 'TechBrabo'}, ajustado pela probabilidade de fechamento.`,
    formula: 'Σ (valor_estimado × probabilidade)'
  };
});



export function getKpiDefinition(key) {
  return kpiDefinitions[key] || {
    label: key,
    description: "Descrição não disponível para este indicador.",
    formula: "—"
  };
}
