import type { ReactNode } from "react";

export interface HeatmapRow {
  label: string;
  /** One Z-score per column, in the same order as `columns`. */
  values: number[];
}

export interface HeatmapColumn {
  id: string;
  label: string;
}

/** Map a Z-score to a teal/neutral/pink colour. */
function zColor(z: number): string {
  const clamped = Math.max(-2, Math.min(2, z));
  const t = (clamped + 2) / 4; // 0..1
  // Low (-2) = blue/teal, middle (0) = dark neutral, high (+2) = pink
  const low = [13, 148, 136]; // teal-600
  const mid = [30, 48, 68]; // slate-800
  const high = [244, 114, 182]; // pink-400
  let r: number, g: number, b: number;
  if (t < 0.5) {
    const u = t * 2;
    r = Math.round(low[0] + (mid[0] - low[0]) * u);
    g = Math.round(low[1] + (mid[1] - low[1]) * u);
    b = Math.round(low[2] + (mid[2] - low[2]) * u);
  } else {
    const u = (t - 0.5) * 2;
    r = Math.round(mid[0] + (high[0] - mid[0]) * u);
    g = Math.round(mid[1] + (high[1] - mid[1]) * u);
    b = Math.round(mid[2] + (high[2] - mid[2]) * u);
  }
  return `rgb(${r}, ${g}, ${b})`;
}

/**
 * Clustered-style heatmap rendered as a CSS grid. Rows = genes,
 * columns = samples, cells coloured by Z-score.
 */
export function Heatmap({
  rows,
  columns,
  footer,
  className,
}: {
  rows: HeatmapRow[];
  columns: HeatmapColumn[];
  footer?: ReactNode;
  className?: string;
}) {
  return (
    <div className={`overflow-x-auto ${className ?? ""}`}>
      <div className="inline-block min-w-full">
        {/* Header row: gene labels + sample columns */}
        <div
          className="grid gap-px"
          style={{
            gridTemplateColumns: `140px repeat(${columns.length}, minmax(56px, 1fr))`,
          }}
        >
          <div />
          {columns.map((c) => (
            <div
              key={c.id}
              className="mono truncate text-center text-xs text-fg-dim"
              title={c.label}
            >
              {c.label}
            </div>
          ))}
        </div>

        {/* Matrix rows */}
        <div className="mt-1 space-y-px">
          {rows.map((row) => (
            <div
              key={row.label}
              className="grid gap-px"
              style={{
                gridTemplateColumns: `140px repeat(${columns.length}, minmax(56px, 1fr))`,
              }}
            >
              <div className="mono flex items-center truncate pr-2 text-xs text-fg">
                {row.label}
              </div>
              {row.values.map((z, ci) => (
                <div
                  key={ci}
                  className="flex h-7 items-center justify-center"
                  style={{ backgroundColor: zColor(z) }}
                  title={`${row.label} · ${columns[ci]?.label ?? ""} · Z=${z.toFixed(2)}`}
                >
                  <span className="mono text-[10px] text-fg/70">
                    {z.toFixed(1)}
                  </span>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
      {footer}
    </div>
  );
}
