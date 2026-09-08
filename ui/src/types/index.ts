/**
 * RNA-seq Analysis Platform — TypeScript Data Model.
 *
 * This module defines the *scientific* domain contracts for the platform.
 * It is intentionally:
 *   - Pure TypeScript (no runtime logic, no React/UI imports)
 *   - UI-independent  : describes the data, not the layout
 *   - API-independent : the same types back both the mock UI (Phase 2)
 *                       and real FastAPI responses (Phase 3)
 *
 * The model is aligned with the existing repository artifacts:
 *   - metadata/samplesheet.csv
 *   - metadata/dataset_manifest.yaml
 *   - metadata/reference_manifest.yaml
 *   - scripts/python/run_differential_expression.py
 *   - scripts/python/run_qc_and_trim.py
 *   - scripts/python/run_pathway_analysis.py
 */

/* =============================================================
   Study-level types
   ============================================================= */

/** DNA/RNA library layout: paired-end (our study) or single-end. */
export type LibraryLayout = "PAIRED" | "SINGLE";

/** Library selection strategy from the dataset manifest. */
export type LibrarySelection = "polyA" | "RANDOM" | "CDNA" | "other";

/** Library preparation strategy from the dataset manifest. */
export type LibraryStrategy = "RNA-Seq" | "miRNA-Seq" | "other";

/**
 * High-level study metadata, mirroring `dataset_manifest.yaml`.
 * Common to every Project so the same fields can be served by an API later.
 */
export interface Dataset {
  /** NCBI GEO accession, e.g. "GSE52778". */
  accession: string;
  /** NCBI BioProject identifier, e.g. "PRJNA229998". */
  bioproject: string;
  /** NCBI SRA study identifier, e.g. "SRP033325". */
  sraStudy: string;
  /** Scientific (binomial) organism name, e.g. "Homo sapiens". */
  organism: string;
  /** NCBI taxonomy id, e.g. 9606 for human. */
  taxonomyId: number;
  /** Full human-readable study title. */
  title: string;
  /** DOI or publication identifier when available. */
  publication: string;
  /** Sequencing instrument, e.g. "Illumina HiSeq 2000". */
  platform: string;
  /** Library strategy (e.g. "RNA-Seq"). */
  libraryStrategy: LibraryStrategy;
  /** Library selection (e.g. "polyA"). */
  librarySelection: LibrarySelection;
  /** Read layout; our study is paired-end. */
  libraryLayout: LibraryLayout;
  /** Nominal read length in bases, e.g. 63. */
  readLength: number;
  /** Reference genome build used for alignment/counting. */
  referenceGenome: string;
  /** Annotation source, e.g. "GENCODE v44 / Ensembl 110". */
  annotationSource: string;
  /** Origin of the dataset, e.g. "NCBI GEO / ENA SRA". */
  source: string;
  /** Optional date the dataset was downloaded (null when unset). */
  downloadDate: string | null;
}

/** Reference construction parameters recorded in `reference_manifest.yaml`. */
export interface ReferenceInfo {
  /** Genome assembly version, e.g. "GRCh38.p14". */
  genomeAssembly: string;
  /** Annotation release, e.g. "GENCODE Release 44 (Ensembl 110)". */
  release: string;
  /** STAR splice-junction overhang parameter (readLength - 1). */
  sjdbOverhang: number;
  /** STAR genomeSAindexNbases parameter (14 for human). */
  genomeSAindexNbases: number;
  /** Salmon k-mer length used for the transcript index (31). */
  salmonKmerLength: number;
  /** Reference file locations (genome fasta, gtf, transcriptome). */
  files: {
    genomeFasta: string;
    annotationGtf: string;
    transcriptomeFasta: string;
  };
}

/**
 * Flags whether the data backing this project is source-derived or
 * synthetic demonstration data. Phase 3 clears this when real results
 * are served by the API. Never presented as real analysis output.
 */
export interface DataProvenance {
  /** true = demonstration/mock data backing this project. */
  isMock: boolean;
  /** true = artifacts on disk are produced by real pipeline execution and
   *  served as source_derived. Independent of isMock. */
  executionReal: boolean;
  /** Locked semantic scope of the execution, e.g. "tutorial_mini_reference". */
  analysisScope: string;
}

/**
 * A logical analysis project: study metadata plus the reference setup
 * used to analyse it. Extends Dataset so projects and datasets share
 * the same study-level fields.
 */
export interface Project extends Dataset, DataProvenance {
  /** Stable local identifier for the project. */
  id: string;
  /** Short display name, e.g. "Dexamethasone in ASM". */
  name: string;
  /** One-line description of the experimental design. */
  designDescription: string;
  /** Reference/genome construction parameters for this project. */
  reference: ReferenceInfo;
}

/* =============================================================
   Sample & cohort types
   ============================================================= */

/** Experimental group assignment; aligned with the samplesheet. */
export type Condition = "control" | "treatment";

/**
 * A single biological sample, mirroring one row of `samplesheet.csv`
 * and each entry of `dataset_manifest.yaml.samples`.
 */
export interface Sample {
  /** Short sample id, e.g. "C1". */
  id: string;
  /** NCBI SRA run id, e.g. "SRR1039508". */
  runId: string;
  /** NCBI GEO sample id, e.g. "GSM1275862" (optional). */
  gsmId?: string;
  /** Donor/biosample identifier, e.g. "N61311". */
  donor: string;
  /** Biological replicate number within a condition (1-based). */
  replicate: number;
  /** Experimental condition (control vs treatment). */
  condition: Condition;
  /** Path to forward (mate 1) FASTQ. */
  fastq1: string;
  /** Path to reverse (mate 2) FASTQ. */
  fastq2: string;
}

/**
 * A named grouping of samples (e.g. all controls, all treated).
 * Keeps conditions first-class so cohort summaries are explicit.
 */
export interface Cohort {
  /** Condition key this cohort represents. */
  condition: Condition;
  /** Human-readable cohort label, e.g. "Control". */
  label: string;
  /** Sample ids belonging to this cohort. */
  sampleIds: string[];
}

/* =============================================================
   Pipeline run-state types
   ============================================================= */

/** Lifecycle state of a pipeline stage. */
export type StageStatus = "done" | "running" | "pending" | "blocked";

/** Ordered pipeline stages for the standard bulk RNA-seq workflow. */
export type StageKey =
  | "metadata"
  | "raw_qc"
  | "preprocessing"
  | "alignment"
  | "quantification"
  | "deseq2";

/** A single stage in the pipeline checklist shown on the project dashboard. */
export interface RunStage {
  /** Machine key for the stage (must be a StageKey). */
  key: StageKey;
  /** Human-readable stage label, e.g. "Raw QC". */
  label: string;
  /** Current lifecycle state. */
  status: StageStatus;
  /** Optional note, e.g. "Metadata validated (8 checks passed)". */
  detail?: string;
}

/* =============================================================
   Quality control types (Chapters 8-10)
   ============================================================= */

/** Mean Phred quality at a single read position (cycle). */
export interface PerBaseQuality {
  /** 1-based read position (cycle number). */
  position: number;
  /** Mean Phred quality score at this position. */
  meanQ: number;
}

/**
 * Per-sample QC summary — combines FastQC-style modules and fastp
 * trimming metrics (see `results/fastqc` and `results/fastp`).
 */
export interface QcMetric {
  /** Sample this QC record belongs to. */
  sampleId: string;
  /** Total reads in the (raw) library. */
  totalReads: number;
  /** GC content percentage. */
  gcPercent: number;
  /** Percentage of bases with Phred >= 20. */
  q20Rate: number;
  /** Percentage of bases with Phred >= 30. */
  q30Rate: number;
  /** Percentage of reads containing adapter sequence. */
  adapterContentPct: number;
  /** Sequence duplication percentage. */
  duplicationPct: number;
  /** Percentage of reads retained after trimming/filtering. */
  retentionPct: number;
  /** Per-cycle mean quality used to render the read-quality chart. */
  perBaseQuality: PerBaseQuality[];
}

/** One row of the aggregated MultiQC general-stats summary. */
export interface MultiQcSummary {
  /** Sample identifier. */
  sampleId: string;
  /** Sequence duplication percentage (FastQC). */
  pctDups: number;
  /** GC content percentage (FastQC). */
  pctGC: number;
  /** Total sequences in millions (FastQC). */
  milSeqs: number;
  /** FastQC module verdict for this sample. */
  status: "PASS" | "WARN" | "FAIL";
}

/* =============================================================
   Alignment & quantification types (Chapters 11-15)
   ============================================================= */

/** Per-sample STAR/SAMtools mapping statistics. */
export interface AlignmentStats {
  /** Sample identifier. */
  sampleId: string;
  /** Total input reads to the aligner. */
  totalReads: number;
  /** Percentage of reads that mapped uniquely. */
  uniquelyMappedPct: number;
  /** Percentage of reads mapping to multiple loci. */
  multiMappedPct: number;
  /** Percentage of reads that failed to map. */
  unmappedPct: number;
  /** Percentage of reads mapped in a proper pair. */
  properlyPairedPct: number;
}

/** Which expression engine produced a quantification record. */
export type QuantMethod = "salmon" | "featurecounts";

/**
 * A single gene's expression estimate from one method.
 * TPM is the Salmon/transcript-level unit; counts is gene-level.
 */
export interface Quantification {
  /** Sample identifier. */
  sampleId: string;
  /** Method that produced this record. */
  method: QuantMethod;
  /** Ensembl gene identifier, e.g. "ENSG00000103196". */
  geneId: string;
  /** Gene symbol when known, e.g. "CRISPLD2". */
  symbol?: string;
  /** Transcripts per million (Salmon). */
  tpm?: number;
  /** Raw/estimated read count (featureCounts). */
  counts?: number;
  /** Transcript/gene effective length used for TPM (Salmon). */
  length?: number;
}

/* =============================================================
   Differential expression types (Chapters 16-20)
   ============================================================= */

/**
 * Provenance of a differential-expression data point.
 *
 * CRITICAL scientific distinction (locked):
 *   - "source_derived" = real values taken from the published study /
 *                        metadata (selected genes, study fields)
 *   - "synthetic_demo" = generated background points used purely to
 *                        demonstrate chart behaviour; NOT experimental
 *                        output
 */
export type DeDataSource = "source_derived" | "synthetic_demo";

/**
 * One gene's differential-expression result, aligned with the columns
 * of `deseq2_results.csv` (baseMean, log2FC, padj, ...).
 */
export interface DeResult {
  /** Ensembl gene identifier. */
  geneId: string;
  /** Gene symbol when known. */
  symbol?: string;
  /** Average normalized count across samples. */
  baseMean: number;
  /** log2 fold change (treatment / control). */
  log2FoldChange: number;
  /** Standard error of the log2 fold change (optional). */
  lfcSE?: number;
  /** Raw p-value. */
  pvalue: number;
  /** FDR-adjusted p-value. */
  padj: number;
  /** true when padj < 0.05 and |log2FoldChange| >= 1. */
  significant: boolean;
  /** Whether this point is source-derived or synthetic demo. */
  dataSource: DeDataSource;
}

/** A single sample's coordinates in PCA space. */
export interface PcaPoint {
  /** Sample identifier, e.g. "C1". */
  sampleId: string;
  /** Principal component 1 score. */
  pc1: number;
  /** Principal component 2 score. */
  pc2: number;
  /** Condition of this sample (for colouring). */
  condition: Condition;
}

/** Variance explained annotation for a PCA axis. */
export interface PcaAxisInfo {
  /** Axis label, e.g. "PC1". */
  label: string;
  /** Fraction of total variance explained by this axis, e.g. 0.894. */
  varianceExplained: number;
}

/** Bundled differential-expression visualisation inputs. */
export interface DeVisualData {
  /** PCA sample coordinates. */
  pca: PcaPoint[];
  /** PCA axis metadata (variance explained). */
  pcaAxis1: PcaAxisInfo;
  pcaAxis2: PcaAxisInfo;
  /** Volcano scatter points (log2FC vs -log10(padj)). */
  volcano: DeResult[];
  /** MA scatter points (mean abundance vs log2FC). */
  ma: DeResult[];
  /** Subset of genes/points that came from the published study. */
  sourceDerived: DeResult[];
}

/* =============================================================
   Pathway enrichment types (Chapters 22-24)
   ============================================================= */

/** Enrichment-database source of a pathway/term. */
export type PathwaySource = "GO" | "KEGG" | "Reactome" | "Hallmark";

/** One enriched functional term, aligned with `pathway_enrichment_results.csv`. */
export interface PathwayEnrichment {
  /** Term identifier, e.g. "GO:0071356" or "KEGG:hsa04925". */
  id: string;
  /** Enrichment database/source. */
  source: PathwaySource;
  /** Human-readable term/pathway description. */
  term: string;
  /** Proportion of query genes hitting the term (optional). */
  geneRatio?: number;
  /** Raw enrichment p-value. */
  pvalue: number;
  /** FDR-adjusted p-value. */
  padj: number;
  /** Gene symbols/ids belonging to this term. */
  genes: string[];
  /** Whether the term is source-derived or synthetic demo. */
  dataSource: DeDataSource;
}
