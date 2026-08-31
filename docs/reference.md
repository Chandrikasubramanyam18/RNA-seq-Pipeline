# Reference Genome & Annotation Management Guide

## 1. Provenance & Version Control

To ensure strict scientific reproducibility and prevent silent alignment corruption, every genomic reference file must be versioned, checksummed, and validated for internal chromosome naming consistency:

| Property | Standard Pipeline Choice | Description |
| :--- | :--- | :--- |
| **Organism** | *Homo sapiens* | Human (Taxonomy ID: 9606) |
| **Genome Build** | GRCh38.p14 (hg38) | Primary assembly excluding patch haplotigs |
| **Gene Annotation** | GENCODE Release 44 | Comprehensive gene annotation (Ensembl 110 compatible) |
| **Chromosome Naming** | UCSC Style | `chr1, chr2, ..., chr22, chrX, chrY, chrM` |
| **Manifest Record** | `metadata/reference_manifest.yaml` | Machine-readable download URLs, file checksums, and parameters |

---

## 2. Critical Pitfalls: Chromosome Naming Discrepancies

One of the most dangerous and common silent bugs in RNA-seq bioinformatics is combining:
* A Genome FASTA from **Ensembl** (which names chromosomes as `1, 2, 3, X`)
* A GTF Annotation from **GENCODE / UCSC** (which names chromosomes as `chr1, chr2, chr3, chrX`)

### The Consequence:
Aligners (such as STAR) will align reads to chromosome `1`, but when `featureCounts` attempts to summarize reads overlapping annotated genes on `chr1`, zero reads will match, producing an empty or severely corrupted count matrix with zero warning from the tool!

### The Solution:
Our pre-flight validator [`scripts/python/validate_reference.py`](../scripts/python/validate_reference.py) inspects the FASTA headers and GTF feature seqnames before any indexing begins to guarantee 100% naming concordance.

---

## 3. Splice-Junction Indexing (STAR `sjdbOverhang`)

STAR incorporates annotated splice junctions directly into its suffix array index to accelerate splice-aware alignment:

$$\text{sjdbOverhang} = \text{ReadLength} - 1$$

* For our **GSE52778** dataset ($2 \times 63$ bp reads):
  $$\text{sjdbOverhang} = 63 - 1 = 62$$
* **Why $L - 1$**: This allows a read to overhang a splice junction by a single base on either side, maximizing mapping sensitivity across exon-exon junctions.

---

## 4. Transcriptome Quasi-Mapping & Decoys (Salmon)

When building a Salmon index:
* **Direct Transcriptome Index**: Reads are mapped directly to cDNA transcript sequences (`transcripts.fa`).
* **Decoy-Aware Index (`gentrome.fa`)**: Because RNA-seq libraries occasionally contain genomic DNA contamination or unprocessed pre-mRNAs, reads originating from non-transcribed genomic regions might falsely align to similar transcript sequences. Appending the whole genome as a **decoy** allows Salmon to detect and discard non-transcriptomic fragments.

---

## 5. Command Reference

```bash
# 1. Validate FASTA and GTF compatibility
python scripts/python/validate_reference.py \
    --fasta data/reference/genome.fa \
    --gtf data/reference/genes.gtf

# 2. Build STAR Index (Linux / WSL)
bash scripts/build_star_index.sh \
    --fasta data/reference/genome.fa \
    --gtf data/reference/genes.gtf \
    --outdir data/reference/star_index \
    --threads 8 \
    --read-len 63

# 3. Build Salmon Index (Linux / WSL)
bash scripts/build_salmon_index.sh \
    --transcripts data/reference/transcripts.fa \
    --genome data/reference/genome.fa \
    --outdir data/reference/salmon_index \
    --threads 8
```
