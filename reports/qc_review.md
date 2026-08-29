# Quality Control Review & Diagnostic Assessment

## 1. Study & Dataset Identification
* **Dataset Accession**: GEO: [GSE52778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52778) / BioProject: [PRJNA229998](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA229998)
* **Biological Organism**: *Homo sapiens* (Human)
* **Cell Type**: Primary Human Airway Smooth Muscle (ASM) cells
* **Treatment**: 1 $\mu\text{M}$ Dexamethasone (Dex) for 18 hours vs untreated vehicle control
* **Total Biological Samples**: 6 (`C1`, `T1`, `C2`, `T2`, `C3`, `T3`)
* **Total FASTQ Files**: 12 paired-end files (`SRR1039508`–`SRR1039517`, R1 and R2)
* **Sequencing Platform**: Illumina HiSeq 2000 ($2 \times 63$ bp)

---

## 2. Experimental Design Matrix

| Biological Sample | Condition | Donor ID | Replicate | FASTQ Pair (Forward / Reverse) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `C1` | `control` | N61311 | 1 | `SRR1039508_1.fastq.gz` / `SRR1039508_2.fastq.gz` | Pending download |
| `T1` | `treatment` | N61311 | 1 | `SRR1039509_1.fastq.gz` / `SRR1039509_2.fastq.gz` | Pending download |
| `C2` | `control` | N052611 | 2 | `SRR1039512_1.fastq.gz` / `SRR1039512_2.fastq.gz` | Pending download |
| `T2` | `treatment` | N052611 | 2 | `SRR1039513_1.fastq.gz` / `SRR1039513_2.fastq.gz` | Pending download |
| `C3` | `control` | N080611 | 3 | `SRR1039516_1.fastq.gz` / `SRR1039516_2.fastq.gz` | Pending download |
| `T3` | `treatment` | N080611 | 3 | `SRR1039517_1.fastq.gz` / `SRR1039517_2.fastq.gz` | Pending download |

---

## 3. Methodological Criteria for QC Evaluation

### 3.1 Distinction Between Sequencing Entities:
* **FASTQ File Count (12)**: The physical compressed files stored on disk.
* **Sequencing Read Count**: Total read fragments ($2 \times \text{paired fragments}$ for paired-end sequencing).
* **Biological Sample Count (6)**: The distinct biological units of replication across 3 human donors.

### 3.2 Key QC Metric Diagnostic Rules:
1. **Per-Base Sequence Quality**:
   * *Criterion*: Phred scores ($Q$) must remain $>30$ across the majority of the read cycle. Minor drops ($Q > 25$) at cycle 60–63 are normal due to flow cell phasing.
2. **Per-Base Sequence Content**:
   * *Criterion*: Non-uniform nucleotide proportions in positions 1–12 are an expected, harmless biochemical signature of random hexamer reverse transcription priming in RNA-seq.
3. **Sequence Duplication**:
   * *Criterion*: High duplication levels in bulk RNA-seq reflect natural, high expression of abundant transcripts (e.g., housekeeping genes, actin, GAPDH). Deduplication must NOT be applied.
4. **Adapter Contamination**:
   * *Criterion*: Reads where cDNA inserts are shorter than 63 bp will contain Illumina Universal Adapter sequences at the 3' end and must be trimmed in Phase 5 via `fastp`.

---

## 4. Execution State & Next Steps
* **Environment**: Execution requires WSL2 / Ubuntu runtime with `fastqc` and `multiqc` active in Conda (`rnaseq-pipeline`).
* **Staging**: Execute `bash scripts/download_dataset.sh` inside WSL2 to retrieve raw reads and verify MD5 checksums prior to FastQC/MultiQC batch processing.
