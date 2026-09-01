# Chapter 13: SAMtools

> The toolkit for manipulating SAM/BAM alignment files -- sorting,
> indexing, statistics, and filtering. It turns raw STAR output into
> organized, queryable BAMs.

---

## 1. What is it?

**SAMtools** is a suite of tools for reading, writing, querying, and
processing SAM/BAM files. It is fundamental to alignment post-
processing.

Common operations in RNA-seq:
- `samtools sort` -- coordinate-sort a BAM
- `samtools index` -- build a `.bai` index
- `samtools flagstat` -- mapping statistics
- `samtools idxstats` -- per-chromosome counts
- `samtools view` -- view/filter alignments

---

## 2. Why do we need it?

- **featureCounts** needs a **coordinate-sorted, indexed** BAM.
- Mapping statistics (**flagstat**) tell you the alignment rate.
- Indexing enables fast region queries and downstream tools.

---

## 3. Where does it fit?

```
STAR (Ch 12) -> SAM -> SAMtools (sort/index) -> BAM  <--- here
                                    |
                                    +--> featureCounts (Ch 15)
                                    +--> RSeQC
```

---

## 4. Input

- Raw SAM/BAM from STAR (per sample).
- These would be in `results/alignment/`.

---

## 5. Output

Per sample:

| File | Description |
|------|-------------|
| `*_sorted.bam` | Coordinate-sorted alignments |
| `*_sorted.bam.bai` | BAM index |
| `*.flagstat` | Mapping statistics |
| `*.idxstats` | Per-chromosome stats |

---

## 6. How it works

### 6.1 Sorting

Coordinate-sorting orders alignments by (chromosome, position), which
is required for efficient random access and for featureCounts.

```bash
samtools sort -o sample_sorted.bam sample.bam
```

### 6.2 Indexing

Produces a `.bai` file that allows fast position-based lookup:

```bash
samtools index sample_sorted.bam   # -> sample_sorted.bam.bai
```

### 6.3 flagstat

Summarizes alignment flags (Chapter 06) into counts:

```bash
samtools flagstat sample_sorted.bam
```

### 6.4 idxstats

Reports mapped reads per chromosome:

```bash
samtools idxstats sample_sorted.bam
```

---

## 7. Biology behind it

- **flagstat** quantifies mapping quality (uniquely mapped,
  properly paired), which reflects library quality.
- **Per-chromosome counts** (idxstats) reveal where reads land;
  anomalies (e.g., lots of mitochondrial reads) can flag contamination.

---

## 8. Command

```bash
# Sort
samtools sort -o results/alignment/C1_sorted.bam results/alignment/C1.bam

# Index
samtools index results/alignment/C1_sorted.bam

# Statistics
samtools flagstat results/alignment/C1_sorted.bam
samtools idxstats results/alignment/C1_sorted.bam

# View first alignments
samtools view results/alignment/C1_sorted.bam | head
```

---

## 9. Example

`flagstat` output:

```
20000000 + 0 in total (QC-passed reads + 0 failed)
18700000 + 0 mapped (93.5% : N/A)
19500000 + 0 paired in sequencing
19000000 + 0 properly paired (97.4% : N/A)
```

- 93.5% mapped, 97.4% properly paired -- good quality.

---

## 10. How to read the output

| Metric | Meaning | Good value |
|--------|---------|-----------|
| mapped % | Reads that aligned | >85-90% |
| properly paired % | Both mates, correct orientation | high |
| % duplicates | PCR duplicates (flag 1024) | low in unique-mapped view |

---

## 11. Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Could not find index" | `.bai` missing | Run `samtools index` |
| "Unsorted BAM" | Not coordinate-sorted | Run `samtools sort` |
| Low mapped % | Trimming/quality | Improve preprocessing |
| Out of memory sorting | Large BAM | More RAM / sort by chunk |

---

## 12. Limitations

- SAMtools operates on alignments, not genes; counting still needs
  featureCounts.
- Large BAMs are disk/memory heavy.
- It doesn't do quantification itself.

---

## 13. How our project uses it

- The workflow architecture documents SAMtools sort, index, flagstat,
  and idxstats after STAR.
- These BAMs feed featureCounts and RSeQC.
- Actual SAMtools execution is part of the **future** Nextflow
  workflow (scripts/alignment not yet implemented).

---

## 14. Official documentation

- **SAMtools**:
  https://www.htslib.org/doc/samtools.html
- **SAM spec**:
  https://samtools.github.io/hts-specs/SAMv1.pdf

---

## 15. Mini exercise

1. Why must a BAM be coordinate-sorted before featureCounts?
2. What does `samtools index` produce, and why is it needed?
3. Distinguish `flagstat` from `idxstats`.
4. Given 20M total and 18.7M mapped, calculate the mapped %.
5. Which downstream tools in our pipeline consume sorted BAMs?

---

**End of Alignment phase.**

> **Next**: [Chapter 14: Salmon](../05_quantification/salmon.md)
