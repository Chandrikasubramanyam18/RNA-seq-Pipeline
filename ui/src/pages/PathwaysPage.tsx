import { Dna } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card } from "@/components/common/Card";
import { SourceLegend } from "@/components/common/SourceLegend";
import { Resolved } from "./Resolved";
import { DataTable } from "@/components/tables/DataTable";
import { usePathways } from "@/hooks/useResults";
import type { ColumnDef } from "@tanstack/react-table";
import type { PathwayEnrichment } from "@/types";

function SourceBadge({ source }: { source: PathwayEnrichment["dataSource"] }) {
  return source === "source_derived" ? (
    <span className="mono uppercase text-ok">source</span>
  ) : (
    <span className="mono uppercase text-muted">demo</span>
  );
}

export function PathwaysPage() {
  const q = usePathways();

  const columns: ColumnDef<PathwayEnrichment, unknown>[] = [
    { header: "ID", accessorKey: "id", cell: (c) => <span className="mono text-accent">{c.getValue<string>()}</span> },
    { header: "Source", accessorKey: "source", cell: (c) => <span className="mono">{c.getValue<string>()}</span> },
    { header: "Term", accessorKey: "term", cell: (c) => <span className="text-fg">{c.getValue<string>()}</span> },
    {
      header: "Genes",
      accessorKey: "genes",
      cell: (c) => (
        <span className="mono flex flex-wrap gap-1">
          {(c.getValue<string[]>() ?? []).map((g) => (
            <span key={g} className="rounded border border-border bg-surface-2 px-1.5 py-0.5 text-xs text-fg-dim">
              {g}
            </span>
          ))}
        </span>
      ),
    },
    { header: "pvalue", accessorKey: "pvalue", cell: (c) => <span className="mono">{c.getValue<number>().toExponential(1)}</span> },
    { header: "padj", accessorKey: "padj", cell: (c) => <span className="mono">{c.getValue<number>().toExponential(1)}</span> },
    { header: "Src", accessorKey: "dataSource", cell: (c) => <SourceBadge source={c.getValue<PathwayEnrichment["dataSource"]>()} /> },
  ];

  return (
    <div>
      <PageHeader
        title="Pathways"
        subtitle="Functional / GO / KEGG / Reactome enrichment (demonstration values)"
        icon={<Dna className="h-5 w-5" />}
      />
      <div className="mb-4">
        <SourceLegend />
      </div>
      <Resolved loading={q.isLoading} error={q.error}>
        <Card>
          <DataTable columns={columns} data={q.data ?? []} pageSize={10} />
        </Card>
      </Resolved>
    </div>
  );
}
