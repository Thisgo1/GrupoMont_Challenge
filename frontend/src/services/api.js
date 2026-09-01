import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export const api = axios.create({
  baseURL: API_BASE_URL,
});

// --- Montseguro ---
export const getMontseguroKpis = (mes) =>
  api.get("/montseguro/kpis/", { params: mes ? { mes } : {} }).then((r) => r.data);

export const getMontseguroFunil = (mes, vendedor, canal) =>
  api.get("/montseguro/funil/", {
    params: {
      mes,
      vendedor,
      canal,
    },
  }).then((r) => r.data);

export const getMontseguroClientesAtivos = () =>
  api.get("/montseguro/clientes-ativos/").then((r) => r.data);

// --- Prop5 ---
export const getProp5Kpis = (mes) =>
  api.get("/prop5/kpis/", { params: mes ? { mes } : {} }).then((r) => r.data);

export const getProp5Oportunidades = (mes, vendedor, canal) =>
  api.get("/prop5/oportunidades/", {
    params: {
      mes,
      vendedor,
      canal,
    },
  }).then((r) => r.data);

// --- TechBrabo ---
export const getTechbraboKpis = (mes) =>
  api.get("/techbrabo/kpis/", { params: mes ? { mes } : {} }).then((r) => r.data);

export const getTechbraboOportunidades = (mes, vendedor, canal) =>
  api.get("/techbrabo/oportunidades/", {
    params: {
      mes,
      vendedor,
      canal,
    },
  }).then((r) => r.data);

export const getTechbraboProjetos = () =>
  api.get("/techbrabo/projetos/").then((r) => r.data);

// --- Comuns ---
export const getMarketing = (empresa) =>
  api.get("/marketing/", { params: empresa ? { empresa } : {} }).then((r) => r.data);

export const getMetas = (empresa) =>
  api.get("/metas/", { params: empresa ? { empresa } : {} }).then((r) => r.data);

export const getCeoOverview = (mes) =>
  api.get("/kpis/ceo-overview/", { params: mes ? { mes } : {} }).then((r) => r.data);

export const getComparativos = (mes) =>
  api.get("/kpis/comparativos/", { params: mes ? { mes } : {} }).then((r) => r.data);

export const getEvolucaoReceita = (meses = 6, mes) =>
  api.get("/kpis/evolucao-receita/", { params: { meses, mes } }).then((r) => r.data);

export const getMetasProjecao = (mes) =>
  api.get("/kpis/metas-projecao/", { params: mes ? { mes } : {} }).then((r) => r.data);
