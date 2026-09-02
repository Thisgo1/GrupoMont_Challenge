import { useEffect, useState } from "react";
import { useParams, Link, Navigate } from "react-router-dom";
import { FUNIL_CONFIG } from "./funilConfig";
import BarList from "../../components/BarList";
import RankingTable from "../../components/RankingTable";
import MesSelector from "../../components/MesSelector";
import FiltrosComercial from "../../components/FiltrosComercial";
import KpiCard from "../../components/KpiCard.jsx";
import { EMPRESAS } from "../../theme/empresas";
import EmpresaLogo from "../../components/EmpresaLogo";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, Legend } from "recharts";

const COLORS = ["#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981", "#ef4444"];

export default function Comercial() {
  const { empresa } = useParams();
  const [mes, setMes] = useState("");
  const [vendedor, setVendedor] = useState("");
  const [canal, setCanal] = useState("");
  const [dados, setDados] = useState(null);
  const [vendedores, setVendedores] = useState([]);
  const [canais, setCanais] = useState([]);

  const config = FUNIL_CONFIG[empresa];

  useEffect(() => {
    if (!config) return;
    setDados(null);
    config
      .fetch(mes || undefined, vendedor || undefined, canal || undefined)
      .then((data) => {
        setDados(data);
        if (data) {
          const vendedoresSet = new Set(data.map((d) => d.vendedor).filter(Boolean));
          setVendedores(Array.from(vendedoresSet));
          const canaisSet = new Set(data.map((d) => d.canal).filter(Boolean));
          setCanais(Array.from(canaisSet));
        }
      });
  }, [empresa, mes, vendedor, canal]);

  if (!config) return <Navigate to="/comercial/montseguro" replace />;

  const accent = EMPRESAS[empresa].accent;
  const stages = dados ? config.stages(dados) : null;
  const ranking = dados ? config.ranking(dados) : null;
  const resumo = dados ? config.resumo(dados) : null;
  const pipelinePonderado = dados ? config.pipelinePonderado(dados) : null;
  const canaisData = dados ? config.canais(dados) : [];

  const conversoes = stages
    ? stages.slice(1).map((etapa, i) => ({
        de: stages[i].label,
        para: etapa.label,
        pct: stages[i].value ? ((etapa.value / stages[i].value) * 100).toFixed(1) : "0.0",
      }))
    : [];

  const taxaConversao = resumo?.totalLeads
    ? ((resumo.totalNegocios / resumo.totalLeads) * 100).toFixed(1)
    : 0;

  return (
    <div>
      <div className="page-header">
        <h2>Comercial</h2>
        <div className="page-subtitle">Funil, conversão por etapa e produtividade por vendedor.</div>
      </div>

      <div className="empresa-switch">
        {Object.entries(EMPRESAS).map(([key, cfg]) => (
          <Link
            key={key}
            to={`/comercial/${key}`}
            className={empresa === key ? "active" : ""}
            style={{ "--empresa-accent": cfg.accent }}
          >
            <EmpresaLogo empresaKey={key} size="sm" />
            {cfg.label}
          </Link>
        ))}
      </div>

      <div className="flex flex-wrap items-center gap-4 my-4">
        <MesSelector value={mes} onChange={setMes} />
        <FiltrosComercial
          vendedor={vendedor}
          setVendedor={setVendedor}
          canal={canal}
          setCanal={setCanal}
          vendedores={vendedores}
          canais={canais}
        />
      </div>

      {/* Cards de resumo */}
      {resumo && (
        <div className="kpi-grid" style={{ marginBottom: "1.5rem" }}>
          <KpiCard
            label="Total de Leads"
            value={resumo.totalLeads}
            accent={accent}
            definition={`${empresa}_total_leads`}
          />
          <KpiCard
            label="Negócios Fechados"
            value={resumo.totalNegocios}
            accent={accent}
            definition={`${empresa}_negocios_fechados`}
          />
          <KpiCard
            label="Taxa de Conversão"
            value={taxaConversao}
            format="percent"
            status={
              taxaConversao >= 20
                ? "verde"
                : taxaConversao >= 10
                ? "amarelo"
                : "vermelho"
            }
            accent={accent}
            definition={`${empresa}_taxa_conversao`}
          />
          <KpiCard
            label="Receita Total"
            value={resumo.receitaTotal}
            format="currency"
            accent={accent}
            definition={`${empresa}_receita_empresa`}
          />
          {pipelinePonderado !== undefined && (
            <KpiCard
              label="Pipeline Ponderado"
              value={pipelinePonderado}
              format="currency"
              accent={accent}
              definition={`${empresa}_pipeline_ponderado`}
            />
          )}
        </div>
      )}

      {/* Gráfico de distribuição por canal */}
      {stages ? (
        <>
          <h3>Leads por Canal</h3>
          <div className="section">
            <BarList items={stages} accent={accent} numbered />
          </div>

          <div className="section">
            <h3>Taxa de conversão entre etapas</h3>
            <table className="data-table">
              <thead>
                <tr><th>De</th><th>Para</th><th>Conversão</th></tr>
              </thead>
              <tbody>
                {conversoes.map((c) => (
                  <tr key={c.de}>
                    <td>{c.de}</td>
                    <td>{c.para}</td>
                    <td>{c.pct}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="section">
            <h3>Por vendedor</h3>
            <p className="muted" style={{ marginTop: -6, marginBottom: 16 }}>
              Só conta o que virou resultado real — não volume de leads ou propostas em aberto.
            </p>
            <RankingTable linhas={ranking} labels={config.rankingLabels} accent={accent} />
          </div>
        </>
      ) : (
        <p className="muted">Carregando…</p>
      )}
    </div>
  );
}
