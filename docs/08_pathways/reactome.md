# Chapter 24: Reactome Pathways

> Curated, mechanistic pathway analysis that maps DE genes onto
> specific biological reaction pathways (e.g., signaling cascades).

---

## 1. What is it?

**Reactome** is a curated, open-source database of biological
**reaction pathways** -- step-by-step molecular mechanisms (reactions,
proteins, complexes). Pathway enrichment tests whether the DE genes
are over-represented in these curated pathways.

Unlike broad GO terms, Reactome pathways describe *specific
mechanisms* (e.g., "MAPK signaling", "glucocorticoid receptor
regulated gene expression").

---

## 2. Why do we need it?

- Reactome provides **mechanistic, curated** pathways, complementing
  GO's general functions (Ch 22) and GSEA's rank-based view (Ch 23).
- It can reveal specific signaling pathways regulated by
  dexamethasone in airway smooth muscle.
- Pathways are manually curated for accuracy.

---

## 3. Where does it fit?

```
DE gene list (Ch 18) -> Reactome enrichment  <--- here
```

This is one of the final biological-interpretation steps.

---

## 4. Input

- The significant DE gene list (from Ch 18).
- Reactome pathway annotation (from `ReactomePA` R package).

---

## 5. Output

| File | Description |
|------|-------------|
| `reactome_enrichment.csv` | Enriched pathways with p-values |
| Pathway network/overview plots | Visual results (optional) |

---

## 6. How it works

1. Map DE genes to Reactome pathway membership.
2. For each pathway, test over-representation (hypergeometric test,
   like GO ORA in Ch 22).
3. Adjust p-values and return significant pathways.
4. Optionally visualize a **pathway hierarchy** (parent/child
   relationships of enriched pathways).

---

## 7. Biology behind it

- Reactome pathways describe actual molecular reactions.
- For dexamethasone-treated ASM, expect:
  - **Glucocorticoid receptor (NR3C1) signaling**
  - **Signal transduction / GPCR** pathways
  - **Immune / inflammatory response** pathways (modulated)
- CRISPLD2, DUSP1, FKBP5 are indirectly linked to glucocorticoid
  signaling and MAPK modules.

---

## 8. Command

```r
# R (part of pathway workflow)
library(ReactomePA)
library(org.Hs.eg.db)
de_genes <- rownames(sig)   # significant genes from Ch 18
pathways <- enrichPathway(gene = de_genes,
                          organism = "human",
                          pvalueCutoff = 0.05,
                          readable = TRUE)
write.csv(as.data.frame(pathways), "results/pathways/reactome.csv")
```

---

## 9. Example

Illustrative enriched Reactome pathways:

| ID | Description | p.adjust |
|----|-------------|----------|
| R-HSA-3371497 | negatively regulated NF-kB | 0.004 |
| R-HSA-167827 | glucocorticoid receptor signaling | 0.002 |
| R-HSA-372708 | p38 MAPK signaling | 0.01 |

---

## 10. How to read the output

| Column | Meaning |
|--------|---------|
| ID (R-HSA-...) | Reactome pathway identifier |
| Description | Pathway name |
| GeneRatio / BgRatio | Enrichment proportions |
| pvalue / p.adjust | Significance |
| geneID | DE genes in the pathway |

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| No conversion to readable | Use `readable=TRUE` for symbols |
| Pathway hierarchy confusion | Distinguish parent vs child terms |
| Background mismatch | Match DE list universe |
| Ignoring p.adjust | Use adjusted values |

---

## 12. Limitations

- Reactome coverage is human-centric and curated; some genes lack
  pathway annotation.
- Overlap with GO/GSEA results is expected (they answer related
  questions).
- Enrichment is correlational, not mechanistic proof.

---

## 13. How our project uses it

- Reactome analysis on the DE gene list complements GO (Ch 22) and
  GSEA (Ch 23).
- `ReactomePA`/`clusterProfiler` are **future** tools.
- Results will populate the pathway section of the API/UI dashboard.

---

## 14. Official documentation

- **Reactome**:
  https://reactome.org/
- **ReactomePA R package**:
  https://bioconductor.org/packages/release/bioc/html/ReactomePA.html

---

## 15. Mini exercise

1. How do Reactome pathways differ from broad GO terms?
2. What type of pathway would you expect from dexamethasone-treated
   airway smooth muscle?
3. Why is Reactome annotation described as "curated"?
4. How does Reactome enrichment complement GO ORA and GSEA?
5. Interpret: R-HSA-167827 "glucocorticoid receptor signaling",
   p.adjust 0.002.

---

**End of Pathway phase.**

> **Next**: [Chapter 25: Nextflow](../09_workflow/nextflow.md)
