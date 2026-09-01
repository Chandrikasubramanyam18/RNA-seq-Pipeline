# Chapter 21: Heatmap

> A matrix visualization of gene expression across samples, with
> clustering, used to inspect the expression patterns of the top DE
> genes.

---

## 1. What is it?

A **heatmap** plots a matrix where rows are genes and columns are
samples. Cell color encodes expression (Z-scored so genes are
comparable). Rows and columns are often hierarchically clustered to
reveal structure.

It shows *how* the top DE genes behave across the 6 samples.

---

## 2. Why do we need it?

- Visualize the full expression pattern of DE genes, not just summary
  statistics.
- Confirm genes group by condition (C vs T).
- See co-regulated gene blocks (e.g., all up-regulated genes in
  treatment).

---

## 3. Where does it fit?

```
DESeq2 results (Ch 18) -> top DE genes -> Heatmap (vst/rlog)  <--- here
```

Uses the same normalized counts as PCA (Ch 19).

---

## 4. Input

- Normalized counts (DESeq2 `vst`/`rlog` or `normTransform`).
- The list of significant DE genes (Ch 18).

---

## 5. Output

- A clustered heatmap of top DE genes across the 6 samples.

---

## 6. How it works

1. Select top DE genes (e.g., top 30 by padj, or `|log2FC|`).
2. **Z-score** each gene's counts row (subtract mean, divide by SD) so
   genes have comparable scales.
3. Plot cells colored by Z-score (red high, blue low).
4. **Hierarchically cluster** genes (rows) and samples (columns) using
   distance + linkage.

---

## 7. Biology behind it

- Clustering groups similarly-expressed genes (co-regulated).
- Sample columns clustering by condition confirms reproducibility
  (C1-C3 together, T1-T3 together).
- Up-regulated genes show high (red) in T columns, low in C.

---

## 8. Command

```r
# R (part of DE workflow)
library(pheatmap)
vsd <- vst(dds, blind=FALSE)
top <- head(rownames(res_shrunk[order(res_shrunk$padj),]), 30)
mat <- assay(vsd)[top, ]
mat <- t(scale(t(mat)))   # Z-score per gene
pheatmap(mat, annotation_col=coldata["condition"],
         show_rownames=TRUE)
```

---

## 9. Example

For our study, the heatmap would show a clear **column split**:
C1-C3 (control) clustered together, T1-T3 (treatment) together. Rows
split into an up-regulated block (FKBP5, CRISPLD2, DUSP1, KLF15 --
red in T, blue in C) and a down-regulated block (SPARCL1, EGR1).

---

## 10. How to read the output

- **Column clustering** = sample structure; verify C vs T separation.
- **Row clustering** = gene co-regulation groups.
- **Z-score scale** = how far each gene's expression is from its own
  mean (not absolute abundance).
- **Biological interpretation**: coordinated gene programs across
  treatment.

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| Plotting raw counts (unscaled) | Z-score per gene row |
| Using all genes (too big) | Subset to top DE genes |
| Misleading absolute color | Note Z-score, not raw expression |
| No clustering | Enable hierarchical clustering |

---

## 12. Limitations

- Z-scoring loses magnitude/absolute expression info.
- Only shows transcript-level pattern, not mechanism (pathways next).
- Selecting top genes is arbitrary.

---

## 13. How our project uses it

- Rendered from DESeq2 VST counts of the top DE genes.
- Shown in the UI/API dashboard.
- Gene-annotation blocks (up/down) highlight co-regulation.

---

## 14. Official documentation

- **pheatmap R package**:
  https://cran.r-project.org/package=pheatmap
- **ComplexHeatmap R package**:
  https://bioconductor.org/packages/release/bioc/html/ComplexHeatmap.html

---

## 15. Mini exercise

1. Why Z-score each gene's row before plotting?
2. What does column clustering tell you?
3. What would blocks of red/blue rows indicate biologically?
4. Why subset to top DE genes rather than plot all genes?
5. How does the heatmap complement the volcano plot (Ch 20)?

---

**End of Visualization phase.**

> **Next**: [Chapter 22: GO Enrichment](../08_pathways/go.md)
