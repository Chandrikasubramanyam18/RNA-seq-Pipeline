# Chapter 10: MultiQC

> The aggregation tool that combines QC reports from many tools and
> many samples into a single interactive HTML dashboard.

---

## 1. What is it?

**MultiQC** parses the output files of many bioinformatics tools
(FastQC, fastp, STAR, SAMtools, Salmon, RSeQC) and combines them into
**one** interactive HTML report with:

- General statistics tables
- Plots summary across all samples
- Filters and sample-specific views
- A unified view of the whole dataset's quality

---

## 2. Why do we need it?

FastQC reports are per-file; with 12 FASTQ files (and later BAMs),
reviewing each individually is tedious and error-prone. MultiQC:

- Aggregates everything into one report
- Highlights samples that look different (outliers)
- Lets you check QC across all samples at a glance

---

## 3. Where does it fit?

MultiQC is an **aggregation layer**, not a sequential computational
step. It consumes outputs from many stages:

```
FastQC (Ch 08) ---+
fastp (Ch 09)  ---+
STAR (Ch 12)   ---+---> MultiQC  <--- here
SAMtools (Ch13)---+
Salmon (Ch 14) ---+
RSeQC           ---+
                    |
                    v
          unified QC report (results/multiqc/)
```

---

## 4. Input

- FastQC report directories
- fastp HTML/JSON reports
- STAR log files
- SAMtools flagstat outputs
- Salmon log files
- RSeQC outputs

---

## 5. Output

| File | Description |
|------|-------------|
| `multiqc_report.html` | Interactive consolidated report |
| `multiqc_data/` | Machine-readable JSON/TSV data |

Stored in `results/multiqc/`.

---

## 6. How it works

MultiQC searches the input directory for files matching known tool
patterns (e.g., `fastqc_data.txt`, `*_fastp.json`, `*.flagstat`),
parses them, and renders combined tables and plots.

It supports sample renaming, filtering, and custom report titles.

---

## 7. Biology behind it

- MultiQC lets you compare **consistency across biological
  replicates** (C1-C3 should be similar, T1-T3 similar).
- It detects **outlier samples** early (e.g., one poor-quality
  library) that could confound differential expression.
- Sequencing depth consistency across samples matters for
  normalization.

---

## 8. Command

```bash
# Aggregate raw FastQC reports (implemented)
bash scripts/run_multiqc.sh \
    --input results/fastqc/raw \
    --output results/multiqc/raw_fastqc \
    --title "Raw Reads QC Report (FastQC)"
```

You can run it again on clean reads or other tool outputs.

---

## 9. Example

The general statistics table would show, per sample:

| Sample | % Dups | % GC | M Seqs | ... |
|--------|--------|------|--------|-----|
| C1 | 35 | 49 | 20 | ... |
| C2 | 34 | 48 | 20 | ... |
| T1 | 33 | 50 | 20 | ... |

A sample with drastically fewer sequences or different %GC would
stand out as an outlier.

---

## 10. How to read the output

- **General Statistics tab**: one row per sample; sort columns to find
  outliers.
- **Module sections**: each tool's metrics, all samples overlaid.
- **Filter/renaming**: group by sample or condition.

Look for:
- Consistent total reads across samples
- Consistent quality/gc
- No single outlier sample

---

## 11. Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| MultiQC finds no files | Wrong input dir or tool outputs missing | Point to correct dir |
| Sample names ignored | Custom naming needed | Use `--sample-names` / config |
| Duplicate module entries | Reporting same dir twice | Clean inputs |

---

## 12. Limitations

- MultiQC only reports what the input tools produced; it doesn't
  re-analyze raw data.
- It's a visualization/aggregation tool, not a QC decision maker.
- Interpreting "outliers" still requires biological judgment.

---

## 13. How our project uses it

- `run_multiqc.sh` aggregates raw QC into
  `results/multiqc/raw_fastqc/multiqc_report.html`.
- The workflow architecture (docs/workflow.md) shows MultiQC
  aggregating FastQC, fastp, STAR, SAMtools, Salmon, and RSeQC outputs.
- It's the visible "dashboard" of pipeline quality.

---

## 14. Official documentation

- **MultiQC website**:
  https://multiqc.info/
- **MultiQC GitHub**:
  https://github.com/MultiQC/MultiQC

---

## 15. Mini exercise

1. In your own words, why is MultiQC described as an aggregation
   layer rather than a sequential pipeline step?
2. Which tool outputs does our pipeline feed into MultiQC?
3. How would you detect a single poor-quality sample using MultiQC?
4. What is the primary output file, and where does our pipeline store
   it?
5. Why is it important that biological replicates show consistent QC
   metrics?

---

**End of QC phase.**

> **Next**: [Chapter 11: Reference Genome](../04_alignment/reference_genome.md)
