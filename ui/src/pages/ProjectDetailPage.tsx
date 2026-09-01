import { Link, useParams } from "react-router-dom";
import { ArrowRight, FlaskConical, Info, Microscope } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card } from "@/components/common/Card";
import { Stat } from "@/components/common/Stat";
import { StatusChip } from "@/components/common/StatusChip";
import { Resolved } from "./Resolved";
import {
  useCohorts,
  useProject,
  useRunStages,
  useSamples,
} from "@/hooks/useResults";

export function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>();
  const project = useProject();
  const samples = useSamples();
  const cohorts = useCohorts();
  const stages = useRunStages();

  const loading =
    project.isLoading || samples.isLoading || cohorts.isLoading || stages.isLoading;
  const error = project.error ?? samples.error ?? cohorts.error ?? stages.error;

  // If the requested id doesn't match the single mock project, still show it.
  const control = cohorts.data?.find((c) => c.condition === "control");
  const treatment = cohorts.data?.find((c) => c.condition === "treatment");

  return (
    <div>
      <PageHeader
        title="Project"
        subtitle={`${project.data?.accession ?? id} — demonstration project`}
      />
      <Resolved loading={loading} error={error}>
        {/* Header card */}
        <Card className="mb-6">
          <div className="mono text-2xl font-bold text-fg">
            {project.data?.accession}
          </div>
          <div className="mt-1 text-sm font-medium text-accent">
            {project.data?.name}
          </div>
          <div className="mono mt-1 text-xs text-fg-dim">
            {project.data?.organism} · {project.data?.designDescription}
          </div>
          <div className="mono mt-3 flex flex-wrap gap-x-6 gap-y-1 text-xs text-fg-dim">
            <span>Platform: {project.data?.platform}</span>
            <span>Layout: {project.data?.libraryLayout} 2×{project.data?.readLength}bp</span>
            <span>Reference: {project.data?.referenceGenome}</span>
          </div>
        </Card>

        {/* Condition split */}
        <div className="grid gap-6 lg:grid-cols-3">
          <Card title="Samples" icon={<Microscope className="h-4 w-4 text-accent" />} className="lg:col-span-2">
            <div className="mb-3 grid grid-cols-2 gap-3">
              <Stat label="Total samples" value={samples.data?.length ?? 0} />
              <Stat label="Paired-end reads" value={project.data?.libraryLayout === "PAIRED" ? "2 mates" : "1 mate"} />
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-lg border border-border bg-surface-2 p-3">
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-sm font-medium text-cyan-glow">
                    {control?.label ?? "Control"}
                  </span>
                  <span className="mono text-xs text-fg-dim">
                    n = {control?.sampleIds.length ?? 0}
                  </span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {control?.sampleIds.map((s) => (
                    <span key={s} className="mono rounded border border-border bg-bg px-2 py-0.5 text-xs text-fg">
                      {s}
                    </span>
                  ))}
                </div>
              </div>
              <div className="rounded-lg border border-border bg-surface-2 p-3">
                <div className="mb-2 flex items-center justify-between">
                  <span className="text-sm font-medium text-pink-400">
                    {treatment?.label ?? "Dexamethasone"}
                  </span>
                  <span className="mono text-xs text-fg-dim">
                    n = {treatment?.sampleIds.length ?? 0}
                  </span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {treatment?.sampleIds.map((s) => (
                    <span key={s} className="mono rounded border border-border bg-bg px-2 py-0.5 text-xs text-fg">
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </Card>

          {/* Pipeline status */}
          <Card title="Pipeline" icon={<Info className="h-4 w-4 text-accent" />}>
            <ul className="space-y-2">
              {stages.data?.map((s) => (
                <li
                  key={s.key}
                  className="flex items-center justify-between rounded-md border border-border bg-surface-2 px-3 py-2"
                >
                  <span className="text-sm text-fg">{s.label}</span>
                  <StatusChip status={s.status} />
                </li>
              ))}
            </ul>
          </Card>
        </div>

        {/* Quick actions */}
        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            to="/qc"
            className="inline-flex items-center gap-1.5 rounded-md border border-accent/50 bg-accent/10 px-4 py-2 text-sm font-medium text-accent hover:bg-accent/20"
          >
            <FlaskConical className="h-4 w-4" /> View QC <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            to="/differential-expression"
            className="inline-flex items-center gap-1.5 rounded-md border border-border bg-surface-2 px-4 py-2 text-sm font-medium text-fg hover:border-accent/50"
          >
            <Microscope className="h-4 w-4" /> View Results <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </Resolved>
    </div>
  );
}
