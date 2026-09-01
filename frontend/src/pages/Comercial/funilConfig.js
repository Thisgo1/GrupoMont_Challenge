import {
  getMontseguroFunil,
  getProp5Oportunidades,
  getTechbraboOportunidades,
} from "../../services/api";

const COMISSAO_MONTSEGURO = 0.12;

export const FUNIL_CONFIG = {
  montseguro: {
    label: "Montseguro",
    fetch: (mes, vendedor, canal) =>
      getMontseguroFunil(mes, vendedor, canal),
    stages: (dados) => [
      { label: "Leads", value: dados.length },
      { label: "Cotação", value: dados.filter((d) => d.data_cotacao).length },
      { label: "Proposta", value: dados.filter((d) => d.data_proposta).length },
      { label: "Contratação", value: dados.filter((d) => d.data_contratacao).length },
      { label: "Implantação", value: dados.filter((d) => d.data_implantacao).length },
    ],
    ranking: (dados) => {
      const porVendedor = {};
      dados
        .filter((d) => d.data_implantacao)
        .forEach((d) => {
          if (!porVendedor[d.vendedor]) porVendedor[d.vendedor] = { vendedor: d.vendedor, quantidade: 0, valor: 0 };
          porVendedor[d.vendedor].quantidade += 1;
          porVendedor[d.vendedor].valor += Number(d.premio_mensal_estimado || 0) * COMISSAO_MONTSEGURO;
        });
      return Object.values(porVendedor).sort((a, b) => b.valor - a.valor);
    },
    rankingLabels: { quantidade: "Implantados", valor: "Comissão gerada" },
    resumo: (dados) => {
      const totalLeads = dados.length;
      const negocios = dados.filter((d) => d.data_contratacao);
      const totalNegocios = negocios.length;
      const receitaTotal = negocios.reduce(
        (acc, d) => acc + (d.premio_mensal_estimado || 0) * COMISSAO_MONTSEGURO,
        0
      );
      return { totalLeads, totalNegocios, receitaTotal };
    },
    pipelinePonderado: (dados) => {
      // Para Montseguro: propostas em aberto com probabilidade estimada (40%)
      const propostasAbertas = dados.filter(
        (d) => d.data_proposta && !d.data_contratacao && !d.data_implantacao
      );
      return propostasAbertas.reduce(
        (acc, d) => acc + (d.premio_mensal_estimado || 0) * 12 * 0.4 * COMISSAO_MONTSEGURO,
        0
      );
    },
    canais: (dados) => {
      const map = {};
      dados.forEach((d) => {
        const canal = d.canal || "Desconhecido";
        if (!map[canal]) map[canal] = 0;
        map[canal] += 1;
      });
      return Object.entries(map).map(([name, value]) => ({ name, value }));
    },
  },
  prop5: {
    label: "Prop5",
    fetch: (mes, vendedor, canal) =>
      getProp5Oportunidades(mes, vendedor, canal),
    stages: (dados) => [
      { label: "Leads", value: dados.length },
      { label: "Diagnóstico", value: dados.filter((d) => d.data_diagnostico).length },
      { label: "Reunião consultiva", value: dados.filter((d) => d.data_reuniao_consultiva).length },
      { label: "Fechado", value: dados.filter((d) => d.estagio === "Fechado").length },
    ],
    ranking: (dados) => {
      const porVendedor = {};
      dados
        .filter((d) => d.estagio === "Fechado")
        .forEach((d) => {
          if (!porVendedor[d.vendedor]) porVendedor[d.vendedor] = { vendedor: d.vendedor, quantidade: 0, valor: 0 };
          porVendedor[d.vendedor].quantidade += 1;
          porVendedor[d.vendedor].valor += Number(d.comissao || 0);
        });
      return Object.values(porVendedor).sort((a, b) => b.valor - a.valor);
    },
    rankingLabels: { quantidade: "Fechamentos", valor: "Comissão gerada" },
    resumo: (dados) => {
      const totalLeads = dados.length;
      const negocios = dados.filter((d) => d.estagio === "Fechado");
      const totalNegocios = negocios.length;
      const receitaTotal = negocios.reduce((acc, d) => acc + Number(d.comissao || 0), 0);
      return { totalLeads, totalNegocios, receitaTotal };
    },
    pipelinePonderado: (dados) => {
      // Para Prop5: pipeline ponderado = soma(valor_estimado * probabilidade)
      return dados
        .filter((d) => d.estagio !== "Fechado" && d.estagio !== "Perdido")
        .reduce((acc, d) => acc + (d.valor_estimado || 0) * (d.probabilidade || 0), 0);
    },
    canais: (dados) => {
      const map = {};
      dados.forEach((d) => {
        const canal = d.canal || "Desconhecido";
        if (!map[canal]) map[canal] = 0;
        map[canal] += 1;
      });
      return Object.entries(map).map(([name, value]) => ({ name, value }));
    },
  },
  techbrabo: {
    label: "TechBrabo",
    fetch: (mes, vendedor, canal) =>
      getTechbraboOportunidades(mes, vendedor, canal),
    stages: (dados) => [
      { label: "Leads", value: dados.length },
      { label: "Proposta enviada", value: dados.filter((d) => d.data_proposta).length },
      { label: "Contrato assinado", value: dados.filter((d) => d.data_contrato).length },
    ],
    ranking: (dados) => {
      const porVendedor = {};
      dados
        .filter((d) => d.estagio === "Contrato assinado")
        .forEach((d) => {
          if (!porVendedor[d.vendedor]) porVendedor[d.vendedor] = { vendedor: d.vendedor, quantidade: 0, valor: 0 };
          porVendedor[d.vendedor].quantidade += 1;
          porVendedor[d.vendedor].valor += Number(d.valor_contrato || 0);
        });
      return Object.values(porVendedor).sort((a, b) => b.valor - a.valor);
    },
    rankingLabels: { quantidade: "Contratos assinados", valor: "Valor contratado" },
    resumo: (dados) => {
      const totalLeads = dados.length;
      const negocios = dados.filter((d) => d.estagio === "Contrato assinado");
      const totalNegocios = negocios.length;
      const receitaTotal = negocios.reduce((acc, d) => {
        let valor = 0;
        if (d.tipo_receita === "Pontual") valor = Number(d.valor_contrato || 0);
        else if (d.tipo_receita === "Recorrente" && d.mrr) valor = Number(d.mrr) * 12;
        return acc + valor;
      }, 0);
      return { totalLeads, totalNegocios, receitaTotal };
    },
    pipelinePonderado: (dados) => {
      // Para TechBrabo: propostas enviadas em aberto (não contratadas ainda)
      return dados
        .filter((d) => d.estagio === "Proposta enviada" || d.estagio === "Negociação")
        .reduce((acc, d) => acc + Number(d.valor_proposta || 0), 0);
    },
    canais: (dados) => {
      const map = {};
      dados.forEach((d) => {
        const canal = d.canal || "Desconhecido";
        if (!map[canal]) map[canal] = 0;
        map[canal] += 1;
      });
      return Object.entries(map).map(([name, value]) => ({ name, value }));
    },
  },
};
