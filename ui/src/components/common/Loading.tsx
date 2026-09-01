import { Loader2 } from "lucide-react";

export function Loading({ label = "Loading" }: { label?: string }) {
  return (
    <div className="flex items-center gap-2 py-10 text-sm text-fg-dim">
      <Loader2 className="h-4 w-4 animate-spin text-accent" />
      <span className="mono">{label}…</span>
    </div>
  );
}
