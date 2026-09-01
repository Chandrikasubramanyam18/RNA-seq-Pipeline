import type { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
  title?: string;
  icon?: ReactNode;
  actions?: ReactNode;
}

export function Card({ children, className = "", title, icon, actions }: CardProps) {
  return (
    <section
      className={`rounded-lg border border-border bg-surface ${className}`}
    >
      {(title || actions) && (
        <header className="flex items-center justify-between gap-3 border-b border-border px-4 py-3">
          <h3 className="flex items-center gap-2 text-sm font-semibold tracking-wide text-fg">
            {icon}
            {title}
          </h3>
          {actions && <div className="flex items-center gap-2">{actions}</div>}
        </header>
      )}
      <div className="p-4">{children}</div>
    </section>
  );
}
