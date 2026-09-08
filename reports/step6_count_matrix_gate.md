# Step 6 Gate Report — featureCounts gene-level count matrix

- **Generated**: Step 6 (quantification), real-loci mini-reference pipeline
- **Scope**: featureCounts v2.1.1 applied to the 6 real sorted STAR BAMs against the real mini-reference GTF → gene-level count matrix
- **Downstream**: STOPPED. No DESeq2, pathway analysis, Nextflow run, backend change, or `isMock` change.

## Inputs & command

- BAMs (coordinate-sorted, indexed, real STAR output): `results/alignment/{C1,C2,C3,T1,T2,T3}_Aligned.sortedByCoord.out.bam`
- Annotation: `data/reference/mini_real/mini_genes.gtf` (real-loci, coordinates identical to the reference used for STAR indexing — no chromosome-name mismatch)
- Command (documented parameter set; Salmon deliberately absent from this run):

```bash
featureCounts \
    -a data/reference/mini_real/mini_genes.gtf \
    -o results/counts/gene_counts.txt \
    -T 8 \
    -p \
    -s 0 \
    results/alignment/C1_Aligned.sortedByCoord.out.bam \
    results/alignment/C2_Aligned.sortedByCoord.out.bam \
    results/alignment/C3_Aligned.sortedByCoord.out.bam \
    results/alignment/T1_Aligned.sortedByCoord.out.bam \
    results/alignment/T2_Aligned.sortedByCoord.out.bam \
    results/alignment/T3_Aligned.sortedByCoord.out.bam
```

- `-s 0` (unstranded) is used because RSeQC `infer_experiment` established the library is non-stranded (Step 5).

## featureCounts run report

- **6 BAM files** consumed, in samplesheet order C1, C2, C3, T1, T2, T3.
- Annotation loaded: **30 features, 3 meta-features (genes), 3 contigs** — matches the 15+9+6 exons of CRISPLD2/GAPDH/ACTB.
- All 6 samples processed inside the single run (no sample skipped), exit 0.

### Gene-level count matrix (`results/counts/gene_counts.txt`)

| Geneid | gene_name | chr | strand | C1 | C2 | C3 | T1 | T2 | T3 |
|---|---|---|---|---|---|---|---|---|---|
| ENSG00000103196.14 | CRISPLD2 | chr16 | + | 5 | 1 | 4 | 35 | 27 | 9 |
| ENSG00000111640.16 | GAPDH | chr12 | + | 225 | 216 | 210 | 212 | 156 | 250 |
| ENSG00000075624.17 | ACTB | chr7 | − | 368 | 422 | 306 | 464 | 596 | 736 |

### Assignment summary (`results/counts/gene_counts.txt.summary`)

| Status | C1 | C2 | C3 | T1 | T2 | T3 |
|---|---|---|---|---|---|---|
| Assigned | 598 | 639 | 520 | 711 | 779 | 995 |
| Unassigned_Unmapped | 0 | 0 | 0 | 0 | 0 | 0 |
| Unassigned_MultiMapping | 426 | 334 | 554 | 546 | 502 | 440 |
| Unassigned_NoFeatures | 164 | 125 | 154 | 187 | 159 | 123 |
| Total alignments (=SAMtools flagstat total) | 1188 | 1098 | 1228 | 1444 | 1440 | 1558 |

- Unmapped = 0 (consistent with flagstat 100% mapped).
- `Unassigned_MultiMapping` + `Unassigned_NoFeatures` reconcile to the total alignment counts exactly — every alignment is accounted for.

## Verification

| gate check | result |
|---|---|
| All six BAMs consumed | PASS (6 inputs, per-sample output lines) |
| Annotation matches reference coordinates (no chr naming mismatch) | PASS — same `mini_genes.gtf` used for the STAR index |
| Counts genuinely produced by featureCounts | PASS — raw tool output header + run log preserved verbatim |
| CRISPLD2, GAPDH, ACTB nonzero counts | PASS — all 3 genes > 0 in all 6 samples |
| Count matrix dimensions | PASS — 3 genes × 6 samples |
| Sample ordering matches samplesheet | PASS — C1 C2 C3 T1 T2 T3 (matches `metadata/samplesheet.csv`) |
| No synthetic counts | PASS — integer counts derived from real alignments; independent idxstats reconciliation below |
| Raw featureCounts output + summary preserved | PASS — `gene_counts.txt`, `gene_counts.txt.summary`, `featurecounts_run.log` |
| Backend unchanged / `isMock` untouched | PASS — neither modified |

### Independent reconciliation (SAMtools idxstats)

Exonic-assigned counts vs whole-locus alignments:

| gene | C1 exonic (featureCounts) | C1 locus alignments (idxstats) | interpretation |
|---|---|---|---|
| CRISPLD2 (chr16) | 5 | 584 | reads land mostly in the huge (≈88 kb) intron; only exonic reads are counted |
| GAPDH (chr12) | 225 | 230 | compact gene — nearly all locus reads are exonic |
| ACTB (chr7) | 368 | 374 | compact gene — nearly all locus reads are exonic |

This matches Step 5's `read_distribution` observation (intronic tags dominated by CRISPLD2's long intron) and confirms featureCounts is counting genuine exonic alignments, not fabricating loci.

## Statistical-power caveat (explicit)

These counts come from only ≈50,000 read pairs/sample against a **3-gene tutorial reference**; they are **not** statistically meaningful differential expression and must not be interpreted as biology for GSE52778. Step 6 proves only that *real genomic alignment → real gene counting* works end-to-end. (CRISPLD2 shows higher T vs C here because most of its few reads happen to fall on exons, but this is incidental at this depth.)

## Gate verdict

| check | result |
|---|---|
| featureCounts executed on real BAMs + real GTF | PASS |
| 6/6 samples counted, 3/3 genes nonzero | PASS |
| Matrix dims + sample order valid | PASS |
| Raw outputs + summary preserved | PASS |
| No backend / `isMock` change | PASS |

**GATE: PASSED. Real count matrix generated; statistical power is a separate concern out of scope for this step.**

## Provenance status

- Count matrix, summary, and featureCounts run log are real tool outputs under `results/counts/` (gitignored).
- Project-level `isMock` flag: **NOT flipped — remains true**.
- Next permitted step when approved: **Step 7 DESeq2 differential expression** on this real count matrix. Do not proceed without explicit gate approval.

> Note: this is a quantification-execution validation at tutorial scale, not a biological claim about GSE52778.