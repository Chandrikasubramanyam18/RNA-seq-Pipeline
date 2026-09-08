# Step 8 Gate Report — Real visualization data from real DESeq2 results

- **Generated**: Step 8 (visualization data), real-loci mini-reference pipeline
- **Scope**: PCA, MA, volcano, and sample-distance/clustered-heatmap data computed **from the real DESeq2 object and count matrix of Step 7**
- **Downstream**: STOPPED. No mock points, no pathway analysis, no backend change, no `isMock` change.

## Inputs (all real, from Steps 6–7)

- `results/differential_expression/real_dds_fitted.rds` — fitted DESeq2 object (`~ donor + condition`, fitType="mean") from the real 3×6 featureCounts matrix
- `results/differential_expression/real_deseq2_results.rds` / `real_deseq2_results.csv` — real Wald results
- `results/counts/gene_counts.txt` — real featureCounts matrix

## Generated data (R 4.5.3, DESeq2 1.50.2)

| File | Contents | Verifiability |
|---|---|---|
| `results/visualization/real_vst_counts.csv` | VST-stabilized counts, 3 genes × 6 samples (`fitType="mean"`) | = readRDS(dds) → vst |
| `results/visualization/real_pca_data.csv` | sample, PC1, PC2, % variance, donor, condition | prcomp on VST |
| `results/visualization/real_ma_data.csv` | gene, baseMean, log2FoldChange (3 rows) | from real DESeq2 results |
| `results/visualization/real_volcano_data.csv` | gene, log2FoldChange, −log10(padj), significant (3 rows, **3 points only**) | from real DESeq2 results |
| `results/visualization/real_sample_distances.csv` | 6×6 Euclidean sample–sample distances on VST | dist(t(vst)) |
| `results/visualization/real_heatmap_clustered_matrix.csv` | VST matrix with rows reordered by complete-linkage hclust | hclust on dist(vst) |
| `results/visualization/real_heatmap_clustering.rds` | dist + col/row hclust objects for faithful rendering | RDS |

## Key numbers (real)

**PCA** (prcomp, scaled, on VST):

| sample | PC1 | PC2 | condition | donor |
|---|---|---|---|---|
| C1 | −0.734 | −0.456 | control | N61311 |
| C2 | −1.209 | −0.196 | control | N052611 |
| C3 | −1.001 | −0.503 | control | N080611 |
| T1 | 1.062 | −0.633 | treatment | N61311 |
| T2 | 1.852 | −0.252 | treatment | N052611 |
| T3 | 0.031 | 2.040 | treatment | N080611 |

- PC1 (50.4% variance): controls (−0.73…−1.21) vs treatments (+1.06…+1.85) **separate**, except T3.
- T3 (PC2 2.04) is pulled away — consistent with its real CRISPLD2 count of 9 (vs T1 35, T2 27), i.e. a genuinely low-count sample. **Not fixed, not hidden.**

**Volcano** (3 points, padj from real Wald tests):

| gene | log2FoldChange | −log10(padj) | significant |
|---|---|---|---|
| CRISPLD2 (ENSG00000103196.14) | +2.212 | 1.582 | YES |
| GAPDH (ENSG00000111640.16) | −0.669 | 1.582 | NO |
| ACTB (ENSG00000075624.17) | +0.129 | 0.211 | NO |

**MA**: CRISPLD2 baseMean 12.72 (log2FC +2.21), GAPDH 228.71 (−0.67), ACTB 485.58 (+0.13).

**Heatmap data**: VST values range ≈1.45 (CRISPLD2, C2) – 9.25 (ACTB, T3); col clustering order `4 5 2 6 1 3` (complete linkage); row order puts CRISPLD2, GAPDH, ACTB by cluster.

## Validation

| check | result |
|---|---|
| Inputs = real DESeq2 object + real count matrix (+ real results table) | PASS |
| PCA from VST of real dds (fitType="mean" consistent with Step 7) | PASS |
| Volcano contains **exactly 3 real points** (no synthetic filling) | PASS |
| MA / volcano values equal the real Step 7 results tables | PASS (identical log2FC/baseMean/padj) |
| Sample-distance and clustered-heatmap data generated (complete linkage) | PASS |
| No manufactured points; low-count T3 anomaly retained, not masked | PASS |
| Backend code / `isMock` unchanged | PASS |

Note: the previous `results/visualization/volcano_data.csv` and `visualization_summary.md` (synthetic Python layer, dated 8/31) remain untouched; real data lives under `real_*` names for the eventual UI swap.

## Gate verdict

| check | result |
|---|---|
| Real visualization data generated from real DE results | PASS |
| 3-point volcano (correct for 3-gene reference) | PASS |
| Inputs traced to real DESeq2/count outputs | PASS |
| Backend / `isMock` untouched | PASS |

**GATE: PASSED. Visualization data is real and directly derived from the Step 7 DESeq2 object.**

## Provenance & scope

- All `real_*` files under `results/visualization/` are genuine R/DESeq2 outputs (gitignored).
- `isMock`: **NOT flipped — remains true**.
- Next permitted step when approved: **Step 9 pathway analysis** (to run on the *full* genome-wide dataset in production; at tutorial scale only the GSE52778-famous genes CRISPLD2/FKBP5/DUSP1 would be meaningful, so the pathway step is expected to be limited or explicitly scoped out at this mini-reference scale). Do not proceed without explicit gate approval.

> Visualization demonstrates pipeline execution at tutorial scale; it is explicitly **not** genome-wide biological inference.