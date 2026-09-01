import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ZAxis,
} from "recharts";
import type { DeResult } from "@/types";

interface VolcanoSeries {
  name: string;
  color: string;
  points: DeResult[];
}

/**
 * Volcano plot: log2FC (x) vs -log10(padj) (y).
 * Source-derived points and synthetic demo points are drawn as
 * separate, explicitly-coloured series so they cannot be conflated.
 */
export function VolcanoPlot({
  source,
  demo,
  className,
}: {
  source: DeResult[];
  demo: DeResult[];
  className?: string;
}) {
  const sourcePoints = source.map((p) => ({
    x: p.log2FoldChange,
    y: -Math.log10(Math.max(p.padj, 1e-30)),
    ...p,
  }));
  const demoPoints = demo.map((p) => ({
    x: p.log2FoldChange,
    y: -Math.log10(Math.max(p.padj, 1e-30)),
    ...p,
  }));

  const series: VolcanoSeries[] = [
    { name: "Source-derived (reported)", color: "#2dd4bf", points: sourcePoints },
    { name: "Synthetic demo (background)", color: "#475569", points: demoPoints },
  ];

  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={360}>
        <ScatterChart margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
          <CartesianGrid stroke="#1e3044" strokeDasharray="3 3" />
          <XAxis
            type="number"
            dataKey="x"
            name="log2FC"
            stroke="#94a3b8"
            tick={{ fontSize: 11 }}
            label={{ value: "log2(FC) treatment/control", position: "insideBottom", offset: -4, fill: "#94a3b8", fontSize: 11 }}
          />
          <YAxis
            type="number"
            dataKey="y"
            name="-log10(padj)"
            stroke="#94a3b8"
            tick={{ fontSize: 11 }}
            label={{ value: "-log10(padj)", angle: -90, position: "insideLeft", fill: "#94a3b8", fontSize: 11 }}
          />
          <ZAxis range={[30, 60]} />
          <Tooltip
            cursor={{ strokeDasharray: "3 3" }}
            content={({ active, payload }) => {
              if (!active || !payload?.length) return null;
              const d = payload[0].payload as DeResult;
              return (
                <div className="rounded-md border border-border bg-surface-2 px-3 py-2 text-xs">
                  <div className="mono font-semibold">{d.symbol ?? d.geneId}</div>
                  <div className="mono text-fg-dim">log2FC: {d.log2FoldChange}</div>
                  <div className="mono text-fg-dim">padj: {d.padj.toExponential(2)}</div>
                </div>
              );
            }}
          />
          <ReferenceLine x={0} stroke="#334155" />
          <ReferenceLine y={-Math.log10(0.05)} stroke="#334155" strokeDasharray="4 4" />
          <ReferenceLine x={1} stroke="#334155" strokeDasharray="4 4" />
          <ReferenceLine x={-1} stroke="#334155" strokeDasharray="4 4" />
          {series.map((s) => (
            <Scatter key={s.name} name={s.name} data={s.points} fill={s.color} />
          ))}
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
