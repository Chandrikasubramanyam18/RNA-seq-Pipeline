# Chapter 22: GO Enrichment

> The pathway analysis step that asks: are the DE genes enriched in
> specific Gene Ontology (GO) biological functions?

---

## 1. What is it?

**Gene Ontology (GO) enrichment** tests whether the differentially
expressed genes are over-represented in annotated functional
categories: **Biological Process (BP)**, **Molecular Function (MF)**,
and **Cellular Component (CC)**.

If many up-regulated genes share a GO term (e.g., response to
glucocorticoid), that term is "enriched" -- suggesting a coordinated
biological response.

---

## 2. Why do we need it?

DE analysis tells you *which* genes change; it doesn't tell you *what
that means*. GO enrichment summarizes the set into interpretable
biological themes (processes, functions, locations).

---

## 3. Where does it fit?

```
DE gene list (Ch 18) -> GO enrichment  <--- here
                             |
                             +--> Reactome pathways (Ch 24)
                             +--> GSEA (Ch 23, rank-based)
```

Over-representation analysis (ORA) on the significant gene list.

---

## 4. Input

- The significant DE gene list (padj<0.05, |log2FC|>1) from Ch 18.
- A gene-to-GO-term annotation database (org.Hs.eg.db).

---

## 5. Output

| File | Description |
|------|-------------|
| `go_enrichment.csv` | Enriched GO terms with p-values |
| Dot plot / network plot | Visual summary (optional) |

---

## 6. How it works (Over-Representation Analysis)

1. Define the **background** = all genes measured.
2. Define the **foreground** = DE genes of interest.
3. For each GO term, test if the proportion of DE genes annotated to
   it is higher than expected by chance (hypergeometric /
   Fisher's exact / R).
4. Adjust p-values (padj / FDR) and return significant terms.

Terms are tested within the *ontology* (BP, MF, CC) being examined.

---

## 7. Biology behind it

- Enriched GO terms point to the biological functions "driven" by the
  DE genes.
- For dexamethasone-treated ASM, expect terms like:
  - **response to glucocorticoid / corticosteroid**
  - **regulation of transcription**
  - **inflammatory response** (suppressed)
- This connects the gene list to the bronchodilator/anti-inflammatory
  context of the study.

---

## 8. Command

```r
# R (part of pathway workflow)
library(clusterProfiler)
library(org.Hs.eg.db)
de_genes <- rownames(sig)   # significant genes from Ch 18
ego <- enrichGO(gene = de_genes,
                universe = rownames(counts),
                OrgDb = org.Hs.eg.db,
                ont = "BP",
                pAdjustMethod = "BH",
                qvalueCutoff = 0.05)
write.csv(as.data.frame(ego), "results/pathways/go_bp.csv")
```

---

## 9. Example

Top enriched BP terms (illustrative):

| GO ID | Term | p.adjust |
|-------|------|----------|
| GO:0007002 | response to glucocorticoid | 0.001 |
| GO:0045944 | positive regulation of transcription | 0.003 |
| GO:0034614 | cellular response to reactive oxygen | 0.01 |

---

## 10. How to read the output

| Column | Meaning |
|--------|---------|
| ID | GO term ID |
| Description | Functional description |
| GeneRatio | DE genes in term / total DE genes |
| BgRatio | Background ratio |
| pvalue / p.adjust | Significance (use adjusted) |
| geneID | Which DE genes hit the term |

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| Wrong background | Use all measured genes, not genome |
| ENTRY_ID mapping | Convert gene symbols <-> entrez |
| Redundant terms | Use simplify() to collapse |
| Ignoring p.adjust | Use adjusted values |

---

## 12. Limitations

- ORA uses a hard gene list threshold; borderline genes are excluded.
- GO annotation can be incomplete/outdated.
- Enrichment is correlational; needs experimental context.

---

## 13. How our project uses it

- GO BP/MF/CC analysis on the DE gene list from DESeq2.
- `clusterProfiler` is a **future** tool (not yet implemented).
- Outputs power the pathway section of the API/UI.

---

## 14. Official documentation

- **clusterProfiler**:
  https://bioconductor.org/packages/release/bioc/html/clusterProfiler.html
- **Gene Ontology**:
  https://geneontology.org/

---

## 15. Mini exercise

1. What are the three GO ontologies (BP/MF/CC)?
2. What does an "enriched" GO term mean?
3. Why set the background to all measured genes?
4. What function types would you expect to be enriched in
   dexamethasone-treated ASM?
5. Why use p.adjust rather than raw p?

---

> **Next**: [Chapter 23: GSEA](gsea.md)
