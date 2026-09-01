import { useEffect, useState } from "react";
import { getCeoOverview, getEvolucaoReceita } from "../services/api";
import KpiCard from "../components/KpiCard";
import EmpresaLogo from "../components/EmpresaLogo";
import InsightsBanner from "../components/InsightsBanner";
import { EMPRESAS } from "../theme/empresas";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
  LineChart,
  Line,
  CartesianGrid
} from "recharts";


function statusPorAtingimento(pct) {
  if (pct === null || pct === undefined) return undefined;
  if (pct >= 95) return "verde";
  if (pct >= 80) return "amarelo";
  return "vermelho";
}

export default function CeoOverview() {
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState(null);
  const [evolucao, setEvolucao] = useState(null);

  useEffect(() => {
  getEvolucaoReceita(6)
    .then(setEvolucao)
    .catch(() => {});
}, []);

  useEffect(() => {
    getCeoOverview()
      .then((data) => {
        setDados(data);
        setLoading(false);
      })
      .catch((err) => {
        setErro(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p className="text-muted-foreground text-center py-8">Carregando dados consolidados...</p>;
  }

  if (erro) {
    return (
      <p className="text-red-600 text-center py-8">
        Erro ao buscar dados: {erro}. Verifique se o backend está rodando.
      </p>
    );
  }

  if (!dados) return null;

  const { empresas, total, mes } = dados;

  return (
    <div className="space-y-8 p-4 max-w-7xl mx-auto">
      {/* Header */}
      <div className="page-header">
        <h2 className="text-2xl font-bold">CEO Overview</h2>
        <p className="text-muted-foreground">
          Montseguro · Prop5 · TechBrabo — visão consolidada do mês <strong>{mes}</strong>
        </p>
      </div>

      {/* Banner de Insights */}
      <InsightsBanner maxItens={3} />

      {/* ===== LINHA 1: TOTAIS DO GRUPO ===== */}
      <div className="bg-muted/30 p-4 rounded-lg border border-border">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-4">
          Grupo Mont — Consolidado
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
          <KpiCard label="Receita Total" value={total.receita_total} format="currency" accent="#1e293b" />
          <KpiCard label="Meta Total" value={total.meta_total} format="currency" accent="#1e293b" />
          <KpiCard
            label="Atingimento"
            value={total.atingimento_geral_pct}
            format="percent"
            status={statusPorAtingimento(total.atingimento_geral_pct)}
            accent="#1e293b"
          />
          <KpiCard label="Forecast" value={total.forecast_total} format="currency" accent="#1e293b" />
          <KpiCard label="Gap" value={total.gap_total} format="currency" accent="#1e293b" />
          <KpiCard label="Ticket Médio" value={total.ticket_medio_consolidado} format="currency" accent="#1e293b" />
          <KpiCard label="Leads Totais" value={total.leads_total} accent="#1e293b" />
          <KpiCard
            label="Taxa de Conversão Geral"
            value={total.taxa_conversao_geral_pct}
            format="percent"
            status={
              total.taxa_conversao_geral_pct >= 20
                ? "verde"
                : total.taxa_conversao_geral_pct >= 15
                ? "amarelo"
                : "vermelho"
            }
            accent="#1e293b"
          />
        </div>
      </div>

      {/* ===== GRÁFICO DE EVOLUÇÃO DA RECEITA ===== */}
      {evolucao && evolucao.meses && evolucao.meses.length > 0 && (
        <div className="bg-card rounded-lg border p-4 space-y-4">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
            Evolução da Receita (últimos 6 meses)
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart
              data={evolucao.meses}
              margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="mes" />
              <YAxis
                tickFormatter={(v) => `R$ ${(v / 1000).toFixed(0)}k`}
              />
              <Tooltip
                formatter={(value) =>
                  value.toLocaleString("pt-BR", {
                    style: "currency",
                    currency: "BRL",
                    maximumFractionDigits: 0,
                  })
                }
                labelFormatter={(label) => `Mês: ${label}`}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="receita_total"
                stroke="#1e293b"
                strokeWidth={3}
                name="Receita Total do Grupo"
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
              />
              <Line
                type="monotone"
                dataKey="receita_montseguro"
                stroke={EMPRESAS.montseguro?.accent || "#2a6f97"}
                strokeWidth={2}
                name="Montseguro"
                dot={{ r: 3 }}
              />
              <Line
                type="monotone"
                dataKey="receita_prop5"
                stroke={EMPRESAS.prop5?.accent || "#d97706"}
                strokeWidth={2}
                name="Prop5"
                dot={{ r: 3 }}
              />
              <Line
                type="monotone"
                dataKey="receita_techbrabo"
                stroke={EMPRESAS.techbrabo?.accent || "#7c3aed"}
                strokeWidth={2}
                name="TechBrabo"
                dot={{ r: 3 }}
              />
            </LineChart>
          </ResponsiveContainer>
          <p className="text-xs text-muted-foreground">
            Receita consolidada do grupo e por empresa nos últimos 6 meses.
          </p>
        </div>
      )}

      {/* ===== LINHA 2: RITMO DE META + MARKETING ===== */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Ritmo */}
        <div className="bg-card rounded-lg border p-4">
          <h4 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">Ritmo de Meta</h4>
          <div className="mt-2 grid grid-cols-2 gap-2">
            <KpiCard label="Meta esperada até hoje" value={total.meta_esperada_ate_hoje} format="currency" accent="#1e293b" />
            <KpiCard label="Gap de ritmo" value={total.gap_ritmo_total} format="currency" accent="#1e293b" />
            <KpiCard label="Necessidade diária" value={total.necessidade_diaria_total} format="currency" accent="#1e293b" />
            <KpiCard label="Dias úteis restantes" value={total.dias_uteis_restantes} accent="#1e293b" />
          </div>
        </div>

        {/* Marketing */}
        <div className="bg-card rounded-lg border p-4">
          <h4 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">Marketing e Crescimento</h4>
          <div className="mt-2 grid grid-cols-2 gap-2">
            <KpiCard label="Crescimento MoM" value={total.crescimento_mom_pct} format="percent" accent="#1e293b" />
            <KpiCard label="Investimento Marketing" value={total.investimento_marketing_total} format="currency" accent="#1e293b" />
            <KpiCard label="CAC Médio" value={total.cac_medio} format="currency" accent="#1e293b" />
            <KpiCard label="ROI de Marketing" value={total.roi_marketing_geral_pct} format="percent" accent="#1e293b" />
          </div>
        </div>
      </div>

      {/* ===== GRÁFICO COMPARATIVO ===== */}
      <div className="bg-card rounded-lg border p-4 space-y-4">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
          Comparativo de Receita e Meta
        </h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={empresas} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <XAxis dataKey="empresa" />
            <YAxis tickFormatter={(v) => `R$ ${(v / 1000).toFixed(0)}k`} />
            <Tooltip
              formatter={(value) =>
                value.toLocaleString("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 })
              }
            />
            <Legend />
            <Bar dataKey="receita" fill="#3b82f6" name="Receita Realizada" radius={[4, 4, 0, 0]} />
            <Bar dataKey="meta" fill="#94a3b8" name="Meta" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>


      {/* ===== DETALHES POR EMPRESA ===== */}
      {empresas.map((emp) => {
        const empresaKey = emp.empresa.toLowerCase().replace(/\s/g, "");
        const accent = EMPRESAS[empresaKey]?.accent || "#1e293b";
        const label = EMPRESAS[empresaKey]?.label || emp.empresa;

        return (
          <div key={emp.empresa} className="space-y-4">
            <div className="flex items-center gap-3">
              <EmpresaLogo empresaKey={empresaKey} size="md" />
              <h3 className="text-lg font-semibold">{label}</h3>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
              <KpiCard label="Receita" value={emp.receita} format="currency" accent={accent} />
              <KpiCard label="Meta" value={emp.meta} format="currency" accent={accent} />
              <KpiCard
                label="Atingimento"
                value={emp.atingimento_pct}
                format="percent"
                status={statusPorAtingimento(emp.atingimento_pct)}
                accent={accent}
              />
              <KpiCard label="Forecast" value={emp.forecast} format="currency" accent={accent} />
              <KpiCard label="Gap" value={emp.gap} format="currency" accent={accent} />
              <KpiCard label="Ticket Médio" value={emp.ticket_medio} format="currency" accent={accent} />
            </div>
          </div>
        );
      })}
    </div>
  );
}
