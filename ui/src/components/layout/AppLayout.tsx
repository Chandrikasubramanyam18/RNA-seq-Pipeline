import type { ReactNode } from "react";
import { AppShell } from "./AppShell";
import { Sidebar } from "./Sidebar";
import { TopBar } from "./TopBar";
import { MockNotice } from "@/components/common/MockNotice";

export function AppLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-screen w-screen flex-col overflow-hidden bg-bg">
      <MockNotice />
      <div className="flex min-h-0 flex-1">
        <AppShell
          sidebar={<Sidebar />}
          header={<TopBar />}
        >
          {children}
        </AppShell>
      </div>
    </div>
  );
}
