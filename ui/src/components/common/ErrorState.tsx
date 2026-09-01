import { AlertTriangle } from "lucide-react";

export function ErrorState({ message }: { message?: string }) {
  return (
    <div className="flex items-center gap-2 rounded-lg border border-fail/40 bg-fail/10 px-4 py-3 text-sm text-fail">
      <AlertTriangle className="h-4 w-4 shrink-0" />
      <span className="mono">{message ?? "An unexpected error occurred."}</span>
    </div>
  );
}
