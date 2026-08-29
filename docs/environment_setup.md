# Computational Environment Setup Guide

## 1. Why a POSIX (Linux / WSL2) Environment is Required

State-of-the-art RNA-seq software packages (such as **STAR**, **SAMtools**, **Salmon**, **RSeQC**, and **Nextflow**) are designed and compiled natively as Linux ELF binaries. 

Running high-throughput bioinformatics workflows directly on Windows PowerShell without POSIX abstraction causes severe compatibility limitations:
* **STAR** (Spliced Transcripts Alignment to a Reference) relies heavily on Linux shared memory primitives (`sys/shm.h`, `sys/mman.h`) and is not compiled natively for Windows Win32.
* **Conda channels** such as `bioconda` predominantly build binary packages targeting `linux-64` and `osx-64`.
* **Process management** and pipe streaming (`|`, named FIFOs, process substitution `<( ... )`) used across Nextflow modules require POSIX shells (`/bin/bash`).

Therefore, Windows users should run this pipeline inside **Windows Subsystem for Linux (WSL2)** or via **Docker Desktop**.

---

## 2. Step-by-Step WSL2 & Ubuntu Setup on Windows

### Step 2.1: Install WSL2 & Ubuntu
Open PowerShell as **Administrator** and run:
```powershell
wsl --install -d Ubuntu
```
*Restart your computer if prompted.*

Once installed, open **Ubuntu** from your Windows Start menu and set up your Linux username and password.

---

### Step 2.2: Navigate to your Project Directory in WSL2
Your Windows drives are automatically mounted under `/mnt/` inside WSL2:
```bash
# In Ubuntu terminal:
cd "/mnt/c/Chandrika/RNA-seq  Pipeline"
ls -la
```

---

### Step 2.3: Install Miniforge (Fast Mamba Package Manager)
Inside your Ubuntu terminal:
```bash
# Download and install Miniforge
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh"
bash Miniforge3-Linux-x86_64.sh -b -p "$HOME/miniforge3"

# Initialize conda/mamba in bash
"$HOME/miniforge3/bin/conda" init bash
source ~/.bashrc

# Configure strict channel priority
conda config --set channel_priority strict
```

---

### Step 2.4: Create the RNA-seq Pipeline Environment
Create the isolated conda environment from our pinned `envs/rnaseq.yml` manifest:
```bash
cd "/mnt/c/Chandrika/RNA-seq  Pipeline"
mamba env create -f envs/rnaseq.yml

# Activate the environment
conda activate rnaseq-pipeline
```

---

### Step 2.5: Verify Tool Availability
Run the verification scripts:
```bash
bash scripts/check_environment.sh
python3 scripts/python/check_environment.py
```

---

## 3. Tool Inventory & Pinned Dependencies

| Tool / Package | Version | Purpose | Biological / Analytical Context |
| :--- | :--- | :--- | :--- |
| **Python** | 3.11 | Scripting & Validation | Parsing metadata, validating samplesheets, QC automation |
| **R** | 4.3.2 | Statistical Computing | Core computational engine for differential expression & plots |
| **OpenJDK** | 17.0.8 | JVM Runtime | Execution runtime for Nextflow workflow manager |
| **Nextflow** | >=23.10.0 | Workflow Engine | Orchestration, parallelization, failure retries, provenance |
| **FastQC** | 0.12.1 | Raw Quality Control | Per-base quality scores, GC bias, adapter detection |
| **fastp** | 0.23.4 | Read Preprocessing | Ultra-fast adapter trimming, quality filtering, polyG clipping |
| **STAR** | 2.7.11b | Splice-Aware Alignment | Maps reads across spliced intron-exon junctions to genome |
| **SAMtools** | 1.19.2 | High-Throughput SAM/BAM | BAM sorting, indexing, alignment flags, and statistics |
| **Salmon** | 1.10.3 | Transcript Quantification| Alignment-free quasi-mapping and transcript abundance (TPM) |
| **subread (featureCounts)**| 2.0.6 | Gene Summarization | Assigns mapped reads to genomic features (exons/genes) |
| **RSeQC** | 5.0.3 | RNA-seq Specific QC | Assesses gene body coverage, strandedness, junction saturation |
| **MultiQC** | 1.21 | QC Aggregator | Combines reports from all tools into a single HTML dashboard |
| **DESeq2** | 1.42.0 | Differential Expression | Negative Binomial GLM modeling for differential gene expression|
| **clusterProfiler** | 4.10.0 | Functional Enrichment | Over-representation analysis (ORA) and GSEA for GO & KEGG |
| **pheatmap / ggplot2** | Pinned | Visualization | Clustered expression heatmaps, PCA, volcano & MA plots |

---

## 4. Troubleshooting Common Environment Issues

1. **WSL Memory Constraints**:
   By default, WSL2 can allocate up to 50% of total host RAM. For human genome STAR alignment (which requires ~30GB RAM for whole genome index), create a `.wslconfig` file in your Windows user home directory (`C:\Users\<Username>\.wslconfig`):
   ```ini
   [wsl2]
   memory=16GB
   swap=16GB
   processors=4
   ```
   *(For test/tutorial datasets, we use small subset genomes requiring < 2GB RAM).*

2. **Conda Solving Speed**:
   Always use `mamba` instead of vanilla `conda` for resolving bioinformatics dependencies to avoid protracted solver timeouts.
