# Chapter 09: fastp

> The read preprocessing tool that trims adapters, removes
> low-quality bases, and filters reads before alignment. Fastp turns
> raw reads into clean, analysis-ready reads.

---

## 1. What is it?

**fastp** is an ultra-fast, all-in-one read preprocessing tool. It
performs:

- **Adapter trimming** (with automatic detection for paired-end)
- **Poly-G / poly-X tail clipping**
- **Quality filtering** (sliding window)
- **Length filtering**
- **Low-complexity / N filtering**

It outputs cleaned reads plus HTML/JSON reports with before/after
metrics.

---

## 2. Why do we need it?

Raw sequencing reads contain technical artifacts that hurt alignment
and quantification:

- **Adapters** read through when cDNA insert < read length
- **Low-quality 3' ends** cause misalignment
- **Poly-G** tails from 2-color Illumina chemistry
- **Short, low-quality reads** map ambiguously

Trimming these improves mapping and makes downstream counts reliable.

---

## 3. Where does it fit?

```
FASTQ (raw) -> FastQC (Ch 08) -> fastp  <--- here
                                    |
                                    v
                    cleaned FASTQ (data/processed)
                                    |
                                    +--> FastQC (clean)
                                    +--> STAR (Ch 12)
                                    +--> Salmon (Ch 14)
```

---

## 4. Input

- Raw FASTQ files (from the samplesheet)
- The samplesheet `metadata/samplesheet.csv` defines pairing

Command:

```bash
bash scripts/run_fastp.sh \
    --samplesheet metadata/samplesheet.csv \
    --out-fastq data/processed \
    --out-report results/fastp \
    --threads 4
```

---

## 5. Output

Per sample:

| File | Description |
|------|-------------|
| `*_trimmed_R1.fastq.gz` | Cleaned forward reads |
| `*_trimmed_R2.fastq.gz` | Cleaned reverse reads |
| `*_fastp.html` | Interactive HTML report |
| `*_fastp.json` | Machine-readable metrics |

These go in `data/processed/` and `results/fastp/`.

---

## 6. How it works

### 6.1 Adapter detection (paired-end overlap)

Because R1 and R2 come from opposite ends of the same fragment, if the
insert is shorter than the read, the two reads **overlap in adapter
sequence**. fastp aligns R1 and R2 to each other and trims the
overlapping adapter region -- no adapter sequence needed.

### 6.2 Poly-G trimming

In 2-color Illumina (NextSeq/NovaSeq), a dark cycle (no signal) is
called as G. When reagents deplete at the 3' end, reads end in
`GGGGG...`. fastp's `--trim_poly_g` clips these.

Note: our dataset is HiSeq 2000 (4-color), so poly-G is not a real
issue, but the flag is harmless and future-proof.

### 6.3 Sliding-window quality filter

fastp scans bases in a 4-base window. If the average Phred drops below
the threshold (Q20 by default), the tail is trimmed.

### 6.4 Length filter

Reads trimmed below `--length_required` (30 bp) are discarded, since
short reads multi-map ambiguously in STAR.

### 6.5 Our parameters

From `run_fastp.sh`:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--qualified_quality_phred` | 20 | Quality threshold (99% accuracy) |
| `--length_required` | 30 | Minimum read length |
| `--detect_adapter_for_pe` | on | Auto adapter detection |
| `--trim_poly_g` | on | Poly-G clipping |
| `--trim_poly_x` | on | Homopolymer tail clipping |

---

## 7. Biology behind it

- Adapter contamination arises from short cDNA fragments — a physical
  property of the library.
- Removing low-quality bases prevents erroneous base calls from
  creating false mismatches/misalignments.
- Sufficient read length (>=30) is needed for confident unique
  mapping.

---

## 8. Command

```bash
bash scripts/run_fastp.sh \
    --samplesheet metadata/samplesheet.csv \
    --out-fastq data/processed \
    --out-report results/fastp \
    --threads 4 \
    --quality 20 \
    --min-length 30

# Summarize fastp JSON reports to TSV (implemented)
python3 scripts/python/summarize_fastp.py \
    --input-dir results/fastp \
    --output results/fastp/fastp_summary.tsv
```

---

## 9. Example

The fastp summary TSV (`summarize_fastp.py`) columns include:

| sample | raw_total_reads | clean_total_reads | filter_drop_rate_pct | q20_after | adapter_trimmed_reads |
|--------|-----------------|-------------------|----------------------|-----------|------------------------|
| C1 | 20,000,000 | 19,600,000 | 2.00 | 98.4% | 450,000 |

A drop rate under ~5% is expected for high-quality Illumina data.

---

## 10. How to read the output

From the JSON / summary:

| Metric | Meaning | Good value |
|--------|---------|-----------|
| Raw reads | Reads before filtering | -- |
| Clean reads | Reads after filtering | <5% drop |
| Q20/Q30 rate | Base accuracy | >95% / >90% |
| Adapter trimmed | Reads with adapters removed | varies |
| Duplication rate | Sequencing duplicates | minor |

---

## 11. Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| R1/R2 count mismatch | Paired files out of sync | Re-run; verify pairing |
| Too many reads dropped | Overly strict thresholds | Lower quality/length cutoffs |
| Adapters still present | Wrong layout | Ensure paired-end mode |
| Greyed/empty report | Empty input | Check input paths |

---

## 12. Limitations

- fastp is heuristic; parameters must suit the platform/library.
- Poly-G trimming is unnecessary for 4-color chemistry (harmless).
- It cannot fix fundamentally degraded RNA (that's upstream).

---

## 13. How our project uses it

- `run_fastp.sh` processes all 6 samples from the samplesheet.
- `summarize_fastp.py` produces a TSV with **3 passing unit tests**
  (`tests/unit/test_fastp_summary.py`).
- Cleaned reads are stored in `data/processed/` for alignment.
- Reports go to `results/fastp/`.

---

## 14. Official documentation

- **fastp GitHub**:
  https://github.com/OpenGene/fastp
- **fastp paper** (Chen et al. 2018, Bioinformatics):
  https://academic.oup.com/bioinformatics/article/34/17/i884/5093234

---

## 15. Mini exercise

1. Explain how fastp detects adapters in paired-end data without
   knowing the adapter sequence.
2. What do `--qualified_quality_phred 20` and `--length_required 30`
   do?
3. Why is poly-G clipping harmless-but-unnecessary on our HiSeq 2000
   dataset?
4. What metrics does `summarize_fastp.py` extract, and which 3 things
   do its unit tests verify?
5. If trimmed reads drop 40%, is that a problem? What might cause it?

---

> **Next**: [Chapter 10: MultiQC](multiqc.md)
