import { useEffect, useState, useMemo } from "react";
import { useParams, Link, Navigate } from "react-router-dom";
import {
  getMarketing,
  getMontseguroFunil,
  getProp5Oportunidades,
  getTechbraboOportunidades,
} from "../../services/api";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  Cell,
} from "recharts";
import BarList from "../../components/BarList";
import { EMPRESAS } from "../../theme/empresas";
import EmpresaLogo from "../../components/EmpresaLogo";
import KpiCard from "../../components/KpiCard";

const formatBRL = (v) =>
  v.toLocaleString("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 2 });


function aggregateMontseguro(funilData) {
  const porCanal = {};
  funilData
    .filter((f) => f.data_implantacao)
    .forEach((f) => {
      const canal = f.canal || "Outros";
      const receita = (f.premio_mensal_estimado || 0) * 0.12;
      if (!porCanal[canal]) {
        porCanal[canal] = { canal, receita: 0, mes: f.mes_referencia };
      }
      porCanal[canal].receita += receita;
    });
  return Object.values(porCanal);
}

function aggregateProp5(oportunidades) {
  const porCanal = {};
  oportunidades
    .filter((o) => o.estagio === "Fechado" && o.comissao)
    .forEach((o) => {
      const canal = o.canal || "Outros";
      const receita = o.comissao || 0;
      if (!porCanal[canal]) {
        porCanal[canal] = { canal, receita: 0, mes: o.mes_referencia };
      }
      porCanal[canal].receita += receita;
    });
  return Object.values(porCanal);
}

function aggregateTechbrabo(oportunidades) {
  const porCanal = {};
  oportunidades
    .filter((o) => o.estagio === "Contrato assinado")
    .forEach((o) => {
      const canal = o.canal || "Outros";
      let receita = 0;
      if (o.tipo_receita === "Pontual") {
        receita = o.valor_contrato || 0;
      } else if (o.tipo_receita === "Recorrente" && o.mrr) {
        receita = o.mrr * 12; // anualizado para comparar
      }
      if (receita > 0) {
        if (!porCanal[canal]) {
          porCanal[canal] = { canal, receita: 0, mes: o.mes_referencia };
        }
        porCanal[canal].receita += receita;
      }
    });
  return Object.values(porCanal);
}

const AGGREGATORS = {
  montseguro: aggregateMontseguro,
  prop5: aggregateProp5,
  techbrabo: aggregateTechbrabo,
};

const fetchOportunidades = {
  montseguro: getMontseguroFunil,
  prop5: getProp5Oportunidades,
  techbrabo: getTechbraboOportunidades,
};

export default function Marketing() {
  const { empresa } = useParams();
  const [dadosMarketing, setDadosMarketing] = useState(null);
  const [dadosOportunidades, setDadosOportunidades] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!EMPRESAS[empresa]) return;
    setLoading(true);
    const fetchMkt = getMarketing(empresa);
    const fetchOpp = fetchOportunidades[empresa]();
    Promise.all([fetchMkt, fetchOpp])
      .then(([mkt, opp]) => {
        setDadosMarketing(mkt);
        setDadosOportunidades(opp);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [empresa]);

  if (!EMPRESAS[empresa]) return <Navigate to="/marketing/montseguro" replace />;

  const accent = EMPRESAS[empresa].accent;

  const marketingAgg = useMemo(() => {
    if (!dadosMarketing) return { porMes: [], porCanal: [] };
    const porMes = {};
    const porCanal = {};
    dadosMarketing.forEach((d) => {
      const mes = d.mes;
      const canal = d.canal;
      const invest = Number(d.investimento);
      const leads = d.leads_gerados || 0;

      if (!porMes[mes]) porMes[mes] = { mes, investimento: 0, leads: 0 };
      porMes[mes].investimento += invest;
      porMes[mes].leads += leads;

      if (!porCanal[canal]) porCanal[canal] = { canal, investimento: 0, leads: 0 };
      porCanal[canal].investimento += invest;
      porCanal[canal].leads += leads;
    });
    return {
      porMes: Object.values(porMes).sort((a, b) => a.mes.localeCompare(b.mes)),
      porCanal: Object.values(porCanal),
    };
  }, [dadosMarketing]);

  const receitaAgg = useMemo(() => {
    if (!dadosOportunidades) return { porMes: [], porCanal: [] };
    const aggregator = AGGREGATORS[empresa];
    if (!aggregator) return { porMes: [], porCanal: [] };

    const porCanal = aggregator(dadosOportunidades);

    const porMes = {};
    const agruparPorMes = (item) => {
      const mes = item.mes || "2026-01";
      const receita = item.receita || 0;
      if (!porMes[mes]) porMes[mes] = { mes, receita: 0 };
      porMes[mes].receita += receita;
    };

    if (empresa === "montseguro") {
      dadosOportunidades
        .filter((f) => f.data_implantacao)
        .forEach((f) => {
          const mes = f.mes_referencia || "2026-01";
          const receita = (f.premio_mensal_estimado || 0) * 0.12;
          if (!porMes[mes]) porMes[mes] = { mes, receita: 0 };
          porMes[mes].receita += receita;
        });
    } else if (empresa === "prop5") {
      dadosOportunidades
        .filter((o) => o.estagio === "Fechado" && o.comissao)
        .forEach((o) => {
          const mes = o.mes_referencia || "2026-01";
          const receita = o.comissao || 0;
          if (!porMes[mes]) porMes[mes] = { mes, receita: 0 };
          porMes[mes].receita += receita;
        });
    } else if (empresa === "techbrabo") {
      dadosOportunidades
        .filter((o) => o.estagio === "Contrato assinado")
        .forEach((o) => {
          const mes = o.mes_referencia || "2026-01";
          let receita = 0;
          if (o.tipo_receita === "Pontual") {
            receita = o.valor_contrato || 0;
          } else if (o.tipo_receita === "Recorrente" && o.mrr) {
            receita = o.mrr * 12;
          }
          if (receita > 0) {
            if (!porMes[mes]) porMes[mes] = { mes, receita: 0 };
            porMes[mes].receita += receita;
          }
        });
    }

    return {
      porMes: Object.values(porMes).sort((a, b) => a.mes.localeCompare(b.mes)),
      porCanal,
    };
  }, [dadosOportunidades, empresa]);

  const evolucaoMensal = useMemo(() => {
    const mktMap = {};
    marketingAgg.porMes.forEach((m) => {
      mktMap[m.mes] = { ...m, receita: 0 };
    });
    receitaAgg.porMes.forEach((r) => {
      if (mktMap[r.mes]) {
        mktMap[r.mes].receita = r.receita;
      } else {
        mktMap[r.mes] = { mes: r.mes, investimento: 0, leads: 0, receita: r.receita };
      }
    });
    return Object.values(mktMap).sort((a, b) => a.mes.localeCompare(b.mes));
  }, [marketingAgg.porMes, receitaAgg.porMes]);

  const canaisComROI = useMemo(() => {
    const mktMap = {};
    marketingAgg.porCanal.forEach((c) => {
      mktMap[c.canal] = { ...c, receita: 0 };
    });
    receitaAgg.porCanal.forEach((r) => {
      if (mktMap[r.canal]) {
        mktMap[r.canal].receita = r.receita;
      } else {
        mktMap[r.canal] = { canal: r.canal, investimento: 0, leads: 0, receita: r.receita };
      }
    });
    return Object.values(mktMap).map((c) => ({
      ...c,
      roi: c.investimento > 0 ? (c.receita - c.investimento) / c.investimento : null,
    }));
  }, [marketingAgg.porCanal, receitaAgg.porCanal]);

  // Totais
  const totalInvestimento = marketingAgg.porCanal.reduce((acc, c) => acc + c.investimento, 0);
  const totalLeads = marketingAgg.porCanal.reduce((acc, c) => acc + c.leads, 0);
  const totalReceita = canaisComROI.reduce((acc, c) => acc + c.receita, 0);
  const roiGeral = totalInvestimento > 0 ? (totalReceita - totalInvestimento) / totalInvestimento : null;

  if (loading) return <p className="text-muted-foreground text-center py-8">Carregando dados de marketing...</p>;

  return (
    <div>
      <div className="page-header">
        <h2>Marketing</h2>
        <div className="page-subtitle">Investimento, leads, evolução mensal e ROI por canal.</div>
      </div>

      {/* Switcher de empresas com logos */}
      <div className="empresa-switch">
        {Object.entries(EMPRESAS).map(([key, cfg]) => (
          <Link
            key={key}
            to={`/marketing/${key}`}
            className={empresa === key ? "active" : ""}
            style={{ "--empresa-accent": cfg.accent }}
          >
            <EmpresaLogo empresaKey={key} size="sm" />
            {cfg.label}
          </Link>
        ))}
      </div>

      {/* Cards de resumo */}
      <div className="kpi-grid" style={{ marginBottom: "1.5rem" }}>
        <KpiCard
          label="Investimento Total"
          value={totalInvestimento}
          format="currency"
          accent={accent}
          definition="investimento_total"
        />
        <KpiCard
          label="Leads Gerados"
          value={totalLeads}
          accent={accent}
          definition="leads_gerados"
        />
        <KpiCard
          label="Receita Estimada"
          value={totalReceita}
          format="currency"
          accent={accent}
          definition="receita_estimada"
        />
        <KpiCard
          label="ROI Geral"
          value={roiGeral !== null ? (roiGeral * 100).toFixed(1) : null}
          format="percent"
          accent={accent}
          definition="roi_geral"
          status={
            roiGeral !== null
              ? roiGeral > 0.5 ? "verde" : roiGeral > 0 ? "amarelo" : "vermelho"
              : undefined
          }
        />
      </div>

      {/* Gráfico de evolução mensal */}
      {evolucaoMensal.length > 0 && (
        <div className="section">
          <h3>Evolução Mensal</h3>
          <div style={{ width: "100%", height: 250 }}>
            <ResponsiveContainer>
              <LineChart data={evolucaoMensal} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <XAxis dataKey="mes" />
                <YAxis
                  yAxisId="left"
                  orientation="left"
                  tickFormatter={(v) => `R$ ${(v / 1000).toFixed(2)}k`}
                />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip
                  formatter={(value, name) => {
                    if (name === "investimento" || name === "receita") {
                      return formatBRL(value);
                    }
                    
                    return value;
                  }}
                  labelFormatter={(label) => `Mês: ${label}`}
                />
                <Legend />
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="investimento"
                  stroke={accent}
                  name="Investimento"
                  strokeWidth={2}
                  dot={{ r: 4 }}
                />
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="receita"
                  stroke="#16a34a"
                  name="Receita Estimada"
                  strokeWidth={2}
                  dot={{ r: 4 }}
                />
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="leads"
                  stroke="#eab308"
                  name="Leads"
                  strokeWidth={2}
                  dot={{ r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Tabela de canais com ROI */}
      {canaisComROI.length > 0 && (
        <div className="section">
          <h3>Desempenho por Canal</h3>
          <table className="data-table">
            <thead>
              <tr>
                <th>Canal</th>
                <th>Investimento</th>
                <th>Leads</th>
                <th>CPL</th>
                <th>Receita Estimada</th>
                <th>ROI</th>
              </tr>
            </thead>
            <tbody>
              {canaisComROI.map((c) => (
                <tr key={c.canal}>
                  <td>{c.canal}</td>
                  <td>{formatBRL(c.investimento)}</td>
                  <td>{c.leads}</td>
                  <td>{c.leads > 0 ? formatBRL(c.investimento / c.leads) : "—"}</td>
                  <td>{formatBRL(c.receita)}</td>
                  <td
                    style={{
                      color:
                        c.roi === null
                          ? "#64748b"
                          : c.roi > 0.5
                          ? "#16a34a"
                          : c.roi > 0
                          ? "#eab308"
                          : "#dc2626",
                    }}
                  >
                    {c.roi !== null ? `${(c.roi * 100).toFixed(1)}%` : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
