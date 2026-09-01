# Chapter 11: Reference Genome

> The genome and annotation that reads are mapped against. Preparing a
> correct, consistent reference is essential for reproducible
> alignment and counting.

---

## 1. What is it?

The **reference genome** is the complete DNA sequence of an organism
(here *Homo sapiens*, GRCh38) used as the coordinate system for
alignment. Associated with it is a **gene annotation** (GTF) that
marks genes/exons.

Reads are aligned *to* the reference; expression is *counted* using
the annotation.

---

## 2. Why do we need it?

- Without a reference, we cannot locate reads in the genome.
- Without annotation, we cannot assign reads to genes.
- A **consistent** reference (matching chromosome naming) is
  essential; mismatches silently corrupt count matrices.

---

## 3. Where does it fit?

```
Reference genome (FASTA) + annotation (GTF)
    |
    +--> validate (Ch 11)  <--- here
    +--> STAR index (Ch 12)
    +--> Salmon index (Ch 14)
    +--> featureCounts (Ch 15)
```

Reference files live in `data/reference/` and are documented in
`metadata/reference_manifest.yaml`.

---

## 4. Input

For our study:

| File | Description |
|------|-------------|
| `genome.fa` | GRCh38 primary assembly (chr1-22, X, Y, M) |
| `genes.gtf` | GENCODE v44 primary assembly annotation |
| `transcripts.fa` | GENCODE v44 transcript sequences (for Salmon) |

All use **UCSC chromosome naming** (`chr1, chr2, ..., chrX, chrM`).

---

## 5. Output

Reference preparation produces:

- STAR genome index (`data/reference/star_index/`)
- Salmon transcript index (`data/reference/salmon_index/`)
- A validated, reproducible reference setup

---

## 6. How it works

### 6.1 The genome build

- **GRCh38.p14** (hg38) is the current human reference.
- The **primary assembly** excludes non-chromosomal patches/haplotigs.

### 6.2 Chromosome naming -- the critical pitfall

Two conventions coexist:

| Convention | Example | Used by |
|------------|---------|---------|
| UCSC | chr1, chr2, ..., chrX, chrM | GENCODE, UCSC |
| Ensembl | 1, 2, ..., X, MT | Ensembl browser |

**The dangerous bug**: If `genome.fa` uses `chr1` but `genes.gtf`
uses `1`, STAR aligns reads successfully to `chr1`, but featureCounts
looks for genes on `1` and finds none -- producing an **empty count
matrix with no error**.

Our `validate_reference.py` prevents this by checking chromosome
name overlap before indexing.

### 6.3 Splice-junction indexing (sjdbOverhang)

STAR builds annotated splice junctions into its index. The key
parameter:

```
sjdbOverhang = read_length - 1
```

For our 63 bp reads:

```
sjdbOverhang = 63 - 1 = 62
```

This lets a read overhang a junction by one base on either side,
maximizing junction-mapping sensitivity.

### 6.4 genomeSAindexNbases

Controls the suffix array index size. Standard for human
(~3.1 Gbp): **14**. (Reduced for small test genomes.)

---

## 7. Biology behind it

- The reference represents the genome's linear sequence.
- Splice junctions (intron boundaries) come from the GTF annotation.
- Chromosome naming must be consistent so alignment coordinates match
  annotation coordinates.

---

## 8. Command

```bash
# Validate reference compatibility (implemented)
python3 scripts/python/validate_reference.py \
    --fasta data/reference/genome.fa \
    --gtf data/reference/genes.gtf

# Build STAR index (implemented)
bash scripts/build_star_index.sh \
    --fasta data/reference/genome.fa \
    --gtf data/reference/genes.gtf \
    --outdir data/reference/star_index \
    --threads 8 \
    --read-len 63

# Build Salmon index (implemented)
bash scripts/build_salmon_index.sh \
    --transcripts data/reference/transcripts.fa \
    --genome data/reference/genome.fa \
    --outdir data/reference/salmon_index \
    --threads 8
```

---

## 9. Example

The `reference_manifest.yaml` records:

```yaml
genome_assembly: "GRCh38.p14"
release: "GENCODE Release 44 (Ensembl 110)"
chromosome_naming: "UCSC style (chr1, chr2, ..., chrX, chrM)"
star_parameters:
  sjdbOverhang: 62   # 63 - 1
  genomeSAindexNbases: 14
```

This machine-readable record ensures reproducibility.

---

## 10. How to read the output

The validator outputs one of:

- `[SUCCESS] Reference FASTA and GTF are 100% COMPATIBLE.`
- `[FAILED] ... Chromosome naming incompatibility detected!`

The STAR index builder also runs the validator automatically before
indexing.

---

## 11. Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| Chromosome naming mismatch | FASTA chr1 vs GTF 1 | Normalize both naming |
| Empty count matrix | chr naming mismatch | Use validator |
| Out-of-memory indexing | Full human genome | Use WSL2 with enough RAM / mini genome |
| Corrupt reference | Bad download | Verify MD5 from manifest |

---

## 12. Limitations

- Reference quality is only as good as annotation completeness.
- Building the full human STAR index needs ~30 GB RAM.
- For testing, use a **mini reference** (`build_test_reference.py`).

---

## 13. How our project uses it

- `build_star_index.sh` and `build_salmon_index.sh` are implemented
  and documented.
- `validate_reference.py` has **4 passing unit tests**.
- `build_test_reference.py` creates a mini reference (CRISPLD2,
  GAPDH, ACTB) for fast CI/CD.
- `reference_manifest.yaml` tracks versions and parameters.

---

## 14. Official documentation

- **GENCODE human releases**:
  https://www.gencodegenes.org/human/
- **UCSC Genome Browser**:
  https://genome.ucsc.edu/
- **Ensembl human (GRCh38)**:
  https://www.ensembl.org/Homo_sapiens/

---

## 15. Mini exercise

1. Why is chromosome naming consistency between FASTA and GTF
   critical?
2. Calculate `sjdbOverhang` for our 63 bp reads.
3. What does `reference_manifest.yaml` record, and why?
4. Why does the full human STAR index need ~30 GB RAM?
5. Which tool in our project auto-runs the reference validator before
   indexing?

---

> **Next**: [Chapter 12: STAR Aligner](star.md)
