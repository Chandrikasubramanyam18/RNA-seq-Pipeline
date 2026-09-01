/**
 * Query layer backing the UI.
 *
 * Each hook resolves from the Phase 3 FastAPI backend when it is reachable,
 * otherwise falls back to the Phase 2 mock dataset. Both sources share the
 * same typed contracts, so the pages never need to know which is in use.
 *
 * Provenance note: the project's `isMock` flag is always taken from the data
 * source (the API serves `isMock: true` because the full pipeline has not run
 * against the raw data); it is never invented on the client.
 */

import { useQuery, type UseQueryResult } from "@tanstack/react-query";
import { api, isApiAvailable } from "@/api/client";
import {
  alignmentStats,
  cohorts,
  datasetMetadata,
  deVisualData,
  mockProject,
  multiQcSummary,
  pathwayEnrichment,
  qcMetrics,
  quantification,
  runStages,
  samples,
  sourceDerivedDe,
} from "@/data/mockData";
import type {
  AlignmentStats,
  Cohort,
  Dataset,
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

/** Cache the backend availability probe so it only runs once per session. */
let availability: Promise<boolean> | null = null;
function apiAvailable(): Promise<boolean> {
  if (availability === null) availability = isApiAvailable();
  return availability;
}

/** Synthetic latency so loading states are observable (mock fallback path). */
function mockDelay(value: unknown): Promise<unknown> {
  return new Promise((resolve) => setTimeout(() => resolve(value), 150));
}

/** Try the live API; on any failure (or if the backend is down) use mock. */
async function resolve<T>(live: () => Promise<T>, fallback: T): Promise<T> {
  try {
    if (await apiAvailable()) {
      return await live();
    }
  } catch {
    // Backend reachable but errored — fall through to mock.
  }
  return (await mockDelay(fallback)) as T;
}

export function useProject(): UseQueryResult<Project, Error> {
  return useQuery<Project, Error>({
    queryKey: ["project"],
    queryFn: () => resolve(() => api.project("gse52778"), mockProject),
    staleTime: Infinity,
  });
}

export function useDataset(): UseQueryResult<Dataset, Error> {
  return useQuery<Dataset, Error>({
    queryKey: ["dataset"],
    queryFn: () => resolve(() => api.project("gse52778"), datasetMetadata),
    staleTime: Infinity,
  });
}

export function useSamples(): UseQueryResult<Sample[], Error> {
  return useQuery<Sample[], Error>({
    queryKey: ["samples"],
    queryFn: () => resolve(() => api.samples(), samples),
    staleTime: Infinity,
  });
}

export function useCohorts(): UseQueryResult<Cohort[], Error> {
  return useQuery<Cohort[], Error>({
    queryKey: ["cohorts"],
    queryFn: () => resolve(() => api.cohorts(), cohorts),
    staleTime: Infinity,
  });
}

export function useRunStages(): UseQueryResult<RunStage[], Error> {
  return useQuery<RunStage[], Error>({
    queryKey: ["run-stages"],
    queryFn: () => resolve(() => api.stages(), runStages),
    staleTime: Infinity,
  });
}

export function useQcMetrics(): UseQueryResult<QcMetric[], Error> {
  return useQuery<QcMetric[], Error>({
    queryKey: ["qc-metrics"],
    queryFn: () => resolve(() => api.qcMetrics(), qcMetrics),
    staleTime: Infinity,
  });
}

export function useMultiQcSummary(): UseQueryResult<MultiQcSummary[], Error> {
  return useQuery<MultiQcSummary[], Error>({
    queryKey: ["multiqc-summary"],
    queryFn: () => resolve(() => api.multiQc(), multiQcSummary),
    staleTime: Infinity,
  });
}

export function useAlignmentStats(): UseQueryResult<AlignmentStats[], Error> {
  return useQuery<AlignmentStats[], Error>({
    queryKey: ["alignment-stats"],
    queryFn: () => resolve(() => api.alignment(), alignmentStats),
    staleTime: Infinity,
  });
}

export function useQuantification(): UseQueryResult<Quantification[], Error> {
  return useQuery<Quantification[], Error>({
    queryKey: ["quantification"],
    queryFn: () => resolve(() => api.quantification(), quantification),
    staleTime: Infinity,
  });
}

export function useDeResults(): UseQueryResult<DeResult[], Error> {
  return useQuery<DeResult[], Error>({
    queryKey: ["de-results"],
    queryFn: () =>
      resolve(
        () => api.deResults(),
        [...sourceDerivedDe, ...deVisualData.volcano.filter((d) => d.dataSource === "synthetic_demo")]
      ),
    staleTime: Infinity,
  });
}

export function useDeVisualData(): UseQueryResult<DeVisualData, Error> {
  return useQuery<DeVisualData, Error>({
    queryKey: ["de-visual-data"],
    queryFn: () => resolve(() => api.deVisual(), deVisualData),
    staleTime: Infinity,
  });
}

export function usePathways(): UseQueryResult<PathwayEnrichment[], Error> {
  return useQuery<PathwayEnrichment[], Error>({
    queryKey: ["pathways"],
    queryFn: () => resolve(() => api.pathways(), pathwayEnrichment),
    staleTime: Infinity,
  });
}
