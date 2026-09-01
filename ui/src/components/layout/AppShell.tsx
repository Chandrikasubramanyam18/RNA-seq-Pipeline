import type { ReactNode } from "react";

interface AppShellProps {
  sidebar: ReactNode;
  header?: ReactNode;
  children: ReactNode;
}

/**
 * Two-column console shell: fixed sidebar nav + scrollable main pane.
 */
export function AppShell({ sidebar, header, children }: AppShellProps) {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-bg text-fg">
      <aside className="flex w-60 shrink-0 flex-col border-r border-border bg-surface">
        {sidebar}
      </aside>
      <div className="flex min-w-0 flex-1 flex-col">
        {header && (
          <header className="flex h-14 shrink-0 items-center border-b border-border bg-surface px-4">
            {header}
          </header>
        )}
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  );
}
