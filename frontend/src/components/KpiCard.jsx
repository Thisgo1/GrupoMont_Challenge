import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

function formatValue(value, format) {
  if (value === null || value === undefined) return "—";
  if (format === "currency") {
    return Number(value).toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
      maximumFractionDigits: 0
    });
  }
  if (format === "percent") return `${Number(value).toFixed(1)}%`;
  if (format === "dias") return `${Number(value).toFixed(0)} dias`;
  return Number(value).toLocaleString("pt-BR");
}

export default function KpiCard({ label, value, format = "number", status, accent, definition }) {
  const statusClass =
    status === "verde" ? "text-green-600" :
    status === "amarelo" ? "text-yellow-600" :
    status === "vermelho" ? "text-red-600" :
    "";

  return (

    <div className="kpi-card" style={{ borderTopColor: accent || "#101b2d" }}>
      <Card className="border-0 shadow-none">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            {label}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className={`text-2xl font-bold ${statusClass}`}>
            {formatValue(value, format)}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
