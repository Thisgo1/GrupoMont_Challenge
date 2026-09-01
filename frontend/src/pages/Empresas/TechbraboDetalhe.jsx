import { useEffect, useState } from "react";
import { getTechbraboOportunidades, getTechbraboProjetos } from "../../services/api";
import BarList from "../../components/BarList";
import StatusTable from "../../components/StatusTable";
import { EMPRESAS } from "../../theme/empresas";

const accent = EMPRESAS.techbrabo.accent;

export default function TechbraboDetalhe({ mes }) {
  const [oportunidades, setOportunidades] = useState(null);
  const [projetos, setProjetos] = useState(null);

  useEffect(() => {
    setOportunidades(null);
    getTechbraboOportunidades(mes).then(setOportunidades);
  }, [mes]);

  useEffect(() => {
    // Status de projeto (concluído/atrasado/em andamento) é estado atual da
    // operação, não filtra por mês de criação do lead.
    getTechbraboProjetos().then(setProjetos);
  }, []);

  if (!oportunidades || !projetos) return <p className="muted">Carregando…</p>;

  const stages = [
    { label: "Leads", value: oportunidades.length },
    { label: "Proposta enviada", value: oportunidades.filter((o) => o.data_proposta).length },
    { label: "Contrato assinado", value: oportunidades.filter((o) => o.data_contrato).length },
  ];

  const porStatusProjeto = {};
  projetos.forEach((p) => {
    porStatusProjeto[p.status] = (porStatusProjeto[p.status] || 0) + 1;
  });
  const statusRows = Object.entries(porStatusProjeto).map(([status, count]) => ({ status, count }));

  const recorrente = oportunidades.filter((o) => o.mrr).length;
  const pontual = oportunidades.filter((o) => o.data_contrato && !o.mrr).length;

  return (
    <div>
      <div className="section">
        <h3>Comercial x entrega</h3>
        <BarList items={stages} accent={accent} numbered />
      </div>

      <div className="section">
        <h3>Status dos projetos</h3>
        <StatusTable rows={statusRows} />
      </div>

      <div className="section">
        <h3>Natureza da receita contratada</h3>
        <p>{recorrente} contratos com componente recorrente (MRR) · {pontual} contratos pontuais</p>
        <p className="muted">Quanto maior a fatia recorrente, menos a empresa depende de vender projeto novo todo mês.</p>
      </div>
    </div>
  );
}
