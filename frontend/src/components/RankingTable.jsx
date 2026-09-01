import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const formatBRL = (v) => v.toLocaleString("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 });

export default function RankingTable({ linhas, labels, accent }) {
  if (!linhas.length) return <p className="text-muted-foreground">Sem resultados fechados nesse recorte ainda.</p>;

  const max = Math.max(...linhas.map((l) => l.valor), 1);

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Vendedor</TableHead>
          <TableHead>{labels.quantidade}</TableHead>
          <TableHead>{labels.valor}</TableHead>
          <TableHead></TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {linhas.map((l) => (
          <TableRow key={l.vendedor}>
            <TableCell>{l.vendedor}</TableCell>
            <TableCell>{l.quantidade}</TableCell>
            <TableCell>{formatBRL(l.valor)}</TableCell>
            <TableCell className="w-32">
              <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full"
                  style={{ width: `${(l.valor / max) * 100}%`, backgroundColor: accent }}
                />
              </div>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
