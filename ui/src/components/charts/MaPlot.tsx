import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import type { DeResult } from "@/types";

interface MaSeries {
  name: string;
  color: string;
  points: DeResult[];
}

/**
 * MA plot: mean abundance (baseMean) vs log2FC.
 * Same source/provenance separation as the volcano.
 */
export function MaPlot({
  source,
  demo,
  className,
}: {
  source: DeResult[];
  demo: DeResult[];
  className?: string;
}) {
  const toPoints = (arr: DeResult[]) =>
    arr.map((p) => ({
      x: Math.log10(p.baseMean + 1),
      y: p.log2FoldChange,
      ...p,
    }));

  const series: MaSeries[] = [
    { name: "Source-derived (reported)", color: "#2dd4bf", points: toPoints(source) },
    { name: "Synthetic demo (background)", color: "#475569", points: toPoints(demo) },
  ];

  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={360}>
        <ScatterChart margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
          <CartesianGrid stroke="#1e3044" strokeDasharray="3 3" />
          <XAxis
            type="number"
            dataKey="x"
            name="log10(baseMean)"
            stroke="#94a3b8"
            tick={{ fontSize: 11 }}
            label={{ value: "log10(mean normalized count)", position: "insideBottom", offset: -4, fill: "#94a3b8", fontSize: 11 }}
          />
          <YAxis
            type="number"
            dataKey="y"
            name="log2FC"
            stroke="#94a3b8"
            tick={{ fontSize: 11 }}
            label={{ value: "log2(FC)", angle: -90, position: "insideLeft", fill: "#94a3b8", fontSize: 11 }}
          />
          <Tooltip
            cursor={{ strokeDasharray: "3 3" }}
            content={({ active, payload }) => {
              if (!active || !payload?.length) return null;
              const d = payload[0].payload as DeResult;
              return (
                <div className="rounded-md border border-border bg-surface-2 px-3 py-2 text-xs">
                  <div className="mono font-semibold">{d.symbol ?? d.geneId}</div>
                  <div className="mono text-fg-dim">baseMean: {d.baseMean}</div>
                  <div className="mono text-fg-dim">log2FC: {d.log2FoldChange}</div>
                </div>
              );
            }}
          />
          {series.map((s) => (
            <Scatter key={s.name} name={s.name} data={s.points} fill={s.color} />
          ))}
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
