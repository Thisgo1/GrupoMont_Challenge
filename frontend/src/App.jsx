import { BrowserRouter, Routes, Route, Navigate, NavLink } from "react-router-dom";
import CeoOverview from "./pages/CeoOverview";
import Comercial from "./pages/Comercial";
import Marketing from "./pages/Marketing";
import Empresas from "./pages/Empresas";
import Insights from "./pages/Insights";
import Comparativos from "./pages/Comparativos";
import Metas from "./pages/Metas";
import {
  LayoutDashboard,
  TrendingUp,
  Megaphone,
  Building2,
  Lightbulb,
  GitCompare,
  Target as TargetIcon
} from "lucide-react";

import './App.css'

const NAV = [
  { to: "/", label: "CEO Overview", icon: LayoutDashboard, end: true },
  { to: "/comercial", label: "Comercial", icon: TrendingUp },
  { to: "/marketing", label: "Marketing", icon: Megaphone },
  { to: "/empresas", label: "Empresas", icon: Building2 },
  { to: "/insights", label: "Insights", icon: Lightbulb, end: true },
  { to: "/comparativos", label: "Comparativos", icon: GitCompare, end: true },
  { to: "/metas", label: "Metas", icon: TargetIcon, end: true },
];

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <aside className="sidebar h-screen sticky top-0 overflow-y-auto flex flex-col">
          <div className="sidebar-brand">Grupo Mont</div>
          <div className="sidebar-subbrand">Dashboard executivo</div>
          <ul className="nav-list">
            {NAV.map((item) => (
              <li key={item.label}>
                <NavLink
                  to={item.to}
                  end={item.end}
                  className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
                >
                  <item.icon size={18} />
                  {item.label}
                </NavLink>
              </li>
            ))}
          </ul>
            <div className="mt-auto pt-4 border-t border-white/10">
            </div>
        </aside>

        <main className="main">
          <Routes>
            <Route path="/" element={<CeoOverview />} />

            <Route path="/comercial" element={<Navigate to="/comercial/montseguro" replace />} />
            <Route path="/comercial/:empresa" element={<Comercial />} />

            <Route path="/marketing" element={<Navigate to="/marketing/montseguro" replace />} />
            <Route path="/marketing/:empresa" element={<Marketing />} />

            <Route path="/empresas" element={<Navigate to="/empresas/montseguro" replace />} />
            <Route path="/empresas/:empresa" element={<Empresas />} />

            <Route path="/insights" element={<Insights />} />

            <Route path="/comparativos" element={<Comparativos />} />
            <Route path="/metas" element={<Metas />} />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
