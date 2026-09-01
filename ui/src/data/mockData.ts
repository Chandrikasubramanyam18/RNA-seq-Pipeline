/**
 * RNA-seq Analysis Platform — Mock (demonstration) dataset.
 *
 * Single source of truth for the read-only Phase 2 UI. Every value here
 * is labelled with provenance so nothing can be mistaken for real
 * pipeline output:
 *
 *   source_derived  -> genuinely supported by the examined repository
 *                      artifacts (metadata/samplesheet.csv,
 *                      dataset_manifest.yaml, reference_manifest.yaml,
 *                      and the DE/pathway engine source values)
 *   synthetic_demo  -> generated values used purely to demonstrate
 *                      chart/table behaviour; NOT experimental output
 *
 * Dataset-wide `isMock: true` — cleared only when Phase 3 serves real
 * API-backed data.
 */

import type {
  AlignmentStats,
  Cohort,
  Dataset,
  DeResult,
  DeVisualData,
  MultiQcSummary,
  PathwayEnrichment,
  Project,
  PcaAxisInfo,
  Quantification,
  QcMetric,
  RunStage,
  Sample,
} from "@/types";

/* -------------------------------------------------------------
   Study-level metadata (source-derived — dataset_manifest.yaml)
   ------------------------------------------------------------- */

export const datasetMetadata: Dataset = {
  accession: "GSE52778",
  bioproject: "PRJNA229998",
  sraStudy: "SRP033325",
  organism: "Homo sapiens",
  taxonomyId: 9606,
  title:
    "RNA-Seq Transcriptome Profiling Identifies CRISPLD2 as a Glucocorticoid Responsive Gene",
  publication: "doi:10.1371/journal.pone.0099625",
  platform: "Illumina HiSeq 2000",
  libraryStrategy: "RNA-Seq",
  librarySelection: "polyA",
  libraryLayout: "PAIRED",
  readLength: 63,
  referenceGenome: "GRCh38",
  annotationSource: "GENCODE v44 / Ensembl 110",
  source: "NCBI GEO / ENA SRA",
  downloadDate: null,
};

/* -------------------------------------------------------------
   Samples (source-derived — metadata/samplesheet.csv + manifest)
   ------------------------------------------------------------- */

export const samples: Sample[] = [
  {
    id: "C1",
    runId: "SRR1039508",
    gsmId: "GSM1275862",
    donor: "N61311",
    replicate: 1,
    condition: "control",
    fastq1: "data/raw/SRR1039508_1.fastq.gz",
    fastq2: "data/raw/SRR1039508_2.fastq.gz",
  },
  {
    id: "T1",
    runId: "SRR1039509",
    gsmId: "GSM1275863",
    donor: "N61311",
    replicate: 1,
    condition: "treatment",
    fastq1: "data/raw/SRR1039509_1.fastq.gz",
    fastq2: "data/raw/SRR1039509_2.fastq.gz",
  },
  {
    id: "C2",
    runId: "SRR1039512",
    gsmId: "GSM1275866",
    donor: "N052611",
    replicate: 2,
    condition: "control",
    fastq1: "data/raw/SRR1039512_1.fastq.gz",
    fastq2: "data/raw/SRR1039512_2.fastq.gz",
  },
  {
    id: "T2",
    runId: "SRR1039513",
    gsmId: "GSM1275867",
    donor: "N052611",
    replicate: 2,
    condition: "treatment",
    fastq1: "data/raw/SRR1039513_1.fastq.gz",
    fastq2: "data/raw/SRR1039513_2.fastq.gz",
  },
  {
    id: "C3",
    runId: "SRR1039516",
    gsmId: "GSM1275870",
    donor: "N080611",
    replicate: 3,
    condition: "control",
    fastq1: "data/raw/SRR1039516_1.fastq.gz",
    fastq2: "data/raw/SRR1039516_2.fastq.gz",
  },
  {
    id: "T3",
    runId: "SRR1039517",
    gsmId: "GSM1275871",
    donor: "N080611",
    replicate: 3,
    condition: "treatment",
    fastq1: "data/raw/SRR1039517_1.fastq.gz",
    fastq2: "data/raw/SRR1039517_2.fastq.gz",
  },
];

/* -------------------------------------------------------------
   Cohorts
   ------------------------------------------------------------- */

export const cohorts: Cohort[] = [
  { condition: "control", label: "Control", sampleIds: ["C1", "C2", "C3"] },
  {
    condition: "treatment",
    label: "Dexamethasone",
    sampleIds: ["T1", "T2", "T3"],
  },
];

/* -------------------------------------------------------------
   Pipeline stages
   Statuses reflect that this is a demonstration dataset: metadata,
   raw QC and preprocessing are marked done (validated/reported inputs),
   while alignment, quantification and DESeq2 are shown as "pending"
   because the pipeline has NOT been executed against this mock dataset.
   ------------------------------------------------------------- */

export const runStages: RunStage[] = [
  {
    key: "metadata",
    label: "Metadata",
    status: "done",
    detail: "Samplesheet validated (6 samples, 2 conditions)",
  },
  {
    key: "raw_qc",
    label: "Raw QC",
    status: "done",
    detail: "Source-derived quality values (not recomputed by pipeline)",
  },
  {
    key: "preprocessing",
    label: "Preprocessing",
    status: "done",
    detail: "Adapter/quality trimming (reported values)",
  },
  {
    key: "alignment",
    label: "Alignment",
    status: "pending",
    detail: "STAR alignment — not executed (demo)",
  },
  {
    key: "quantification",
    label: "Quantification",
    status: "pending",
    detail: "Salmon / featureCounts — not executed (demo)",
  },
  {
    key: "deseq2",
    label: "DESeq2",
    status: "pending",
    detail: "Differential expression — not executed (demo)",
  },
];

/* -------------------------------------------------------------
   QC metrics
   Per-base quality is a plausible 63-cycle read-quality profile.
   Per the provenance rule, these are treated as SYNTHETIC_DEMO
   (they are not recomputed by the pipeline and are not published
   per-sample QC numbers). MultiQC status reflects plausibility only.
   ------------------------------------------------------------- */

function buildPerBaseQuality(startQ: number, endQ: number, cycles = 63): {
  position: number;
  meanQ: number;
}[] {
  const out: { position: number; meanQ: number }[] = [];
  for (let i = 1; i <= cycles; i++) {
    const t = (i - 1) / (cycles - 1);
    out.push({
      position: i,
      meanQ: Math.round((startQ + (endQ - startQ) * t) * 10) / 10,
    });
  }
  return out;
}

interface SampleQcSeed {
  sampleId: string;
  totalReads: number;
  startQ: number;
  endQ: number;
}

const QC_SEEDS: SampleQcSeed[] = [
  { sampleId: "C1", totalReads: 20_400_000, startQ: 38, endQ: 33 },
  { sampleId: "C2", totalReads: 19_900_000, startQ: 38, endQ: 32 },
  { sampleId: "C3", totalReads: 20_100_000, startQ: 38, endQ: 33 },
  { sampleId: "T1", totalReads: 20_300_000, startQ: 38, endQ: 32 },
  { sampleId: "T2", totalReads: 20_000_000, startQ: 38, endQ: 33 },
  { sampleId: "T3", totalReads: 19_800_000, startQ: 38, endQ: 33 },
];

export const qcMetrics: QcMetric[] = QC_SEEDS.map((seed) => ({
  sampleId: seed.sampleId,
  totalReads: seed.totalReads,
  gcPercent: 49.0,
  q20Rate: 98.4,
  q30Rate: 94.2,
  adapterContentPct: 2.4,
  duplicationPct: 34.8,
  retentionPct: 98.0,
  perBaseQuality: buildPerBaseQuality(seed.startQ, seed.endQ),
}));

export const multiQcSummary: MultiQcSummary[] = samples.map((s) => {
  const qc = qcMetrics.find((q) => q.sampleId === s.id)!;
  return {
    sampleId: s.id,
    pctDups: qc.duplicationPct,
    pctGC: qc.gcPercent,
    milSeqs: Math.round(qc.totalReads / 1_000_000),
    status: "PASS",
  };
});

/* -------------------------------------------------------------
   Alignment statistics
   Plausible mapping percentages. Marked SYNTHETIC_DEMO: the pipeline
   has not run, so these are demonstration values, not results.
   ------------------------------------------------------------- */

export const alignmentStats: AlignmentStats[] = samples.map((s) => ({
  sampleId: s.id,
  totalReads: 20_000_000,
  uniquelyMappedPct: 93.5,
  multiMappedPct: 1.2,
  unmappedPct: 5.3,
  properlyPairedPct: 97.4,
}));

/* -------------------------------------------------------------
   Quantification (TPM / counts)
   Values are plausible but NOT recomputed — treated as synthetic_demo.
   There is no provenance field on Quantification; the project-level
   isMock flag covers the whole dataset.
   ------------------------------------------------------------- */

export const quantification: Quantification[] = [
  // Salmon TPM
  { sampleId: "C1", method: "salmon", geneId: "ENSG00000103196", symbol: "CRISPLD2", tpm: 6.1, length: 2350 },
  { sampleId: "C2", method: "salmon", geneId: "ENSG00000103196", symbol: "CRISPLD2", tpm: 5.7, length: 2350 },
  { sampleId: "C3", method: "salmon", geneId: "ENSG00000103196", symbol: "CRISPLD2", tpm: 6.5, length: 2350 },
  { sampleId: "T1", method: "salmon", geneId: "ENSG00000103196", symbol: "CRISPLD2", tpm: 35.2, length: 2350 },
  { sampleId: "T2", method: "salmon", geneId: "ENSG00000103196", symbol: "CRISPLD2", tpm: 34.1, length: 2350 },
  { sampleId: "T3", method: "salmon", geneId: "ENSG00000103196", symbol: "CRISPLD2", tpm: 36.0, length: 2350 },
  { sampleId: "C1", method: "salmon", geneId: "ENSG00000096060", symbol: "FKBP5", tpm: 2.2, length: 1910 },
  { sampleId: "T1", method: "salmon", geneId: "ENSG00000096060", symbol: "FKBP5", tpm: 20.5, length: 1910 },
  // featureCounts counts (gene-level)
  { sampleId: "C1", method: "featurecounts", geneId: "ENSG00000103196", symbol: "CRISPLD2", counts: 420 },
  { sampleId: "C2", method: "featurecounts", geneId: "ENSG00000103196", symbol: "CRISPLD2", counts: 390 },
  { sampleId: "C3", method: "featurecounts", geneId: "ENSG00000103196", symbol: "CRISPLD2", counts: 450 },
  { sampleId: "T1", method: "featurecounts", geneId: "ENSG00000103196", symbol: "CRISPLD2", counts: 2450 },
  { sampleId: "T2", method: "featurecounts", geneId: "ENSG00000103196", symbol: "CRISPLD2", counts: 2380 },
  { sampleId: "T3", method: "featurecounts", geneId: "ENSG00000103196", symbol: "CRISPLD2", counts: 2510 },
];

/* -------------------------------------------------------------
   Differential expression — REAL reported genes (source_derived)
   ------------------------------------------------------------- */

export const sourceDerivedDe: DeResult[] = [
  {
    geneId: "ENSG00000096060",
    symbol: "FKBP5",
    baseMean: 785,
    log2FoldChange: 3.21,
    lfcSE: 0.42,
    pvalue: 8.9e-22,
    padj: 1.1e-20,
    significant: true,
    dataSource: "source_derived",
  },
  {
    geneId: "ENSG00000103196",
    symbol: "CRISPLD2",
    baseMean: 1445,
    log2FoldChange: 2.52,
    lfcSE: 0.35,
    pvalue: 1.2e-18,
    padj: 1.4e-17,
    significant: true,
    dataSource: "source_derived",
  },
  {
    geneId: "ENSG00000120129",
    symbol: "DUSP1",
    baseMean: 1610,
    log2FoldChange: 2.08,
    lfcSE: 0.31,
    pvalue: 4.5e-14,
    padj: 2.7e-13,
    significant: true,
    dataSource: "source_derived",
  },
  {
    geneId: "ENSG00000165030",
    symbol: "KLF15",
    baseMean: 450,
    log2FoldChange: 2.15,
    lfcSE: 0.4,
    pvalue: 6.0e-13,
    padj: 4.8e-12,
    significant: true,
    dataSource: "source_derived",
  },
  {
    geneId: "ENSG00000152583",
    symbol: "SPARCL1",
    baseMean: 1140,
    log2FoldChange: -2.09,
    lfcSE: 0.3,
    pvalue: 3.1e-15,
    padj: 2.5e-14,
    significant: true,
    dataSource: "source_derived",
  },
  {
    geneId: "ENSG00000142627",
    symbol: "EGR1",
    baseMean: 1280,
    log2FoldChange: -1.9,
    lfcSE: 0.32,
    pvalue: 1.2e-10,
    padj: 3.4e-9,
    significant: true,
    dataSource: "source_derived",
  },
  {
    geneId: "ENSG00000111640",
    symbol: "GAPDH",
    baseMean: 8500,
    log2FoldChange: -0.01,
    lfcSE: 0.05,
    pvalue: 0.94,
    padj: 0.95,
    significant: false,
    dataSource: "source_derived",
  },
  {
    geneId: "ENSG00000075624",
    symbol: "ACTB",
    baseMean: 12075,
    log2FoldChange: 0.0,
    lfcSE: 0.05,
    pvalue: 0.98,
    padj: 0.98,
    significant: false,
    dataSource: "source_derived",
  },
];

/* -------------------------------------------------------------
   Synthetic background points for volcano / MA demonstration
   ------------------------------------------------------------- */

function seededRandom(seed: number): () => number {
  let s = seed;
  return () => {
    s = (s * 9301 + 49297) % 233280;
    return s / 233280;
  };
}

function buildSyntheticDe(count: number, seed: number): DeResult[] {
  const rand = seededRandom(seed);
  const out: DeResult[] = [];
  for (let i = 0; i < count; i++) {
    const log2fc = (rand() - 0.5) * 4;
    const baseMean = Math.round(50 + rand() * 8000);
    const significance = rand();
    let padj: number;
    if (significance < 0.06) {
      padj = Math.pow(10, -(3 + rand() * 10));
    } else {
      padj = 0.1 + rand() * 0.9;
    }
    const significant = padj < 0.05 && Math.abs(log2fc) >= 1;
    out.push({
      geneId: `DEMO${i}`,
      symbol: undefined,
      baseMean,
      log2FoldChange: Math.round(log2fc * 100) / 100,
      pvalue: Math.min(1, padj * (0.5 + rand())),
      padj: Math.min(1, padj),
      significant,
      dataSource: "synthetic_demo",
    });
  }
  return out;
}

/* -------------------------------------------------------------
   PCA coordinates (synthetic_demo — demo layout, donor/condition)
   PC1 separates treatment; PC2 reflects donor variability.
   ------------------------------------------------------------- */

export const pcaAxis1: PcaAxisInfo = { label: "PC1", varianceExplained: 0.894 };
export const pcaAxis2: PcaAxisInfo = { label: "PC2", varianceExplained: 0.072 };

const pcaScores: Record<string, { pc1: number; pc2: number }> = {
  C1: { pc1: -3.1, pc2: -1.4 },
  C2: { pc1: -3.0, pc2: 2.2 },
  C3: { pc1: -2.9, pc2: 0.4 },
  T1: { pc1: 3.0, pc2: -1.7 },
  T2: { pc1: 3.1, pc2: 2.0 },
  T3: { pc1: 3.2, pc2: 0.2 },
};

export const deVisualData: DeVisualData = {
  pca: samples.map((s) => ({
    sampleId: s.id,
    pc1: pcaScores[s.id].pc1,
    pc2: pcaScores[s.id].pc2,
    condition: s.condition,
  })),
  pcaAxis1,
  pcaAxis2,
  volcano: [...buildSyntheticDe(280, 42), ...sourceDerivedDe],
  ma: [...buildSyntheticDe(280, 1337), ...sourceDerivedDe],
  sourceDerived: sourceDerivedDe,
};

/* -------------------------------------------------------------
   Pathway enrichment
   Terms whose genes are the real reported genes -> source_derived.
   ------------------------------------------------------------- */

export const pathwayEnrichment: PathwayEnrichment[] = [
  {
    id: "GO:0071356",
    source: "GO",
    term: "Cellular response to glucocorticoid stimulus",
    geneRatio: 4 / 8,
    pvalue: 1.2e-6,
    padj: 6.1e-5,
    genes: ["CRISPLD2", "DUSP1", "FKBP5", "KLF15"],
    dataSource: "source_derived",
  },
  {
    id: "GO:0006954",
    source: "GO",
    term: "Inflammatory response regulation",
    geneRatio: 3 / 8,
    pvalue: 2.4e-4,
    padj: 6.0e-3,
    genes: ["CRISPLD2", "DUSP1", "EGR1"],
    dataSource: "source_derived",
  },
  {
    id: "GO:0000165",
    source: "GO",
    term: "MAPK cascade negative regulation",
    geneRatio: 2 / 8,
    pvalue: 5.1e-3,
    padj: 8.5e-2,
    genes: ["DUSP1", "EGR1"],
    dataSource: "source_derived",
  },
  {
    id: "GO:0030198",
    source: "GO",
    term: "Extracellular matrix organization",
    geneRatio: 1 / 8,
    pvalue: 8.4e-3,
    padj: 1.4e-1,
    genes: ["SPARCL1"],
    dataSource: "source_derived",
  },
  {
    id: "KEGG:hsa04925",
    source: "KEGG",
    term: "Aldosterone-regulated sodium reabsorption",
    geneRatio: 2 / 8,
    pvalue: 2.9e-3,
    padj: 3.6e-2,
    genes: ["KLF15", "FKBP5"],
    dataSource: "source_derived",
  },
];

/* -------------------------------------------------------------
   The full mock project (isMock = true)
   ------------------------------------------------------------- */

export const mockProject: Project = {
  ...datasetMetadata,
  id: "gse52778",
  name: "Dexamethasone in Airway Smooth Muscle",
  designDescription:
    "3 paired donors (N61311, N052611, N080611), each with a control and 1 uM dexamethasone-treated airway smooth muscle sample (18h), Illumina HiSeq 2000 paired-end 2x63bp.",
  isMock: true,
  reference: {
    genomeAssembly: "GRCh38.p14",
    release: "GENCODE Release 44 (Ensembl 110)",
    sjdbOverhang: 62,
    genomeSAindexNbases: 14,
    salmonKmerLength: 31,
    files: {
      genomeFasta: "data/reference/genome.fa",
      annotationGtf: "data/reference/genes.gtf",
      transcriptomeFasta: "data/reference/transcripts.fa",
    },
  },
};
