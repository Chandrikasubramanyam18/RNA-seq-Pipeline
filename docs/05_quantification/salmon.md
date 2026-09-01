# Chapter 14: Salmon

> An alignment-free quantifier that estimates transcript-level
> abundance (TPM and counts) using quasi-mapping.

---

## 1. What is it?

**Salmon** is a tool for quantifying transcript abundances directly
from reads, without performing full genome alignment. It uses
**quasi-mapping** to pseudo-align reads to a **transcriptome index**
and estimates abundance using an expectation-maximization (EM)
algorithm.

Outputs include **transcripts per million (TPM)** and estimated counts
per transcript.

---

## 2. Why do we need it?

- Provides a fast, alignment-free alternative to genome alignment.
- Quantifies at the **transcript (isoform) level**, not just gene.
- Corrects for sequence-specific and fragment GC biases.
- TPM is directly comparable across samples (though normalization is
  still needed for DE).

It runs **in parallel** with the STAR/featureCounts path in our
pipeline.

---

## 3. Where does it fit?

```
Cleaned FASTQ (Ch 09) + Salmon index (Ch 11)
        |
        v
      Salmon  <--- here
        |
        v
   quant.sf (TPM, counts)
```

This is a **parallel** quantification path to featureCounts.

---

## 4. Input

- **Salmon index**: `data/reference/salmon_index/`
- **Cleaned reads**: `data/processed/*_trimmed_R{1,2}.fastq.gz`

The index comes from `build_salmon_index.sh` (Ch 11).

---

## 5. Output

Per sample, a `quant.sf` file (in `results/salmon/<sample>/`):

| Column | Meaning |
|--------|---------|
| Name | Transcript ID |
| Length | Transcript length |
| EffectiveLength | Length adjusted for bias |
| TPM | Transcripts per million |
| NumReads | Estimated read count |

`salmon quant` writes a directory per sample containing
`quant.sf`, `quant.genes.sf`, `lib_format_counts.json`, and logs.

---

## 6. How it works

### 6.1 Quasi-mapping

Salmon indexes transcripts into a hash of k-mers. Reads are
**quasi-mapped** (approximate, without full base-level alignment) to
transcripts.

### 6.2 Decoy-aware indexing

To handle genomic DNA contamination / pre-mRNA, Salmon can index
transcripts **plus the genome as decoys** (build_salmon_index.sh).
Reads that match only decoys are excluded, preventing false
transcript hits.

### 6.3 Abundance estimation (EM)

Salmon assigns reads to transcripts using an **expectation-
maximization** algorithm, resolving multi-mapping ambiguity and
estimating relative abundance. TPM is derived from these estimates.

### 6.4 Bias correction

Salmon models sequencing biases (GC, positional, sequence-specific)
to produce more accurate abundance estimates.

---

## 7. Biology behind it

- Salmon quantifies **transcripts**, capturing isoform differences.
- TPM reflects relative abundance normalized to transcript length and
  library size.
- Decoy-aware indexing prevents contamination reads from inflating
  transcript counts.

---

## 8. Command

```bash
# Build index (implemented; Ch 11)
bash scripts/build_salmon_index.sh \
    --transcripts data/reference/transcripts.fa \
    --genome data/reference/genome.fa \
    --outdir data/reference/salmon_index

# Quantify (standard Salmon quant; part of future workflow)
salmon quant \
    -i data/reference/salmon_index \
    -l A \
    -1 data/processed/C1_trimmed_R1.fastq.gz \
    -2 data/processed/C1_trimmed_R2.fastq.gz \
    -p 8 \
    -o results/salmon/C1
```

---

## 9. Example

A few lines of `quant.sf`:

| Name | Length | EffectiveLength | TPM | NumReads |
|------|--------|-----------------|-----|----------|
| ENST00000219431 | 1200 | 1130 | 42.5 | 4800 |
| ENST00000229239 | 1040 | 980 | 210.3 | 20400 |

High TPM = highly expressed.

---

## 10. How to read the output

| Column | Meaning | Use |
|--------|---------|-----|
| TPM | Transcripts per million | Relative abundance, cross-sample comparable |
| NumReads | Estimated counts | For DE (needs normalization) |
| EffectiveLength | Bias-adjusted length | Internal for TPM |

For DESeq2, you typically aggregate transcript counts to **gene
level** (via tximport) or use featureCounts instead.

---

## 11. Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| Index not compatible | Rebuilt index needed | Rebuild with same params |
| `-l A` library type error | Auto-detect fails | Set `-l IU`/`ISR` explicitly |
| Low mapping/quant | Poor trimming | Re-run fastp |
| Decoy file malformed | Bad decoys.txt | Regenerate decoy list |

---

## 12. Limitations

- Salmon is alignment-free; some detailed alignment-based QC (RSeQC,
  junction analysis) still needs STAR/BAM.
- Requires a transcriptome index (from `transcripts.fa`).
- TPM is relative abundance, not absolute count; DE still needs
  count-based normalization.

---

## 13. How our project uses it

- `build_salmon_index.sh` is **implemented** and creates a decoy-aware
  index.
- Salmon quantification is a **parallel** path to featureCounts in the
  workflow architecture.
- Outputs (`results/salmon/`) are consumed for transcript-level
  analysis.
- Actual `salmon quant` execution is part of the **future** Nextflow
  workflow.

---

## 14. Official documentation

- **Salmon**:
  https://combine-lab.github.io/salmon/
- **Salmon paper** (Patro et al. 2017, Nature Methods):
  https://www.nature.com/articles/nmeth.4197

---

## 15. Mini exercise

1. What is quasi-mapping, and why is it faster than full alignment?
2. Why is a decoy-aware index beneficial?
3. What is TPM, and how does it differ from raw read counts?
4. Why does DE still require normalizing Salmon counts even though
   TPM is "normalized"?
5. In our pipeline, which two quantification approaches run in
   parallel?

---

> **Next**: [Chapter 15: featureCounts](featurecounts.md)
