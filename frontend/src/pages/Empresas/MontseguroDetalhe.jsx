import { useEffect, useState } from "react";
import { getMontseguroFunil, getMontseguroClientesAtivos } from "../../services/api";
import BarList from "../../components/BarList";
import StatusTable from "../../components/StatusTable";
import { EMPRESAS } from "../../theme/empresas";

const accent = EMPRESAS.montseguro.accent;

export default function MontseguroDetalhe({ mes }) {
  const [funil, setFunil] = useState(null);
  const [ativos, setAtivos] = useState(null);

  useEffect(() => {
    setFunil(null);
    getMontseguroFunil(mes).then(setFunil);
  }, [mes]);

  useEffect(() => {
    getMontseguroClientesAtivos().then(setAtivos);
  }, []);

  if (!funil || !ativos) return <p className="muted">Carregando…</p>;

  const stages = [
    { label: "Leads", value: funil.length },
    { label: "Cotação", value: funil.filter((f) => f.data_cotacao).length },
    { label: "Proposta", value: funil.filter((f) => f.data_proposta).length },
    { label: "Contratação", value: funil.filter((f) => f.data_contratacao).length },
    { label: "Implantação", value: funil.filter((f) => f.data_implantacao).length },
  ];

  const motivosPerda = {};
  funil.filter((f) => f.motivo_perda).forEach((f) => {
    motivosPerda[f.motivo_perda] = (motivosPerda[f.motivo_perda] || 0) + 1;
  });
  const motivosPerdaRows = Object.entries(motivosPerda).map(([status, count]) => ({ status, count }));

  const cancelados = ativos.filter((c) => c.cancelado).length;

  return (
    <div>
      <div className="section">
        <h3>Funil de vendas</h3>
        <p className="muted" style={{ marginTop: -6, marginBottom: 16 }}>
          Cada etapa conta quantos leads alcançaram aquela data — não é status atual, é histórico.
        </p>
        <BarList items={stages} accent={accent} numbered />
      </div>

      <div className="section">
        <h3>Motivos de perda</h3>
        {motivosPerdaRows.length ? <StatusTable rows={motivosPerdaRows} /> : <p className="muted">Sem perdas registradas.</p>}
      </div>

      <div className="section">
        <h3>Carteira ativa</h3>
        <p>
          {ativos.length} contratos implantados na base · {cancelados} cancelados
          ({ativos.length ? ((cancelados / ativos.length) * 100).toFixed(1) : 0}% churn acumulado)
        </p>
      </div>
    </div>
  );
}
