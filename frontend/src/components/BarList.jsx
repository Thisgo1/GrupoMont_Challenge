// src/components/BarList.jsx (versão melhorada)
export default function BarList({ items, accent = "#101b2d", numbered = false, formatValue }) {
  const max = Math.max(...items.map((i) => i.value), 1);
  const fmt = formatValue || ((v) => v.toLocaleString("pt-BR"));

  return (
    <div className="space-y-3">
      {items.map((item, idx) => (
        <div
          key={item.label}
          className="flex items-center gap-3 group transition-all hover:bg-muted/30 p-1 rounded-md"
        >
          {numbered && (
            <span className="text-sm font-medium text-muted-foreground w-6 text-right">
              {idx + 1}
            </span>
          )}
          <span className="text-sm font-medium w-32 truncate">{item.label}</span>
          <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-500 group-hover:opacity-80"
              style={{
                width: `${(item.value / max) * 100}%`,
                backgroundColor: accent
              }}
            />
          </div>
          <span className="text-sm font-mono w-24 text-right font-medium">
            {fmt(item.value)}
          </span>
        </div>
      ))}
    </div>
  );
}
