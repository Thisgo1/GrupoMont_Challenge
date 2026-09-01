import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate, NavLink } from "react-router-dom";
import Comercial from "./pages/Comercial";

import './App.css'

const NAV = [
  { to: "/comercial", label: "Comercial", icon: TrendingUp },
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
              <ThemeToggle />
            </div>
        </aside>

        <main className="main">
          <Routes>

            <Route path="/comercial" element={<Navigate to="/comercial/montseguro" replace />} />
            <Route path="/comercial/:empresa" element={<Comercial />} />


            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
