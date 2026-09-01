import { useEffect, useState } from "react";
import { getMontseguroKpis, getProp5Kpis, getTechbraboKpis } from "../services/api";
import { gerarInsights } from "../pages/Insights/rules";
import { AlertCircle, AlertTriangle, CheckCircle, XCircle } from "lucide-react";

const ICONES = {
  risco: <XCircle className="w-5 h-5" />,
  meta: <AlertTriangle className="w-5 h-5" />,
  operacao: <AlertCircle className="w-5 h-5" />,
  positivo: <CheckCircle className="w-5 h-5" />,
};

const CORES = {
  risco: "bg-red-50 border-red-200 text-red-700",
  meta: "bg-yellow-50 border-yellow-200 text-yellow-700",
  operacao: "bg-orange-50 border-orange-200 text-orange-700",
  positivo: "bg-green-50 border-green-200 text-green-700",
};

export default function InsightsBanner({ maxItens = 3 }) {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getMontseguroKpis(), getProp5Kpis(), getTechbraboKpis()])
      .then(([montseguro, prop5, techbrabo]) => {
        const all = gerarInsights({ montseguro, prop5, techbrabo });
        const criticos = all.filter((i) => i.tipo !== "positivo");
        setInsights(criticos.slice(0, maxItens));
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [maxItens]);

  if (loading) return null;
  if (insights.length === 0) return null;

  return (
    <div className="space-y-2 mb-6">
      {insights.map((i, idx) => (
        <div
          key={idx}
          className={`flex items-center gap-3 p-3 rounded-lg border ${CORES[i.tipo]}`}
        >
          {ICONES[i.tipo] || ICONES.risco}
          <div>
            <span className="font-semibold">{i.empresa}:</span> {i.texto}
          </div>
        </div>
      ))}
    </div>
  );
}
