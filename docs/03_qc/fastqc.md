# Chapter 08: FastQC

> The first quality-control tool in the pipeline. FastQC profiles raw
> sequencing reads and flags problems before they propagate through
> alignment and quantification.

---

## 1. What is it?

**FastQC** is a tool that produces a set of **quality control reports**
for raw high-throughput sequencing reads. It analyzes a FASTQ file and
generates an HTML report (plus a zip archive) summarizing metrics like:

- Per-base quality
- GC content
- Adapter content
- Sequence duplication
- Overrepresented sequences

Each module is given a status of **PASS**, **WARN**, or **FAIL**.

---

## 2. Why do we need it?

- Sequencing data can be **low-quality** or **contaminated**.
- Problems detected early (adapters, poor base calls, low complexity)
  can be fixed by trimming (fastp) before alignment.
- It is far cheaper to catch issues at the read level than after
  alignment.
- FastQC is the standard, unbiased first look at any dataset.

---

## 3. Where does it fit?

```
FASTQ (Ch 04) -> FastQC (raw QC)  <--- here (first step)
                    |
                    v
                fastp (trim)
                    |
                    v
              FastQC (clean QC)
                    |
                    v
           MultiQC (aggregate, Ch 10)
```

We run FastQC **twice**: once on raw reads and once on trimmed reads,
to confirm trimming improved quality.

---

## 4. Input

- One or more FASTQ files (raw reads from `data/raw/`).
- For our study: 12 FASTQ files (6 samples x 2 mates).

Command to run on raw reads:

```bash
bash scripts/run_fastqc.sh --input data/raw --output results/fastqc/raw --threads 4
```

---

## 5. Output

For each FASTQ file, FastQC produces:

| File | Description |
|------|-------------|
| `*_fastqc.html` | Human-readable HTML report |
| `*_fastqc.zip` | Machine-readable data (fastqc_data.txt, etc.) |

These go into `results/fastqc/raw/` (and later `results/fastqc/clean/`).

Our parser (`summarize_fastqc.py`) converts these into a TSV summary:
`results/fastqc/raw/fastqc_summary.tsv`.

---

## 6. How it works

FastQC reads the FASTQ line-by-line, computes statistics, and scores
each module. Key modules:

### 6.1 Per-Base Sequence Quality

Average Phred quality at each position across all reads.

- **Expected**: Q > 30 through most of the read, slight 3' decline.
- **FAIL**: quality drops early / dramatically.

### 6.2 Per-Tile Sequence Quality

Quality by flow-cell tile. Flags localized issues (e.g., bubbles,
retention) on the flow cell.

### 6.3 Per-Sequence Quality Scores

Distribution of mean quality across reads. Should be a single peak
near high Q.

### 6.4 Per-Base Sequence Content

Proportion of A/C/G/T at each position.

- **RNA-seq note**: random hexamer priming causes non-uniform content
  in the first 9-12 bases. This produces a WARN/FAIL that is
  **biologically expected**, not a real problem.

### 6.5 Per-Sequence GC Content

GC% distribution compared to a theoretical normal curve.

- RNA-seq transcripts have natural GC variation; moderate deviations
  are common.

### 6.6 Duplication Levels

How many reads are identical.

- **RNA-seq note**: highly expressed genes (GAPDH, ACTB, ribosomal)
  produce millions of identical reads. **Do NOT deduplicate bulk
  RNA-seq** -- this is real biological signal, not PCR bias.

### 6.7 Adapter Content

Presence of Illumina adapter sequences read through.

- Happens when cDNA insert < read length.
- **Indicates trimming is needed** (fastp, Ch 09).

### 6.8 Overrepresented Sequences

Sequences appearing far more often than expected (adapters, rRNA,
high-copy transcripts).

---

## 7. Biology behind it

- Quality scores reflect sequencing chemistry (Chapter 04).
- Adapter content arises because short cDNA inserts (< 63 bp) cause
  read-through into adapters.
- Duplication from abundant transcripts is biological, not technical.
- GC bias can affect coverage of genes.

---

## 8. Command

```bash
# Raw QC (implemented script)
bash scripts/run_fastqc.sh --input data/raw --output results/fastqc/raw --threads 4

# Clean QC after trimming
bash scripts/run_fastqc.sh --input data/processed --output results/fastqc/clean --threads 4

# Parse FastQC reports to TSV summary (implemented)
python3 scripts/python/summarize_fastqc.py \
    --input-dir results/fastqc/raw \
    --output results/fastqc/raw/fastqc_summary.tsv
```

---

## 9. Example

Sample `fastqc_data.txt` (from our `summarize_fastqc.py` test):

```
>>Basic Statistics pass
Filename  SRR1039508_1.fastq.gz
Total Sequences  1000000
Sequence length  63
%GC  49
>>Per base sequence quality pass
>>Per sequence GC content warn
>>Adapter Content pass
```

- Quality passes
- GC flagged warn (expected for RNA-seq)
- Adapters pass (this library happens to be clean)

---

## 10. How to read the output

Status flags:

| Status | Meaning | Action |
|--------|---------|--------|
| PASS | Within expected range | None |
| WARN | Slightly unusual | Review in biological context |
| FAIL | Outside expected range | Fix (trim, re-sequence) |

For RNA-seq, common WARN/FAIL that are **acceptable**:
- Per-base sequence content (hexamer priming bias)
- Sequence duplication (highly expressed genes)

Common FAIL that **needs action**:
- Adapter content -> trim
- Per-base quality -> quality trim

---

## 11. Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| Adapter content FAIL | Short inserts read through | fastp adapter trimming |
| Low 3' quality | Chemistry / degradation | Quality trim (fastp) |
| High duplication FAIL | Abundant transcripts | Accept (RNA-seq) |
| Content bias WARN | Hexamer priming | Accept (RNA-seq) |
| Fail to parse | Missing/corrupt reports | Re-run FastQC |

---

## 12. Limitations

- FastQC reports per-file; comparing many samples needs MultiQC
  (Ch 10).
- It flags technical issues but is not a substitute for biological
  interpretation.
- WARN/FAIL statuses are heuristic; context matters.

---

## 13. How our project uses it

- `run_fastqc.sh` runs FastQC on raw and processed reads.
- `summarize_fastqc.py` parses results into a TSV.
- Results stored in `results/fastqc/`.
- The parser has **5 passing unit tests**
  (`tests/unit/test_qc_summary.py`).

---

## 14. Official documentation

- **Babraham Bioinformatics FastQC**:
  https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
- **FastQC at nf-core/rnaseq** (usage):
  https://nf-co.re/rnaseq

---

## 15. Mini exercise

1. List the metadata fields that `summarize_fastqc.py` extracts.
2. Why do we run FastQC both before and after trimming?
3. Explain why high duplication is *expected* (not a problem) in bulk
   RNA-seq.
4. Which FastQC module tells us trimming is needed?
5. Look at `tests/unit/test_qc_summary.py` and name the 5 things it
   tests.

---

> **Next**: [Chapter 09: fastp](fastp.md)
