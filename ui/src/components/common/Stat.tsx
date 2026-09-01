import type { ReactNode } from "react";

interface StatProps {
  label: string;
  value: string | number;
  sub?: string;
  accent?: boolean;
  icon?: ReactNode;
}

export function Stat({ label, value, sub, accent = false, icon }: StatProps) {
  return (
    <div className="flex flex-col gap-1 rounded-lg border border-border bg-surface-2 px-4 py-3">
      <span className="flex items-center gap-1.5 text-xs uppercase tracking-wider text-fg-dim">
        {icon}
        {label}
      </span>
      <span
        className={`mono text-xl font-semibold ${
          accent ? "text-accent" : "text-fg"
        }`}
      >
        {value}
      </span>
      {sub && <span className="text-xs text-fg-dim">{sub}</span>}
    </div>
  );
}
