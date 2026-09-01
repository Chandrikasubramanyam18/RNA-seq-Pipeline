# Chapter 19: PCA (Principal Component Analysis)

> An unsupervised dimensionality-reduction plot that shows how samples
> group by biological condition -- the first check of whether replicates
> cluster together.

---

## 1. What is it?

**Principal Component Analysis (PCA)** reduces thousands of gene
dimensions to a few **principal components** that capture the largest
variation in the data. Samples are plotted in the space of PC1 vs PC2.

It's **unsupervised** -- it doesn't use condition labels -- so if
samples cluster by condition, it confirms the biological signal
dominates variance.

---

## 2. Why do we need it?

- Quickly verify that control and treatment samples separate.
- Detect **outlier** or mislabeled samples.
- Check that replicates (C1-C3, T1-T3) are similar (tight clustering).
- Sanity-check data quality before DE interpretation.

---

## 3. Where does it fit?

```
DESeq2 normalized counts (Ch 17/18) -> PCA (rlog/vst)  <--- here
```

Computed from **normalized, stabilized** counts (VST or rlog).

---

## 4. Input

- Normalized count matrix (DESeq2 `vst` or `rlog`).

---

## 5. Output

- A scatter plot of samples on PC1 vs PC2 (and optionally PC3 vs PC4),
  colored by condition.

---

## 6. How it works

1. **Transform counts** to reduce heteroscedasticity (variance
   stabilizing transformation, VST, or regularized log, rlog, from
   DESeq2).
2. Compute the **covariance matrix** of genes.
3. Find eigenvectors (principal components) explaining the most
   variance.
4. Project samples onto PC1, PC2, ... and plot.

- **PC1** = direction of greatest variance.
- **PC2** = next, orthogonal direction.
- Percent variance explained is labeled on axes.

---

## 7. Biology behind it

- If treatment has a strong effect, samples separate along PC1/PC2.
- Biological replicates should cluster tightly (similar expression).
- A mislabeled/contaminated sample appears as an isolated outlier.

---

## 8. Command

```r
# R (part of DE workflow)
library(DESeq2)
vsd <- vst(dds, blind=FALSE)
plotPCA(vsd, intgroup="condition")
# Or use DESeq2's plotPCA / PCAtools for richer plots
```

---

## 9. Example

For our study, PC1 could separate **control vs treatment**, with C1-C3
clustering on the left and T1-T3 on the right. Replicates tight,
conditions distinct -- supporting reliable DE.

---

## 10. How to read the output

- **Conditions separated**: strong biological effect; DE trustworthy.
- **Replicates tight**: low technical noise, consistent grouping.
- **% variance on axes**: PC1 explaining most (e.g., 60%) is good.
- **Outlier far from group**: investigate (contamination, mislabel).

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| Outlier dominates PC1 | Remove/inspect mislabeled sample |
| No separation | Weak effect, batch effect, or normalization issue |
| Batch effect confounds | Use `~ batch + condition` design |
| Reading too much into low-PC axes | Only interpret high-variance PCs |

---

## 12. Limitations

- PCA reflects *global* variance, which may be dominated by batch
  effects, not the condition of interest.
- It's a visualization/sanity check, not a statistical test.
- Clustering doesn't prove causation.

---

## 13. How our project uses it

- Generated from DESeq2 VST counts for the 6 samples.
- Plotted for the UI/API dashboard (Phase 2/3).
- Serves as a quality/interrogation view in the platform.

---

## 14. Official documentation

- **DESeq2 PCA / VST**:
  https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html
- **PCAtools R package**:
  https://github.com/kevinblighe/PCAtools

---

## 15. Mini exercise

1. Why is PCA described as "unsupervised"?
2. What would tightly-clustered replicates and well-separated
   conditions suggest?
3. Why use VST/rlog counts for PCA, not raw counts?
4. What does a far-outlier sample suggest, and what would you do?
5. Can batch effects be separated from treatment effects in PCA?
   How?

---

> **Next**: [Chapter 20: Volcano Plot](volcano.md)
