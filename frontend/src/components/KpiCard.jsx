import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import KpiTooltip from "./KpiTooltip";
import { getKpiDefinition } from "@/lib/kpiDefinitions";

function formatValue(value, format) {
  if (value === null || value === undefined) return "—";
  if (format === "currency") {
    return Number(value).toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
      maximumFractionDigits: 2,
    });
  }
  if (format === "percent") return `${Number(value).toFixed(1)}%`;
  if (format === "dias") return `${Number(value).toFixed(0)} dias`;
  return Number(value).toLocaleString("pt-BR");
}

export default function KpiCard({
  label,
  value,
  format = "number",
  status,
  accent,
  definition
}) {
  const def = definition ? getKpiDefinition(definition) : null;

  const statusClass =
    status === "verde" ? "text-green-600 dark:text-green-400" :
    status === "amarelo" ? "text-yellow-600 dark:text-yellow-400" :
    status === "vermelho" ? "text-red-600 dark:text-red-400" :
    "";

  const tooltipLabel = def?.label || label;
  const tooltipDescription = def?.description || "Descrição não disponível para este indicador.";
  const tooltipFormula = def?.formula || null;

  const formattedValue = formatValue(value, format);
  const isLong = formattedValue.length > 15;

  return (
    <div
      className="kpi-card h-full flex flex-col"
      style={{ borderTop: `3px solid ${accent || "#101b2d"}` }}
    >
      <Card className="border-0 shadow-none flex-1 flex flex-col">
        <CardHeader className="pb-2">
          <KpiTooltip
            label={tooltipLabel}
            description={tooltipDescription}
            formula={tooltipFormula}
          >
            <CardTitle className="text-sm font-medium text-muted-foreground truncate">
              {label}
            </CardTitle>
          </KpiTooltip>
        </CardHeader>
        <CardContent className="flex-1 flex items-end">
          <div
            className={`font-bold ${isLong ? 'text-lg' : 'text-2xl'} ${statusClass} truncate w-full`}
            title={formattedValue}
          >
            {formattedValue}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
