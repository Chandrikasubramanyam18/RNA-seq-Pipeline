# Chapter 05: FASTA Format

> The simple text format used for reference genome sequences and
> transcript sequences -- files the aligner and quantifier need to
> know what to map reads against.

---

## 1. What is it?

**FASTA** is a plain-text format for representing nucleotide or
protein sequences. It is much simpler than FASTQ: it contains just
**sequence headers** and **sequence lines**, with **no quality
scores**.

A FASTA file looks like:

```
>header/description
SEQSEQSEQSEQ...
SEQSEQ...
```

- A line starting with `>` is a **header** (sequence identifier +
  optional description).
- Lines after the header are the **sequence** (wrapped across lines).

For RNA-seq, FASTA is most importantly used for:

- The **reference genome** (`genome.fa`)
- The **transcriptome** (`transcripts.fa`)

---

## 2. Why do we need it?

To map reads, an aligner must know the **reference sequence**. The
reference genome (in FASTA format) is what STAR aligns reads against.
Salmon also needs transcript sequences (FASTA) to build its index.

Without a correct, consistent FASTA reference, alignment and
quantification fail or produce garbage.

---

## 3. Where does it fit?

```
Reference genome FASTA (this chapter)
    |
    +--> STAR genome index (Ch 12)
    |
    +--> Salmon index (Ch 14)
    |
    +--> read alignment & quantification
```

FASTA files live in `data/reference/` and are described by
`metadata/reference_manifest.yaml`.

---

## 4. Input

The reference FASTA files for our study (found in `data/reference`):

| File | Description | Source |
|------|-------------|--------|
| `genome.fa` | GRCh38 primary assembly (chromosomes 1-22, X, Y, M) | GENCODE v44 |
| `transcripts.fa` | All protein-coding and non-coding transcripts | GENCODE v44 |

These are documented in `metadata/reference_manifest.yaml` with URLs
and checksums.

---

## 5. Output

FASTA is an input to building **indices**:

- STAR genome index (from `genome.fa`)
- Salmon transcript index (from `transcripts.fa`)

It can also be validated for chromosome-naming consistency using our
`validate_reference.py` script.

---

## 6. How it works

### 6.1 The Header Line

The header (starting with `>`) contains the chromosome/contig
identifier. This is **critical** because aligners match reads to these
identifiers.

Example GRCh38 header:

```
>chr1 AC:CM000663.2
ACCTCTGGCTAA...
```

Here the identifier is `chr1` (UCSC chromosome naming). The rest
after the first space is description.

### 6.2 Chromosome Naming

There are two common naming conventions:

| Convention | Example | Used by |
|------------|---------|---------|
| **UCSC** | chr1, chr2, ..., chrX, chrM | GENCODE, UCSC tools |
| **Ensembl** | 1, 2, ..., X, MT | Ensembl browser |

**Critical pitfall**: If the genome FASTA uses `chr1` but the GTF
annotation uses `1`, reads will align but featureCounts will map zero
reads to genes -- with no error message. Our `validate_reference.py`
catches this (Chapter 11, 12).

### 6.3 Sequence Lines

The sequence lines contain the nucleotides (A, C, G, T, N). They may
be wrapped across multiple lines; tools ignore line breaks. Bases are
case-insensitive (though uppercase is conventional).

### 6.4 Nucleotide codes

| Symbol | Meaning |
|--------|---------|
| A / C / G / T | The four standard bases |
| N | Unknown/ambiguous |
| R / Y / S / W / K / M | IUPAC ambiguity codes (rare in genome files) |

### 6.5 Building the STAR / Salmon indices

The FASTA is fed to index builders:

```bash
# STAR genome index (Ch 12)
bash scripts/build_star_index.sh \
    --fasta data/reference/genome.fa \
    --gtf data/reference/genes.gtf \
    --outdir data/reference/star_index

# Salmon index (Ch 14)
bash scripts/build_salmon_index.sh \
    --transcripts data/reference/transcripts.fa \
    --genome data/reference/genome.fa \
    --outdir data/reference/salmon_index
```

---

## 7. Biology behind it

- The genome FASTA is the **complete DNA sequence** of the organism.
- The transcriptome FASTA is the **cDNA sequences** of all transcripts.
- Reads are matched against these sequences; the number of reads
  matching each gene/transcript gives expression.

---

## 8. Command

Our implemented reference validator checks FASTA compatibility:

```bash
python3 scripts/python/validate_reference.py \
    --fasta data/reference/genome.fa \
    --gtf data/reference/genes.gtf

# Or from build_star_index.sh (auto-runs the validator first)
```

This verifies:
- FASTA headers exist
- GTF chromosomes exist
- The chromosome naming conventions match (chr prefix consistency)

---

## 9. Example

A tiny FASTA (from our test reference builder in
`scripts/python/build_test_reference.py`):

```
>chr16 Human Chromosome 16 locus (CRISPLD2 region)
ATGCGATCGATCGATCGATCGATCGATCGACTAGCTAGCTAG
GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAG
>chr12 Human Chromosome 12 locus (GAPDH region)
GGCCAAATTTCCCGGGAAATTTCCCGGGAAATTTCCCGGG
GGCCAAATTTCCCGGGAAATTTCCCGGGAAATTTCCCGGG
```

Two chromosomes (`chr16`, `chr12`), each with wrapped sequence lines.

---

## 10. How to read the output

When validating a FASTA:

| Field | What to check |
|-------|---------------|
| Header identifiers | Match GTF chromosomes (chr prefix) |
| Sequence only A/C/G/T/N | No unexpected characters |
| Consistent case | Convention only, not important |
| Wrapped lines | Line breaks are fine |

---

## 11. Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| **Chromosome naming mismatch** | FASTA uses chr1, GTF uses 1 | Normalize both; validate |
| **Missing/duplicate chromosomes** | Truncated or bad reference | Re-download, checksum verify |
| **Corrupt gzip`*.fa.gz`** | Bad download | Verify MD5 (reference_manifest) |
| **Whitespace/blank lines in sequence** | Formatting | Should be fine mimixed, but validate |

---

## 12. Limitations

- FASTA has **no quality information** (it's a reference, not reads).
- FASTA tells you sequence, not annotation; for gene structure you
  need GTF (Chapter 07).
- Large genome FASTA files are memory-heavy for indexing.

---

## 13. How our project uses it

- `data/reference/genome.fa` feeds STAR index building.
- `data/reference/transcripts.fa` feeds Salmon index building.
- `validate_reference.py` ensures the FASTA and GTF chromosomes match.
- `reference_manifest.yaml` tracks versions, URLs, and MD5s for
  reproducibility.
- The reference validator has 4 passing unit tests
  (`tests/unit/test_reference_validator.py`).

---

## 14. Official documentation

- **FASTA format (Wikipedia)**:
  https://en.wikipedia.org/wiki/FASTA_format
- **NCBI FASTA format**:
  https://www.ncbi.nlm.nih.gov/genbank/fastaformat/
- **GENCODE human release**:
  https://www.gencodegenes.org/human/

---

## 15. Mini exercise

1. Write a FASTA header and a few sequence lines for a short
   chromosome `chrX`.
2. Explain the difference between FASTA and FASTQ.
3. Why would it be a serious bug if `genome.fa` used `chr1` but
   `genes.gtf` used `1`?
4. Which two FASTA files does our pipeline use, and which tools
   consume each?
5. Run `python3 scripts/python/validate_reference.py` with the
   reference files (if present) and note the output.

---

> **Next**: [Chapter 06: SAM/BAM Format](bam.md)
