import { FlaskConical } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card } from "@/components/common/Card";
import { Resolved } from "./Resolved";
import { QualityLineChart } from "@/components/charts/QualityLineChart";
import { QcBarChart } from "@/components/charts/QcBarChart";
import { SourceLegend } from "@/components/common/SourceLegend";
import { DataTable } from "@/components/tables/DataTable";
import {
  useMultiQcSummary,
  useQcMetrics,
} from "@/hooks/useResults";
import type { ColumnDef } from "@tanstack/react-table";
import type { MultiQcSummary } from "@/types";

export function QcPage() {
  const qc = useQcMetrics();
  const multi = useMultiQcSummary();

  const loading = qc.isLoading || multi.isLoading;
  const error = qc.error ?? multi.error;

  const retentionData = (qc.data ?? []).map((m) => ({
    sample: m.sampleId,
    "Adapter %": m.adapterContentPct,
  }));

  const gcData = (qc.data ?? []).map((m) => ({
    sample: m.sampleId,
    "GC %": m.gcPercent,
    "Duplication %": m.duplicationPct,
  }));

  const summaryColumns: ColumnDef<MultiQcSummary, unknown>[] = [
    { header: "Sample", accessorKey: "sampleId", cell: (c) => <span className="mono">{c.getValue<string>()}</span> },
    { header: "M Seqs", accessorKey: "milSeqs", cell: (c) => <span className="mono">{c.getValue<number>()}</span> },
    { header: "% GC", accessorKey: "pctGC", cell: (c) => <span className="mono">{c.getValue<number>().toFixed(1)}</span> },
    { header: "% Dups", accessorKey: "pctDups", cell: (c) => <span className="mono">{c.getValue<number>().toFixed(1)}</span> },
    {
      header: "Status",
      accessorKey: "status",
      cell: (c) => {
        const v = c.getValue<string>();
        const color = v === "PASS" ? "text-ok" : v === "WARN" ? "text-warn" : "text-fail";
        return <span className={`mono ${color}`}>{v}</span>;
      },
    },
  ];

  return (
    <div>
      <PageHeader
        title="Quality Control"
        subtitle="Read quality, GC, adapter, duplication and retention (demonstration values)"
        icon={<FlaskConical className="h-5 w-5" />}
      />
      <div className="mb-4">
        <SourceLegend />
      </div>

      <Resolved loading={loading} error={error}>
        <div className="grid gap-6 lg:grid-cols-2">
          <Card title="Read Quality (per base)" icon={<FlaskConical className="h-4 w-4 text-accent" />} className="lg:col-span-2">
            <QualityLineChart metrics={qc.data ?? []} />
          </Card>

          <Card title="GC Content & Duplication" icon={<FlaskConical className="h-4 w-4 text-accent" />}>
            <QcBarChart
              data={gcData}
              xKey="sample"
              xLabel="Sample"
              yLabel="Percent"
              series={[
                { dataKey: "GC %", name: "GC %", color: "#22d3ee" },
                { dataKey: "Duplication %", name: "Duplication %", color: "#475569" },
              ]}
            />
          </Card>

          <Card title="Adapter Content" icon={<FlaskConical className="h-4 w-4 text-accent" />}>
            <QcBarChart
              data={retentionData}
              xKey="sample"
              xLabel="Sample"
              yLabel="Percent"
              series={[{ dataKey: "Adapter %", name: "Adapter %", color: "#fbbf24" }]}
            />
          </Card>

          <Card title="MultiQC Summary" icon={<FlaskConical className="h-4 w-4 text-accent" />} className="lg:col-span-2">
            <DataTable columns={summaryColumns} data={multi.data ?? []} pageSize={6} />
          </Card>
        </div>
      </Resolved>
    </div>
  );
}
