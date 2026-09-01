import { EMPRESAS } from "../theme/empresas";

export default function EmpresaLogo({ empresaKey, size = "md", className = "" }) {
  const config = EMPRESAS[empresaKey];
  if (!config) return null;

  const sizeMap = {
    sm: "w-6 h-6",
    md: "w-8 h-8",
    lg: "w-10 h-10",
  };

  if (config.logo) {
    return (
      <img
        src={config.logo}
        alt={config.label}
        className={`${sizeMap[size]} rounded-full object-cover ${className}`}
      />
    );
  }

  return (
    <div
      className={`${sizeMap[size]} rounded-full flex items-center justify-center font-bold text-white ${className}`}
      style={{ backgroundColor: config.accent }}
    >
      {config.initial}
    </div>
  );
}
