# RNA-seq Analysis Platform -- Project Overview

> The master syllabus for understanding, building, and operating
> an end-to-end bulk RNA-seq analysis platform.

---

## Table of Contents

1. [What Is This Project?](#1-what-is-this-project)
2. [The Biological Question](#2-the-biological-question)
3. [The 4-Layer Architecture](#3-the-4-layer-architecture)
4. [The Data Flow](#4-the-data-flow)
5. [Repository Structure](#5-repository-structure)
6. [Learning Path (35 Chapters)](#6-learning-path-35-chapters)
7. [Current Status](#7-current-status)
8. [Quick Start](#8-quick-start)
9. [Prerequisites](#9-prerequisites)

---

## 1. What Is This Project?

This is a **production-grade bulk RNA-seq analysis platform** that
takes raw sequencing reads (FASTQ files) from an RNA-seq experiment
and processes them through every analytical stage -- from quality
control to differential gene expression to pathway enrichment.

It answers the biological question:

> **Which genes are significantly differentially expressed between
> a treatment group and a control group, and what biological pathways
> are affected?**

### What you will learn

- **Molecular biology** behind RNA sequencing
- **Bioinformatics tools** (FastQC, fastp, STAR, Salmon, DESeq2, clusterProfiler)
- **Data formats** (FASTQ, FASTA, BAM, GTF)
- **Statistical methods** (normalization, hypothesis testing, FDR correction)
- **Workflow engineering** (Nextflow, containers, reproducibility)
- **Infrastructure** (Linux, HPC/Slurm, cloud/AWS)
- **Software engineering** (React UI, FastAPI backend, database design)

### How to use this guide

- **Sequential**: Start at Chapter 01 and work through to Chapter 35
- **By tool**: Jump to the specific tool chapter you need
- **By phase**: Biology first, then data, then tools, then engineering

---

## 2. The Biological Question

### The Study

| Property | Value |
|----------|-------|
| Accession | GSE52778 |
| Publication | Himes et al., PLoS ONE 2014 |
| Organism | Homo sapiens (GRCh38) |
| Cell Type | Primary Airway Smooth Muscle (ASM) |
| Treatment | 1 uM Dexamethasone, 18 hours |
| Platform | Illumina HiSeq 2000 |
| Layout | Paired-end 2 x 63 bp |

### The Experiment

Glucocorticoids (such as Dexamethasone) are the standard anti-inflammatory
treatment for asthma and COPD. This study investigates transcriptional
remodeling in human ASM cells following glucocorticoid exposure.

### The Design

3 paired biological replicate donors, each with a control and treated sample:

| Sample | Condition | Donor | SRA Run |
|--------|-----------|-------|---------|
| C1 | control | N61311 | SRR1039508 |
| T1 | treatment | N61311 | SRR1039509 |
| C2 | control | N052611 | SRR1039512 |
| T2 | treatment | N052611 | SRR1039513 |
| C3 | control | N080611 | SRR1039516 |
| T3 | treatment | N080611 | SRR1039517 |

### Published Reference Findings

The following values are from the **published study** (Himes et al. 2014)
and serve as ground truth for validating our pipeline implementation.
These are NOT results from our pipeline -- they are the reference
values we aim to reproduce.

| Gene | log2FC | padj | Role |
|------|--------|------|------|
| CRISPLD2 | +2.52 | 1.4e-17 | Glucocorticoid-responsive; modulates airway inflammation |
| FKBP5 | +3.21 | 1.1e-20 | Glucocorticoid receptor co-chaperone |
| DUSP1 | +2.08 | 2.7e-13 | Dephosphorylates MAPK inflammatory kinases |
| KLF15 | +2.15 | 4.8e-12 | Glucocorticoid-inducible transcription factor |
| SPARCL1 | -2.09 | 2.5e-14 | Extracellular matrix remodeling (downregulated) |

---

## 3. The 4-Layer Architecture

```
+--------------------------------------------------+
|              LAYER 4: USER INTERFACE             |
|                                                  |
|    React + TypeScript + Tailwind CSS             |
|    Dashboard | QC | Results | Pathways           |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
|              LAYER 3: APPLICATION / API          |
|                                                  |
|    FastAPI + Python + SQLAlchemy + SQLite         |
|    Projects | Samples | Runs | Results           |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
|              LAYER 2: WORKFLOW ENGINE            |
|                                                  |
|    Nextflow + Docker / Apptainer                 |
|    Local | Slurm HPC | AWS Batch                |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
|              LAYER 1: BIOINFORMATICS ENGINE      |
|                                                  |
|    FastQC -> fastp -> STAR -> SAMtools           |
|    Salmon -> featureCounts -> DESeq2             |
|    clusterProfiler (GO, KEGG, GSEA)              |
+--------------------------------------------------+
```

---

## 4. The Data Flow

```
Raw FASTQ Reads (Paired-End)
    |
    +---> FastQC (Raw Read QC) --------+
    |                                   |
    v                                   |
fastp (Adapter trimming,               |
       quality filtering)               |
    |                                   |
    +---> FastQC (Clean Read QC) ---+  |
    |                               |  |
    +---> STAR (Alignment) ------+  |  |
    |       |                    |  |  |
    |       v                    |  |  |
    |    SAMtools (Sort, Index)  |  |  |
    |       |                    |  |  |
    |       +---> RSeQC ------+  |  |  |
    |       |                  |  |  |  |
    |       v                  |  |  |  |
    |    featureCounts         |  |  |  |
    |       |                  |  |  |  |
    +---> Salmon (Quant) ------+--+--+--+
              |                  |  |  |
              |                  v  v  v
              |         MultiQC (aggregates all
              |         QC reports into one
              |         interactive HTML dashboard)
              |
              v
       DESeq2 (Differential expression)
              |
              +---> PCA, Volcano, Heatmap (Visualization)
              |
              +---> GO, KEGG, GSEA (Pathway enrichment)
```

**MultiQC** is not a sequential computational step -- it is an
aggregation layer that collects statistics from FastQC, fastp,
STAR, SAMtools, Salmon, and RSeQC and presents them in a single
interactive HTML report.

---

## 5. Repository Structure

```
RNA-seq Pipeline/
|
+-- docs/                  Learning guide (35 chapters)
|   +-- 00_project_overview.md
|   +-- 01_biology/
|   +-- 02_data/
|   +-- 03_qc/
|   +-- 04_alignment/
|   +-- 05_quantification/
|   +-- 06_statistics/
|   +-- 07_visualization/
|   +-- 08_pathways/
|   +-- 09_workflow/
|   +-- 10_reproducibility/
|   +-- 11_infrastructure/
|   +-- 12_platform/
|
+-- scripts/               Bioinformatics scripts
|   +-- python/            Python analysis engines
|   +-- R/                 (Future: R/DESeq2 scripts)
|   +-- *.sh               Shell wrappers
|
+-- workflow/              (Future: Nextflow DSL2)
|   +-- modules/
|   +-- subworkflows/
|
+-- data/                  Biological data (gitignored)
|   +-- raw/               Original FASTQ files
|   +-- processed/         Trimmed FASTQ files
|   +-- reference/         Genome, GTF, indices
|
+-- metadata/              Experiment design
|   +-- samplesheet.csv
|   +-- dataset_manifest.yaml
|   +-- reference_manifest.yaml
|
+-- results/               Pipeline outputs (gitignored)
|   +-- fastqc/
|   +-- fastp/
|   +-- alignment/
|   +-- salmon/
|   +-- multiqc/
|   +-- counts/
|   +-- differential_expression/
|   +-- visualization/
|   +-- pathway_analysis/
|
+-- tests/                 Unit and integration tests
|   +-- unit/
|
+-- ui/                    (Building: React + TypeScript)
|
+-- api/                   (Building: FastAPI + SQLite)
|
+-- envs/                  Conda environments
|   +-- rnaseq.yml
|
+-- reports/               Review documents
+-- containers/            (Future: Docker/Apptainer)
+-- .github/workflows/     (Future: CI/CD)
```

---

## 6. Learning Path (35 Chapters)

### Phase 1: Biology (3 chapters)

| Ch | File | Title | Topics |
|----|------|-------|--------|
| 01 | `01_biology/molecular_biology.md` | Molecular Biology | Central dogma, DNA, RNA, protein synthesis |
| 02 | `01_biology/genetics.md` | Genetics & Gene Expression | Transcription regulation, housekeeping genes |
| 03 | `01_biology/rna_seq.md` | What Is RNA-seq? | Bulk vs single-cell, experimental design |

### Phase 2: Data Formats (4 chapters)

| Ch | File | Title | Topics |
|----|------|-------|--------|
| 04 | `02_data/fastq.md` | FASTQ Format | 4-line records, Phred scores, paired-end |
| 05 | `02_data/fasta.md` | FASTA Format | Reference genomes, chromosome naming |
| 06 | `02_data/bam.md` | SAM/BAM Format | Alignment records, flags, CIGAR strings |
| 07 | `02_data/gtf.md` | GTF Format | Gene annotation, exons, introns, transcripts |

### Phase 3: Quality Control (3 chapters)

| Ch | File | Title | Topics |
|----|------|-------|--------|
| 08 | `03_qc/fastqc.md` | FastQC | Per-base quality, GC, adapters, duplication |
| 09 | `03_qc/fastp.md` | fastp | Adapter trimming, quality filtering, poly-G |
| 10 | `03_qc/multiqc.md` | MultiQC | Multi-sample QC aggregation |

### Phase 4: Alignment (3 chapters)

| Ch | File | Title | Topics |
|----|------|-------|--------|
| 11 | `04_alignment/reference_genome.md` | Reference Genome | GRCh38, GENCODE, chromosome compatibility |
| 12 | `04_alignment/star.md` | STAR Aligner | Splice-aware alignment, genome indexing |
| 13 | `04_alignment/samtools.md` | SAMtools | BAM sorting, indexing, flagstat, stats |

### Phase 5: Quantification (2 chapters)

| Ch | File | Title | Topics |
|----|------|-------|--------|
| 14 | `05_quantification/salmon.md` | Salmon | Quasi-mapping, TPM, transcript abundance |
| 15 | `05_quantification/featurecounts.md` | featureCounts | Exon-to-gene read summarization |

### Phase 6: Statistics (3 chapters)

| Ch | File | Title | Topics |
|----|------|-------|--------|
| 16 | `06_statistics/statistics.md` | Statistics Fundamentals | Hypothesis testing, p-values, FDR |
| 17 | `06_statistics/normalization.md` | Normalization | Size factors, median-of-ratios, TMM |
| 18 | `06_statistics/deseq2.md` | DESeq2 | NB GLM, Wald test, log2FC, shrinkage |

### Phase 7: Visualization (3 chapters)

| Ch | File | Title | Topics |
|----|------|-------|--------|
| 19 | `07_visualization/pca.md` | PCA | Variance explained, batch effects, sample QC |
| 20 | `07_visualization/volcano.md` | Volcano Plot | log2FC vs significance, coloring |
| 21 | `07_visualization/heatmap.md` | Heatmap | Clustered expression, dendrograms |

### Phase 8: Pathways (3 chapters)

| Ch | File | Title | Topics |
|----|------|-------|--------|
| 22 | `08_pathways/go.md` | Gene Ontology | ORA, GO terms, BP/MF/CC, enrichment |
| 23 | `08_pathways/gsea.md` | GSEA | Rank-based enrichment, permutation testing |
| 24 | `08_pathways/reactome.md` | Reactome | Pathway database, visualization |

### Phase 9: Workflow Engineering (2 chapters)

| Ch | File | Title | Topics |
|----|------|-------|--------|
| 25 | `09_workflow/nextflow.md` | Nextflow | DSL2, processes, channels, profiles |
| 26 | `09_workflow/nf_core.md` | nf-core | Community standards, conventions |

### Phase 10: Reproducibility (3 chapters)

| Ch | File | Title | Topics |
|----|------|-------|--------|
| 27 | `10_reproducibility/conda.md` | Conda & Mamba | Environments, channels, pinned deps |
| 28 | `10_reproducibility/docker.md` | Docker | Dockerfiles, images, containers |
| 29 | `10_reproducibility/apptainer.md` | Apptainer | Singularity for HPC clusters |

### Phase 11: Infrastructure (3 chapters)

| Ch | File | Title | Topics |
|----|------|-------|--------|
| 30 | `11_infrastructure/linux.md` | Linux & WSL2 | Shell, permissions, file systems |
| 31 | `11_infrastructure/slurm.md` | Slurm | HPC job scheduling, sbatch |
| 32 | `11_infrastructure/aws.md` | AWS | Batch, S3, cloud costs |

### Phase 12: Platform Development (3 chapters)

| Ch | File | Title | Topics |
|----|------|-------|--------|
| 33 | `12_platform/architecture.md` | Architecture | Full system design, data flow |
| 34 | `12_platform/api.md` | API Design | FastAPI endpoints, database schema |
| 35 | `12_platform/frontend.md` | Frontend Design | React components, routing, pages |

### Teaching Template

Every chapter follows this 15-section structure:

```
 1. What is it?
 2. Why do we need it?
 3. Where does it fit?
 4. Input
 5. Output
 6. How it works
 7. Biology behind it
 8. Command
 9. Example
10. How to read the output
11. Common errors
12. Limitations
13. How our project uses it
14. Official documentation
15. Mini exercise
```

---

## 7. Current Status

### Implemented

| Component | Location | Tests |
|-----------|----------|-------|
| Samplesheet validator | `scripts/python/validate_samplesheet.py` | 8 unit tests |
| Reference validator | `scripts/python/validate_reference.py` | 4 unit tests |
| Dataset downloader | `scripts/download_dataset.sh` + `scripts/python/download_dataset.py` | -- |
| FastQC wrapper | `scripts/run_fastqc.sh` | -- |
| FastQC parser | `scripts/python/summarize_fastqc.py` | 5 unit tests |
| fastp wrapper | `scripts/run_fastp.sh` | -- |
| fastp parser | `scripts/python/summarize_fastp.py` | 3 unit tests |
| MultiQC wrapper | `scripts/run_multiqc.sh` | -- |
| STAR index builder | `scripts/build_star_index.sh` | -- |
| Salmon index builder | `scripts/build_salmon_index.sh` | -- |
| Python DE engine | `scripts/python/run_differential_expression.py` | -- |
| Python pathway engine | `scripts/python/run_pathway_analysis.py` | -- |
| Test reference builder | `scripts/python/build_test_reference.py` | -- |
| Environment checker | `scripts/check_environment.sh` + `scripts/python/check_environment.py` | -- |
| Conda environment | `envs/rnaseq.yml` | -- |

### Building Now

| Component | Location | Status |
|-----------|----------|--------|
| Learning guide (35 chapters) | `docs/` | In progress |

### Future (Deliberately Deferred)

| Component | Reason Deferred |
|-----------|-----------------|
| Nextflow main.nf | Requires all tool modules to be containerized first |
| R/DESeq2 proper | Requires R/Bioconductor implementation (Python version is educational fallback) |
| R/clusterProfiler proper | Same as above |
| Docker/Apptainer containers | Requires Nextflow integration |
| GitHub Actions CI/CD | Requires containerized pipeline |
| Integration tests | Requires miniature reference dataset |
| UI-triggered pipeline execution | Requires Nextflow + API integration |

### Important Distinction

The Python DE and pathway engines in this repository are **educational
implementations**. They demonstrate the statistical concepts (median-of-ratios
normalization, Wald testing, Benjamini-Hochberg FDR, hypergeometric enrichment)
but are NOT equivalent to the production R/DESeq2 and clusterProfiler
ecosystem. For publication-quality analysis, the R implementations are
the standard.

---

## 8. Quick Start

This quick start uses only scripts that are confirmed as implemented
in the Status section above.

### Prerequisites

- Windows with WSL2, macOS, or Linux
- ~20 GB disk space (for subsampled dataset)
- 8 GB RAM minimum

### Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd "RNA-seq Pipeline"

# 2. Set up WSL2 (Windows only)
wsl --install -d Ubuntu
# Restart, then open Ubuntu

# 3. Navigate to project in WSL2
cd "/mnt/c/Chandrika/RNA-seq Pipeline"

# 4. Install Miniforge (if not installed)
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh"
bash Miniforge3-Linux-x86_64.sh -b -p "$HOME/miniforge3"
"$HOME/miniforge3/bin/conda" init bash
source ~/.bashrc

# 5. Create the conda environment
mamba env create -f envs/rnaseq.yml
conda activate rnaseq-pipeline

# 6. Verify installation (both scripts exist and are implemented)
bash scripts/check_environment.sh
python3 scripts/python/check_environment.py
```

### Download Data

```bash
# Download subsampled reads for testing (50K read pairs per sample)
python3 scripts/python/download_dataset.py --subsample 50000
```

### Validate Metadata

```bash
# Validate samplesheet format and consistency
python3 scripts/python/validate_samplesheet.py metadata/samplesheet.csv

# Validate reference genome and GTF compatibility
python3 scripts/python/validate_reference.py \
    --fasta data/reference/genome.fa \
    --gtf data/reference/genes.gtf
```

### Run Analysis (Python Educational Engines)

```bash
# QC and trimming (pure Python engine)
python3 scripts/python/run_qc_and_trim.py

# Differential expression analysis (educational fallback)
python3 scripts/python/run_differential_expression.py

# Pathway enrichment analysis (educational fallback)
python3 scripts/python/run_pathway_analysis.py
```

For the full bioinformatics pipeline (FastQC, fastp, STAR, Salmon,
featureCounts), you will need the Linux-native tools available in
the conda environment, run inside WSL2 or on a Linux system. See
the individual tool chapters for command reference.

---

## 9. Prerequisites

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| RAM | 8 GB | 16 GB (32 GB for full human genome STAR) |
| Disk | 20 GB (subsampled) | 50 GB (full dataset) |
| OS | WSL2 on Windows | Native Linux or macOS |
| CPU | 2 cores | 8+ cores for parallel alignment |

### Software Requirements

| Tool | Purpose | Install |
|------|---------|---------|
| WSL2 | Linux on Windows | `wsl --install -d Ubuntu` |
| Miniforge | Package manager | conda-forge installer |
| Conda/Mamba | Environment management | Included with Miniforge |

Everything else (FastQC, fastp, STAR, Salmon, DESeq2, etc.)
is installed automatically by the Conda environment.

### Knowledge Prerequisites

- Basic command line (ls, cd, cat, grep)
- Basic statistics (mean, variance, p-value)
- No prior bioinformatics experience required
  -- this guide teaches from molecular biology onward

---

> **Next**: Read [Chapter 01: Molecular Biology](01_biology/molecular_biology.md)
> to start from the very beginning of the learning path.
