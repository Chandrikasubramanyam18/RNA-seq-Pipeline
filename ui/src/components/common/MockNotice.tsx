import { FlaskConical } from "lucide-react";

/**
 * Persistent, project-wide banner flagging that all data is
 * demonstration (mock) data. Rendered high in the layout so it cannot
 * be mistaken for real pipeline output.
 */
export function MockNotice() {
  return (
    <div
      className="flex items-center gap-2 border-b border-warn/40 bg-warn/10 px-4 py-1.5 text-xs font-medium text-warn"
      role="status"
      aria-label="Demonstration data notice"
    >
      <FlaskConical className="h-3.5 w-3.5 shrink-0" />
      <span>
        <strong>DEMONSTRATION DATA</strong> — mock values for UI evaluation
        only. The analysis pipeline has not been executed; nothing on this
        screen is a real experimental result.
      </span>
    </div>
  );
}
