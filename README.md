# Production-Grade Bulk RNA-seq Analysis Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/UI-React%20%2B%20TypeScript-61DAFB.svg)](https://react.dev/)

A learning-focused, end-to-end bulk RNA-seq analysis platform built around the **GSE52778** dexamethasone airway smooth muscle (ASM) study. It combines a 35-chapter educational guide (`docs/`), a read-only interactive React UI (`ui/`), and a FastAPI + SQLite backend (`backend/`) that serves real DESeq2, pathway, FastQC, and fastp analysis artifacts.

> **Platform status**: The interactive UI + API platform (Phases 2 & 3) is **complete and functional**. The analytical pipeline has been executed **end-to-end with real tools at tutorial scale** (50,000 read pairs/sample against a real-loci 3-gene mini-reference: STAR, SAMtools/RSeQC/MultiQC, featureCounts, DESeq2, visualization, clusterProfiler pathway analysis) — see [8. Analysis & QC](#8-analysis--qc) and the step gate reports in `reports/`. The full **Nextflow DSL2** orchestrated path is **implemented with stub-validated topology** (Step 12); **Docker/Apptainer** container definitions are **authored statically** (Step 13, pending local image builds) — see [Planned](#planned).

---

## Table of Contents
1. [Project Overview & Biological Context](#1-project-overview--biological-context)
2. [Platform Architecture](#2-platform-architecture)
3. [Repository Structure](#3-repository-structure)
4. [Requirements & Prerequisites](#4-requirements--prerequisites)
5. [Installation & Environment Setup](#5-installation--environment-setup)
6. [Dataset & Sample Metadata](#6-dataset--sample-metadata)
7. [Reference Genome Management](#7-reference-genome-management)
8. [Analysis & QC](#8-analysis--qc)
9. [Interactive UI & API](#9-interactive-ui--api)
10. [Output Directory Structure](#10-output-directory-structure)
11. [Reproducibility & Versioning](#11-reproducibility--versioning)
12. [Testing & Quality Assurance](#12-testing--quality-assurance)
13. [Troubleshooting & FAQ](#13-troubleshooting--faq)
14. [Citation & References](#14-citation--references)
15. [License](#15-license)

---

## 1. Project Overview & Biological Context

### Biological Objective
The primary biological objective of this platform is to answer:
> **Which genes are significantly differentially expressed between a treatment group and a control group, and what functional biological pathways, Gene Ontology (GO) terms, and gene sets are significantly dysregulated?**

The analysis is built around a multi-replicate experimental design (Control `C1, C2, C3` vs Treatment `T1, T2, T3`), ensuring rigorous statistical control for biological variability.

### Target Pipeline Workflow
The following is the target end-to-end analytical design (implemented via the UI/API; the full Nextflow execution path is planned):

```
Raw FASTQ Reads (Paired-End / Single-End)
   │
   ├──► FastQC (Raw Read QC) ──────────────────────────────────┐
   │                                                           │
   ▼                                                           │
fastp (Adapter trimming, poly-G clipping, quality filtering)    │
   │                                                           │
   ├──► FastQC (Cleaned Read QC) ──────────────────────────────┤
   │                                                           │
   ├──► STAR (Splice-aware alignment to reference genome)      │
   │       │                                                   │
   │       ▼                                                   │
   │    SAMtools (Sort, index, flagstat, idxstats)             │
   │       │                                                   │
   │       ├──► RSeQC (Read distribution, gene body coverage) ─┤
   │       │                                                   │
   │       ▼                                                   │
   │    featureCounts (Gene-level read count matrix)           │
   │                                                           │
   ├──► Salmon (Alignment-free pseudo-alignment & TPM) ────────┤
   │                                                           │
   ▼                                                           ▼
MultiQC (Unified interactive QC report aggregation) ◄──────────┘
   │
   ▼
DESeq2 (Negative binomial modeling, size-factor normalization, Wald test)
   │
   ├──► Exploratory Data Analysis (PCA, Sample Correlation, Distance Matrix)
   ├──► Statistical Visualizations (Volcano plot, MA plot, Clustered Heatmaps)
   └──► Functional Enrichment (clusterProfiler: GO ORA, KEGG, GSEA)
```

---

## 2. Platform Architecture

The platform is split into three working components:

* **`docs/`** — A 35-chapter educational guide that walks through the entire RNA-seq analysis (biology, data, QC, alignment, quantification, statistics, visualization, pathways, and platform/infrastructure concepts).
* **`ui/`** — A read-only React + TypeScript dashboard that visualizes results. It probes the backend API first (`/health`) and falls back to bundled mock data if the API is unreachable.
* **`backend/`** — A FastAPI + SQLite application that serves real analysis artifacts (DESeq2 DE tables, pathway enrichments, FastQC/fastp summaries) as structured JSON via REST endpoints.

See [`backend/README.md`](backend/README.md) for API details and run steps.

---

## 3. Repository Structure

### Current

```text
rnaseq-pipeline/
├── README.md                          # This documentation
├── LICENSE                            # MIT open-source license
├── .gitignore                         # Genomic/runtime git exclusions
├── .editorconfig                      # Code style and formatting standards
│
├── docs/                              # 35-chapter learning & reference guide
│   ├── 00_project_overview.md         # Master syllabus / project overview
│   ├── 01_biology/                    # Biology principles
│   ├── 02_data/                       # Dataset, FASTQ, metadata
│   ├── 03_qc/                         # FastQC, fastp, MultiQC
│   ├── 04_alignment/                  # STAR, reference genome
│   ├── 05_quantification/             # Salmon, featureCounts
│   ├── 06_statistics/                 # DESeq2, hypothesis testing
│   ├── 07_visualization/              # PCA, volcano, MA, heatmaps
│   ├── 08_pathways/                   # GO, KEGG, GSEA
│   ├── 09_workflow/                   # Orchestration concepts
│   ├── 10_reproducibility/            # Conda, Docker, versioning
│   ├── 11_infrastructure/             # Linux, cloud, storage
│   └── 12_platform/                   # Platform & API concepts
│
├── backend/                           # FastAPI + SQLite API (complete)
│   ├── app/                           # Application package (models, seeders, routers)
│   ├── alembic/                       # Database migrations
│   └── README.md                      # Backend run & API documentation
│
├── ui/                                # Read-only React + TypeScript dashboard (complete)
│   ├── src/                           # Components, API client, hooks, mock data
│   └── package.json
│
├── workflow/                          # Nextflow DSL2 pipeline (Step 12, stub-validated)
│   ├── main.nf                        # Main Nextflow workflow entry point
│   ├── nextflow.config                # Base config & standard/conda/docker/apptainer profiles
│   ├── modules/                       # Reusable Nextflow process modules
│   └── subworkflows/                  # Composed modular subworkflows
│
├── containers/                        # Containerization (Step 13, static authorship)
│   ├── Dockerfile                     # Docker image (Micromamba + envs/rnaseq.yml)
│   └── rnaseq.def                     # Apptainer/Singularity definition file
│
├── metadata/
│   ├── samplesheet.csv                # Sample design table (sample, fastq_1, fastq_2, condition, replicate)
│   ├── dataset_manifest.yaml          # Dataset provenance & download sources
│   └── reference_manifest.yaml        # Reference genome provenance & checksums
│
├── scripts/
│   └── python/                        # Helper/validation scripts
│       ├── check_environment.py       # Environment health check
│       ├── download_dataset.py        # Dataset download/staging helpers
│       ├── validate_samplesheet.py    # Samplesheet validator
│       ├── validate_reference.py      # FASTA/GTF compatibility validator
│       ├── run_qc_and_trim.py         # FastQC + fastp runner
│       ├── summarize_fastqc.py        # FastQC summary -> TSV
│       ├── summarize_fastp.py         # fastp summary -> TSV
│       ├── run_differential_expression.py  # DESeq2 DRIVER (see README)
│       ├── run_pathway_analysis.py    # clusterProfiler DRIVER (see README)
│       └── build_test_reference.py    # Miniature test-reference builder
│
├── envs/
│   └── rnaseq.yml                     # Conda/Mamba environment specification (Linux tools)
│
├── data/
│   ├── raw/                           # Untouched original FASTQ reads (git-ignored)
│   ├── processed/                     # Cleaned FASTQ files post-trimming (git-ignored)
│   └── reference/                     # FASTA genome, GTF annotation, indices (git-ignored)
│
├── results/                           # Pipeline outputs (organized by analytical step)
├── reports/
│   ├── preprocessing_review.md        # Preprocessing review notes
│   └── qc_review.md                   # QC review notes
│
└── tests/
    └── unit/                          # Unit tests for Python scripts (pytest)
```

### Planned

The following components are **not yet implemented** and should not be referenced as executable today:

```text
.github/workflows/                 # GitHub Actions CI/CD                      → planned
tests/integration/                 # Pipeline integration & smoke tests       → planned
```

The **statistical scripts** listed below (`scripts/R/`) are now implemented and executed against real pipeline outputs (tutorial-scale):

```text
scripts/R/
├── run_deseq2.R                   # DESeq2 driver (default fitType demo)     → implemented (Step 7)
├── run_deseq2_fittype_mean.R      # DESeq2 driver (fitType="mean")           → implemented (Step 7)
├── run_visualization.R            # PCA / MA / volcano / heatmap data        → implemented (Step 8)
└── run_pathway_analysis.R         # clusterProfiler GO/KEGG ORA              → implemented (Step 9)
```

---

## 4. Requirements & Prerequisites

The *currently running* components require only:

* **Python 3.14+** — for `scripts/python/` and the `backend/` API.
* **Node.js / npm** — for the `ui/` dashboard.
* **bash / POSIX shell** — only if running the Linux-tooling steps locally (preferred in WSL2 on Windows).

For the **planned** locally-executed Nextflow pipeline, you will additionally need: a POSIX environment (Linux / WSL2 / Docker), Nextflow >= 23.04.0, Java >= 11, R >= 4.3, and container runtimes (Docker / Singularity). See [`docs/10_reproducibility/`](docs/10_reproducibility/) and [`docs/11_infrastructure/linux.md`](docs/11_infrastructure/linux.md).

---

## 5. Installation & Environment Setup

### Python backend & scripts
```bash
pip install -r backend/requirements.txt    # (if present) or the pinned deps in backend/README.md
python -c "import backend.app.main"         # sanity check
```

### UI dashboard
```bash
cd ui
npm install
npm run typecheck
npm run dev          # start the Vite dev server
```

For detailed Windows/WSL2 and tooling guidance, see:
* [`docs/00_project_overview.md`](docs/00_project_overview.md)
* [`docs/11_infrastructure/linux.md`](docs/11_infrastructure/linux.md)
* [`docs/10_reproducibility/conda.md`](docs/10_reproducibility/conda.md)

---

## 6. Dataset & Sample Metadata

This platform uses the benchmark **GSE52778** human airway smooth muscle (ASM) RNA-seq study (Himes et al., *PLoS ONE* 2014) investigating glucocorticoid response (Dexamethasone treatment vs untreated control across 3 biological donor cell lines).

* **Organism**: *Homo sapiens* (GRCh38)
* **Design**: 3 Control vs 3 Treatment replicates (Paired-end, 2 x 63 bp)
* **Metadata Manifest**: [`metadata/dataset_manifest.yaml`](metadata/dataset_manifest.yaml)
* **Samplesheet**: [`metadata/samplesheet.csv`](metadata/samplesheet.csv)
* **Documentation**: [`docs/00_project_overview.md`](docs/00_project_overview.md) and [`docs/02_data/`](docs/02_data/)

### Samplesheet Format
```csv
sample,fastq_1,fastq_2,condition,replicate
C1,data/raw/SRR1039508_1.fastq.gz,data/raw/SRR1039508_2.fastq.gz,control,1
C2,data/raw/SRR1039512_1.fastq.gz,data/raw/SRR1039512_2.fastq.gz,control,2
C3,data/raw/SRR1039516_1.fastq.gz,data/raw/SRR1039516_2.fastq.gz,control,3
T1,data/raw/SRR1039509_1.fastq.gz,data/raw/SRR1039509_2.fastq.gz,treatment,1
T2,data/raw/SRR1039513_1.fastq.gz,data/raw/SRR1039513_2.fastq.gz,treatment,2
T3,data/raw/SRR1039517_1.fastq.gz,data/raw/SRR1039517_2.fastq.gz,treatment,3
```

### Validate Samplesheet
```bash
python scripts/python/validate_samplesheet.py metadata/samplesheet.csv
```

---

## 7. Reference Genome Management

Reference files use the human **GRCh38.p14** primary assembly and **GENCODE Release 44** (Ensembl 110 compatible) gene annotations with UCSC chromosome naming (`chr1, chr2, ...`).

* **Reference Manifest**: [`metadata/reference_manifest.yaml`](metadata/reference_manifest.yaml)
* **Reference Guide**: [`docs/04_alignment/reference_genome.md`](docs/04_alignment/reference_genome.md)
* **Splice Junction Overhang**: `sjdbOverhang = ReadLength - 1 = 63 - 1 = 62`

### Validate Reference Compatibility
```bash
python scripts/python/validate_reference.py \
    --fasta data/reference/genome.fa \
    --gtf data/reference/genes.gtf
```

---

## 8. Analysis & QC

### Quality Control
```bash
# Extract structured QC metrics into a tabular summary
python scripts/python/summarize_fastqc.py --input-dir results/fastqc/raw --output results/fastqc/raw/fastqc_summary.tsv
```
For interpretation guidelines on Phred scores, GC bias, and duplication metrics, see [`docs/03_qc/fastqc.md`](docs/03_qc/fastqc.md).

### Read Preprocessing & Trimming
```bash
# Run fastp adapter trimming / quality filtering and aggregate metrics
python scripts/python/run_qc_and_trim.py
python scripts/python/summarize_fastp.py --input-dir results/fastp --output results/fastp/fastp_summary.tsv
```
For comprehensive preprocessing principles and poly-G clipping documentation, see [`docs/03_qc/fastp.md`](docs/03_qc/fastp.md).

---

## 9. Interactive UI & API

The results are browsable through the read-only React dashboard backed by the FastAPI service, so no local bioinformatics execution is required to explore the curated analysis.

* **Backend**: see [`backend/README.md`](backend/README.md) for setup, seeding, and the full endpoint list.
* **Frontend**: `ui/` — starts with `npm run dev` and connects to the API at `http://localhost:8000` (falls back to mock data if unreachable).
* **Provenance note**: The backend correctly marks the project `isMock: true` until a **publication/full biological analysis** has been completed. Real tutorial-scale artifacts (DESeq2, pathway, FastQC/fastp summaries, alignment QC, count matrix, visualization) are served as source-derived; `isMock` stays true because the current execution is tutorial-scale (50,000 read pairs/sample, 3-gene mini-reference) and not genome-wide biological inference.

---

## 10. Output Directory Structure

*(See [Repository Structure](#3-repository-structure) above.)*

---

## 11. Reproducibility & Versioning

To support scientific reproducibility:
1. **Version-constrained Dependencies**: Conda/Docker dependency versions are declared in `envs/rnaseq.yml` — most core tools are exact-pinned, while the language runtimes and Python scientific stack use version constraints (`>=`/ranges). Exact per-build resolution locking (e.g. `conda-lock`) is a future enhancement.
2. **Fixed Random Seeds**: Stochastic algorithms (e.g., DESeq2 PCA, GSEA permutations) use documented random seeds (`set.seed(42)`).
3. **Reference Provenance**: Genome build, Ensembl/GENCODE release, and source checksums are tracked in `metadata/reference_manifest.yaml`.
4. **Git Versioning**: Revisions are tagged with semantic release versions.

---

## 12. Testing & Quality Assurance

* Python unit tests via `pytest` in [`tests/unit/`](tests/unit/).
* Metadata/samplesheet validation for missing files, invalid headers, and mismatched read pairs.
* `ui/` is verified with `npm run typecheck` and `npm run build`.

---

## 13. Troubleshooting & FAQ

For diagnostics on common RNA-seq pipeline issues (low mapping rates, strandness ambiguity, STAR memory limits), see the platform and infrastructure chapters:
* [`docs/11_infrastructure/linux.md`](docs/11_infrastructure/linux.md)
* [`docs/00_project_overview.md`](docs/00_project_overview.md)
* [`backend/README.md`](backend/README.md)

---

## 14. Citation & References

* **FastQC**: Andrews, S. (2010). FastQC: A Quality Control Tool for High Throughput Sequence Data.
* **fastp**: Chen, S., et al. (2018). *Bioinformatics*, 34(17), i884–i890.
* **STAR**: Dobin, A., et al. (2013). *Bioinformatics*, 29(1), 15–21.
* **SAMtools**: Danecek, P., et al. (2021). *GigaScience*, 10(2), giab008.
* **Salmon**: Patro, R., et al. (2017). *Nature Methods*, 14(4), 417–419.
* **featureCounts**: Liao, Y., et al. (2014). *Bioinformatics*, 30(7), 923–930.
* **DESeq2**: Love, M. I., et al. (2014). *Genome Biology*, 15(12), 550.
* **clusterProfiler**: Wu, T., et al. (2021). *The Innovation*, 2(3), 100141.
* **MultiQC**: Ewels, P., et al. (2016). *Bioinformatics*, 32(19), 3047–3048.
* **Nextflow**: Di Tommaso, P., et al. (2017). *Nature Biotechnology*, 35(4), 316–319.

---

## 15. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
