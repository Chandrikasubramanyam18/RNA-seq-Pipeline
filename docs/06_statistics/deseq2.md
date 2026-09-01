# Chapter 18: DESeq2

> The differential expression (DE) tool that takes the count matrix
> and outputs statistically-determined genes that change between
> conditions.

---

## 1. What is it?

**DESeq2** is an R/Bioconductor package for **differential expression
analysis**. It models raw read counts with a **negative binomial
distribution**, estimates dispersion, applies size-factor
normalization (Ch 17), and tests each gene for differential expression
between conditions.

Output: a results table with log2 fold change, p-values, and adjusted
p-values (FDR) per gene.

---

## 2. Why do we need it?

- It's the standard, rigorous way to find genes that differ between
  control and dexamethasone-treated cells.
- Handles over-dispersion, small replicate numbers, and multiple
  testing.
- Produces the gene list that drives all downstream analysis (volcano,
  heatmap, pathways).

---

## 3. Where does it fit?

```
Count matrix (Ch 15) -> DESeq2  <--- here -> results table
                              |
                              +--> volcano (Ch 20)
                              +--> heatmap (Ch 21)
                              +--> pathway (Ch 22-24)
```

---

## 4. Input

- **Count matrix**: gene x sample (featureCounts, Ch 15)
- **ColData**: sample metadata (condition C/T) -- `metadata/`.

---

## 5. Output

A results table per gene:

| Column | Meaning |
|--------|---------|
| baseMean | Mean normalized count |
| log2FoldChange | log2(T/C) change |
| lfcSE | Std error |
| stat | Wald statistic |
| pvalue | Raw p-value |
| padj | FDR-adjusted p-value |

---

## 6. How it works

### 6.1 Negative binomial model

RNA-seq counts are modeled as **negative binomial** (accounts for
over-dispersion, Ch 16).

`count ~ negative_binomial(mean, dispersion)`

### 6.2 Size factors

Applied from Ch 17 (median-of-ratios).

### 6.3 Dispersion estimation

DESeq2 estimates per-gene dispersion, then **shrinks** estimates
toward a fitted trend, borrowing information across genes -- crucial
with only 3 replicates per condition.

### 6.4 Testing

For `design = ~ condition`, DESeq2 tests the treatment effect with a
**Wald test** (or LRT). Fold changes are also **shrunk** to reduce
noise in low-count genes.

---

## 7. Biology behind it

- The comparison is **control vs dexamethasone (T/C)**.
- Positive log2FC = up in treatment; negative = down.
- For our study, key hits: CRISPLD2 (+2.52), FKBP5 (+3.21), DUSP1
  (+2.08), KLF15 (+2.15 up), SPARCL1 (-2.09 down), EGR1 (down).

---

## 8. Command

```r
# R (part of DE workflow)
library(DESeq2)
coldata <- read.csv("metadata/samples.csv")
dds <- DESeqDataSetFromMatrix(countData = counts, colData = coldata,
                              design = ~ condition)
dds <- DESeq(dds)
res <- results(dds)
res_shrunk <- lfcShrink(dds, coef="condition_treatment_vs_control", type="apeglm")
write.csv(res, "results/deseq2/deseq2_results.csv")
```

---

## 9. Example

Significant genes (padj < 0.05, |log2FC| > 1):

| Gene | baseMean | log2FC | padj |
|------|----------|--------|------|
| FKBP5 | 830 | 3.21 | 0.0001 |
| CRISPLD2 | 420 | 2.52 | 0.0003 |
| DUSP1 | 1500 | 2.08 | 0.0008 |
| KLF15 | 300 | 2.15 | 0.001 |
| SPARCL1 | 500 | -2.09 | 0.002 |

---

## 10. How to read the output

| Column | Meaning / cutoff |
|--------|------------------|
| baseMean | Avg normalized count (higher = more reliable) |
| log2FoldChange | Magnitude/direction of change |
| padj | Significance; use < 0.05 |
| Common DE threshold | `padj < 0.05` and `|log2FC| > 1` |

Filter with:

```r
sig <- subset(res_shrunk, padj < 0.05 & abs(log2FoldChange) > 1)
```

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| Wrong design formula / sample order | Ensure samples match condition mapping |
| All padj = NA | Check for zero-variance / mislabeled conditions |
| Low power | More replicates needed |
| Fold changes noisy | Use lfcShrink (apeglm) |

---

## 12. Limitations

- Requires good replicate design; results depend on count quality
  (Ch 8-15).
- Identifies statistical change, not biological mechanism (pathways
  next).
- With n=3 per group, only large effects are detected.

---

## 13. How our project uses it

- DESeq2 is the **DE engine** (documented in `workflow.md`).
- Its results feed the volcano plot, heatmap, and pathway analyses.
- Future: R/DESeq2 execution and output parsing for the API/UI.

---

## 14. Official documentation

- **DESeq2**:
  https://bioconductor.org/packages/release/bioc/html/DESeq2.html
- **DESeq2 paper** (Love et al. 2014, Genome Biology):
  https://genomebiology.biomedcentral.com/articles/10.1186/s13059-014-0550-8

---

## 15. Mini exercise

1. Why does DESeq2 use a negative binomial (not Poisson) model?
2. What do positive vs negative log2FC mean for our T/C comparison?
3. How do you define a "significant DE gene"?
4. Why use lfcShrink (apeglm)?
5. How does the results table feed the next chapters' visualizations?

---

**End of Statistics phase.**

> **Next**: [Chapter 19: PCA](../07_visualization/pca.md)
