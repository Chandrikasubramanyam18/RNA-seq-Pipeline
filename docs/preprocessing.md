# Read Preprocessing & Trimming Guide (fastp)

## 1. Why Read Preprocessing is Essential

Raw sequencer output contains technical artifacts that degrade alignment accuracy and distort downstream transcript quantification if left unaddressed:

```
Raw Paired-End Reads (data/raw/)
               │
               ▼
   [fastp Multi-Stage Engine]
   ├── 1. Automated Adapter Detection & Clipping
   ├── 2. Poly-G / Poly-X Tail Trimming
   ├── 3. Sliding-Window Quality Filtering (Q >= 20)
   ├── 4. Low-Complexity & N-base Dropping
   └── 5. Minimum Read Length Filtering (>= 30 bp)
               │
               ▼
Cleaned, Analysis-Ready Reads (data/processed/)
```

---

## 2. Core Preprocessing Operations

### 2.1 Adapter Clipping (Overlap Detection in Paired-End Sequencing)
* **The Biological/Technical Problem**: When the biological cDNA insert is shorter than the read length (63 bp in our GSE52778 dataset), the sequencer reads past the cDNA fragment and sequences the synthetic 3' adapter.
* **How fastp Solves It**: `fastp` automatically aligns paired-end read 1 and read 2. Because both reads originate from the opposite ends of the exact same physical cDNA fragment, any sequence extending beyond the insert overlap represents the adapter sequence, enabling precise adapter trimming without requiring manual adapter sequence specifications.

### 2.2 Poly-G Tail Clipping (Two-Color Illumina Chemistry)
* **The Problem**: In two-color Illumina systems (NextSeq, NovaSeq), a base call of **G** is registered when *neither* red nor green fluorophores emit a signal (dark cycles). As the sequencing reagents deplete towards the 3' end, the sequencer defaults to calling endless runs of `GGGGGG...` with high Phred scores.
* **fastp Solution**: `--trim_poly_g` automatically detects and clips trailing poly-G artifacts.

### 2.3 Sliding-Window Quality Filtering ($Q \ge 20$)
* **Mechanism**: Bases are scanned in a sliding window (default 4 bp). If the average Phred score drops below $Q20$ (99% base call accuracy), the low-quality tail is trimmed.
* **Length Filtering**: If trimming reduces a read below 30 bp (`--length_required 30`), the read is discarded to prevent ambiguous multi-mapping in STAR.

---

## 3. Data Integrity & Safety Principles

1. **Immutable Raw Data**: Raw FASTQ files in `data/raw/` remain 100% untouched.
2. **Dedicated Target Directory**: All trimmed outputs are directed to `data/processed/`.
3. **Structured Metrics**: `fastp` outputs both interactive HTML reports (`results/fastp/*.html`) and structured JSON logs (`results/fastp/*.json`).

---

## 4. Execution Command Reference

```bash
# Execute fastp across samplesheet design
bash scripts/run_fastp.sh \
    --samplesheet metadata/samplesheet.csv \
    --out-fastq data/processed \
    --out-report results/fastp \
    --threads 4 \
    --quality 20 \
    --min-length 30

# Aggregate JSON reports into tabular summary
python3 scripts/python/summarize_fastp.py \
    --input-dir results/fastp \
    --output results/fastp/fastp_summary.tsv
```
