import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import type { QcMetric } from "@/types";

/**
 * Per-base (per-cycle) mean Phred quality lines for one or more samples.
 */
export function QualityLineChart({
  metrics,
  className,
}: {
  metrics: QcMetric[];
  className?: string;
}) {
  // Build series per sample, keyed by position.
  const positions = metrics[0]?.perBaseQuality.map((p) => p.position) ?? [];
  const combined = positions.map((position, i) => {
    const row: Record<string, number | string> = { position };
    for (const m of metrics) {
      const p = m.perBaseQuality[i];
      if (p) row[m.sampleId] = p.meanQ;
    }
    return row;
  });

  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={combined} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
          <CartesianGrid stroke="#1e3044" strokeDasharray="3 3" />
          <XAxis
            dataKey="position"
            stroke="#94a3b8"
            tick={{ fontSize: 11 }}
            label={{ value: "Position (cycle)", position: "insideBottom", offset: -4, fill: "#94a3b8", fontSize: 11 }}
          />
          <YAxis
            stroke="#94a3b8"
            tick={{ fontSize: 11 }}
            domain={[20, 40]}
            label={{ value: "Mean Phred", angle: -90, position: "insideLeft", fill: "#94a3b8", fontSize: 11 }}
          />
          <Tooltip
            contentStyle={{
              background: "#0d1622",
              border: "1px solid #1e3044",
              borderRadius: 6,
              fontSize: 12,
            }}
          />
          <Legend wrapperStyle={{ fontSize: 12 }} />
          {metrics.map((m, i) => (
            <Line
              key={m.sampleId}
              type="monotone"
              dataKey={m.sampleId}
              stroke={i % 2 === 0 ? "#2dd4bf" : "#22d3ee"}
              dot={false}
              strokeWidth={1.5}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
