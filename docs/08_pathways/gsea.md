# Chapter 23: GSEA (Gene Set Enrichment Analysis)

> A rank-based pathway method that detects whether entire gene sets
> shift systematically, without requiring an arbitrary DE-gene cutoff.

---

## 1. What is it?

**Gene Set Enrichment Analysis (GSEA)** ranks ALL genes by a metric
(e.g., fold change) and tests whether known gene sets (pathways,
GO terms, hallmark sets) are **enriched** at the top or bottom of the
ranking -- even if individual genes aren't individually significant.

It's complementary to GO ORA (Ch 22): ORA uses a hard cutoff, GSEA
uses the full distribution.

---

## 2. Why do we need it?

- ORA (Ch 22) discards genes that just miss the significance cutoff.
- GSEA captures **coordinated** shifts in whole pathways, which is
  more powerful for subtle, widespread effects (common in
  glucocorticoid response).
- Detects both up- and down-regulated gene sets.

---

## 3. Where does it fit?

```
DESeq2 results (all genes, ranked) -> GSEA  <--- here
                                             |
                                             +--> Reactome (Ch 24)
```

It uses ALL genes ranked by log2FC, not just significant hits.

---

## 4. Input

- A **ranked gene list**: every gene with a ranking metric (e.g.,
  `-log10(p) * sign(log2FC)`, or just `log2FC`).
- Gene set collections (Hallmark, KEGG, Reactome, GO).

---

## 5. Output

| File | Description |
|------|-------------|
| `gsea_hallmark.csv` | Enriched gene sets with NES & padj |
| Enrichment plots / heatmaps | Visual results (optional) |

---

## 6. How it works

1. **Rank** all genes by the selected metric.
2. For each gene set, walk down the ranked list computing an
   **Enrichment Score (ES)**: how clustered the set's genes are at the
   top or bottom.
3. Normalize for set size -> **NES (Normalized Enrichment Score)**.
4. Estimate significance by permuting sample labels -> padj.
5. Positive NES = enriched at top (up in treatment); negative NES =
   down.

---

## 7. Biology behind it

- Glucocorticoid (dexamethasone) activates a broad, coordinated
  transcriptional program.
- GSEA can reveal enrichment of:
  - **hallmark TNFA signaling** / inflammatory pathways (suppressed)
  - **glucocorticoid response** hallmark
  - **apoptosis / cell signaling** sets
- This captures system-level shifts even with modest individual-gene
  effects.

---

## 8. Command

```r
# R (part of pathway workflow) -- clusterProfiler GSEA
library(clusterProfiler)
library(msigdbr)
ranks <- res$log2FoldChange; names(ranks) <- rownames(res)
ranks <- sort(ranks, decreasing=TRUE)
gsea <- gseGO(geneList = ranks, OrgDb = org.Hs.eg.db,
              ont = "BP", pAdjustMethod = "BH", verbose=FALSE)
# or gseKEGG / gsea for Hallmark gene sets
write.csv(as.data.frame(gsea), "results/pathways/gsea_go.csv")
```

---

## 9. Example

Illustrative enriched sets:

| Description | NES | p.adjust |
|-------------|-----|----------|
| reactive oxygen / inflammation | -2.1 | 0.002 |
| glucocorticoid receptor signaling | +2.4 | 0.001 |
| response to corticosteroid | +2.2 | 0.003 |

---

## 10. How to read the output

| Column | Meaning |
|--------|---------|
| Description | Gene set name |
| NES | Normalized enrichment score (direction/size) |
| pvalue / p.adjust | Significance |
| setSize | Genes in set |
| leadingEdge | Core genes driving the enrichment |

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| Duplicate gene names in ranks | Collapse to unique genes |
| Wrong rank metric direction | Positive = up in treatment |
| Uninformative ranks | Use shrunk log2FC |
| Not adjusting for gene set size | Use NES (already normalized) |

---

## 12. Limitations

- Requires good gene set annotations.
- Overlapping/redundant gene sets can inflate focus on a few functions.
- Subtle global shifts may still need pathway-level validation.

---

## 13. How our project uses it

- GSEA complements GO ORA on the full ranked DESeq2 results.
- `clusterProfiler` / GSEA are **future** tools.
- Outputs will populate pathway views in the API/UI.

---

## 14. Official documentation

- **GSEA (Broad)**:
  https://www.gsea-msigdb.org/gsea/index.jsp
- **clusterProfiler GSEA**:
  https://bioconductor.org/packages/release/bioc/html/clusterProfiler.html
- **MSigDB gene sets**:
  https://www.gsea-msigdb.org/gsea/msigdb/

---

## 15. Mini exercise

1. How does GSEA differ from GO over-representation analysis (Ch 22)?
2. What is a ranked gene list, and how do you build one?
3. What does a positive vs negative NES mean?
4. Why might GSEA detect an effect ORA misses?
5. What is the leadingEdge, and why is it useful?

---

> **Next**: [Chapter 24: Reactome Pathways](reactome.md)
