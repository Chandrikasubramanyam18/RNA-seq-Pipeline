import { FileText, Download } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card } from "@/components/common/Card";
import { Resolved } from "./Resolved";
import { useProject } from "@/hooks/useResults";

const REPORT_ROWS = [
  { label: "Project overview", id: "overview", note: "GSE52778 metadata" },
  { label: "Quality control", id: "qc", note: "Demonstration QC values" },
  { label: "Alignment stats", id: "alignment", note: "Demonstration values" },
  { label: "Differential expression", id: "de", note: "Source-derived genes + demo background" },
  { label: "Pathway enrichment", id: "pathways", note: "Demo enrichment terms" },
];

export function ReportsPage() {
  const project = useProject();
  return (
    <div>
      <PageHeader
        title="Reports"
        subtitle="Available report artifacts (demonstration — nothing exported to real files)"
        icon={<FileText className="h-5 w-5" />}
      />
      <Resolved loading={project.isLoading} error={project.error}>
        <Card>
          <ul className="divide-y divide-border">
            {REPORT_ROWS.map((r) => (
              <li key={r.id} className="flex items-center justify-between py-3">
                <div>
                  <div className="text-sm font-medium text-fg">{r.label}</div>
                  <div className="mono text-xs text-fg-dim">{r.note}</div>
                </div>
                <button
                  disabled
                  className="inline-flex items-center gap-1.5 rounded-md border border-border bg-surface-2 px-3 py-1.5 text-xs text-fg-dim"
                  title="Not available in demo build"
                >
                  <Download className="h-3.5 w-3.5" /> Export (demo)
                </button>
              </li>
            ))}
          </ul>
          <p className="mono mt-3 text-xs text-warn">
            Export is disabled — this is a read-only demonstration UI.
          </p>
        </Card>
      </Resolved>
    </div>
  );
}
