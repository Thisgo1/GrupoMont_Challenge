export function gerarInsights({ montseguro, prop5, techbrabo }) {
  const insights = [];

  // ---------- MONTSEGURO ----------
  if (montseguro?.taxa_churn_pct !== null && montseguro?.taxa_churn_pct > 5) {
    insights.push({
      tipo: "risco",
      empresa: "Montseguro",
      texto: `Churn de ${montseguro.taxa_churn_pct}% no mês, acima do limite de 5%.`,
    });
  }

  if (montseguro?.atingimento_meta_pct !== null && montseguro?.atingimento_meta_pct < 80) {
    insights.push({
      tipo: "meta",
      empresa: "Montseguro",
      texto: `Atingimento de meta em ${montseguro.atingimento_meta_pct}%, abaixo do ritmo esperado.`,
    });
  }

  // Conversão baixa (lead -> contratação)
  if (montseguro?.taxa_conversao_lead_contratacao !== null && montseguro?.taxa_conversao_lead_contratacao < 15) {
    insights.push({
      tipo: "risco",
      empresa: "Montseguro",
      texto: `Taxa de conversão lead → contratação em ${montseguro.taxa_conversao_lead_contratacao}%, abaixo do esperado (15%).`,
    });
  }

  // CAC alto (comparado com receita média)
  if (montseguro?.cac !== null && montseguro?.ticket_medio_premio_mensal !== null) {
    const cacRatio = montseguro.cac / montseguro.ticket_medio_premio_mensal;
    if (cacRatio > 0.5) {
      insights.push({
        tipo: "risco",
        empresa: "Montseguro",
        texto: `CAC de ${montseguro.cac} representa mais de 50% do ticket médio mensal (${montseguro.ticket_medio_premio_mensal}).`,
      });
    }
  }

  // ---------- PROP5 ----------
  if (prop5?.ciclo_medio_dias !== null && prop5?.ciclo_medio_dias > 90) {
    insights.push({
      tipo: "risco",
      empresa: "Prop5",
      texto: `Ciclo médio de venda em ${prop5.ciclo_medio_dias} dias, acima do usual — investigar objeções na negociação.`,
    });
  }

  if (prop5?.atingimento_meta_pct !== null && prop5?.atingimento_meta_pct < 80) {
    insights.push({
      tipo: "meta",
      empresa: "Prop5",
      texto: `Atingimento de meta em ${prop5.atingimento_meta_pct}%, abaixo do ritmo esperado.`,
    });
  }

  // Pipeline ponderado baixo (comparado com meta)
  if (prop5?.pipeline_ponderado !== null && prop5?.meta_receita !== null) {
    const pipelineRatio = prop5.pipeline_ponderado / prop5.meta_receita;
    if (pipelineRatio < 0.8) {
      insights.push({
        tipo: "risco",
        empresa: "Prop5",
        texto: `Pipeline ponderado (${prop5.pipeline_ponderado}) representa ${(pipelineRatio * 100).toFixed(0)}% da meta — insuficiente para garantir o fechamento.`,
      });
    }
  }

  // Conversão lead -> fechamento baixa
  if (prop5?.taxa_conversao_lead_fechamento_pct !== null && prop5?.taxa_conversao_lead_fechamento_pct < 5) {
    insights.push({
      tipo: "risco",
      empresa: "Prop5",
      texto: `Taxa de conversão lead → fechamento em ${prop5.taxa_conversao_lead_fechamento_pct}%, abaixo do esperado (5%).`,
    });
  }

  // CAC alto (comparado com comissão média)
  if (prop5?.cac !== null && prop5?.ticket_medio_fechado !== null) {
    const cacRatio = prop5.cac / prop5.ticket_medio_fechado;
    if (cacRatio > 0.10) { // comissão média é ~3-6% do valor, então CAC > 10% do ticket é alto
      insights.push({
        tipo: "risco",
        empresa: "Prop5",
        texto: `CAC de ${prop5.cac} representa mais de 10% do ticket médio fechado (${prop5.ticket_medio_fechado}).`,
      });
    }
  }

  // ---------- TECHBRABO ----------
  if (techbrabo?.pct_projetos_no_prazo !== null && techbrabo?.pct_projetos_no_prazo < 70) {
    insights.push({
      tipo: "operacao",
      empresa: "TechBrabo",
      texto: `Só ${techbrabo.pct_projetos_no_prazo}% dos projetos concluídos no prazo — capacidade operacional pode estar no limite.`,
    });
  }

  if (techbrabo?.crescimento_mrr_mom_pct !== null && techbrabo?.crescimento_mrr_mom_pct < 0) {
    insights.push({
      tipo: "risco",
      empresa: "TechBrabo",
      texto: `MRR caiu ${Math.abs(techbrabo.crescimento_mrr_mom_pct)}% em relação ao mês anterior.`,
    });
  }

  // MRR estagnado (crescimento menor que 2%)
  if (techbrabo?.crescimento_mrr_mom_pct !== null && techbrabo?.crescimento_mrr_mom_pct >= 0 && techbrabo?.crescimento_mrr_mom_pct < 2) {
    insights.push({
      tipo: "meta",
      empresa: "TechBrabo",
      texto: `Crescimento MRR de apenas ${techbrabo.crescimento_mrr_mom_pct}% — ritmo lento.`,
    });
  }

  // Margem média baixa (menor que 25%)
  if (techbrabo?.margem_media_pct !== null && techbrabo?.margem_media_pct < 25) {
    insights.push({
      tipo: "operacao",
      empresa: "TechBrabo",
      texto: `Margem média de ${techbrabo.margem_media_pct}% — abaixo do ideal (25%). Revisar custos dos projetos.`,
    });
  }

  // Atingimento baixo
  if (techbrabo?.atingimento_meta_pct !== null && techbrabo?.atingimento_meta_pct < 80) {
    insights.push({
      tipo: "meta",
      empresa: "TechBrabo",
      texto: `Atingimento de meta em ${techbrabo.atingimento_meta_pct}%, abaixo do ritmo esperado.`,
    });
  }

  // Pipeline/forecast baixo (comparado com meta)
  if (techbrabo?.pipeline_forecast !== null && techbrabo?.meta_receita !== null) {
    const pipelineRatio = techbrabo.pipeline_forecast / techbrabo.meta_receita;
    if (pipelineRatio < 0.7) {
      insights.push({
        tipo: "risco",
        empresa: "TechBrabo",
        texto: `Pipeline/forecast (${techbrabo.pipeline_forecast}) representa ${(pipelineRatio * 100).toFixed(0)}% da meta — insuficiente para o fechamento.`,
      });
    }
  }

  // Se não houver insights, adiciona um positivo
  if (!insights.length) {
    insights.push({
      tipo: "positivo",
      empresa: "Grupo",
      texto: "Nenhum alerta disparado nos limiares configurados.",
    });
  }

  // Ordenar: primeiro riscos, depois meta, depois operacao, depois positivo
  const ordem = { risco: 0, meta: 1, operacao: 2, positivo: 3 };
  insights.sort((a, b) => (ordem[a.tipo] || 4) - (ordem[b.tipo] || 4));

  return insights;
}
