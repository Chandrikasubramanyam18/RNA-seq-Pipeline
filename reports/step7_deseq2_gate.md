# Step 7 Gate Report — Real DESeq2 on the real featureCounts matrix (paired donor design)

- **Generated**: Step 7 (differential expression), real-loci mini-reference pipeline
- **Scope**: validate the paired experimental design, run **real R/DESeq2** on the **real featureCounts count matrix**, capture genuine output/error, and record the outcome honestly
- **Downstream**: STOPPED. No pathway analysis, no backend change, no `isMock` change.

## 1. Experimental-design validation

Source of truth: `metadata/dataset_manifest.yaml` (donor/condition per sample).

| sample | run_id | donor | condition | replicate |
|---|---|---|---|---|
| C1 | SRR1039508 | N61311 | control | 1 |
| C2 | SRR1039512 | N052611 | control | 2 |
| C3 | SRR1039516 | N080611 | control | 3 |
| T1 | SRR1039509 | N61311 | treatment | 1 |
| T2 | SRR1039513 | N052611 | treatment | 2 |
| T3 | SRR1039517 | N080611 | treatment | 3 |

3 donors × (control + treatment) = 6 samples → **paired** design, `design = ~ donor + condition`.

Rank check of the design matrix (intercept, 2 donor coefficients, 1 condition coefficient = 4 columns, 6 rows):

```
   (Intercept) donorN080611 donorN61311 conditiontreatment
C1           1            0           1                  0
C2           1            0           0                  0
C3           1            1           0                  0
T1           1            0           1                  1
T2           1            0           0                  1
T3           1            1           0                  1
```

Full column rank → the model is **algebraically identifiable** at the design level.

## 2. Run 1 — default settings (genuine failure, preserved)

`DESeq(dds)` with `design = ~ donor + condition`, default `fitType="parametric"` on the real 3×6 count matrix.

- Size factors: estimated successfully (C1 0.797, C2 0.914, C3 0.663, T1 1.012, T2 1.291, T3 1.209).
- **Dispersion trend fit FAILED** at the local-regression fallback:

```
estimating size factors
estimating dispersions
gene-wise dispersion estimates
mean-dispersion relationship
-- note: fitType='parametric', but the dispersion trend was not well captured...
   a local regression fit was automatically substituted...
Error in lfproc(x, y, weights = weights, ...) :
  newsplit: out of vertex space
Calls: DESeq ... estimateDispersionsFit -> localDispersionFit -> locfit -> lfproc
Execution halted  (RSCRIPT_EXIT=1)
```

This is a **bona fide statistic of the dataset, not a pipeline fault**: with only 3 genes, there are too few observations to estimate the mean–dispersion relationship, and locfit cannot build a trend. Full genuine log: `results/differential_expression/real_deseq2_run1_default.log`.

Per the gate instructions, this was **not** papered over with pseudocounts, fabricated samples, or synthetic counts.

## 3. Run 2 — documented remedy for very small gene sets (real, successful)

`fitType="mean"` is DESeq2's documented option for datasets where a dispersion *trend* cannot be constructed (e.g. very few genes). Same real counts, same paired design, **no data modification**:

| Gene | gene_name | baseMean | log2FoldChange | lfcSE | stat | pvalue | padj | significant |
|---|---|---|---|---|---|---|---|---|
| ENSG00000103196.14 | CRISPLD2 | 12.72 | 2.2125 | 0.8905 | 2.4845 | 0.0130 | 0.0262 | YES |
| ENSG00000111640.16 | GAPDH | 228.71 | −0.6693 | 0.2816 | −2.3771 | 0.0174 | 0.0262 | NO |
| ENSG00000075624.17 | ACTB | 485.58 | 0.1294 | 0.2575 | 0.5026 | 0.6152 | 0.6152 | NO |

- Size factors: as above (median-of-ratios on real counts).
- Final dispersions: 0.389 / 0.052 / 0.046 (per gene, mean-dispersion mode).
- Wald tests + Benjamini-Hochberg padj computed by DESeq2 on the real counts.

> CRISPLD2 shows a nominal "up" change (log2FC +2.2, padj 0.026) consistent in direction with the CRISPLD2-as-dexamethasone-target hypothesis for this study — but see the caveat below. This is an artefact of the tutorial-scale data, **not** evidence of differential expression in GSE52778.

## 4. Result-schema check

`real_deseq2_results.csv` matches the contract schema (`gene_id, baseMean, log2FoldChange, lfcSE, stat, pvalue, padj, significant`) consumed downstream by the platform; RDS objects (`real_deseq2_results.rds`, `real_dds_fitted.rds`) preserve the full fitted objects.

## 5. Gate verdict

| check | result |
|---|---|
| Sample/design factors validated (paired 3-donor design, full-rank matrix) | PASS |
| Real R/DESeq2 executed on real featureCounts matrix | PASS (2 runs) |
| Actual DESeq2 output/error captured | PASS (default-fit failure + fitType="mean" success, logs preserved) |
| Size factors / dispersion / model fit validated | PASS (size factors good; trend non-estimable at 3 genes — documented; mean-dispersion used) |
| Genuine outputs preserved | PASS (`results/differential_expression/real_*`, RDS, run log) |
| No manufactured DE results | PASS (real counts, real R, no insertion of values) |
| Statistical limitation documented | PASS (see below) |
| No pathway analysis | PASS |
| Backend unchanged / `isMock` untouched | PASS — synthetic `deseq2_results.csv` (8/31) left in place; only new `real_*` artifacts added |

**GATE: PASSED — the real count → real DESeq2 execution path is demonstrated.**

## 6. Statistical-power caveat (explicit)

- The count matrix is **3 genes × 6 samples** from ~50,000 read pairs/sample on a deliberately tiny reference.
- The **default DESeq2 dispersion-trend fit fails** with this many genes (genuine error preserved) — the 3-gene set is far below the gene count needed for reliable dispersion shrinkage.
- `fitType="mean"` lets the fitting complete but with severely underpowered inference; the p-values above are **not** statistically meaningful biological claims for GSE52778.
- Purpose achieved: prove that the real genome-based quantification → real DESeq2 execution path works on this engineering dataset. A publication-quality DE analysis requires the full GSE52778 dataset and a genome-wide reference.

## Provenance status

- Real DESeq2 outputs: `results/differential_expression/real_deseq2_results.csv`, `real_sig_upregulated_genes.csv`, `real_sig_downregulated_genes.csv`, `real_deseq2_results.rds`, `real_dds_fitted.rds`, `real_deseq2_run1_default.log` (gitignored).
- R scripts: `scripts/R/run_deseq2.R` (default) and `scripts/R/run_deseq2_fittype_mean.R` (documented-remedy path).
- Project-level `isMock` flag: **NOT flipped — remains true**.
- Next permitted step when approved: **Step 8 visualization** (PCA/volcano on the real DE results), using the genuine `real_deseq2_results.csv`. Do not proceed without explicit gate approval.

> Note: analysis is execution-validation at tutorial scale, not a biological claim for GSE52778.