import {
  Dna,
  FlaskConical,
  LayoutDashboard,
  Microscope,
  Route,
  FileText,
  Folder,
  Sigma,
  Dna as Scaffold,
} from "lucide-react";
import { NavItem } from "./NavItem";

const NAV = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/projects", label: "Projects", icon: Folder },
  { to: "/qc", label: "QC", icon: FlaskConical },
  { to: "/alignment", label: "Alignment", icon: Route },
  { to: "/expression", label: "Expression", icon: Microscope },
  { to: "/differential-expression", label: "DE Results", icon: Sigma },
  { to: "/pathways", label: "Pathways", icon: Dna },
  { to: "/reports", label: "Reports", icon: FileText },
];

export function Sidebar() {
  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-2 border-b border-border px-4 py-4">
        <Scaffold className="h-6 w-6 text-accent" />
        <div className="leading-tight">
          <div className="text-sm font-semibold text-fg">
            RNA-seq Analysis Platform
          </div>
          <div className="mono text-[11px] text-fg-dim">
            read-only • GSE52778 demo
          </div>
        </div>
      </div>
      <nav className="flex-1 space-y-1 overflow-y-auto p-3">
        {NAV.map(({ to, label, icon: Icon }) => (
          <NavItem key={to} to={to} end={to === "/"}>
            <Icon className="h-4 w-4" />
            {label}
          </NavItem>
        ))}
      </nav>
      <div className="border-t border-border p-3">
        <div className="flex items-center gap-2 rounded-md bg-warn/10 px-3 py-2 text-[11px] text-warn">
          <FlaskConical className="h-3.5 w-3.5 shrink-0" />
          DEMO DATA — not real results
        </div>
      </div>
    </div>
  );
}
