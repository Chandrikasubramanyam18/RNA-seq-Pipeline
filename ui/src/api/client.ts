/**
 * FastAPI client for the Phase 3 backend.
 *
 * All functions return the API's camelCase payloads, which match the domain
 * contracts in `@/types` one-for-one, so consumers share the same shapes as
 * the Phase 2 mock data.
 */

import type {
  AlignmentStats,
  Cohort,
  DeResult,
  DeVisualData,
  MultiQcSummary,
  PathwayEnrichment,
  Project,
  Quantification,
  QcMetric,
  RunStage,
  Sample,
} from "@/types";

const API_BASE =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ??
  "http://127.0.0.1:8000/api/v1";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    throw new Error(`API ${res.status} for ${path}`);
  }
  return (await res.json()) as T;
}

/** Probe whether the backend is reachable. */
export async function isApiAvailable(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(2500) });
    return res.ok;
  } catch {
    return false;
  }
}

export const api = {
  project: (id: string) => get<Project>(`/projects/${id}`),
  projects: () => get<Project[]>("/projects"),
  samples: () => get<Sample[]>("/samples"),
  cohorts: () => get<Cohort[]>("/samples/cohorts"),
  qcMetrics: () => get<QcMetric[]>("/qc/metrics"),
  multiQc: () => get<MultiQcSummary[]>("/qc/multiqc"),
  alignment: () => get<AlignmentStats[]>("/alignment"),
  quantification: () => get<Quantification[]>("/quantification"),
  deResults: () => get<DeResult[]>("/de/results"),
  deVisual: () => get<DeVisualData>("/de/visual"),
  pathways: () => get<PathwayEnrichment[]>("/pathways"),
  stages: () => get<RunStage[]>("/stages"),
};
