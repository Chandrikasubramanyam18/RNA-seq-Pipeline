/**
 * Legend that makes the provenance distinction explicit on any chart or
 * table that mixes source-derived values with synthetic demo background.
 */
export function SourceLegend() {
  return (
    <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-fg-dim">
      <span className="inline-flex items-center gap-1.5">
        <span className="h-2.5 w-2.5 rounded-sm bg-accent" />
        <span className="text-ok">
          Source-derived
        </span>
        (reported study values)
      </span>
      <span className="inline-flex items-center gap-1.5">
        <span className="h-2.5 w-2.5 rounded-sm bg-muted" />
        <span className="text-muted">Synthetic demo</span>
        (generated background)
      </span>
    </div>
  );
}
