# Chapter 15: featureCounts

> The tool that summarizes aligned reads into a gene-level count
> matrix -- the input to differential expression analysis.

---

## 1. What is it?

**featureCounts** (part of the `subread` package) assigns aligned reads
(in BAM) to genomic **features** (genes/exons, defined by the GTF) and
produces a **count matrix** of how many reads map to each gene in each
sample.

It is the bridge between **alignments** (BAM) and **gene expression**
(count matrix).

---

## 2. Why do we need it?

DESeq2 (and other DE tools) need a **gene x sample count matrix** --
integer counts of reads per gene per sample. featureCounts produces
exactly this from BAM + GTF.

Without counting, we have coordinates but no gene-level expression.

---

## 3. Where does it fit?

```
Sorted BAM (Ch 13) + GTF (Ch 07)
        |
        v
   featureCounts  <--- here
        |
        v
   gene_counts.txt (gene x sample matrix)
        |
        v
   DESeq2 (Ch 18)
```

This is the **genome-based counting** path (parallel to Salmon).

---

## 4. Input

- **Coordinate-sorted, indexed BAM** files (from SAMtools)
- **GTF** annotation (`data/reference/genes.gtf`)

---

## 5. Output

| File | Description |
|------|-------------|
| `gene_counts.txt` | Gene x sample count matrix |
| `*_summary` | Assignment statistics |

Stored in `results/counts/`.

---

## 6. How it works

### 6.1 Feature assignment

featureCounts counts reads that **overlap exons** of each gene. A read
is assigned to a gene if it overlaps the gene's exons (using the GTF).

### 6.2 Parameters that matter

| Parameter | Purpose |
|-----------|---------|
| `-a genes.gtf` | Annotation file |
| `-o output.txt` | Output matrix |
| `-p` | Paired-end mode |
| `-s 0/1/2` | Strandness (0=unstranded, 1=stranded, 2=reverse) |
| `-T threads` | Threads |
| `-t exon` | Count at exon level |
| `-g gene_id` | Summarize by gene_id |

### 6.3 Strandness

Critical for our dataset: GSE52778 is **non-stranded** (poly-A,
non-stranded). So `-s 0` (unstranded) is correct. Getting strandness
wrong halves effective counts.

---

## 7. Biology behind it

- The count matrix represents **gene expression** at the gene level.
- Reads spanning junctions (CIGAR `N`) are counted for the gene.
- Multi-mapping reads are handled conservatively (assigned to one
  location or excluded).
- Strandness reflects whether the library preserved mRNA direction.

---

## 8. Command

```bash
# featureCounts (standard; part of future workflow)
featureCounts \
    -a data/reference/genes.gtf \
    -o results/counts/gene_counts.txt \
    -T 8 \
    -p \
    -s 0 \
    results/alignment/C1_sorted.bam \
    results/alignment/C2_sorted.bam \
    results/alignment/C3_sorted.bam \
    results/alignment/T1_sorted.bam \
    results/alignment/T2_sorted.bam \
    results/alignment/T3_sorted.bam
```

---

## 9. Example

`gene_counts.txt` (gene x sample):

| Geneid | Chr | Start | End | C1 | C2 | C3 | T1 | T2 | T3 |
|--------|-----|-------|-----|----|----|----|----|----|----|
| ENSG00000103196 | chr16 | ... | ... | 420 | 390 | 450 | 2450 | 2380 | 2510 |
| ENSG00000111640 | chr12 | ... | ... | 8500 | 8420 | 8610 | 8490 | 8520 | 8450 |

This is the raw input to DESeq2.

---

## 10. How to read the output

| Content | Meaning |
|---------|---------|
| Geneid | Gene identifier (from gtf `gene_id`) |
| Sample columns | Raw read counts per sample |
| Assignment summary % | Fraction of reads assigned to genes |

A high assignment rate (`% assigned`) indicates good alignment and
annotation match.

---

## 11. Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| Zero counts for a gene | Chromosome naming mismatch | Fix FASTA/GTF naming |
| Low assignment % | Unsorted BAM / wrong strand | Sort BAM; set `-s` correctly |
| Strandness error | Wrong `-s` | Confirm library type (unstranded here) |
| Multi-map handling | Ambiguous reads | Use default (count once) |

---

## 12. Limitations

- Counts are **gene-level**; isoform resolution needs Salmon.
- Requires accurate strandness and annotation.
- Multi-mapping reads ambiguity can bias counts.

---

## 13. How our project uses it

- featureCounts produces `results/counts/gene_counts.txt`.
- This is the raw input to DESeq2 (Ch 18).
- The workflow architecture documents featureCounts after STAR/SAMtools.
- Actual featureCounts execution is part of the **future** Nextflow
  workflow.

---

## 14. Official documentation

- **featureCounts / subread**:
  https://subread.sourceforge.net/
- **featureCounts paper** (Liao et al. 2014, Bioinformatics):
  https://academic.oup.com/bioinformatics/article/30/7/923/232889

---

## 15. Mini exercise

1. What functional matrix does featureCounts output, and why is it the
   input to DESeq2?
2. Why is the strandness parameter (`-s`) important, and what value is
   correct for our non-stranded dataset?
3. How does featureCounts connect BAM alignments to the GTF annotation?
4. Why would a chromosome-naming mismatch cause zero counts?
5. How does the featureCounts path relate to the parallel Salmon path?

---

**End of Quantification phase.**

> **Next**: [Chapter 16: Statistics Fundamentals](../06_statistics/statistics.md)
