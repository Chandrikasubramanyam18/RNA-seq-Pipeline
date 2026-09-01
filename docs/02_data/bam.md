# Chapter 06: SAM/BAM Format

> The binary alignment format produced after mapping reads to the
> reference genome. It records where every read aligned, how it
> aligned, and with what confidence.

---

## 1. What is it?

**SAM** (Sequence Alignment/Map) is a text format describing read
alignments to a reference. **BAM** is the **binary, compressed**
version of SAM. Tools almost always use BAM because it is far smaller.

Every aligned read gets a **single line** in a SAM/BAM file, containing
~11 mandatory fields ending with the **CIGAR** string and the **FLAG**.

BAM/SAM files are produced by aligners (STAR) and manipulated by
SAMtools.

---

## 2. Why do we need it?

Alignment is the step that determines **where each read came from** in
the genome. The BAM file records this information and is the input to:

- **featureCounts** (count reads per gene)
- **RSeQC** (gene body coverage, read distribution)
- **SAMtools** (sorting, indexing, statistics)

Without BAM files, we cannot summarize reads into gene counts or
assess many QC metrics.

---

## 3. Where does it fit?

```
FASTQ -> STAR (align) -> BAM   <--- here
                               |
                               +--> SAMtools (sort/index/flagstat)
                               +--> featureCounts (Ch 15)
                               +--> RSeQC
```

BAM lives in `results/alignment/`.

---

## 4. Input

The input to alignment is the **trimmed FASTQ** files and the
**STAR genome index**:

- Trimmed reads: `data/processed/*_trimmed_R{1,2}.fastq.gz`
- STAR index: `data/reference/star_index/`

---

## 5. Output

Alignment produces, per sample:

| File | Description |
|------|-------------|
| `*.bam` | Coordinate-sorted binary alignments |
| `*.bai` | BAM index |
| `*.flagstat` | Mapping statistics |
| `*.idxstats` | Per-chromosome mapping stats |
| STAR Log files | Alignment summary |

These live in `results/alignment/`.

---

## 6. How it works

### 6.1 The 11 mandatory SAM fields

Each alignment line has tab-separated fields:

| Col | Field | Meaning |
|-----|-------|---------|
| 1 | QNAME | Read name |
| 2 | FLAG | Bitwise flags (see below) |
| 3 | RNAME | Reference/contig name (chromosome) |
| 4 | POS | 1-based leftmost position |
| 5 | MAPQ | Mapping quality |
| 6 | CIGAR | Alignment summary (see below) |
| 7 | RNEXT | Paired mate reference |
| 8 | PNEXT | Paired mate position |
| 9 | TLEN | Template length (insert size) |
| 10 | SEQ | Read sequence |
| 11 | QUAL | Read quality |

Optional fields (tag:type:value) follow, e.g., `NH:i:1` (number of
place this read mapped).

### 6.2 The FLAG

The FLAG is a number encoding alignment properties as bits. Common
values:

| Flag (decimal) | Meaning |
|----------------|---------|
| 0 | Read unmapped = 4 |
| 1 | Read is paired |
| 2 | Properly paired (both mates aligned) |
| 4 | Read unmapped |
| 8 | Mate unmapped |
| 16 | Read on reverse strand |
| 32 | Mate on reverse strand |
| 64 | First in pair (R1) |
| 128 | Second in pair (R2) |
| 256 | Secondary alignment |
| 2048 | Supplementary alignment |

For RNA-seq:
- **16** (reverse strand) matters for stranded libraries.
- **256/2048** (multiple/supplementary) matter for reads spanning
  splice junctions or multimapping.

### 6.3 The CIGAR string

CIGAR (Compact Idiosyncratic Gapped Alignment Report) describes how a
read aligns, using operations:

| Op | Meaning |
|----|---------|
| M | Match/mismatch (aligned) |
| I | Insertion (in read) |
| D | Deletion (in reference) |
| N | Skipped region (intron!) -- key for RNA-seq |
| S | Soft clip (unaligned bases at ends) |
| H | Hard clip |
| P | Padding |
| = / X | Match / mismatch specifically |

Example CIGAR: `5M2N8M`

- 5 bases match, then skip 2 bases (**intron/exon junction**), then
  8 bases match.

The `N` operation is fundamental to RNA-seq, which aligns reads
across splice junctions (exon1 ... intron ... exon2).

### 6.4 SAMtools operations

SAMtools is the standard tool for working with BAM:

```bash
# Sort BAM by coordinate
samtools sort -o sorted.bam input.bam

# Index the BAM
samtools index sorted.bam

# Mapping statistics
samtools flagstat sorted.bam

# Per-chromosome counts
samtools idxstats sorted.bam
```

---

## 7. Biology behind it

- Each BAM record maps a read to a genomic locus.
- **MAPQ** reflects alignment confidence (higher = more unique).
- The **CIGAR N** operation represents introns -- genuine biology
  captured by splice-aware alignment.
- **Flags** encode strandedness, pairing, and multimapping, which
  affect counting.

---

## 8. Command

```bash
# Check mapping statistics for a sorted BAM
samtools flagstat results/alignment/C1_sorted.bam

# Index a BAM
samtools index results/alignment/C1_sorted.bam

# Inspect alignments in a region
samtools view results/alignment/C1_sorted.bam chr16:1-1000 | head
```

(Requires alignment to have been run and files to exist.)

---

## 9. Example

A simplified BAM line:

```
SRR1039508.1  99  chr16  1000  60  30M   =   1200  230  ACGT...  IIHH...
```

- `99` = flag (128+16+2+1: paired, proper, reverse, second-in-pair)
- RNAME = `chr16`
- POS = 1000
- MAPQ = 60 (high confidence)
- CIGAR = `30M` (30 bases matched)

---

## 10. How to read the output

`flagstat` output example meaning:

```
32356870 + 0 in total (QC-passed reads)
31420000 + 0 mapped (97.1% : N/A)
  ... properly paired ...
```

Key metrics:
- **% mapped**: fraction of reads that aligned (should be high, ~90%+)
- **properly paired %**: both mates aligned in correct orientation
- **unmapped**: reads that failed to map

---

## 11. Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| Low mapping rate | Adapter contamination / poor quality | Trim better in fastp |
| Properly paired low | RNA-seq library issues | Check strandness/insert |
| "Chr not found" | Reference naming mismatch | Fix FASTA/GTF naming |
| Unmapped due to N | CIGAR over intron misunderstood | This is normal for RNA-seq |
| BAM too big | Uncompressed SAM | Convert to BAM |

---

## 12. Limitations

- BAM/SAM does **not** tell you gene-level counts directly; you need
  featureCounts (quantification).
- Not all reads map uniquely; multimapping complicates counting.
- Interpreting strandness requires knowing library type.

---

## 13. How our project uses it

- STAR produces SAM; SAMtools converts to sorted, indexed **BAM**.
- BAM files are stored in `results/alignment/`.
- featureCounts reads BAM to build gene counts (Chapter 15).
- RSeQC reads BAM for gene body coverage (alignment QC).
- The workflow architecture documents SAMtools sort/index/flagstat.

Note: The actual STAR/SAMtools execution is part of the *future*
Nextflow implementation; the scripts currently in the repo are the
index builders and QC wrappers.

---

## 14. Official documentation

- **SAMtools / SAM specification**:
  https://samtools.github.io/hts-specs/SAMv1.pdf
- **SAMtools documentation**:
  https://www.htslib.org/doc/samtools.html
- **Understanding BAM flags & CIGAR**:
  https://bioinformatics.stackexchange.com/questions/tagged/cigar

---

## 15. Mini exercise

1. Decode the CIGAR `5M2N8M` -- what does it tell you about an exon
   junction?
2. What does a FLAG of 64 mean in paired-end data?
3. Give two reasons a read might be reported as unmapped.
4. Which tool converts STAR's raw SAM output into a sorted, indexed
   BAM?
5. Why is `N` (skipped) in CIGAR so important specifically for
   RNA-seq?

---

> **Next**: [Chapter 07: GTF Format](gtf.md)
