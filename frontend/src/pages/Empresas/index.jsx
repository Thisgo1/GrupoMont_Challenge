import { useEffect, useState } from "react";
import { useParams, Link, useSearchParams, Navigate } from "react-router-dom";
import MontseguroDetalhe from "./MontseguroDetalhe";
import Prop5Detalhe from "./Prop5Detalhe";
import TechbraboDetalhe from "./TechbraboDetalhe";
import MesSelector from "../../components/MesSelector";
import KpiCard from "../../components/KpiCard";
import EmpresaLogo from "../../components/EmpresaLogo";
import { EMPRESAS } from "../../theme/empresas";
import {
  getMontseguroKpis,
  getProp5Kpis,
  getTechbraboKpis,
} from "../../services/api";

const DETALHES = {
  montseguro: MontseguroDetalhe,
  prop5: Prop5Detalhe,
  techbrabo: TechbraboDetalhe,
};

const KPI_FETCHERS = {
  montseguro: getMontseguroKpis,
  prop5: getProp5Kpis,
  techbrabo: getTechbraboKpis,
};

export default function Empresas() {
  const { empresa } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  const mes = searchParams.get("mes") || "";
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    if (!empresa || !KPI_FETCHERS[empresa]) return;
    KPI_FETCHERS[empresa](mes || undefined)
      .then(setKpis)
      .catch(() => setKpis(null));
  }, [empresa, mes]);

  if (!DETALHES[empresa]) return <Navigate to="/empresas/montseguro" replace />;
  const Detalhe = DETALHES[empresa];
  const config = EMPRESAS[empresa];

  return (
    <div>
      <div className="page-header">
        <h2>Empresas</h2>
        <div className="page-subtitle">Drill-down individual — cada empresa com a lógica do seu próprio negócio.</div>
      </div>

      <div className="empresa-switch">
        {Object.entries(EMPRESAS).map(([key, cfg]) => (
          <Link
            key={key}
            to={`/empresas/${key}${mes ? `?mes=${mes}` : ""}`}
            className={empresa === key ? "active" : ""}
            style={{ "--empresa-accent": cfg.accent }}
          >
            <EmpresaLogo empresaKey={key} size="sm" />
            {cfg.label}
          </Link>
        ))}
      </div>

      <MesSelector value={mes} onChange={(v) => setSearchParams(v ? { mes: v } : {})} />

      {kpis && (
        <div className="kpi-grid" style={{ marginBottom: "1.5rem" }}>
          {/* ===== MONTSEGURO ===== */}
          {empresa === "montseguro" && (
            <>
              <KpiCard
                label="Receita de comissão"
                value={kpis.receita_comissao_mes}
                format="currency"
                accent={config.accent}
                definition="receita_comissao"
              />
              <KpiCard
                label="Atingimento de meta"
                value={kpis.atingimento_meta_pct}
                format="percent"
                status={
                  kpis.atingimento_meta_pct >= 95
                    ? "verde"
                    : kpis.atingimento_meta_pct >= 80
                    ? "amarelo"
                    : "vermelho"
                }
                accent={config.accent}
                definition="atingimento_meta"
              />
              <KpiCard
                label="Vidas ativas"
                value={kpis.vidas_ativas}
                accent={config.accent}
                definition="vidas_ativas"
              />
              <KpiCard
                label="CAC"
                value={kpis.cac}
                format="currency"
                accent={config.accent}
                definition="cac"
              />
              <KpiCard
                label="Churn"
                value={kpis.taxa_churn_pct}
                format="percent"
                accent={config.accent}
                definition="churn"
              />
            </>
          )}

          {/* ===== PROP5 ===== */}
          {empresa === "prop5" && (
            <>
              <KpiCard
                label="Comissão realizada"
                value={kpis.receita_comissao_mes}
                format="currency"
                accent={config.accent}
                definition="receita_comissao"
              />
              <KpiCard
                label="Atingimento de meta"
                value={kpis.atingimento_meta_pct}
                format="percent"
                status={
                  kpis.atingimento_meta_pct >= 95
                    ? "verde"
                    : kpis.atingimento_meta_pct >= 80
                    ? "amarelo"
                    : "vermelho"
                }
                accent={config.accent}
                definition="atingimento_meta"
              />
              <KpiCard
                label="Pipeline ponderado"
                value={kpis.pipeline_ponderado}
                format="currency"
                accent={config.accent}
                definition="pipeline_ponderado"
              />
              <KpiCard
                label="Ciclo médio"
                value={kpis.ciclo_medio_dias}
                format="dias"
                accent={config.accent}
                definition="ciclo_medio"
              />
              <KpiCard
                label="CAC"
                value={kpis.cac}
                format="currency"
                accent={config.accent}
                definition="cac"
              />
            </>
          )}

          {/* ===== TECHBRABO ===== */}
          {empresa === "techbrabo" && (
            <>
              <KpiCard
                label="MRR atual"
                value={kpis.mrr_atual}
                format="currency"
                accent={config.accent}
                definition="mrr"
              />
              <KpiCard
                label="Crescimento MRR"
                value={kpis.crescimento_mrr_mom_pct}
                format="percent"
                accent={config.accent}
                definition="crescimento_mom"
              />
              <KpiCard
                label="Atingimento de meta"
                value={kpis.atingimento_meta_pct}
                format="percent"
                status={
                  kpis.atingimento_meta_pct >= 95
                    ? "verde"
                    : kpis.atingimento_meta_pct >= 80
                    ? "amarelo"
                    : "vermelho"
                }
                accent={config.accent}
                definition="atingimento_meta"
              />
              <KpiCard
                label="Margem média"
                value={kpis.margem_media_pct}
                format="percent"
                accent={config.accent}
                definition="margem_media"
              />
              <KpiCard
                label="Projetos no prazo"
                value={kpis.pct_projetos_no_prazo}
                format="percent"
                accent={config.accent}
                definition="projetos_prazo"
              />
            </>
          )}
        </div>
      )}

      <Detalhe mes={mes || undefined} />
    </div>
  );
}
