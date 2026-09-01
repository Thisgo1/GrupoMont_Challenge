import { useEffect, useState } from "react";
import { getMontseguroKpis, getProp5Kpis, getTechbraboKpis } from "../../services/api";
import { gerarInsights } from "./rules";
import { EMPRESAS } from "../../theme/empresas";
import InsightsBanner from "../../components/InsightsBanner";

const CORES_TIPO = {
  risco: "var(--status-vermelho)",
  meta: "var(--status-amarelo)",
  operacao: EMPRESAS.techbrabo.accent,
  positivo: "var(--status-verde)",
};

export default function Insights() {
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    Promise.all([getMontseguroKpis(), getProp5Kpis(), getTechbraboKpis()]).then(
      ([montseguro, prop5, techbrabo]) => setKpis({ montseguro, prop5, techbrabo })
    );
  }, []);

  if (!kpis) return <p className="muted">Carregando…</p>;

  const insights = gerarInsights(kpis);

  return (
    <div>
      <div className="page-header">
        <h2>Insights</h2>

        <div className="page-subtitle">Alertas gerados por regras de limiar sobre os KPIs já calculados no back-end.</div>
      </div>
      <InsightsBanner maxItens={3} />
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {insights.map((i, idx) => (
          <div key={idx} className="insight" style={{ "--insight-accent": CORES_TIPO[i.tipo] }}>
            <strong>{i.empresa}</strong> — {i.texto}
          </div>
        ))}
      </div>
    </div>
  );
}
