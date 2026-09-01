// src/components/FiltrosComercial.jsx
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function FiltrosComercial({
  vendedor,
  setVendedor,
  canal,
  setCanal,
  vendedores,
  canais,
  loading,
}) {
  return (
    <div className="flex flex-wrap gap-3 my-4">
      <Select value={vendedor} onValueChange={setVendedor}>
        <SelectTrigger className="w-[180px]">
          <SelectValue placeholder="Todos os vendedores" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="">Todos os vendedores</SelectItem>
          {vendedores.map((v) => (
            <SelectItem key={v} value={v}>
              {v}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      <Select value={canal} onValueChange={setCanal}>
        <SelectTrigger className="w-[180px]">
          <SelectValue placeholder="Todos os canais" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="">Todos os canais</SelectItem>
          {canais.map((c) => (
            <SelectItem key={c} value={c}>
              {c}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
