import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ZAxis,
} from "recharts";
import type { PcaAxisInfo, PcaPoint } from "@/types";

/**
 * PCA scatter: PC1 (x) vs PC2 (y), coloured by condition.
 */
export function PCAPlot({
  points,
  axis1,
  axis2,
  className,
}: {
  points: PcaPoint[];
  axis1: PcaAxisInfo;
  axis2: PcaAxisInfo;
  className?: string;
}) {
  const data = points.map((p) => ({ x: p.pc1, y: p.pc2, ...p }));

  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={360}>
        <ScatterChart margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
          <CartesianGrid stroke="#1e3044" strokeDasharray="3 3" />
          <XAxis
            type="number"
            dataKey="x"
            name="PC1"
            stroke="#94a3b8"
            tick={{ fontSize: 11 }}
            label={{
              value: `${axis1.label} (${(axis1.varianceExplained * 100).toFixed(1)}%)`,
              position: "insideBottom",
              offset: -4,
              fill: "#94a3b8",
              fontSize: 11,
            }}
          />
          <YAxis
            type="number"
            dataKey="y"
            name="PC2"
            stroke="#94a3b8"
            tick={{ fontSize: 11 }}
            label={{
              value: `${axis2.label} (${(axis2.varianceExplained * 100).toFixed(1)}%)`,
              angle: -90,
              position: "insideLeft",
              fill: "#94a3b8",
              fontSize: 11,
            }}
          />
          <ZAxis range={[60, 80]} />
          <Tooltip
            cursor={{ strokeDasharray: "3 3" }}
            content={({ active, payload }) => {
              if (!active || !payload?.length) return null;
              const d = payload[0].payload as PcaPoint;
              return (
                <div className="rounded-md border border-border bg-surface-2 px-3 py-2 text-xs">
                  <div className="mono font-semibold">{d.sampleId}</div>
                  <div className="mono text-fg-dim">condition: {d.condition}</div>
                </div>
              );
            }}
          />
          <Legend wrapperStyle={{ fontSize: 12 }} />
          <Scatter name="Control" data={data.filter((d) => d.condition === "control")} fill="#22d3ee" />
          <Scatter name="Treatment" data={data.filter((d) => d.condition === "treatment")} fill="#f472b6" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
