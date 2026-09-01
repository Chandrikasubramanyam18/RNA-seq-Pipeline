import { Activity } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card } from "@/components/common/Card";
import { Resolved } from "./Resolved";
import { DataTable } from "@/components/tables/DataTable";
import { useAlignmentStats } from "@/hooks/useResults";
import type { ColumnDef } from "@tanstack/react-table";
import type { AlignmentStats } from "@/types";

export function AlignmentPage() {
  const q = useAlignmentStats();

  const columns: ColumnDef<AlignmentStats, unknown>[] = [
    { header: "Sample", accessorKey: "sampleId", cell: (c) => <span className="mono">{c.getValue<string>()}</span> },
    { header: "Total reads", accessorKey: "totalReads", cell: (c) => <span className="mono">{c.getValue<number>().toLocaleString()}</span> },
    { header: "Uniquely mapped %", accessorKey: "uniquelyMappedPct", cell: (c) => <span className="mono text-ok">{c.getValue<number>().toFixed(1)}</span> },
    { header: "Multi-mapped %", accessorKey: "multiMappedPct", cell: (c) => <span className="mono">{c.getValue<number>().toFixed(1)}</span> },
    { header: "Unmapped %", accessorKey: "unmappedPct", cell: (c) => <span className="mono text-warn">{c.getValue<number>().toFixed(1)}</span> },
    { header: "Properly paired %", accessorKey: "properlyPairedPct", cell: (c) => <span className="mono">{c.getValue<number>().toFixed(1)}</span> },
  ];

  return (
    <div>
      <PageHeader
        title="Alignment"
        subtitle="STAR alignment statistics (demonstration values — pipeline not executed)"
        icon={<Activity className="h-5 w-5" />}
      />
      <Resolved loading={q.isLoading} error={q.error}>
        <Card>
          <DataTable columns={columns} data={q.data ?? []} pageSize={6} />
        </Card>
      </Resolved>
    </div>
  );
}
