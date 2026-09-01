import { Link } from "react-router-dom";
import {
  Activity,
  ArrowRight,
  Dna,
  Folder,
  FlaskConical,
  Microscope,
  Sigma,
} from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card } from "@/components/common/Card";
import { Stat } from "@/components/common/Stat";
import { StatusChip } from "@/components/common/StatusChip";
import { Resolved } from "./Resolved";
import {
  useCohorts,
  useProject,
  useQcMetrics,
  useRunStages,
  useSamples,
} from "@/hooks/useResults";

const QUICK_LINKS = [
  { to: "/qc", label: "Quality Control", icon: FlaskConical },
  { to: "/alignment", label: "Alignment", icon: Activity },
  { to: "/expression", label: "Expression", icon: Microscope },
  { to: "/differential-expression", label: "Differential Expression", icon: Sigma },
  { to: "/pathways", label: "Pathways", icon: Dna },
  { to: "/reports", label: "Reports", icon: Folder },
];

export function DashboardPage() {
  const project = useProject();
  const samples = useSamples();
  const cohorts = useCohorts();
  const qc = useQcMetrics();
  const stages = useRunStages();

  const loading =
    project.isLoading || samples.isLoading || cohorts.isLoading || qc.isLoading;
  const error = project.error ?? samples.error ?? cohorts.error ?? qc.error;

  const totalReads =
    qc.data?.reduce((sum, m) => sum + m.totalReads, 0) ?? 0;

  return (
    <div>
      <PageHeader
        title="Dashboard"
        subtitle="Read-only overview of the GSE52778 demonstration project"
      />

      <Resolved loading={loading} error={error}>
        <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
          <Stat label="Project" value={project.data?.accession ?? "—"} accent icon={<Folder className="h-3.5 w-3.5" />} />
          <Stat label="Samples" value={samples.data?.length ?? 0} icon={<Microscope className="h-3.5 w-3.5" />} />
          <Stat label="Conditions" value={cohorts.data?.length ?? 0} icon={<Sigma className="h-3.5 w-3.5" />} />
          <Stat label="Best Q30" value={`${qc.data?.[0]?.q30Rate.toFixed(1) ?? 0}%`} icon={<Activity className="h-3.5 w-3.5" />} />
        </div>

        <div className="mt-6 grid gap-6 lg:grid-cols-3">
          {/* Pipeline status card */}
          <Card
            title="Pipeline"
            icon={<Activity className="h-4 w-4 text-accent" />}
            className="lg:col-span-2"
          >
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

          {/* Entry CTAs */}
          <Card
            title="Explore"
            icon={<Dna className="h-4 w-4 text-accent" />}
          >
            <div className="space-y-2">
              {QUICK_LINKS.map(({ to, label, icon: Icon }) => (
                <Link
                  key={to}
                  to={to}
                  className="group flex items-center justify-between rounded-md border border-border bg-surface-2 px-3 py-2 text-sm text-fg transition-colors hover:border-accent/50"
                >
                  <span className="inline-flex items-center gap-2">
                    <Icon className="h-4 w-4 text-fg-dim" />
                    {label}
                  </span>
                  <ArrowRight className="h-4 w-4 text-fg-dim transition-transform group-hover:translate-x-0.5 group-hover:text-accent" />
                </Link>
              ))}
            </div>
          </Card>

          {/* Study summary */}
          <Card
            title="Project"
            icon={<Folder className="h-4 w-4 text-accent" />}
            className="lg:col-span-3"
          >
            <p className="text-sm text-fg">{project.data?.title}</p>
            <div className="mono mt-3 grid gap-2 text-xs text-fg-dim sm:grid-cols-3">
              <div>Organism: {project.data?.organism}</div>
              <div>Platform: {project.data?.platform}</div>
              <div>Reads: {project.data?.libraryLayout} 2×{project.data?.readLength}bp</div>
              <div>Reference: {project.data?.referenceGenome}</div>
              <div>Annotation: {project.data?.annotationSource}</div>
              <div>{totalReads.toLocaleString()} total reads (demo)</div>
            </div>
          </Card>
        </div>
      </Resolved>
    </div>
  );
}
