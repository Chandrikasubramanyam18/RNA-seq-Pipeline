# RNA-seq Pipeline Workflow Architecture

## 1. High-Level Pipeline Flowchart

```
Public Data (GEO / SRA / ENA)
         │
         ▼
[Dataset Selection & Manifest] ───► metadata/dataset_manifest.yaml
         │
         ▼
[Sample Design Sheet] ─────────────► metadata/samplesheet.csv
         │
         ▼
[Metadata Validator] ──────────────► scripts/python/validate_samplesheet.py
   │            │
 (Valid)     (Invalid)
   │            │
   │            └──► Halt with actionable error diagnostics
   ▼
[Download / Staging] ──────────────► data/raw/*.fastq.gz (Untracked in Git)
   │
   ▼
[Phase 4: Raw QC (FastQC)] ────────► results/fastqc/raw/
   │
   ▼
[Phase 5: Preprocessing (fastp)] ──► data/processed/*.fastq.gz
   │
   ├──► [Cleaned QC (FastQC)] ─────► results/fastqc/clean/
   │
   ├──► [STAR Alignment] ──────────► results/alignment/*.bam
   │       │
   │       ├──► [SAMtools] ────────► results/alignment/*.bai, flagstat
   │       │
   │       ├──► [RSeQC] ───────────► results/rseqc/
   │       │
   │       └──► [featureCounts] ───► results/counts/gene_counts.txt
   │
   ├──► [Salmon Quasi-mapping] ────► results/salmon/*/quant.sf
   │
   ▼
[MultiQC Aggregation] ─────────────► results/multiqc/multiqc_report.html
   │
   ▼
[DESeq2 Differential Expression] ──► results/differential_expression/
   │
   ├──► [Exploratory Data Analysis]► results/visualization/ (PCA, Heatmap, Volcano, MA)
   │
   └──► [clusterProfiler Pathways] ─► results/pathway_analysis/ (GO, KEGG, GSEA)
```

---

## 2. Phase Breakdown & Logic

### Stage 1: Data Ingestion & Metadata Validation
* **Purpose**: Prevents silent execution failures, duplicate sample processing, and malformed experimental matrices prior to heavy computational tasks.
* **Outputs**: Validated sample mapping, verified FASTQ pairs, documented experimental conditions and biological replicates.

### Stage 2: Quality Control & Read Preprocessing
* **FastQC**: Analyzes per-base Phred quality scores, GC distribution, adapter presence, sequence duplication levels.
* **fastp**: Performs automated Illumina adapter clipping, poly-G tail trimming (critical for two-color Illumina chemistry like NextSeq/NovaSeq), and sliding-window quality filtering (Q >= 20).

### Stage 3: Alignment & Quantification
* **STAR**: Splice-aware alignment mapping reads across annotated and novel splice junctions against the GRCh38 reference genome.
* **SAMtools**: BAM coordinate sorting, BAI indexing, flag statistics, and mapping rate diagnostics.
* **Salmon**: Dual-phase quasi-mapping for direct transcript-level quantification (TPM and counts).
* **featureCounts**: Exon-level summarization yielding integer count matrices per gene locus.

### Stage 4: Multi-QC Report
* **MultiQC**: Consolidates statistics from FastQC, fastp, STAR, SAMtools, Salmon, and RSeQC into an interactive HTML quality control dashboard.

### Stage 5: Statistical Modeling & Functional Enrichment
* **DESeq2**: Fits Negative Binomial generalized linear models with size-factor normalization and empirical Bayes dispersion shrinkage.
* **Visualizations**: PCA for batch effect detection, sample distance clustering heatmaps, volcano plots, and MA plots.
* **clusterProfiler**: Over-Representation Analysis (ORA) and Gene Set Enrichment Analysis (GSEA) across Gene Ontology (BP, MF, CC) and KEGG databases.
