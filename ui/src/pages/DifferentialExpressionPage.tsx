import { useState } from "react";
import { Sigma } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card } from "@/components/common/Card";
import { Tabs } from "@/components/common/Tabs";
import { SourceLegend } from "@/components/common/SourceLegend";
import { Resolved } from "./Resolved";
import { PCAPlot } from "@/components/charts/PCAPlot";
import { VolcanoPlot } from "@/components/charts/VolcanoPlot";
import { MaPlot } from "@/components/charts/MaPlot";
import { Heatmap, type HeatmapRow } from "@/components/charts/Heatmap";
import { DataTable } from "@/components/tables/DataTable";
import { useDeResults, useDeVisualData } from "@/hooks/useResults";
import type { ColumnDef } from "@tanstack/react-table";
import type { DeResult } from "@/types";

/** Per-gene normalized counts (control then treatment), demo-only. */
const HEATMAP_NORM: Record<string, number[]> = {
  FKBP5: [190, 178, 208, 1405, 1366, 1445],
  CRISPLD2: [420, 390, 450, 2450, 2380, 2510],
  DUSP1: [610, 580, 640, 2600, 2480, 2710],
  KLF15: [210, 195, 230, 920, 880, 950],
  SPARCL1: [1800, 1750, 1920, 420, 390, 450],
  EGR1: [1450, 1380, 1510, 380, 360, 410],
};

const HEATMAP_COLUMNS = [
  { id: "C1", label: "C1" },
  { id: "C2", label: "C2" },
  { id: "C3", label: "C3" },
  { id: "T1", label: "T1" },
  { id: "T2", label: "T2" },
  { id: "T3", label: "T3" },
];

function zScoreRow(values: number[]): number[] {
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const sd = Math.sqrt(values.reduce((a, b) => a + (b - mean) ** 2, 0) / values.length) || 1;
  return values.map((v) => (v - mean) / sd);
}

type TabKey = "pca" | "volcano" | "ma" | "heatmap" | "table";

function SourceBadge({ source }: { source: DeResult["dataSource"] }) {
  return source === "source_derived" ? (
    <span className="mono uppercase text-ok">source</span>
  ) : (
    <span className="mono uppercase text-muted">demo</span>
  );
}

export function DifferentialExpressionPage() {
  const de = useDeResults();
  const vis = useDeVisualData();
  const [tab, setTab] = useState<TabKey>("pca");

  const loading = de.isLoading || vis.isLoading;
  const error = de.error ?? vis.error;

  const demoDe = de.data?.filter((d) => d.dataSource === "synthetic_demo") ?? [];
  const sourceDe = de.data?.filter((d) => d.dataSource === "source_derived") ?? [];

  const heatmapRows: HeatmapRow[] = Object.entries(HEATMAP_NORM).map(
    ([gene, vals]) => ({
      label: gene,
      values: zScoreRow(vals),
    })
  );

  const columns: ColumnDef<DeResult, unknown>[] = [
    { header: "Gene", accessorKey: "symbol", cell: (c) => <span className="mono font-medium">{c.getValue<string>() ?? c.row.original.geneId}</span> },
    { header: "baseMean", accessorKey: "baseMean", cell: (c) => <span className="mono">{c.getValue<number>().toLocaleString()}</span> },
    {
      header: "log2FC",
      accessorKey: "log2FoldChange",
      cell: (c) => {
        const v = c.getValue<number>();
        const color = v > 0 ? "text-ok" : v < 0 ? "text-fail" : "text-fg-dim";
        return <span className={`mono ${color}`}>{v.toFixed(2)}</span>;
      },
    },
    {
      header: "padj",
      accessorKey: "padj",
      cell: (c) => <span className="mono">{c.getValue<number>().toExponential(1)}</span>,
    },
    {
      header: "Sig",
      accessorKey: "significant",
      cell: (c) =>
        c.getValue<boolean>() ? (
          <span className="mono text-ok">YES</span>
        ) : (
          <span className="mono text-muted">no</span>
        ),
    },
    { header: "Src", accessorKey: "dataSource", cell: (c) => <SourceBadge source={c.getValue<DeResult["dataSource"]>()} /> },
  ];

  return (
    <div>
      <PageHeader
        title="Differential Expression"
        subtitle="PCA, volcano, MA, heatmap and DE table — source-derived genes + synthetic demo background"
        icon={<Sigma className="h-5 w-5" />}
      />
      <div className="mb-4">
        <SourceLegend />
      </div>

      <Resolved loading={loading} error={error}>
        <Card>
          <Tabs<TabKey>
            tabs={[
              { key: "pca", label: "PCA" },
              { key: "volcano", label: "Volcano" },
              { key: "ma", label: "MA Plot" },
              { key: "heatmap", label: "Heatmap" },
              { key: "table", label: "DE Table" },
            ]}
            active={tab}
            onChange={setTab}
          />

          <div className="pt-4">
            {tab === "pca" && vis.data && (
              <PCAPlot
                points={vis.data.pca}
                axis1={vis.data.pcaAxis1}
                axis2={vis.data.pcaAxis2}
              />
            )}

            {tab === "volcano" && (
              <VolcanoPlot source={sourceDe} demo={demoDe} />
            )}

            {tab === "ma" && (
              <MaPlot source={sourceDe} demo={demoDe} />
            )}

            {tab === "heatmap" && (
              <Heatmap
                rows={heatmapRows}
                columns={HEATMAP_COLUMNS}
                footer={
                  <p className="mono mt-3 text-xs text-fg-dim">
                    Rows Z-scored per gene. Control (C1–C3) vs Dexamethasone (T1–T3) — demo heatmap.
                  </p>
                }
              />
            )}

            {tab === "table" && (
              <DataTable columns={columns} data={de.data ?? []} pageSize={10} />
            )}
          </div>
        </Card>
      </Resolved>
    </div>
  );
}
