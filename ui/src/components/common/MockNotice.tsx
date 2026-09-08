import { FlaskConical } from "lucide-react";
import { useProject } from "../../hooks/useResults";

/**
 * Persistent, project-wide banner explaining the data provenance.
 *
 * Semantic split (locked):
 *  - executionReal=true  -> every number shown is source-derived from real
 *    tool artifacts on disk (FastQC/fastp/STAR/featureCounts/DESeq2/
 *    clusterProfiler) executed at tutorial scale.
 *  - isMock=true         -> it is NOT publication/full biological analysis
 *    (a 3-gene mini-reference, single DEG, zero enriched terms), so it must
 *    not be presented as genome-wide published results.
 */
export function MockNotice() {
  const query = useProject();
  const project = query.data;
  const isReal = project?.executionReal ?? false;
  const scope = project?.analysisScope ?? "tutorial_mini_reference";
  return (
    <div
      className="flex items-center gap-2 border-b border-warn/40 bg-warn/10 px-4 py-1.5 text-xs font-medium text-warn"
      role="status"
      aria-label="Real execution tutorial-scale notice"
    >
      <FlaskConical className="h-3.5 w-3.5 shrink-0" />
      <span>
        {isReal ? (
          <>
            <strong>REAL EXECUTION — TUTORIAL SCALE</strong> — every value on
            this screen is source-derived from real pipeline artifacts
            (scope <code>{scope}</code>). This is NOT publication/full
            biological analysis: the known reference contains only 3 genes and
            enrichment is expected to be zero.
          </>
        ) : (
          <>
            <strong>DEMONSTRATION DATA</strong> — mock values for UI evaluation
            only. The analysis pipeline has not been executed; nothing on this
            screen is a real experimental result.
          </>
        )}
      </span>
    </div>
  );
}