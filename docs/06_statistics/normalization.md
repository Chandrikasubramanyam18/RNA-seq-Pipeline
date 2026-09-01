# Chapter 17: Normalization

> The step that removes technical bias (library size, composition, gene
> length) from raw counts so that expression can be compared across
> samples and genes.

---

## 1. What is it?

**Normalization** transforms raw counts so that differences between
samples (and genes) reflect biology, not technical artifacts. Because
no two libraries have identical total reads, raw counts are not
directly comparable across samples.

Key methods: **counts per million (CPM)**, **RPKM/FPKM**,
**TPM**, and **DESeq2's median-of-ratios**.

---

## 2. Why do we need it?

- Libraries differ in total sequencing depth (e.g., one sample gets
  more reads).
- Gene length biases raw counts (longer genes get more reads).
- Highly expressed genes can shift the "composition" of a library,
  biasing depth estimates.

Normalization makes samples (and genes) comparable.

---

## 3. Where does it fit?

```
Count matrix (Ch 15) -> normalize -> DESeq2 (Ch 18)
```

Normalization happens *within* DESeq2 and influences its statistics.

---

## 4. Input

- The gene x sample count matrix (featureCounts output).

---

## 5. Output

- A normalized count matrix (per-sample scaling factors).
- For DESeq2: a `sizeFactor` per sample applied before testing.

---

## 6. How it works

### 6.1 CPM

```
CPM = (reads_gene / total_reads) * 10^6
```

Counts per million, per sample. Simple; removes depth differences.

### 6.2 RPKM / FPKM (gene length + depth)

```
RPKM = reads_gene / (gene_length_kb * total_reads_in_millions)
```

Adds gene-length normalization. **Deprecated** for between-sample
comparisons.

### 6.3 TPM

```
TPM = (reads_gene / gene_length_kb) / sum(all genes normalized) * 10^6
```

TPM normalizes by length *then* by total. Rational and recommended.
Salmon (Ch 14) outputs TPM directly.

### 6.4 DESeq2 median-of-ratios (size factors)

DESeq2 computes a **size factor** per sample:

1. For each gene, compute its geometric mean across samples.
2. For each sample, take the median of the ratio
   `count / geometric_mean`.
3. This median is the **size factor**, applied to all genes.

This controls for **library composition** -- a few highly expressed
genes don't skew everything. This is why DESeq2 uses raw counts with
size factors rather than CPM/TPM.

---

## 7. Biology behind it

- Sequencing depth varies per library (technical).
- Gene length and GC bias affect counts (technical).
- Composition bias: a highly-expressed gene set in one condition can
  influence relative abundance of all others.

Correct normalization is prerequisite to detecting real differential
expression.

---

## 8. Command

```python
# R / DESeq2 - size factor estimation (part of DE, Ch 18)
library(DESeq2)
dds <- DESeqDataSetFromMatrix(countData = counts, colData = coldata,
                              design = ~ condition)
dds <- estimateSizeFactors(dds)
sizeFactors(dds)   # per-sample scaling factors
```

---

## 9. Example

Size factors for our 6 samples might be:

| Sample | Size Factor |
|--------|-------------|
| C1 | 1.02 |
| C2 | 0.98 |
| C3 | 1.05 |
| T1 | 0.95 |
| T2 | 1.01 |
| T3 | 0.99 |

Values near 1 mean roughly equal depth; a size factor of 2 would mean
that sample was sequenced ~2x deeper.

---

## 10. How to read the output

- **Size factors near 1**: balanced library depths.
- **Extreme size factors** (e.g., >1.5 or <0.7): flag sequencing-depth
  imbalance; investigate.
- Normalized counts can be compared across samples for plotting.

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| Comparing raw counts across samples | Always normalize |
| Using RPKM/FPKM for DE | Use TPM or DESeq2 size factors |
| Normalizing by CPM for DE | Size factors / TPM better for composition bias |
| Zero totals (all counts 0) | Geometric-mean guard in DESeq2 |

---

## 12. Limitations

- No single normalization is universally perfect.
- CPM/TPM don't capture composition bias as well as DESeq2's
  median-of-ratios.
- Normalization cannot fix poor library preparation.

---

## 13. How our project uses it

- DESeq2 applies median-of-ratios size factors to the featureCounts
  matrix.
- TPM from Salmon (Ch 14) is used for expression-level visualization
  and isoform analysis.
- Normalized counts power PCA/volcano/heatmap (Ch 19-21).

---

## 14. Official documentation

- **DESeq2 size factors / normalization**:
  https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html
- **TPM vs RPKM discussion**:
  https://www.rna-seqblog.com/rpkm-fpkm-tpm-explained/

---

## 15. Mini exercise

1. Why must counts be normalized before comparing samples?
2. Compare TPM and DESeq2 median-of-ratios (size factors).
3. What is the composition bias, and why does DESeq2 address it?
4. Why are RPKM/FPKM discouraged for differential expression?
5. What do size factors near 1 vs 2 mean?

---

> **Next**: [Chapter 18: DESeq2](deseq2.md)
