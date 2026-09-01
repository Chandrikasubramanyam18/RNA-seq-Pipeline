import { Microscope } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card } from "@/components/common/Card";
import { Resolved } from "./Resolved";
import { DataTable } from "@/components/tables/DataTable";
import { useQuantification } from "@/hooks/useResults";
import type { ColumnDef } from "@tanstack/react-table";
import type { Quantification } from "@/types";

export function ExpressionPage() {
  const q = useQuantification();

  const columns: ColumnDef<Quantification, unknown>[] = [
    { header: "Sample", accessorKey: "sampleId", cell: (c) => <span className="mono">{c.getValue<string>()}</span> },
    { header: "Method", accessorKey: "method", cell: (c) => <span className="mono text-accent">{c.getValue<string>()}</span> },
    { header: "Gene", accessorKey: "symbol", cell: (c) => <span className="mono font-medium">{c.getValue<string>() ?? c.row.original.geneId}</span> },
    { header: "TPM", accessorKey: "tpm", cell: (c) => (c.getValue<number>() != null ? <span className="mono">{c.getValue<number>().toFixed(1)}</span> : <span className="text-fg-dim">—</span>) },
    { header: "Counts", accessorKey: "counts", cell: (c) => (c.getValue<number>() != null ? <span className="mono">{c.getValue<number>()}</span> : <span className="text-fg-dim">—</span>) },
  ];

  return (
    <div>
      <PageHeader
        title="Expression"
        subtitle="Quantification (Salmon TPM / featureCounts counts) — demonstration values"
        icon={<Microscope className="h-5 w-5" />}
      />
      <Resolved loading={q.isLoading} error={q.error}>
        <Card>
          <DataTable columns={columns} data={q.data ?? []} pageSize={10} />
        </Card>
      </Resolved>
    </div>
  );
}
