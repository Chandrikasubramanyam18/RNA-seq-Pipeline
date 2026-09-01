# Chapter 12: STAR Aligner

> STAR (Spliced Transcripts Alignment to a Reference) is the
> splice-aware aligner used to map RNA-seq reads to the genome,
> including reads that span exon junctions.

---

## 1. What is it?

**STAR** is a fast and accurate **splice-aware aligner**. It maps
short reads to a reference genome while recognizing **splice
junctions** -- where a read spans an intron (exon1 ... exon2).

It is the de facto standard for bulk RNA-seq alignment, offering high
sensitivity and speed.

---

## 2. Why do we need it?

RNA-seq reads can span **exon junctions**. A simple length-agnostic
mapper (like a plain BLAST) would break such reads. STAR:

- Aligns the full read, including across junctions (CIGAR `N`)
- Uses annotated splice junctions (from the GTF) plus novel junctions
- Produces BAM alignments for downstream counting

---

## 3. Where does it fit?

```
Cleaned FASTQ (Ch 09) + STAR index (Ch 11)
        |
        v
      STAR  <--- here
        |
        v
   BAM (Ch 06/13)
        |
        +--> featureCounts (Ch 15)
        +--> RSeQC
```

STAR aligns each sample to produce a BAM.

---

## 4. Input

- **Reference index**: `data/reference/star_index/` (built in Ch 11)
- **Cleaned reads**: `data/processed/*_trimmed_R{1,2}.fastq.gz`

---

## 5. Output

Per sample:

| File | Description |
|------|-------------|
| `*.sam` / `*.bam` | Alignments |
| `*Log.final.out` | Summary statistics |
| `*Log.out` | Run log |
| `SJ.out.tab` | Detected splice junctions |

(Actual STAR output is part of the future Nextflow workflow.)

---

## 6. How it works

### 6.1 Two-pass approach

1. **Index generation** (done in Ch 11): build a suffix array
   incorporating annotated splice junctions (`sjdbOverhang=62`).
2. **Alignment**: for each read, find the best mapping.

### 6.2 Splice-aware alignment

STAR searches for the read's **exonic portions** and joins them across
**introns** with the `N` CIGAR operation:

```
read:   AAAAACCCCCTTTTT
genome: AAAAACCCCC------TTTTT   (------ = intron)
CIGAR:  5M5N5M
```

### 6.3 Novel vs annotated junctions

- STAR uses annotated junctions from the GTF (in the index).
- It also **discovers novel junctions** during alignment.
- Junctions are reported in `SJ.out.tab`.

### 6.4 Modes

- **genomeGenerate**: build index (used in Ch 11).
- **alignReads**: align reads (this chapter's role).

---

## 7. Biology behind it

- The `N` (skipped) CIGAR op represents **introns** -- genuine
  biology (pre-mRNA splicing).
- Mapping across junctions is essential because most multi-exon genes
  produce reads that span junctions.
- `sjdbOverhang=62` ensures reads overhang junctions properly.

---

## 8. Command

```bash
# Index (already covered in Ch 11) -- implemented
bash scripts/build_star_index.sh \
    --fasta data/reference/genome.fa \
    --gtf data/reference/genes.gtf \
    --outdir data/reference/star_index \
    --threads 8 --read-len 63

# Align reads (standard STAR command; part of future workflow)
STAR \
    --genomeDir data/reference/star_index \
    --readFilesIn data/processed/C1_trimmed_R1.fastq.gz data/processed/C1_trimmed_R2.fastq.gz \
    --readFilesCommand zcat \
    --runThreadN 8 \
    --outSAMtype BAM SortedByCoordinate \
    --outFileNamePrefix results/alignment/C1_
```

---

## 9. Example

The `*Log.final.out` summary reports key stats:

```
Number of input reads                20000000
Uniquely mapped reads %                93.5%
Number of reads mapped to multiple loci  1.2%
% of reads unmapped: too short            1.0%
```

- **% uniquely mapped** is the key quality metric (~90%+ is good).

---

## 10. How to read the output

| Metric | Meaning | Good value |
|--------|---------|-----------|
| Uniquely mapped % | Reads mapped to one locus | >85-90% |
| Multiple loci % | Multimapping reads | low |
| % unmapped: too short | Reads too short after trimming | low |
| Splice junctions found | Novel junctions detected | expected |

---

## 11. Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Error: could not open index" | Index not built / wrong path | Build/re-run index |
| Out of memory | Full human genome index | More RAM / mini genome |
| Low mapping rate | Adapters/quality | Better trimming |
| chr mismatch | Wrong reference naming | Validate reference |

---

## 12. Limitations

- STAR needs substantial RAM for the full human genome (~30 GB).
- It produces genome-level alignments but not directly gene counts
  (that's featureCounts).
- For protein alignment / other organisms, parameters vary.

---

## 13. How our project uses it

- The STAR index builder (`build_star_index.sh`) is **implemented**.
- The index uses `sjdbOverhang=62` and `genomeSAindexNbases=14`.
- Actual read alignment is part of the **future** Nextflow workflow,
  but the index prep is ready.
- RSeQC / featureCounts consume STAR's BAM output.

---

## 14. Official documentation

- **STAR GitHub**:
  https://github.com/alexdobin/STAR
- **STAR manual**:
  https://github.com/alexdobin/STAR/blob/master/doc/STARmanual.pdf
- **STAR paper** (Dobin et al. 2013, Bioinformatics):
  https://academic.oup.com/bioinformatics/article/29/1/15/272537

---

## 15. Mini exercise

1. Why is splice-aware alignment essential for RNA-seq?
2. What does the `N` CIGAR operation represent biologically?
3. Explain the meaning of `sjdbOverhang=62` for our 63 bp reads.
4. What is the key quality metric in STAR's `Log.final.out`?
5. Distinguish STAR's *index* step (Ch 11) from its *alignment* step
   (this chapter).

---

> **Next**: [Chapter 13: SAMtools](samtools.md)
