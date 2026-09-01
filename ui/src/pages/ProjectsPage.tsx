import { Link } from "react-router-dom";
import { ArrowRight, Folder } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card } from "@/components/common/Card";
import { Resolved } from "./Resolved";
import { useProject } from "@/hooks/useResults";

export function ProjectsPage() {
  const project = useProject();
  return (
    <div>
      <PageHeader title="Projects" subtitle="Select a demonstration project" />
      <Resolved loading={project.isLoading} error={project.error}>
        {project.data && (
          <Card className="max-w-2xl">
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <Folder className="h-8 w-8 text-accent" />
                <div>
                  <div className="mono text-sm font-semibold text-fg">
                    {project.data.accession}
                  </div>
                  <div className="text-sm text-fg">{project.data.name}</div>
                  <div className="mono mt-0.5 text-xs text-fg-dim">
                    {project.data.organism} · {project.data.designDescription}
                  </div>
                </div>
              </div>
              <Link
                to={`/projects/${project.data.id}`}
                className="inline-flex items-center gap-1.5 rounded-md border border-accent/50 bg-accent/10 px-3 py-1.5 text-sm text-accent hover:bg-accent/20"
              >
                Open <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </Card>
        )}
      </Resolved>
    </div>
  );
}
