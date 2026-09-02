import { useEffect, useState } from "react";
import { getProp5Oportunidades } from "../../services/api";
import BarList from "../../components/BarList";
import StatusTable from "../../components/StatusTable";
import { EMPRESAS } from "../../theme/empresas";

const accent = EMPRESAS.prop5.accent;

export default function Prop5Detalhe({ mes }) {
  const [oportunidades, setOportunidades] = useState(null);

  useEffect(() => {
    setOportunidades(null);
    getProp5Oportunidades(mes).then(setOportunidades);
  }, [mes]);

  if (!oportunidades) return <p className="muted">Carregando…</p>;

  const stages = [
    { label: "Leads", value: oportunidades.length },
    { label: "Diagnóstico", value: oportunidades.filter((o) => o.data_diagnostico).length },
    { label: "Reunião consultiva", value: oportunidades.filter((o) => o.data_reuniao_consultiva).length },
    {
      label: "Negociação/Estruturação",
      value: oportunidades.filter((o) => ["Negociação/Estruturação", "Fechado"].includes(o.estagio)).length,
    },
    { label: "Fechado", value: oportunidades.filter((o) => o.estagio === "Fechado").length },
  ];

  const porPais = {};
  oportunidades.forEach((o) => {
    porPais[o.pais_residencia] = (porPais[o.pais_residencia] || 0) + 1;
  });
  const porPaisRows = Object.entries(porPais)
    .map(([status, count]) => ({ status, count }))
    .sort((a, b) => b.count - a.count);

  const fechadas = oportunidades.filter((o) => o.estagio === "Fechado");
  const volumeFechado = fechadas.reduce((acc, o) => acc + Number(o.valor_fechado || 0), 0);
  const comissaoTotal = fechadas.reduce((acc, o) => acc + Number(o.comissao || 0), 0);

  return (
    <div>
      <div className="section">
        <h3>Pipeline consultivo</h3>
        <BarList items={stages} accent={accent} numbered />
      </div>

      <div className="section">
        <h3>Leads por país de residência</h3>
        <StatusTable rows={porPaisRows} />
      </div>

      <div className="section">
        <h3>Volume transacionado x receita real</h3>
        <p>
          {volumeFechado.toLocaleString("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 2 })}
          {" "}estruturados no total ·{" "}
          {comissaoTotal.toLocaleString("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 2 })}
          {" "}de comissão efetiva
          ({volumeFechado ? ((comissaoTotal / volumeFechado) * 100).toFixed(1) : 0}% do volume)
        </p>
        <p className="muted">O valor do imóvel não é a receita da Prop5 — a diferença acima é proposital.</p>
      </div>
    </div>
  );
}
