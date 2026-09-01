# Chapter 20: Volcano Plot

> A scatter plot of log2 fold change (x-axis) vs statistical
> significance (y-axis) that visualizes which genes change and how
> confidently.

---

## 1. What is it?

A **volcano plot** shows every gene as a point:

- **x-axis**: log2 fold change (treatment/control)
- **y-axis**: -log10 adjusted p-value (FDR)

Points in the upper-left (downregulated, significant) and upper-right
(upregulated, significant) are the DE hits. The shape resembles a
volcano, hence the name.

---

## 2. Why do we need it?

- Quickly see the *global* distribution of all ~20k genes.
- Identify the significant, strongly-changing genes at a glance.
- Verify there are genuinely up- and down-regulated genes.

---

## 3. Where does it fit?

```
DESeq2 results (Ch 18) -> Volcano plot  <--- here
```

One of the primary visual summaries of DE results.

---

## 4. Input

- DESeq2 results table (gene, log2FC, padj).

---

## 5. Output

- A scatter plot of all genes, colored by significance/direction.

---

## 6. How it works

1. From the DESeq2 results (Ch 18), get `log2FoldChange` and `padj`.
2. Compute `-log10(padj)` as the y-axis (higher = more significant).
3. Plot each gene; color by threshold:
   - Gray: not significant
   - Red: significant & up (log2FC > +1, padj < 0.05)
   - Blue: significant & down (log2FC < -1, padj < 0.05)
4. Label top hits (e.g., FKBP5, CRISPLD2).

---

## 7. Biology behind it

- **Right side** = genes up-regulated by dexamethasone.
- **Left side** = genes down-regulated.
- **Height** = statistical confidence.
- For asthma/glucocorticoid study: FKBP5, DUSP1, CRISPLD2 appear as
  striking up-regulated points.

---

## 8. Command

```r
# R (part of DE workflow)
library(ggplot2)
res <- read.csv("results/deseq2/deseq2_results.csv")
res$sig <- "NS"
res$sig[res$log2FoldChange > 1 & res$padj < 0.05] <- "Up"
res$sig[res$log2FoldChange < -1 & res$padj < 0.05] <- "Down"
ggplot(res, aes(log2FoldChange, -log10(p adj), color=sig)) +
  geom_point(alpha=0.5) +
  scale_color_manual(values=c("NS"="grey","Up"="red","Down"="blue"))
```

---

## 9. Example

For our study, expected hits:

| Gene | log2FC | padj | Position |
|------|--------|------|----------|
| FKBP5 | +3.21 | 1e-4 | upper right |
| CRISPLD2 | +2.52 | 3e-4 | upper right |
| DUSP1 | +2.08 | 8e-4 | upper right |
| SPARCL1 | -2.09 | 2e-3 | upper left |

---

## 10. How to read the output

- **Upper right region**: confidently up-regulated genes.
- **Upper left region**: confidently down-regulated genes.
- **Lower band of spread**: non-significant genes (NS).
- **Corners vs edges**: significance (height) and magnitude (width)
  are independent.

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| Using raw p instead of padj | Use adjusted p-values |
| Thresholds too loose | `padj<0.05`, `|log2FC|>1` |
| Not shrinking FC | Use lfcShrink to label stably |
| Overlapping labels | Use ggrepel on top genes only |

---

## 12. Limitations

- Shows statistical DE, not biological function (pathways next).
- Effect size and significance are both shown, but genes with small
  effects at very high significance can be visually misleading.
- Thresholds are arbitrary; explore sensitivity.

---

## 13. How our project uses it

- Rendered from the DESeq2 results table in the visualization phase.
- Shown in the UI/API dashboard so users inspect DE at a glance.
- Top genes (CRISPLD2, FKBP5, DUSP1, KLF15, SPARCL1) are labeled.

---

## 14. Official documentation

- **EnhancedVolcano R package**:
  https://github.com/kevinblighe/EnhancedVolcano
- **ggplot2**:
  https://ggplot2.tidyverse.org/

---

## 15. Mini exercise

1. What do the x and y axes represent?
2. Where do significant up-regulated genes appear on the plot?
3. Why use padj rather than raw p on the y-axis?
4. Why is FKBP5 plotted in the "upper right"?
5. How do you label only the top hits?

---

> **Next**: [Chapter 21: Heatmap](heatmap.md)
