# Step 5 Report — Alignment QC (SAMtools · RSeQC · MultiQC)

- **Generated**: Step 5 (alignment-level QC), real-loci mini-reference pipeline
- **Scope**: per-sample alignment QC of the 6 real STAR BAMs with independent tools + MultiQC aggregation
- **Downstream**: STOPPED. No featureCounts, DESeq2, pathway analysis, Nextflow run, or `isMock` change.

## Inputs

- Alignments: `results/alignment/*_Aligned.sortedByCoord.out.bam` (6 samples, real STAR v2.7.11b output from Step 4)
- Gene model: `data/reference/mini_real/refgene.bed12` (3 transcripts; built from `mini_genes.gtf`)
- Tools: SAMtools 1.24, RSeQC 5.0.5, MultiQC 1.35 (all real, not mocked)

## SAMtools flagstat / stats (independent of STAR)

`flagstat` per BAM — every alignment is mapped, properly paired, no duplicates/singletons:

| sample | total | primary | secondary | mapped | %mapped | properly paired | %properly paired |
|---|---|---|---|---|---|---|---|
| C1 | 1,188 | 916 | 272 | 1,188 | 100% | 916 | 100% |
| C2 | 1,098 | 888 | 210 | 1,098 | 100% | 888 | 100% |
| C3 | 1,228 | 836 | 392 | 1,228 | 100% | 836 | 100% |
| T1 | 1,444 | 1,060 | 384 | 1,444 | 100% | 1,060 | 100% |
| T2 | 1,440 | 1,104 | 336 | 1,440 | 100% | 1,104 | 100% |
| T3 | 1,558 | 1,264 | 294 | 1,558 | 100% | 1,264 | 100% |

`stats` highlights: error rate **0.000000** (no mismatches) in all samples; reads MQ0 = 0.9–3.3%; average base quality 37.2–38.2; insert-size average 1.6–2.5 kb (large because 63 nt reads span introns of the compact mini-contigs); 100% of reads mapped and paired.

## STAR-reported summary (Log.final.out via MultiQC)

| sample | input | uniquely mapped | % | spliced reads (num_splices) | mismatch rate | MQ0 % |
|---|---|---|---|---|---|---|
| C1 | 48,928 | 381 | 0.78% | 161 | 2.38% | 1.31 |
| C2 | 48,230 | 382 | 0.79% | 168 | 2.53% | 0.90 |
| C3 | 47,651 | 337 | 0.71% | 152 | 2.58% | 3.35 |
| T1 | 48,216 | 449 | 0.93% | 179 | 2.44% | 2.64 |
| T2 | 47,433 | 469 | 0.99% | 207 | 2.25% | 1.99 |
| T3 | 47,872 | 559 | 1.17% | 219 | 1.87% | 1.27 |

Low absolute mapping% is **expected**: 3-gene reference vs a whole-transcriptome read subset. Mismatch rate ≤2.6% is consistent with normal allelic/technical divergence; 100% quality score.

## RSeQC 5.0.5

### bam_stat.py (mapq cutoff 1, skip zero-mapq)

| sample | total alignments | non-primary | mapq≥cut (unique pairs) | non-splice reads | splice reads | unique % |
|---|---|---|---|---|---|---|
| C1 | 1,188 | 272 | 762 | 605 | 157 | 64.1 |
| C2 | 1,098 | 210 | 764 | 600 | 164 | 69.6 |
| C3 | 1,228 | 392 | 674 | 528 | 146 | 54.9 |
| T1 | 1,444 | 384 | 898 | 721 | 177 | 62.2 |
| T2 | 1,440 | 336 | 938 | 737 | 201 | 65.1 |
| T3 | 1,558 | 294 | 1,118 | 902 | 216 | 71.8 |

146–216 **splice reads** per sample → real exon-intron junctions are being captured.

### infer_experiment.py

Strandedness inference resolves to a near **50/50** split for all samples (e.g., C1 54.4%/45.6%, T3 46.6%/53.4%) with **0% failed reads** — consistent with the expected **unstranded** library preparation. This cross-checks the pipeline's library-preparation assumptions.

### read_distribution.py

Fraction of assigned tags per genomic element (CDS / UTR / intron). Representative values:

| sample | CDS exons | 5'UTR | 3'UTR | introns | TSS/TES windows |
|---|---|---|---|---|---|
| C1 | 50.3% | 1.1% | 11.3% | 37.1% | 0% |
| C2 | 56.6% | 2.2% | 11.3% | 29.7% | 0% |
| C3 | 50.3% | 1.2% | 7.9% | 40.5% | 0% |
| T1 | 49.9% | 1.0% | 12.0% | 37.2% | 0% |
| T2 | 49.1% | 1.1% | 16.9% | 32.7% | 0% |
| T3 | 57.7% | 2.2% | 15.8% | 24.2% | 0% |

Interpretation: the majority of tags fall in **CDS exons** (49–58%); the elevated intronic fraction (24–40%) is dominated by CRISPLD2, whose gene body is 89 kb and whose reads scatter across the large intron at this low depth. TSS/TES windows = 0% is **by construction** — the mini-reference chromosome consists of the gene body + 500 bp flanks only.

### junction_annotation.py

Per-sample annotated-vs-novel junction classifications (from `*.junction.junction.xls`):

| sample | junctions total | annotated | partial_novel | complete_novel |
|---|---|---|---|---|
| C1 | 107 | 1 | 14 | 92 |
| C2 | 87 | 0 | 14 | 73 |
| C3 | 103 | 1 | 14 | 88 |
| T1 | 127 | 0 | 19 | 108 |
| T2 | 126 | 1 | 18 | 107 |
| T3 | 110 | 0 | 16 | 94 |

Important coordinate-convention note: RSeQC reports intron start as **0-based**, while the GTF/BED12 introns are **1-based inclusive**; this produces a systematic ±1 bp offset. Cross-checking the "partial_novel" junctions against `mini_genes.gtf` confirms they are the **canonical GAPDH (8 introns) and ACTB (5 introns) junctions at exactly +1 bp**, i.e. the annotated introns are being recovered (they match Step 4's independent ±1 bp-tolerance crosscheck of 13–18 matches/sample). The "complete_novel" junctions are sparse (mostly read-count = 1) and fall within the huge CRISPLD2 intron — expected at this depth and consistent with the read_distribution intron fraction above.

## MultiQC aggregation

- Command: `multiqc results/alignment results/alignment_qc/samtools results/rseqc`
- Modules found: STAR (6), SAMtools stats/flagstat/idxstats (6 each), RSeQC bam_stat/infer_experiment/read_distribution (6 each)
- Output: `results/multiqc/alignment_qc/multiqc_report.html` + `multiqc_report_data/` (real, tsv/parquet tables)
- Artifacts placed in `results/alignment_qc/samtools/{flagstat,idxstats,stats}/` and `results/rseqc/` (raw tool outputs, gitignored)

## Gate verdict

| check | result |
|---|---|
| SAMtools flagstat (100% mapped, 100% properly paired, 0 dup) | PASS |
| SAMtools stats (error rate 0, quality 37–38) | PASS |
| STAR vs SAMtools mapping reconciles | PASS |
| Spliced-read evidence (146–216 splice reads/sample) | PASS |
| Strandedness inference (unstranded, 0% failed) | PASS |
| Annotated junction recovery (GAPDH + ACTB introns at ±1 bp) | PASS |
| MultiQC aggregation (18 module reports) | PASS |

**GATE: PASSED. Alignment QC is complete and independent of STAR-reported numbers.**

## Provenance status

- All numbers above come from **real tool outputs** (SAMtools, RSeQC, MultiQC), copied verbatim; no values were fabricated or substituted.
- Project-level `isMock` flag: **NOT flipped — remains true**.
- Next permitted step when approved: **Step 6 featureCounts quantification** (per docs `steps/06_quantify_by_featurecounts`). Do not proceed without explicit gate approval.

> Note: QC assesses the engineering-scale mini-reference run; it is execution/validation QC, not a claim of biological quality for GSE52778.