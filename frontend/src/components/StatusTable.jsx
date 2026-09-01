import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default function StatusTable({ rows }) {
  const total = rows.reduce((acc, r) => acc + r.count, 0);

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Status</TableHead>
          <TableHead>Qtd.</TableHead>
          <TableHead>%</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {rows.map((r) => (
          <TableRow key={r.status}>
            <TableCell>{r.status}</TableCell>
            <TableCell>{r.count}</TableCell>
            <TableCell>{total ? ((r.count / total) * 100).toFixed(1) : 0}%</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
