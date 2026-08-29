# Production-Grade Bulk RNA-seq Analysis Pipeline

[![Nextflow](https://img.shields.io/badge/Nextflow-%E2%89%A523.04.0-brightgreen.svg)](https://www.nextflow.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![R](https://img.shields.io/badge/R-%E2%89%A54.3.0-blue.svg)](https://www.r-project.org/)
[![Python](https://img.shields.io/badge/Python-%E2%89%A53.10-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Container-Docker%20%7C%20Singularity-blue.svg)](https://www.docker.com/)

An end-to-end, reproducible, modular, and production-ready bulk RNA-seq data processing, differential expression, and pathway enrichment analysis pipeline built for local workstations, HPC clusters (Slurm), and cloud environments.

---

## Table of Contents
1. [Project Overview & Biological Context](#1-project-overview--biological-context)
2. [Workflow Architecture](#2-workflow-architecture)
3. [Repository Structure](#3-repository-structure)
4. [Requirements & Prerequisites](#4-requirements--prerequisites)
5. [Installation & Environment Setup](#5-installation--environment-setup)
6. [Dataset & Sample Metadata](#6-dataset--sample-metadata)
7. [Reference Genome Management](#7-reference-genome-management)
8. [Pipeline Execution](#8-pipeline-execution)
9. [Configuration & Execution Profiles](#9-configuration--execution-profiles)
10. [Output Directory Structure](#10-output-directory-structure)
11. [Downstream Analysis & Results](#11-downstream-analysis--results)
12. [Reproducibility & Versioning](#12-reproducibility--versioning)
13. [Testing & Quality Assurance](#13-testing--quality-assurance)
14. [HPC & Cloud Deployment](#14-hpc--cloud-deployment)
15. [Troubleshooting & FAQ](#15-troubleshooting--faq)
16. [Citation & References](#16-citation--references)
17. [License](#17-license)

---

## 1. Project Overview & Biological Context

### Biological Objective
The primary biological objective of this pipeline is to answer:
> **Which genes are significantly differentially expressed between a treatment group and a control group, and what functional biological pathways, Gene Ontology (GO) terms, and gene sets are significantly dysregulated?**

The pipeline is designed around a multi-replicate experimental design (e.g., Control `C1, C2, C3` vs Treatment `T1, T2, T3`), ensuring rigorous statistical control for biological variability.

---

## 2. Workflow Architecture

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

## 3. Repository Structure

```text
rnaseq-pipeline/
├── README.md                          # Comprehensive project documentation
├── LICENSE                            # MIT open-source license
├── .gitignore                         # Genomic/runtime git exclusions
├── .editorconfig                      # Code style and formatting standards
│
├── data/
│   ├── raw/                           # Untouched original FASTQ reads (symlinks/uncommitted)
│   ├── processed/                     # Cleaned FASTQ files post-trimming
│   └── reference/                     # FASTA genome, GTF annotation, STAR/Salmon indices
│
├── metadata/
│   └── samplesheet.csv                # Sample design table (sample, fastq_1, fastq_2, condition, replicate)
│
├── workflow/
│   ├── main.nf                        # Main Nextflow workflow entry point
│   ├── nextflow.config                # Base Nextflow configuration & profile declarations
│   ├── modules/                       # Granular, reusable Nextflow process modules
│   └── subworkflows/                  # Composed modular subworkflows
│
├── scripts/
│   ├── python/                        # Helper scripts (metadata validation, QC parsers)
│   └── R/                             # Statistical scripts (DESeq2, EDA, pathway enrichment)
│
├── envs/
│   └── rnaseq.yml                     # Conda/Mamba environment specification
│
├── containers/                        # Dockerfile / Singularity definition files
│
├── results/                           # Pipeline outputs (organized by analytical step)
│   ├── fastqc/                        # FastQC HTML/zip outputs (raw & clean)
│   ├── fastp/                         # Trimming HTML/JSON logs & summary metrics
│   ├── alignment/                     # Coordinate-sorted BAMs, BAI indexes, STAR logs
│   ├── salmon/                        # Salmon quant.sf transcript quantification directories
│   ├── rseqc/                         # RSeQC strandness, coverage, junction reports
│   ├── multiqc/                       # Consolidated MultiQC HTML report & data tables
│   ├── counts/                        # Raw count matrices & featureCounts summaries
│   ├── differential_expression/       # Full DESeq2 tables, filtered DEGs (padj < 0.05)
│   ├── visualization/                 # Publication-ready plots (PCA, Volcano, Heatmap, MA)
│   └── pathway_analysis/              # GO terms, KEGG enrichment, and GSEA output tables
│
├── reports/
│   ├── figures/                       # High-resolution vector & raster figures (PDF/PNG)
│   └── final_report/                  # Consolidated final biological analysis report
│
├── docs/
│   ├── workflow.md                    # In-depth pipeline workflow explanation
│   ├── methods.md                     # Formal scientific methods and parameter documentation
│   ├── interpretation.md              # Biological interpretation of results and limitations
│   └── troubleshooting.md             # Common errors, debugging steps, and solutions
│
├── tests/
│   ├── unit/                          # Unit tests for Python scripts (pytest)
│   └── integration/                   # Pipeline integration & smoke tests
│
└── .github/
    └── workflows/                     # GitHub Actions CI/CD workflows
```

---

## 4. Requirements & Prerequisites

* **Operating System**: Linux (Ubuntu 20.04+ / RHEL 8+) or macOS (with Docker / WSL2 on Windows)
* **Shell**: Bash / Zsh
* **Language Runtimes**:
  * Python >= 3.10
  * R >= 4.3.0
  * Java >= 11 (required for Nextflow)
* **Workflow Engine**: Nextflow >= 23.04.0
* **Container Runtimes** (recommended): Docker or Singularity/Apptainer

---

## 5. Installation & Environment Setup

The computational environment is managed through Conda/Mamba using pinned dependencies defined in [`envs/rnaseq.yml`](envs/rnaseq.yml).

### Quick Setup:
```bash
# 1. Create environment
mamba env create -f envs/rnaseq.yml

# 2. Activate environment
conda activate rnaseq-pipeline

# 3. Verify environment health
bash scripts/check_environment.sh
python scripts/python/check_environment.py
```
For detailed Windows WSL2 instructions, refer to [`docs/environment_setup.md`](docs/environment_setup.md).

---

## 6. Dataset & Sample Metadata

This pipeline uses the benchmark **GSE52778** human airway smooth muscle (ASM) RNA-seq study (Himes et al., *PLoS ONE* 2014) investigating glucocorticoid response (Dexamethasone treatment vs untreated control across 3 biological donor cell lines).

* **Organism**: *Homo sapiens* (GRCh38)
* **Design**: 3 Control vs 3 Treatment replicates (Paired-end, $2 \times 63$ bp)
* **Metadata Manifest**: [`metadata/dataset_manifest.yaml`](metadata/dataset_manifest.yaml)
* **Samplesheet**: [`metadata/samplesheet.csv`](metadata/samplesheet.csv)
* **Documentation**: [`docs/dataset.md`](docs/dataset.md)

### Samplesheet Format:
```csv
sample,fastq_1,fastq_2,condition,replicate
C1,data/raw/SRR1039508_1.fastq.gz,data/raw/SRR1039508_2.fastq.gz,control,1
C2,data/raw/SRR1039512_1.fastq.gz,data/raw/SRR1039512_2.fastq.gz,control,2
C3,data/raw/SRR1039516_1.fastq.gz,data/raw/SRR1039516_2.fastq.gz,control,3
T1,data/raw/SRR1039509_1.fastq.gz,data/raw/SRR1039509_2.fastq.gz,treatment,1
T2,data/raw/SRR1039513_1.fastq.gz,data/raw/SRR1039513_2.fastq.gz,treatment,2
T3,data/raw/SRR1039517_1.fastq.gz,data/raw/SRR1039517_2.fastq.gz,treatment,3
```

### Validate Samplesheet:
```bash
python scripts/python/validate_samplesheet.py metadata/samplesheet.csv
```

---

## 7. Reference Genome Management

*(Will be documented in detail in Phase 6)*

---

## 8. Pipeline Execution

*(Will be documented as workflow modules are built)*

---

## 9. Configuration & Execution Profiles

Execution profiles supported:
* `-profile local`: Standard local workstation execution using Conda environments.
* `-profile docker`: Local execution with fully isolated Docker containers.
* `-profile singularity`: HPC-compliant execution using Singularity/Apptainer images.
* `-profile slurm`: Automated job submission to Slurm workload managers.
* `-profile awsbatch`: Cloud-native scale-out on AWS Batch.

---

## 10. Output Directory Structure

*(See Repository Structure above)*

---

## 11. Downstream Analysis & Results

*(Will be populated during DESeq2 and Pathway enrichment phases)*

---

## 12. Reproducibility & Versioning

To ensure strict scientific reproducibility:
1. **Pinned Dependencies**: All Conda/Docker software dependencies specify exact version numbers.
2. **Fixed Random Seeds**: All stochastic algorithms (e.g., DESeq2 PCA, GSEA permutations) use explicitly documented random seeds (`set.seed(42)`).
3. **Reference Provenance**: Genome build, Ensembl/Gencode release, and source checksums are tracked.
4. **Git Versioning**: Workflow revisions are tagged with semantic release versions.

---

## 13. Testing & Quality Assurance

* Python script testing via `pytest`.
* Metadata validation testing for missing files, invalid headers, and mismatched read pairs.
* Modular smoke tests on a miniature reference subset.

---

## 14. HPC & Cloud Deployment

*(Detailed configuration files in `workflow/nextflow.config`)*

---

## 15. Troubleshooting & FAQ

Refer to [`docs/troubleshooting.md`](docs/troubleshooting.md) for diagnostics on common RNA-seq pipeline issues (e.g., low mapping rates, strandness ambiguity, memory limits in STAR).

---

## 16. Citation & References

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

## 17. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
