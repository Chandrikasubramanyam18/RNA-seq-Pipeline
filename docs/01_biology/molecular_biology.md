# Chapter 01: Molecular Biology

> The foundation of RNA-seq analysis. Before we can quantify gene
> expression, we must understand what genes are, how they are
> transcribed into RNA, and why measuring RNA tells us about
> cellular state.

---

## 1. What is it?

Molecular biology is the branch of biology that studies the structure,
function, and interactions of the molecules of life: **DNA, RNA, and
proteins**. It explains how genetic information flows from the genome
to produce the functional molecules that make cells work.

For our purposes, the central concept is the **central dogma of
molecular biology**:

```
DNA  --(transcription)-->  RNA  --(translation)-->  Protein
```

- **DNA** is the long-term storage of genetic information.
- **RNA** is a temporary copy used to carry instructions and perform functions.
- **Protein** is the functional product that does the work in the cell.

RNA-seq measures the **RNA** in between -- how much of each gene is
being transcribed at a given moment.

---

## 2. Why do we need it?

RNA-seq analysis is ultimately about **measuring gene expression**.
To interpret the numbers coming out of the pipeline (how many reads
aligned to a gene, fold changes, etc.), you must understand:

- What a **gene** is and where it lives in the genome
- How **transcription** turns a gene into RNA
- What **expression level** means biologically
- Why different cells express different genes
- How **regulation** controls expression

Without this foundation, a log2 fold change of +2.5 for CRISPLD2 is
just a number. With it, you understand: *"the transcription of the
CRISPLD2 gene increased roughly 5.7-fold in response to
dexamethasone, meaning the cell produced more CRISPLD2 mRNA."*

---

## 3. Where does it fit?

In the pipeline architecture, molecular biology is the substrate for
**Layer 1 (the bioinformatics engine)**.

```
Molecular Biology (this chapter)
    |
    v
RNA-seq technology (Chapter 03)
    |
    v
FASTQ data (Chapter 04)
    |
    v
QC, alignment, quantification, statistics...
```

Every downstream step assumes you already understand the biology
behind the data.

---

## 4. Input

There is no computational input to this chapter. The "input" is
conceptual:

- Knowledge of cells and their components
- The structure of the genome
- The process of transcription

---

## 5. Output

Understanding of the biological concepts needed to interpret RNA-seq
results:

- What a gene is
- How genes are transcribed into RNA
- What the transcriptome is
- How expression is regulated
- Key terminology (mRNA, exon, intron, promoter, isoform, etc.)

These terms appear constantly in RNA-seq literature and tools.

---

## 6. How it works

### 6.1 The Cell and Its Nucleus

A human cell contains a **nucleus**, which houses the **genome** --
all of the DNA of the organism. The human genome is ~3.1 billion
base pairs (~3.1 Gbp) organized into **23 chromosome pairs** (22
autosomes + 1 pair of sex chromosomes).

### 6.2 DNA: The Storage Medium

DNA is a double helix made of two complementary strands. Each
strand is a sequence of **nucleotides**, each containing one of
four **nitrogenous bases**:

| Base | Abbreviation | Complements with |
|------|-------------|------------------|
| Adenine | A | T |
| Thymine | T | A |
| Guanine | G | C |
| Cytosine | C | G |

The sequence of these bases along the DNA encodes the instructions
for building proteins.

### 6.3 The Gene

A **gene** is a segment of DNA that contains the instructions to
produce a functional product, usually an RNA molecule or a protein.
A human cell has roughly **20,000-25,000 protein-coding genes**.

Each gene is composed of:

- **Promoter**: The regulatory region *upstream* (before) the gene
  where transcription starts. This is where regulatory proteins bind.
- **Exons**: The coding regions that remain in the final mRNA and
  get translated into protein.
- **Introns**: The non-coding regions *between* exons that are
  removed during processing.
- **5' UTR / 3' UTR**: Untranslated regions at the start and end
  that regulate stability and translation but are not translated
  into protein.

```
Promoter     Exon 1   Intron 1    Exon 2   Intron 2   Exon 3
   |            |        |           |        |          |
   +===+=======+========+===========+========+==========+
      transcription start                               transcription end
```

### 6.4 Transcription: DNA to RNA

**Transcription** is the process of copying a gene's DNA sequence
into an RNA molecule.

1. The enzyme **RNA polymerase II** binds to the gene's promoter.
2. It unwinds the DNA and synthesizes a complementary RNA strand
   (using **Uracil / U** instead of **Thymine / T** for RNA).
3. The result is a **primary transcript** (pre-mRNA) that still
   contains both exons and introns.

### 6.5 RNA Processing: From Pre-mRNA to Mature mRNA

The pre-mRNA undergoes processing before it is functional:

1. **5' capping**: A modified guanine cap is added to the start,
   protecting the RNA from degradation.
2. **Splicing**: **Introns are removed** and **exons are joined
   together**. This is where RNA-seq's *splice-aware alignment*
   becomes essential.
3. **Alternative splicing**: A single gene can be spliced in
   multiple ways, producing different **isoforms** (different
   transcript variants) from the same gene. This dramatically
   increases protein diversity.
4. **Polyadenylation**: A poly-A tail (a string of A's) is added
   to the 3' end. Many RNA-seq library protocols select for this
   poly-A tail to enrich for mRNA.

```
Pre-mRNA:  [Exon 1][Intron 1][Exon 2][Intron 2][Exon 3]
                      |  splicing  |
                      v
mRNA:      [Exon 1][Exon 2][Exon 3]
```

### 6.6 Translation: mRNA to Protein (briefly)

The mature mRNA is exported to the cytoplasm, where **ribosomes**
read it in triplets of nucleotides called **codons**. Each codon
specifies one amino acid. The resulting chain of amino acids folds
into a functional protein.

For RNA-seq purposes, we mostly care about the mRNA (transcript)
level. Translation to protein is the downstream consequence.

### 6.7 The Transcriptome

The **transcriptome** is the complete set of RNA transcripts in a
cell at a given moment. It includes:

- **mRNA** (messenger RNA): protein-coding transcripts
- **rRNA** (ribosomal RNA): part of ribosomes (usually removed
  from RNA-seq libraries)
- **tRNA** (transfer RNA): carries amino acids during translation
- **lncRNA** (long non-coding RNA): regulatory, non-coding
- **miRNA** (microRNA): small regulatory RNA

RNA-seq measures the abundance of these transcripts -- most
commonly the mRNA / poly-A transcripts.

---

## 7. Biology behind it

### 7.1 Gene Expression

**Gene expression** is the process by which information from a gene
is used to produce a functional product. The **expression level**
of a gene is roughly how much mRNA it produces.

Every cell in your body has the same DNA, but different cells
**express different genes**. A muscle cell expresses muscle genes;
a liver cell expresses liver genes. The differences in expression
determine cell identity and function.

### 7.2 Regulation of Expression

Cells control which genes are expressed and how much, through:

- **Transcription factors**: proteins that bind promoters/enhancers
  to activate or repress transcription
- **Epigenetic modifications**: DNA methylation, histone modification
- **Signaling pathways**: external signals (like a hormone) trigger
  cascades that change expression

IMPORTANT for our study: **Dexamethasone** is a **glucocorticoid
hormone**. It binds to the **glucocorticoid receptor**, a
transcription factor. This receptor then moves into the nucleus and
directly changes the expression of target genes (like CRISPLD2,
FKBP5, DUSP1). This is exactly what differential expression analysis
detects.

### 7.3 Housekeeping Genes

Some genes are expressed at relatively constant levels in nearly all
cells because their products are needed for basic cellular function
(e.g., GAPDH, ACTB/actin, EEF1A1, ribosomal proteins).

These **housekeeping genes** are used in RNA-seq as:
- **Normalization controls**: to confirm libraries are comparable
- **Positive controls**: they should show ~zero fold change across
  conditions

In our study, GAPDH and ACTB show log2FC ~ 0.0, confirming the
normalization is correct.

### 7.4 Why Measure RNA Instead of DNA?

DNA is the same in all cells and over time. RNA is **dynamic** --
it reflects what the cell is actively doing right now. If you want
to know how a drug (dexamethasone) changes cellular behavior, you
measure RNA before/after.

---

## 8. Command

There is no command-line tool for this chapter. It is conceptual
background.

However, a useful analogy script is the standard **central dogma**
visualization you can render in any markdown viewer:

```text
DNA (storage)
   |
   | transcription (RNA polymerase II)
   v
pre-mRNA
   |
   | RNA processing (splicing, capping, poly-A)
   v
mRNA  <----- WHAT RNA-SEQ MEASURES
   |
   | translation (ribosome)
   v
Protein (function)
```

---

## 9. Example

Take the gene **CRISPLD2** (ENSG00000103196) -- the headline gene of
our GSE52778 study.

- It is a protein-coding gene on chromosome 16.
- It contains multiple exons separated by introns.
- In untreated control ASM cells, it is expressed at a low level.
- When cells are treated with dexamethasone, the glucocorticoid
  receptor activates its promoter, and transcription increases.
- The result: more CRISPLD2 mRNA, which RNA-seq detects as a higher
  read count, and which differential expression reports as
  log2FC = +2.52 (~5.7-fold upregulation).

This single example ties together every concept: gene, transcription,
regulation, expression, and measurement.

---

## 10. How to read the output

There is no tool output in this chapter. The "output" is your
**mental model**, which you will apply when reading later chapters:

| Concept | Meaning for RNA-seq |
|---------|---------------------|
| Gene | The unit being quantified (rows in the count matrix) |
| Exon/Intron | Why spliced alignment matters; reads span exon junctions |
| Transcription factors | Drugs like dexamethasone change expression via these |
| Isoform/alternative splicing | A gene can map to multiple transcripts |
| Housekeeping gene | Stable control gene (GAPDH, ACTB) |
| Transcriptome | The full set of RNA measured by RNA-seq |

---

## 11. Common errors

| Error | Misconception | Correct view |
|-------|---------------|--------------|
| "RNA-seq measures protein levels" | mRNA != protein (many steps between) | RNA-seq measures RNA abundance, a proxy for gene activity |
| "More DNA = more expression" | DNA is constant; RNA is dynamic | Expression is about RNA, not DNA content |
| "All genes are either on or off" | Expression is continuous and graded | Genes show continuous abundance levels |
| "A gene = one protein" | Alternative splicing produces isoforms | One gene -> many transcripts/proteins |
| "Housekeeping genes never change" | They are *relatively* stable, not truly constant | They can vary slightly; used as reference, not absolute |

---

## 12. Limitations

- This chapter gives the essential cellular background but is not a
  full molecular biology course.
- Real transcription/splicing regulation is far more complex
  (enhancers, silencers, chromatin state, RNA modifications).
- RNA is subject to degradation and technical variation; measuring
  it requires careful handling -- which is exactly what QC
  (Chapters 08-10) addresses.

---

## 13. How our project uses it

Every downstream script and result assumes this biology:

- **featureCounts / Salmon** count reads per *gene / transcript*.
- **DESeq2** models how *expression levels* differ between control
  and treatment.
- **Housekeeping genes** (GAPDH, ACTB) are used to sanity-check
  normalization (log2FC must be ~0).
- **Pathway analysis** maps differentially expressed genes to
  biological processes (like *cellular response to glucocorticoid
  stimulus*), which only makes sense if you understand that
  dexamethasone is a glucocorticoid.

---

## 14. Official documentation

- **NCBI "A Science Primer" -- Molecular Biology**:
  https://www.ncbi.nlm.nih.gov/books/NBK22354/
- **Nature Scitable: The Central Dogma**:
  https://www.nature.com/scitable/topicpage/translation-dna-to-mrna-to-protein-393/
- **Khan Academy: Central Dogma of Molecular Biology**:
  https://www.khanacademy.org/science/ap-biology/gene-expression-and-regulation
- **Wikipedia: Central Dogma of Molecular Biology**:
  https://en.wikipedia.org/wiki/Central_dogma_of_molecular_biology

---

## 15. Mini exercise

1. Draw the structure of a gene, labeling the promoter, exons,
   introns, 5' UTR, and 3' UTR.
2. Describe in your own words the series of events from the binding
   of dexamethasone to the glucocorticoid receptor, to an increase
   in CRISPLD2 mRNA.
3. Why do we use housekeeping genes like GAPDH when analyzing
   differential expression?
4. Explain why two different spliced isoforms of the same gene
   would complicate read counting. (Think ahead to alignment.)
5. Write one sentence explaining *why measuring RNA reveals what a
   cell is actively doing, whereas DNA cannot.*

---

> **Next**: [Chapter 02: Genetics & Gene Expression](genetics.md)
