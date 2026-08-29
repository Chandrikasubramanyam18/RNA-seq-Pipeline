# Quality Control Assessment & Biological Interpretation Guide

## 1. Fundamentals of Sequencing Data Quality

The transition from a physical RNA molecule to a digital FASTQ file follows a multi-step biochemical and computational progression:

```
Biological RNA
      │ (Reverse Transcription & cDNA Fragmentation)
      ▼
cDNA Library (with ligated sequencing adapters)
      │ (Illumina Bridge Amplification on Flow Cell)
      ▼
Fluorescent Cluster Imaging (Cycle-by-cycle 4-color or 2-color chemistry)
      │ (Base Calling Algorithm, e.g., Illumina RTA / bcl2fastq)
      ▼
Base Calls + Phred Quality Scores ($Q$)
      │
      ▼
FASTQ Raw Sequencing Reads
      │
      ▼
FastQC (Per-sample quality metric profiling)
      │
      ▼
MultiQC (Multi-sample consolidated quality dashboard)
```

---

## 2. Anatomy of a FASTQ Record

Every sequencing read in a FASTQ file is represented by a 4-line block:

```text
@SRR1039508.1 HWI-ST1182:144:D1DVKACXX:5:1101:1234:2145 length=63
NTGACCGTTAGGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTA
+
#<<BBFFFFFFFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
```

* **Line 1 (`@`)**: Sequence Identifier (Instrument ID, Flow cell ID, Tile coordinates, Pair direction `1` or `2`).
* **Line 2**: The raw called nucleotide sequence (`A`, `C`, `G`, `T`, or ambiguous `N`).
* **Line 3 (`+`)**: Separator (optionally repeats sequence ID).
* **Line 4**: ASCII-encoded Phred quality scores corresponding 1-to-1 with nucleotides in Line 2.

---

## 3. Understanding Phred Quality Scores ($Q$)

Phred quality scores measure the probability ($P$) that a given base was called incorrectly by the sequencer's optical detector:

$$Q = -10 \log_{10}(P)$$

| Phred Score ($Q$) | Error Probability ($P$) | Base Call Accuracy | Standard Interpretation |
| :--- | :--- | :--- | :--- |
| **Q10** | $1 \text{ in } 10$ ($0.1$) | **90.0%** | Poor / Unacceptable |
| **Q20** | $1 \text{ in } 100$ ($0.01$) | **99.0%** | Standard Quality Benchmark (fastp default) |
| **Q30** | $1 \text{ in } 1,000$ ($0.001$) | **99.9%** | High-Quality Sequencing Standard |
| **Q40** | $1 \text{ in } 10,000$ ($0.0001$) | **99.99%** | Exceptional Base Call Confidence |

---

## 4. Key FastQC Modules & Biological Interpretation

### 4.1 Per-Base Sequence Quality
* **What it measures**: The distribution of Phred quality scores across every sequencing cycle (base position from 1 to read length).
* **Expected Profile**: High quality ($Q > 30$) across the 5' and middle of the read, with a slight, natural decline towards the 3' end due to fluorophore degradation and phasing/pre-phasing accumulation in Illumina flow cells.
* **Troubleshooting**: Severe drops ($Q < 20$) in the first 10 bp or premature 3' degradation require quality trimming in Phase 5 (`fastp`).

### 4.2 Per-Base Sequence Content & GC Distribution
* **What it measures**: The relative proportion of `A`, `T`, `C`, and `G` at each cycle, and the overall %GC distribution across reads compared to a theoretical normal curve.
* **RNA-seq Context**: In RNA-seq, random hexamer priming used during reverse transcription introduces a well-known, harmless non-random nucleotide bias in the first 9–12 bp. FastQC often marks this as **WARN** or **FAIL**. This is an expected biochemical artifact of cDNA synthesis, not sample degradation.

### 4.3 Sequence Duplication Levels
* **What it measures**: The percentage of identical reads in the library.
* **RNA-seq vs WGS**: In Whole Genome Sequencing (WGS), high duplication usually indicates PCR amplification bias. In **bulk RNA-seq**, however, highly expressed housekeeping genes (e.g., *GAPDH*, *ACTB*, *EEF1A1*, mitochondrial transcripts) naturally produce millions of identical transcript fragments. **Do NOT deduplicate bulk RNA-seq data**, as doing so artificially flattens true biological expression dynamics.

### 4.4 Adapter Content
* **What it measures**: Detection of Illumina Universal or Nextera adapter read-through.
* **Why it happens**: When cDNA fragment lengths are shorter than the sequencing read length (e.g., a 45 bp cDNA insert sequenced with 63 bp reads), the sequencer reads past the biological insert and into the synthetic 3' adapter.
* **Action**: Adapter sequences must be trimmed by `fastp` before alignment to prevent mapping penalties in STAR.

---

## 5. Summary of Multi-Sample Comparison for GSE52778

When reviewing the combined **MultiQC** report across our 6 biological samples (`C1, T1, C2, T2, C3, T3`):

1. **Sequencing Depth Uniformity**: Ensure all samples have comparable total read counts (typically 15–30 million reads per library).
2. **Replicate Consistency**: Confirm that control and treated replicates from the same donor exhibit similar GC content and quality distributions.
3. **No Automatic Sample Rejection**: Flagged modules (such as GC bias or duplication) are documented and evaluated in biological context rather than discarded.
