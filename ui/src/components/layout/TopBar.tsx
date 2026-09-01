import { CircleDot } from "lucide-react";
import { useProject } from "@/hooks/useResults";

/**
 * Top bar showing the active project context and demo/tooling status.
 */
export function TopBar() {
  const { data: project } = useProject();
  return (
    <div className="flex w-full items-center justify-between">
      <div className="flex items-center gap-2">
        <CircleDot className="h-4 w-4 text-accent" />
        <span className="mono text-sm text-fg">
          {project ? project.accession : "—"}
        </span>
        <span className="hidden text-sm text-fg-dim sm:inline">
          {project ? `• ${project.name}` : ""}
        </span>
      </div>
      <span className="mono inline-flex items-center gap-1.5 rounded-full border border-border bg-surface-2 px-2.5 py-0.5 text-[11px] text-fg-dim">
        <span className="h-1.5 w-1.5 rounded-full bg-warn" />
        v0.1 · demo build
      </span>
    </div>
  );
}
