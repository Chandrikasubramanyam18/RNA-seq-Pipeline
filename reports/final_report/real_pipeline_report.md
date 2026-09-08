# Real Pipeline Final Report — Tutorial-Scale Execution (Steps 3–9)

**Project**: Airway Smooth Muscle Glucocorticoid Response — GSE52778 (tutorial scale)
**Study Accession**: GEO GSE52778 / SRA SRP033325
**Organism**: *Homo sapiens*
**Scope**: Real-loci mini-reference (3 genes: CRISPLD2, GAPDH, ACTB) · 50,000 read pairs/sample
**Generated**: Step 10 (consolidated synthesis of the real Steps 3–9 gate artifacts)
**Status**: REAL EXECUTION — TUTORIAL SCALE. **Not** genome-wide biological inference; not a full re-analysis of GSE52778.

> Consolidated from the committed gate reports of the real execution: `step4_alignment_gate.md`, `step5_alignment_qc.md`, `step6_count_matrix_gate.md`, `step7_deseq2_gate.md`, `step8_visualization_gate.md`, `step9_pathway_gate.md`. The 8/31 `final_analysis_report.md` (former synthetic-level narrative) is intentionally left untouched and does not describe this real run.

---

## 1. Design & Data (real)

- **Study**: 3 paired donors (N61311, N052611, N080611), each with control + 1 µM dexamethasone-treated ASM sample (18 h), Illumina HiSeq 2000 PE 2×63 bp.
- **Design matrix** (DESeq2): `~ donor + condition` (full rank, paired test).
- **Scale**: 50,000 read pairs per sample (100,000 reads/sample input; 94,866–97,856 clean reads/sample retained by fastp).
- **Reference**: real-loci mini-reference (`data/reference/mini_real/`: `mini_genome.fa`, `mini_genes.gtf`, `refgene.bed12`, STAR index) containing CRISPLD2, GAPDH, ACTB.

## 2. Raw QC & Preprocessing (real fastqc 0.12.1 / fastp)

| sample | raw reads | clean reads | retention % | Q20 after % | Q30 after % | GC after % | adapters trimmed |
|---|---|---|---|---|---|---|---|
| C1 | 100,000 | 97,856 | 97.86 | 99.49 | 98.03 | 50.05 | 368 |
| C2 | 100,000 | 96,460 | 96.46 | 99.05 | 96.92 | 49.61 | 286 |
| C3 | 100,000 | 95,302 | 95.30 | 98.72 | 95.92 | 49.27 | 278 |
| T1 | 100,000 | 96,432 | 96.43 | 99.41 | 97.88 | 49.74 | 600 |
| T2 | 100,000 | 94,866 | 94.87 | 98.75 | 95.91 | 48.61 | 984 |
| T3 | 100,000 | 95,744 | 95.74 | 98.69 | 95.78 | 49.54 | 384 |

FastQC: `pass` for all core modules; `warn` only on "Overrepresented sequences" for some lanes (expected for a scaled-down subset). No tiles/modules fail.

## 3. Alignment (real STAR 2.7.x, mini-reference)

STAR per-sample (from `Log.final.out`, aggregated in MultiQC):

| sample | input reads | uniquely mapped | % unique | spliced reads | mismatch rate % |
|---|---|---|---|---|---|
| C1 | 48,928 | 381 | 0.78 | 161 | 2.38 |
| C2 | 48,230 | 382 | 0.79 | 168 | 2.53 |
| C3 | 47,651 | 337 | 0.71 | 152 | 2.58 |
| T1 | 48,216 | 449 | 0.93 | 179 | 2.44 |
| T2 | 47,433 | 469 | 0.99 | 207 | 2.25 |
| T3 | 47,872 | 559 | 1.17 | 219 | 1.87 |

Low genome-mapping % (0.71–1.17%) is **expected and documented**: the mini-genome contains only 3 gene loci, so reads from the rest of the human transcriptome cannot map — an engineering feature of the tutorial reference, not a QC failure.

SAMtools (independent of STAR): **100% mapped, 100% properly paired, 0 duplicates/singletons; error rate 0.0; avg base quality 37.2–38.2** (all samples). GAPDH (8 introns) + ACTB (5 introns) canonical junctions recovered; RSeQC "partial_novel" labels = ±1 bp GTF-coordinate convention artifact (verified).

## 4. Quantification (real featureCounts 2.1.1)

`featureCounts -p -s 0 -T 8` on the 6 real BAMs; real 3×6 count matrix (`results/counts/gene_counts.txt`):

| gene | C1 | C2 | C3 | T1 | T2 | T3 |
|---|---|---|---|---|---|---|
| CRISPLD2 (ENSG00000103196.14) | 5 | 1 | 4 | 35 | 27 | 9 |
| GAPDH (ENSG00000111640.16) | 225 | 216 | 210 | 212 | 156 | 250 |
| ACTB (ENSG00000075624.17) | 368 | 422 | 306 | 464 | 596 | 736 |

Reconciles with idxstats/STAR (GAPDH 225/230 and ACTB 368/374 exonic; CRISPLD2 reads mostly intronic).

## 5. Differential Expression (real DESeq2 1.50.2, R 4.5.3)

- Default `fitType="parametric"` genuinely failed at 3 genes (`Error in lfproc(...): newsplit: out of vertex space`); preserved at `real_deseq2_run1_default.log`.
- `fitType="mean"` succeeded. Wald test, `~ donor + condition`:

| gene | baseMean | log2FC | lfcSE | stat | pvalue | padj | significant |
|---|---|---|---|---|---|---|---|
| CRISPLD2 | 12.72 | +2.2125 | 0.8905 | 2.4845 | 0.01297 | 0.02617 | **YES** |
| GAPDH | 228.71 | −0.6693 | 0.2816 | −2.3771 | 0.01745 | 0.02617 | NO |
| ACTB | 485.58 | +0.1294 | 0.2575 | 0.5026 | 0.61525 | 0.61525 | NO |

> Interpretation: with only 3 genes, the *padj are identical* for CRISPLD2 and GAPDH (both p<0.05 and both the two fold-change-dominant genes); the same DH multiple-testing correction applies across the mini panel. Only CRISPLD2 passes the `|log2FC|≥1` + `padj<0.05` gate — consistent with the biology (glucocorticoid marker CRISPLD2 up).

## 6. Visualization (real R/DESeq2 → `results/visualization/real_*`)

- **PCA** (prcomp, scaled, VST `fitType="mean"`): **PC1 50.4%** variance separates controls (−0.73…−1.21) from treatments (+1.06…+1.85) except T3; T3 (PC2 2.04) pulled away by its genuinely low CRISPLD2 count (9 vs 35/27). Not corrected, not hidden.
- **MA plot**: CRISPLD2 baseMean 12.72 / log2FC +2.21; GAPDH 228.71 / −0.67; ACTB 485.58 / +0.13.
- **Volcano**: exactly 3 real points; only CRISPLD2 significant (−log10 padj = 1.582).
- **Heatmap**: VST 3×6 clustered (complete linkage), col order `4 5 2 6 1 3`; clustering objects saved (`real_heatmap_clustering.rds`).

## 7. Pathway Analysis (real clusterProfiler 4.18.4, org.Hs.eg.db 3.22.0)

- DEGs (`significant=YES`): 1 (CRISPLD2 → ENTREZ 83716). Universe = real 3-gene mini-reference.
- **GO ORA (BP/MF/CC): 0 terms.** **KEGG (hsa): none returned** (empty at thresholds; recorded, not fabricated).
- **Zero enrichment is the genuine, expected result** at this scale — a 1-gene query cannot enrich at FDR α=0.05. Thresholds were **not** loosened and no terms invented.
- GSEA deliberately skipped (a 3-gene ranked list is not a meaningful GSEA).

## 8. Provenance & limits

- Every number in this report traces to a real tool output preserved under `results/` (`fastqc_summary.tsv`, `fastp_summary.tsv`, STAR `Log.final.out`, SAMtools/RSeQC/MultiQC artifacts, `gene_counts.txt`, `real_*` DESeq2/visualization/pathway files) and to the committed step gate reports.
- `isMock` remains **true** in the backend because this is tutorial-scale execution, **not** publication-grade biological analysis. Backend untouched in Steps 4–9.
- Synthetic legacy artifacts (8/31 `final_analysis_report.md`, `pathway_enrichment_results.csv`, `visualization_summary.md`) are untouched and clearly separate from `real_*` outputs.

## Gate checklist (Steps 4–9)

| Step | Outcome | Evidence |
|---|---|---|
| 4 Alignment gate | PASS | real STAR BAMs, low-mapping% documented |
| 5 Alignment QC | PASS | SAMtools/RSeQC/MultiQC real |
| 6 featureCounts | PASS | real 3×6 matrix, reconciled |
| 7 DESeq2 | PASS | real Wald results, fitType="mean" (run-1 failure preserved) |
| 8 Visualization | PASS | real PCA/MA/volcano/heatmap data |
| 9 Pathway | PASS | genuine zero-enrichment recorded |

**Overall**: The pipeline is mechanically proven **end-to-end** with real tools on a real (subsampled) dataset against a real-loci mini-reference. It demonstrates execution integrity and provenance discipline, but it is **explicitly not** genome-wide biological inference and must not be reported as a GSE52778 re-analysis. Full genome-wide interpretation is a separate later research milestone.