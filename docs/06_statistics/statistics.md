# Chapter 16: Statistics Fundamentals

> The statistical concepts underlying differential expression:
> hypothesis testing, p-values, multiple testing, and dispersion.

---

## 1. What is it?

**Statistics** for differential expression is the process of testing
whether observed read-count changes between conditions (e.g., control
vs dexamethasone) are **real** or due to **random sampling variation**.

Key concepts covered here: mean/variance, hypothesis testing, the
t-test, p-values, false discovery rate (FDR), and why RNA-seq needs
special treatment.

---

## 2. Why do we need it?

- Raw fold-changes alone are misleading (noise dominates).
- We need a principled way to decide which genes change **significantly**.
- Millions of genes tested -> need multiple-testing correction.

---

## 3. Where does it fit?

```
Count matrix (Ch 15) -> this chapter (theory) -> DESeq2 (Ch 18)
```

This chapter provides the conceptual foundation applied by DESeq2.

---

## 4. Input

- Conceptual (no code); the count matrix is the practical input.

---

## 5. Output

- Understanding of p-values, FDR, dispersion -- needed to interpret
  DESeq2 output (Ch 18).

---

## 6. How it works

### 6.1 Mean vs variance in RNA-seq

Naive approach: use a t-test per gene. But real RNA-seq has **over-
dispersion**: variance > mean. A misleading t-test treats all variance
as noise.

### 6.2 Hypothesis testing

For each gene:

```
H0: gene expression is unchanged between conditions
H1: gene expression differs between conditions
```

A test statistic is computed; a **p-value** is the probability of
observing such an extreme result *if H0 were true*.

### 6.3 Multiple testing problem

Testing ~20,000 genes individually at p<0.05 yields ~1,000 false
positives by chance. We need to control the **false discovery rate**
(FDR / adjusted p-value).

A common correction is **Benjamini-Hochberg (BH)**, which controls
FDR at a chosen level (e.g., 0.05).

### 6.4 Dispersion

The **dispersion** parameter models biological variability
(over-dispersion). DESeq2 shares information across genes to estimate
dispersion robustly, especially with few replicates.

---

## 7. Biology behind it

- Biological replicates (C1-C3, T1-T3) are essential to estimate
  biological variability -- technical replicates alone underestimate it.
- Over-dispersion reflects real biological heterogeneity among
  individuals.
- FDR balances finding real DE genes vs controlling false positives.

---

## 8. Command

No standalone command; concepts feed into DESeq2 (Ch 18). Read-only
Python can illustrate:

```python
from scipy import stats
# Not part of the pipeline; illustrative only
t_stat, pval = stats.ttest_ind(control, treatment)
```

---

## 9. Example

If a gene has t-test p-value 0.01, we cannot yet declare it
significant -- after BH correction (FDR) it may be 0.4 (not
significant).

| Gene | Raw p | adjusted p (FDR) | Significant? |
|------|-------|------------------|--------------|
| A | 0.0001 | 0.001 | Yes |
| B | 0.01 | 0.40 | No |
| C | 0.02 | 0.45 | No |

---

## 10. How to read the output

- **p-value**: raw test probability (weak evidence alone).
- **adjusted p-value / padj (FDR)**: corrected for multiple testing.
  This is the value to trust.
- **Dispersion**: biological noise parameter, used in the test.

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| Using raw p-values as significance | Use adjusted p (FDR) |
| No biological replicates | Can't estimate dispersion reliably |
| Treating variance as fixed (t-test only) | Use over-dispersion model (DESeq2) |
| Ignoring library size differences | Normalize first (Ch 17) |

---

## 12. Limitations

- Statistics identify *association*, not causation -- the biological
  interpretation (dexamethasone response) comes from context (Ch 1-3).
- With small replicate numbers, power is limited.
- Multiple-testing corrections trade sensitivity for specificity.

---

## 13. How our project uses it

- The 6 samples (3 control, 3 treatment) provide replicates for
  dispersion estimation.
- DESeq2 applies these concepts to the featureCounts matrix.
- Reading the DESeq2 results table (Ch 18) uses padj, not raw p.

---

## 14. Official documentation

- **Benjamini-Hochberg FDR procedure**:
  https://en.wikipedia.org/wiki/False_discovery_rate
- **Hypothesis testing primer**:
  https://en.wikipedia.org/wiki/Statistical_hypothesis_testing

---

## 15. Mini exercise

1. Why can't we use a plain t-test for RNA-seq differential
   expression?
2. What problem does multiple-testing correction solve?
3. Why are biological replicates essential?
4. What is FDR (adjusted p-value), and why trust it over raw p?
5. Why does biological over-dispersion matter?

---

> **Next**: [Chapter 17: Normalization](normalization.md)
