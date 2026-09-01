import { useEffect, useState } from "react";
import { getMetasProjecao } from "../../services/api";
import KpiCard from "../../components/KpiCard";
import EmpresaLogo from "../../components/EmpresaLogo";
import { EMPRESAS } from "../../theme/empresas";

export default function Metas() {
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMetasProjecao()
      .then((data) => {
        setDados(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-muted-foreground text-center py-8">Carregando metas...</p>;
  if (!dados) return <p className="text-muted-foreground text-center py-8">Nenhum dado disponível.</p>;

  const { empresas, mes, dia_corrido, dias_uteis_mes } = dados;

  return (
    <div className="space-y-8 p-4 max-w-7xl mx-auto">
      {/* Header */}
      <div className="page-header">
        <h2 className="text-2xl font-bold">Metas e Projeção</h2>
        <p className="text-muted-foreground">
          Acompanhamento de metas, ritmo e necessidade diária – mês {mes} · Dia {dia_corrido} de {dias_uteis_mes} dias úteis
        </p>
      </div>

      {empresas.map((emp) => {
        const empresaKey = emp.empresa.toLowerCase().replace(/\s/g, "");
        const accent = EMPRESAS[empresaKey]?.accent || "#1e293b";
        const label = EMPRESAS[empresaKey]?.label || emp.empresa;

        return (
          <div key={emp.empresa} className="bg-card border rounded-lg p-4 space-y-4">
            <div className="flex items-center gap-3">
              <EmpresaLogo empresaKey={empresaKey} size="md" />
              <h3 className="text-lg font-semibold">{label}</h3>
            </div>

            {/* Cards de KPIs */}
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
              <KpiCard label="Meta" value={emp.meta} format="currency" accent={accent} />
              <KpiCard label="Realizado" value={emp.receita} format="currency" accent={accent} />
              <KpiCard
                label="Atingimento"
                value={emp.atingimento_pct}
                format="percent"
                status={
                  emp.atingimento_pct >= 95
                    ? "verde"
                    : emp.atingimento_pct >= 80
                    ? "amarelo"
                    : "vermelho"
                }
                accent={accent}
              />
              <KpiCard label="Meta esperada hoje" value={emp.meta_esperada_ate_hoje} format="currency" accent={accent} />
              <KpiCard label="Gap de ritmo" value={emp.gap_ritmo} format="currency" accent={accent} />
              <KpiCard label="Necessidade diária" value={emp.necessidade_diaria} format="currency" accent={accent} />
              <KpiCard label="Dias úteis restantes" value={emp.dias_uteis_restantes} accent={accent} />
              <KpiCard label="Negócios no mês" value={emp.qtd_negocios} accent={accent} />
            </div>

            {/* Barra de progresso da meta */}
            <div className="space-y-1">
              <div className="flex justify-between text-sm text-muted-foreground">
                <span>Progresso da meta</span>
                <span>{Math.min(emp.atingimento_pct || 0, 100)}%</span>
              </div>
              <div className="h-2 w-full bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all"
                  style={{
                    width: `${Math.min(emp.atingimento_pct || 0, 100)}%`,
                    backgroundColor: accent,
                  }}
                />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
