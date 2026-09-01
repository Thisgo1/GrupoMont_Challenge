import { useEffect, useState } from "react";
import { getComparativos } from "../../services/api";
import { EMPRESAS } from "../../theme/empresas";
import { ResponsiveContainer, BarChart, XAxis, YAxis, Tooltip, Legend, Bar } from "recharts";

export default function Comparativos() {
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    getComparativos()
      .then((data) => {
        setDados(data);
        setLoading(false);
      })
      .catch((err) => {
        setErro(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p className="text-muted-foreground text-center py-8">Carregando comparativos...</p>;
  if (erro) return <p className="text-red-600 text-center py-8">Erro: {erro}</p>;
  if (!dados || !dados.comparativos) return <p className="text-muted-foreground text-center py-8">Nenhum dado disponível.</p>;

  const { mes, comparativos } = dados;
  const sorted = [...comparativos].sort((a, b) => b.produtividade_ajustada - a.produtividade_ajustada);

  return (
    <div className="space-y-8 p-4 max-w-7xl mx-auto">
      <div className="page-header">
        <h2 className="text-2xl font-bold">Comparativo entre Empresas</h2>
        <p className="text-muted-foreground">
          Produtividade ajustada, CPLQ e conversão ajustada — mês <strong>{mes}</strong>.
        </p>
      </div>

      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={sorted} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <XAxis dataKey="empresa" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="produtividade_ajustada" fill="#3b82f6" name="Produtividade Ajustada" />
          <Bar dataKey="conversao_ajustada_pct" fill="#eab308" name="Conversão Ajustada (%)" />
          <Bar dataKey="cplq" fill="#8b5cf6" name="CPLQ (R$)" />
        </BarChart>
      </ResponsiveContainer>

      {/* Tabela comparativa */}
      <div className="overflow-x-auto border rounded-lg">
        <table className="w-full text-sm">
          <thead className="bg-muted/50">
            <tr>
              <th className="text-left p-3 font-semibold">Empresa</th>
              <th className="text-left p-3 font-semibold">Produtividade Ajustada</th>
              <th className="text-left p-3 font-semibold">CPLQ (Custo por Lead Qualif.)</th>
              <th className="text-left p-3 font-semibold">Conversão Ajustada</th>
              <th className="text-left p-3 font-semibold">Leads Qualif.</th>
              <th className="text-left p-3 font-semibold">Fechamentos</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {sorted.map((item) => {
              const key = item.empresa.toLowerCase().replace(" ", "");
              const accent = EMPRESAS[key]?.accent || "#1e293b";
              return (
                <tr key={item.empresa} style={{ borderLeft: `4px solid ${accent}` }}>
                  <td className="p-3 font-medium">{item.empresa}</td>
                  <td className="p-3">{item.produtividade_ajustada}</td>
                  <td className="p-3">{item.cplq !== null ? `R$ ${item.cplq}` : "—"}</td>
                  <td className="p-3">{item.conversao_ajustada_pct !== null ? `${item.conversao_ajustada_pct}%` : "—"}</td>
                  <td className="p-3">{item.leads_qualificados}</td>
                  <td className="p-3">{item.fechamentos}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Cards de destaque por métrica */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {sorted.map((item) => {
          const key = item.empresa.toLowerCase().replace(" ", "");
          const accent = EMPRESAS[key]?.accent || "#1e293b";
          return (
            <div key={item.empresa} className="bg-card rounded-lg border p-4 space-y-2" style={{ borderTop: `4px solid ${accent}` }}>
              <h4 className="font-semibold">{item.empresa}</h4>
              <div className="text-sm text-muted-foreground space-y-1">
                <div>Produtividade ajustada: <span className="font-medium">{item.produtividade_ajustada}</span></div>
                <div>CPLQ: <span className="font-medium">{item.cplq !== null ? `R$ ${item.cplq}` : "—"}</span></div>
                <div>Conversão ajustada: <span className="font-medium">{item.conversao_ajustada_pct !== null ? `${item.conversao_ajustada_pct}%` : "—"}</span></div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
