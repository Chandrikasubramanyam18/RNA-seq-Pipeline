import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

interface BarSeries {
  dataKey: string;
  name: string;
  color: string;
}

/**
 * Minimal grouped/stacked bar chart for QC distributions.
 */
export function QcBarChart({
  data,
  series,
  xKey,
  xLabel,
  yLabel,
  className,
}: {
  data: Record<string, number | string>[];
  series: BarSeries[];
  xKey: string;
  xLabel?: string;
  yLabel?: string;
  className?: string;
}) {
  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
          <CartesianGrid stroke="#1e3044" strokeDasharray="3 3" />
          <XAxis
            dataKey={xKey}
            stroke="#94a3b8"
            tick={{ fontSize: 11 }}
            label={
              xLabel
                ? { value: xLabel, position: "insideBottom", offset: -4, fill: "#94a3b8", fontSize: 11 }
                : undefined
            }
          />
          <YAxis
            stroke="#94a3b8"
            tick={{ fontSize: 11 }}
            label={
              yLabel
                ? { value: yLabel, angle: -90, position: "insideLeft", fill: "#94a3b8", fontSize: 11 }
                : undefined
            }
          />
          <Tooltip
            contentStyle={{
              background: "#0d1622",
              border: "1px solid #1e3044",
              borderRadius: 6,
              fontSize: 12,
            }}
          />
          {series.map((s) => (
            <Bar key={s.dataKey} dataKey={s.dataKey} name={s.name} fill={s.color} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
