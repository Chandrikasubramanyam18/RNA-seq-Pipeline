# Chapter 02: Genetics & Gene Expression

> How genetic information is organized, inherited, and regulated --
> and why differential expression analysis detects transcript-level
> changes that reflect cellular responses.

---

## 1. What is it?

Genetics is the study of **genes, heredity, and genetic variation**.
Gene expression is the process by which the information encoded in a
gene is used to produce a functional product. Together they explain:

- How the genome is organized
- How genes are turned on and off
- How cells achieve different identities from the same DNA
- Why comparing expression between conditions reveals biology

For RNA-seq, the key takeaway is: **the genome is the blueprint;
the transcriptome is what is actively being read.**

---

## 2. Why do we need it?

Differential expression analysis compares the **amount of RNA**
produced by each gene across conditions (control vs. treatment).
To interpret those differences you must understand:

- How **gene regulation** turns genes up or down
- What **transcription factors** do (like the glucocorticoid receptor)
- The role of **replicates** and **biological variability**
- How **housekeeping genes** provide an expression baseline

The dexamethasone story is fundamentally a story about **gene
regulation**: a hormone activates a transcription factor that changes
the expression of specific target genes.

---

## 3. Where does it fit?

```
Genetics & Gene Expression (this chapter)
    |
    +--> explains what differential expression measures
    +--> explains experimental design (replicates)
    +--> explains normalization (housekeeping genes)
    |
    v
RNA-seq technology (Chapter 03)
```

This chapter connects molecular biology (Chapter 01) to the
statistical analysis of expression (Chapter 06).

---

## 4. Input

Conceptual input:

- The structure of genes (from Chapter 01)
- The process of transcription
- The idea of the transcriptome

---

## 5. Output

Understanding of:

- Genome organization (chromosomes, genes)
- The spectrum of gene expression (low to high)
- Regulation mechanisms (transcription factors, enhancers)
- Why biological replicates matter
- How normalization uses reference genes

---

## 6. How it works

### 6.1 The Human Genome

The human genome contains ~3.1 billion base pairs split across
**23 chromosome pairs**. Only a small fraction (~1.5-2%) codes for
proteins. The rest includes regulatory regions, introns, and
non-coding elements.

Gene density varies by chromosome. Our study genes are on:

| Gene | Chromosome | Location Region |
|------|-----------|-----------------|
| CRISPLD2 | chr16 | 16q24.1 |
| FKBP5 | chr6 | 6p21.31 |
| DUSP1 | chr5 | 5q35.1 |
| KLF15 | chr3 | 3q21.3 |
| GAPDH | chr12 | 12p13.31 |
| ACTB | chr7 | 7p22.1 |

### 6.2 Levels of Gene Expression

Expression is continuous, not binary. Genes range from:
- **Not expressed** (effectively zero transcripts) to
- **Lowly expressed** to
- **Highly expressed** (housekeeping genes can produce millions
  of transcripts)

RNA-seq measures this abundance on a wide dynamic range -- which is
why count data must be normalized (Chapter 17).

### 6.3 Regulation of Gene Expression

Multiple control points determine how much mRNA a gene produces:

**Transcriptional regulation (primary):**
- **Transcription factors** bind DNA at promoters/enhancers
- **Activators** increase transcription; **repressors** decrease it
- **Enhancers** are distal regulatory elements that loop to the
  promoter to boost transcription

**Post-transcriptional regulation:**
- mRNA stability (short vs. long half-life)
- Alternative splicing
- miRNA-mediated degradation

**For our study:** Dexamethasone binds the **glucocorticoid receptor
(NR3C1)**. This receptor translocates to the nucleus and acts as a
transcription factor, directly activating or repressing target genes.

```
Cytoplasm                        Nucleus
[Dexamethasone]--+
                 |
                 v
         [Glucocorticoid receptor]
                 |
                 | bind ligand, move to nucleus
                 v
              [GR-Dex complex]
                 |
        binds enhancers/promoters
                 v
    activates CRISPLD2, FKBP5, DUSP1, KLF15
    represses SPARCL1, EGR1
```

### 6.4 Transcription Factors and the Dexamethasone Response

The differentially expressed genes in our study are largely
**glucocorticoid receptor (GR) target genes**:

| Gene | Direction | Relationship to GR |
|------|-----------|--------------------|
| CRISPLD2 | Up | Direct GR target; anti-inflammatory mediator |
| FKBP5 | Up | GR co-chaperone; regulates GR sensitivity (negative feedback) |
| DUSP1 | Up | Phosphatase that shuts down MAPK inflammatory signaling |
| KLF15 | Up | GR-inducible transcription factor |
| SPARCL1 | Down | Matrix protein; suppressed during remodeling |
| EGR1 | Down | Immediate-early gene; often downregulated by glucocorticoids |

### 6.5 Biological Replicates and Variability

Individual cells/samples are noisy. To measure expression changes
statistically, we need **biological replicates** -- independent
samples from separate donors.

Our study uses **3 donors**, each with a control and treated sample:

| Donor | Control | Treatment |
|-------|---------|-----------|
| N61311 | C1 | T1 |
| N052611 | C2 | T2 |
| N080611 | C3 | T3 |

This is a **paired design**: each treated sample has a matched
control from the same donor. This controls for donor-to-donor
baseline differences.

### 6.6 Housekeeping Genes as Reference

Housekeeping genes (GAPDH, ACTB, EEF1A1, TBP) are constitutively
expressed in most cells. They serve as references because their
expression is expected to be relatively stable across conditions.

In our results, GAPDH and ACTB show log2FC ~ 0.0, confirming that
most of the transcriptome is unchanged and that normalization is
working correctly.

---

## 7. Biology behind it

### 7.1 Differential Expression = Regulation in Action

When a drug changes gene expression, it is altering regulation. The
DEGs we find in Chapter 18 (DESeq2) are the genes whose regulation
was most affected by dexamethasone.

### 7.2 Redundancy and Isoforms

Genes can overlap or exist in gene families with redundant function.
This complicates read assignment (Chapter 15) but also means
regulation is finely tuned.

### 7.3 Non-coding Genes

Many RNA-seq libraries capture non-coding transcripts too (lncRNA,
pseudogenes). These are important biologically, but our focused
study centers on protein-coding genes.

---

## 8. Command

No command-line tool belongs to this conceptual chapter. However,
you can inspect the actual genes in our reference using the GTF
annotation (Chapter 07). Example grep to find CRISPLD2 in the
annotation (after preparing reference):

```bash
# (Conceptual -- requires the reference GTF to be present)
grep -w "CRISPLD2" data/reference/genes.gtf | head -n 5
```

This would return the gene/transcript/exon records for CRISPLD2,
showing its chromosome, coordinates, and structure.

---

## 9. Example

Consider the **FKBP5** gene:

- FKBP5 encodes an **immunophilin/co-chaperone** that associates
  with the glucocorticoid receptor.
- It is a classic **GR target gene**, strongly induced by
  dexamethasone (log2FC = +3.21 in the published study).
- FKBP5 also participates in **negative feedback**: high FKBP5
  reduces GR hormone binding sensitivity.
- Detecting FKBP5 upregulation confirms the glucocorticoid response
  pathway is active in our samples.

This illustrates how a single DEG connects genetics (genomic locus),
regulation (GR activation), and biology (feedback control).

---

## 10. How to read the output

There is no statistical output for this chapter. But it frames how
you will read DESeq2 results later:

| DESeq2 concept | Biological meaning |
|----------------|--------------------|
| baseMean | Average expression level of the gene |
| log2FoldChange | How much regulation changed (up or down) |
| p-value | Is the change likely real (not noise) |
| padj (FDR) | Corrected for testing thousands of genes |
| Housekeeping ~0 FC | Confirms normalization is valid |

---

## 11. Common errors

| Error | Misconception | Correct view |
|-------|---------------|--------------|
| "DEGs mean the gene is more important" | Significance reflects change, not importance | A gene can be critical yet unchanged |
| "Fold change alone = significance" | High FC can be noisy with low expression | Must consider p-value/padj and baseMean |
| "I can use 1 replicate per condition" | No statistical power for DE | Need replicates to estimate variability |
| "Donors are interchangeable" | Donor differences exist and confound | Use paired design / include donor in model |
| "Housekeeping genes are always validated" | They should be confirmed in each dataset | Check FC is actually ~0 in your data |

---

## 12. Limitations

- Gene regulation is far more complex than transcription factors
  alone (chromatin, enhancers, feedback loops).
- Expressing "more important gene" from fold change is a common
  misinterpretation.
- This chapter covers concept-level genetics; population genetics,
  heritability, and variant analysis are out of scope for bulk
  RNA-seq (those belong to other fields like GWAS/WGS analysis).

---

## 13. How our project uses it

- The **paired design** (3 donors x control/treatment) is encoded in
  `metadata/samplesheet.csv` and used by the DESeq2 model.
- **Housekeeping controls** (GAPDH, ACTB) are used to validate
  normalization.
- **Transcription factor biology** (GR targets) explains why the
  specific DEGs (CRISPLD2, FKBP5, DUSP1, KLF15) are the ones
  detected.
- The **educational Python DE engine** implements the normalization
  and statistical tests that rely on this experimental-design
  understanding.

---

## 14. Official documentation

- **NCBI: Regulome / Gene Regulation resources**:
  https://www.ncbi.nlm.nih.gov/books/NBK26834/
- **Nature Scitable: Gene Expression and Regulation**:
  https://www.nature.com/scitable/topicpage/gene-expression-14121669/
- **OMMBID: Transcription Factors**:
  https://ommbid.mhmedical.com/
- **Rosenberg, L.E. & Rosenberg, D.D. Human Genes and Genomes**,
  Academic Press (reference text)

---

## 15. Mini exercise

1. Using `metadata/samplesheet.csv`, write the 3x2 experimental
   design table (donor x condition). Why is it called "paired"?
2. Explain in two sentences how dexamethasone changes the expression
   of CRISPLD2, referencing transcription factors.
3. Why would using a single replicate per condition make
   differential expression statistically unreliable?
4. If GAPDH showed log2FC = -3.0 in your results, what would that
   suggest about your normalization?
5. List the glucocorticoid receptor target genes from our study and
   state whether each is up- or down-regulated.

---

> **Next**: [Chapter 03: What Is RNA-seq?](rna_seq.md)
