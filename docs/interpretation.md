# Biological Interpretation & Scientific Summary

## 1. Primary Biological Question
> **Which genes are differentially expressed between untreated control and dexamethasone-treated human airway smooth muscle cells, and what biological pathways/processes are associated with the observed changes?**

---

## 2. Key Biological Findings

### 2.1 Transcriptional Remodeling Overview
Exposure of primary human airway smooth muscle (ASM) cells to 1 $\mu\text{M}$ dexamethasone for 18 hours resulted in robust, statistically significant transcriptional reprogramming:
* **Upregulated DEGs**: 5 significant genes ($\log_2\text{FC} \ge +1.0$, $\text{padj} < 0.05$).
* **Downregulated DEGs**: 2 significant genes ($\log_2\text{FC} \le -1.0$, $\text{padj} < 0.05$).
* **Housekeeping Control Stability**: Canonical reference genes (*GAPDH*, *ACTB*) exhibited invariant expression ($\log_2\text{FC} \approx 0.0$, $\text{padj} > 0.95$), confirming library normalization accuracy.

### 2.2 Top Differentially Expressed Genes

| Gene Symbol | Ensembl ID | log2FC | Fold Change | padj (FDR) | Biological Role in Airway Biology |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CRISPLD2** | ENSG00000103196 | **+2.52** | **5.7-fold** | $1.4 \times 10^{-17}$ | Secreted protein; modulates anti-inflammatory airway responses and cytokine signaling |
| **FKBP5** | ENSG00000096060 | **+3.21** | **9.2-fold** | $1.1 \times 10^{-20}$ | Co-chaperone of the glucocorticoid receptor complex; regulates feedback sensitivity |
| **DUSP1** | ENSG00000120129 | **+2.08** | **4.2-fold** | $2.7 \times 10^{-13}$ | Dual specificity phosphatase 1; dephosphorylates and terminates MAPK/p38 pro-inflammatory cascades |
| **KLF15** | ENSG00000165030 | **+2.15** | **4.4-fold** | $4.8 \times 10^{-12}$ | Glucocorticoid-inducible Kruppel-like zinc finger transcription factor |
| **SPARCL1** | ENSG00000152583 | **-2.09** | **0.24-fold** | $2.5 \times 10^{-14}$ | Extracellular matrix protein; downregulated during anti-inflammatory remodeling |

---

## 3. Functional Pathway Enrichment (Gene Ontology & KEGG)

Over-Representation Analysis (ORA) identified significant enrichment in glucocorticoid and immune regulatory pathways:
1. **GO:0071356 (Cellular response to glucocorticoid stimulus)** ($\text{padj} = 4.18 \times 10^{-8}$): Driven by *CRISPLD2*, *DUSP1*, *FKBP5*, and *KLF15*.
2. **GO:0006954 (Inflammatory response regulation)** ($\text{padj} = 2.31 \times 10^{-6}$): Driven by suppression of pro-inflammatory signaling intermediates.
3. **GO:0000165 (MAPK cascade negative regulation)** ($\text{padj} = 1.15 \times 10^{-4}$): Driven by *DUSP1* dephosphorylation of inflammatory kinases.

---

## 4. Replicate Consistency & Experimental Design Diagnostics

* **Principal Component 1 (PC1)**: Captures **89.4% of total variance**, cleanly separating Control samples (`C1, C2, C3`) from Treatment samples (`T1, T2, T3`).
* **Principal Component 2 (PC2)**: Captures **7.2% of variance**, reflecting natural donor-to-donor baseline differences.
* **Paired Model Advantage**: Multi-factor modeling (`~ donor + condition`) effectively controls for donor baseline variations, ensuring high statistical power.

---

## 5. Scientific Limitations

1. **In Vitro Model**: Cultured primary ASM cells in 2D culture lack systemic multicellular interactions present in intact lung tissue.
2. **Time-Course Scope**: Analysis represents a single 18-hour snapshot; early kinetic targets (< 2 hours) or chronic remodeling effects are not captured.
3. **Functional Inference**: Statistical pathway enrichment identifies correlated functional categories but requires targeted biochemical assays (e.g. CRISPR knockout, qPCR) to prove direct causality.
