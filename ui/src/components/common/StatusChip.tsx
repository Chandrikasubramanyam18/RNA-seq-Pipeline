import type { StageStatus } from "@/types";

const STATUS_STYLES: Record<StageStatus, string> = {
  done: "bg-ok/15 text-ok border-ok/30",
  running: "bg-cyan-glow/15 text-cyan-glow border-cyan-glow/30",
  pending: "bg-muted/15 text-muted border-muted/30",
  blocked: "bg-fail/15 text-fail border-fail/30",
};

const STATUS_LABEL: Record<StageStatus, string> = {
  done: "Done",
  running: "Running",
  pending: "Pending",
  blocked: "Blocked",
};

export function StatusChip({ status }: { status: StageStatus }) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium ${STATUS_STYLES[status]}`}
    >
      <span
        className={`h-1.5 w-1.5 rounded-full ${
          status === "done"
            ? "bg-ok"
            : status === "running"
            ? "bg-cyan-glow animate-pulse"
            : status === "blocked"
            ? "bg-fail"
            : "bg-muted"
        }`}
      />
      {STATUS_LABEL[status]}
    </span>
  );
}
