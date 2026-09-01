# Chapter 07: GTF Format

> The gene annotation format that tells us where genes, transcripts,
> exons, and introns are in the reference genome. Essential for
> counting reads per gene and interpreting alignments.

---

## 1. What is it?

**GTF** (Gene Transfer Format) is a tab-separated text format that
describes the **structure and location of genomic features** -- genes,
transcripts, exons, CDS (coding sequences), and UTRs.

Each line is a **feature** with 9 tab-separated fields:

```
seqname  source  feature  start  end  score  strand  frame  attribute
```

The GTF is the link between **genomic coordinates** (from BAM) and
**gene identity** (for counting).

---

## 2. Why do we need it?

Reads align to genomic coordinates (BAM), but science is about genes.
The GTF tells us which coordinate ranges belong to which gene. Tools
use it to:

- **featureCounts**: assign reads to genes based on exons
- **STAR**: build splice-junction databases (`sjdbOverhang`)
- **RSeQC**: interpret read distribution across features

Without GTF, you have coordinates but no gene names.

---

## 3. Where does it fit?

```
Reference genome (FASTA) + annotation (GTF)
    |
    +--> STAR index (Ch 12)
    +--> featureCounts (Ch 15)
    +--> gene counts
```

The GTF lives in `data/reference/genes.gtf`.

---

## 4. Input

For our study:

| File | Description | Source |
|------|-------------|--------|
| `genes.gtf` | GENCODE v44 primary assembly annotation | GENCODE/Ensembl 110 |

Documented in `metadata/reference_manifest.yaml` with chromosome
naming (UCSC style: chr1, chr2, ...).

---

## 5. Output

The GTF is consumed to produce:

- STAR genome index (splice junctions)
- Gene-level count matrices (featureCounts)
- Validated reference compatibility (with FASTA)

---

## 6. How it works

### 6.1 The 9 GTF fields

| Field | Meaning |
|-------|---------|
| 1 seqname | Chromosome (chr1, chr2, ...) |
| 2 source | Database (e.g., GENCODE, HAVANA) |
| 3 feature | `gene`, `transcript`, `exon`, `CDS`, `UTR` |
| 4 start | 1-based start coordinate |
| 5 end | End coordinate (inclusive) |
| 6 score | Usually `.` (no score) |
| 7 strand | `+` or `-` |
| 8 frame | Reading frame (0,1,2 or `.`) |
| 9 attribute | Key-value pairs (gene_id, gene_name, etc.) |

### 6.2 Feature hierarchy

GTF expresses the nested structure:

```
gene
  L__ transcript
        L__ exon
        L__ exon
        L__ CDS
```

The `attribute` column uses `gene_id` and `transcript_id` to link
them.

### 6.3 Example GTF lines (from our test reference)

```
chr16  HAVANA  gene       1  200  .  +  .  gene_id "ENSG00000103196.14"; gene_name "CRISPLD2";
chr16  HAVANA  transcript 1  200  .  +  .  gene_id "..."; transcript_id "ENST00000219431.9"; gene_name "CRISPLD2";
chr16  HAVANA  exon       1  90   .  +  .  gene_id "..."; transcript_id "..."; exon_number 1; gene_name "CRISPLD2";
chr16  HAVANA  exon       110 200 .  +  .  gene_id "..."; transcript_id "..."; exon_number 2; gene_name "CRISPLD2";
```

### 6.4 Chromosome naming consistency

The GTF `seqname` must match the FASTA headers. If FASTA says `chr1`
but GTF says `1`, alignment and counting silently break.

This is exactly what our `validate_reference.py` checks.

---

## 7. Biology behind it

- **Exons**: coding regions retained in mature mRNA.
- **Introns**: regions removed during splicing (represented by `N`
  in BAM CIGAR; not directly annotated as separate GTF lines in the
  primary annotation, but their boundaries are the exon edges).
- **Transcripts**: isoforms of a gene.
- **gene_id / gene_name**: unique identifiers used in count matrices
  and DESeq2.

---

## 8. Command

Validate compatibility:

```bash
python3 scripts/python/validate_reference.py \
    --fasta data/reference/genome.fa \
    --gtf data/reference/genes.gtf
```

Inspect the annotation:

```bash
# Count gene records
grep -c $'\tgene\t' data/reference/genes.gtf

# Find CRISPLD2
grep -w "CRISPLD2" data/reference/genes.gtf | head -n 5
```

---

## 9. Example

The top genes in our focal study all have GTF records:

- `ENSG00000103196` -> `CRISPLD2` (chr16)
- `ENSG00000096060` -> `FKBP5` (chr6)
- `ENSG00000120129` -> `DUSP1` (chr5)
- `ENSG00000111640` -> `GAPDH` (chr12)
- `ENSG00000075624` -> `ACTB` (chr7)

The GTF maps these gene_ids to genomic exons used for counting.

---

## 10. How to read the output

When validating GTF:

| Field | What to check |
|-------|---------------|
| seqname | Matches FASTA chromosomes (chr prefix) |
| feature | Has `exon`, `gene`, `transcript` |
| attribute | Has `gene_id` (required) and ideally `gene_name` |
| Strand | Consistent with library type |

Our validator returns lists such as:
- `gene_id` presence
- `exon` feature presence
- chromosome overlap with FASTA

---

## 11. Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| **Chromosome prefix mismatch** | FASTA/GTF naming differs | Normalize both |
| **Missing gene_id** | Malformed GTF | Use proper GENCODE GTF |
| **No exon features** | Wrong/corrupt GTF | featureCounts needs exons |
| **Gene IDs with version vs without** | `.1`, `.14` suffixes | Keep consistent |
| **Strand inconsistency** | Library type vs annotation | Confirm strandness |

---

## 12. Limitations

- GTF gives locations but **not** expression (that needs reads/counts).
- Annotation completeness depends on the source (GENCODE is very
  thorough for human).
- Gene models can conflict; counting is as good as the annotation.

---

## 13. How our project uses it

- `data/reference/genes.gtf` supplies exons to featureCounts (Ch 15).
- STAR uses the GTF for the splice-junction index with
  `sjdbOverhang = 62` (Ch 12).
- `validate_reference.py` verifies GTF-FASTA compatibility (4 passing
  unit tests).
- The mini test reference in `build_test_reference.py` contains GTF
  for CRISPLD2, GAPDH, ACTB for CI/CD.

---

## 14. Official documentation

- **GTF format (Ensembl)**:
  https://useast.ensembl.org/info/website/upload/gff.html
- **GENCODE GTF**:
  https://www.gencodegenes.org/human/
- **GFF/GTF spec**:
  https://github.com/The-Sequence-Ontology/Specifications

---

## 15. Mini exercise

1. Write the GTF lines for a single gene with two exons.
2. Explain the relationship between `id` and `name` fields and the
   gene counts we produce.
3. Why must the GTF chromosome names match the FASTA names?
4. Which feature records does featureCounts need to count reads?
5. Using `metadata/reference_manifest.yaml`, state the exact GTF file
   and its chromosome naming convention.

---

**End of Data Formats phase.**

> **Next**: [Chapter 08: FastQC](../03_qc/fastqc.md)
