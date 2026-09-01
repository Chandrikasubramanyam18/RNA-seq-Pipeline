# Chapter 03: What Is RNA-seq?

> RNA sequencing (RNA-seq) is the technology that measures the
> transcriptome. It is the raw material source for every downstream
> step in this pipeline.

---

## 1. What is it?

RNA-seq (RNA sequencing) is a high-throughput technology that
quantifies the **abundance of RNA transcripts** in a biological
sample. It produces the raw **FASTQ** files that our pipeline
processes.

Instead of measuring one gene at a time, RNA-seq captures the
expression of **thousands of genes simultaneously** by:

1. Converting RNA to complementary DNA (cDNA)
2. Fragmenting and amplifying it
3. Sequencing the fragments (yielding millions of short reads)
4. Mapping those reads back to the genome/transcriptome to determine
   which genes they came from and how many

The output is, ultimately, a **count per gene**: how many reads
represent each gene's transcripts.

---

## 2. Why do we need it?

To answer the biological question *(which genes change with
dexamethasone treatment?)*, we need a method that:

- Measures the **whole transcriptome**, not just a few genes
- Provides **quantitative** abundance (not just presence/absence)
- Covers a **wide dynamic range** (from rare to very abundant)
- Distinguishes **isoforms** via splicing information

RNA-seq satisfies all of these, making it the standard for
differential expression analysis in modern biology.

Older technologies (microarrays) could only measure probes that were
pre-designed, had limited dynamic range, and could not easily detect
novel transcripts or isoforms. RNA-seq is more powerful and unbiased.

---

## 3. Where does it fit?

RNA-seq is the **source of the data** for the entire pipeline:

```
Biological RNA
    |
    | RNA-seq library preparation + sequencing
    v
FASTQ files  <----- every downstream step starts here
    |
    +--> QC (Ch 08-10)
    +--> alignment (Ch 12-13)
    +--> quantification (Ch 14-15)
    +--> statistics (Ch 16-18)
```

It connects biology (Chapters 01-02) to the data formats we will
study in Chapters 04-07.

---

## 4. Input

The biological input to RNA-seq is **RNA extracted from a sample**:

- In our study: RNA from cultured primary human airway smooth
  muscle cells
- 6 samples total: 3 control (C1-C3) and 3 dexamethasone-treated
  (T1-T3)
- Sourced across 3 donors for biological replication

---

## 5. Output

The direct output of RNA sequencing is **FASTQ files**:

- One file per read-pair direction per sample
- For our 6 samples with paired-end 2x63 bp: **12 FASTQ files**
  (6 samples x 2 mates)
- Each FASTQ contains millions of 63-base reads with quality scores

These FASTQ files are the input to the whole pipeline and are stored
in `data/raw/`.

---

## 6. How it works

### 6.1 Overview of the RNA-seq Workflow (in the lab)

```
Cells
  |
  | lysis + RNA extraction
  v
Total RNA
  |
  | poly-A selection (or rRNA depletion)
  v
mRNA
  |
  | reverse transcription (cDNA synthesis)
  v
cDNA
  |
  | fragmentation + adapter ligation
  v
Sequencing library
  |
  | bridge amplification on flow cell
  v
Clusters
  |
  | sequencing-by-synthesis
  v
Base calls -> FASTQ
```

### 6.2 Step 1: RNA Extraction

RNA is extracted from cells. Because RNA is unstable (RNases are
everywhere), this is done carefully. The quality of extraction
affects QC results (Chapter 08).

### 6.3 Step 2: Enrichment for mRNA

Most RNA in a cell is rRNA (~80-90%). To study gene expression, we
enrich for mRNA. Two common approaches:

- **Poly-A selection**: Uses the poly-A tail of mRNA to capture it.
  This is what the GSE52778 study used (`library_selection: polyA`).
- **rRNA depletion**: Removes ribosomal RNA, retaining other RNA
  (including non-coding).

Because the study used poly-A selection, our library mainly contains
mRNA from polyadenylated transcripts.

### 6.4 Step 3: cDNA Synthesis (Reverse Transcription)

RNA is converted to complementary DNA (cDNA) using the enzyme
**reverse transcriptase**, because DNA is more stable and easier to
amplify and sequence.

Random hexamer primers bind throughout the RNA to initiate synthesis.

### 6.5 Step 4: Fragmentation and Adapter Ligation

cDNA is fragmented into short pieces (our library: 63 bp reads).
Sequencing adapters are ligated to both ends so the fragments can be
amplified and attached to the flow cell.

The cDNA insert length can be variable. If the insert is *shorter*
than the read length, the sequencer reads into the adapter -- this
causes **adapter contamination**, which fastp removes (Chapter 09).

### 6.6 Step 5: Sequencing (Illumina)

Illumina sequencing-by-synthesis works by:

1. Attaching fragments to a flow cell
2. Amplifying each fragment into a local cluster (bridge PCR)
3. Adding labeled nucleotides one at a time, imaging the cluster
4. Recording the base at each position per cycle

Each base call has an associated **Phred quality score** (Chapter 04).

### 6.7 Step 6: Base Calling -> FASTQ

The sequencer's software converts fluorescence images into base
calls and quality scores, output as FASTQ. This is the raw data
our pipeline consumes.

### 6.8 Paired-End Sequencing

In **paired-end** sequencing, each fragment is sequenced from **both**
ends:

```
            <-- R2 reads reverse -->
|---- insert ----|
--> R1 reads forward -->

Read 1 (R1): from the 5' end
Read 2 (R2): from the 3' end, reading back
```

The insert length between R1 and R2 is known. This is why fastp can
**detect adapters by overlapping R1 and R2** (Chapter 09).

Paired-end reads improve:
- Alignment accuracy across repetitive regions
- Detection of splice junctions (both ends can be in different exons)
- Isoform resolution

---

## 7. Biology behind it

### 7.1 What We Are Really Measuring

RNA-seq measures **transcript abundance** as a proxy for **gene
expression**. A higher read count for a gene usually means more mRNA
was present, reflecting higher transcriptional activity.

But abundance depends on both:
- **Transcription rate** (how fast new mRNA is made)
- **Degradation rate** (how quickly old mRNA is removed)

A gene can appear "upregulated" because transcription increased OR
because mRNA became more stable. Bulk RNA-seq cannot distinguish
these; it reports net steady-state abundance.

### 7.2 Biological and Technical Variability

Expression varies due to:
- **Biological variation**: genuine donor differences, cell state
- **Technical variation**: library prep, sequencing depth

Replicates (Chapter 02) and normalization (Chapter 17) handle these.

### 7.3 Deep vs. Shallow Sequencing

- **Sequencing depth** = total reads per sample.
- Deep sequencing (more reads) detects low-abundance transcripts.
- Our samples have roughly 15-30 million read pairs each.

More depth improves sensitivity but costs more. There's a plateau
where extra reads add little new information for typical gene-level
analysis.

---

## 8. Command

RNA-seq itself is done in the laboratory, not via a command line in
our pipeline. The pipeline begins after sequencing, with the FASTQ
files.

To download real/subset FASTQ data for our study, we use the
implemented downloader:

```bash
# Download subsampled reads (50K read pairs per sample) for testing
python3 scripts/python/download_dataset.py --subsample 50000

# Or download the full dataset (large; ~14 GB)
python3 scripts/python/download_dataset.py --subsample 0
```

The subsampled mode streams only the first 50,000 read pairs from
ENA -- small enough to run the pipeline quickly on a laptop.

---

## 9. Example

For our study (GSE52778):

- 6 samples, each with R1 and R2 FASTQ files
- Example output filenames in `data/raw/`:
  - `SRR1039508_1.fastq.gz` (C1, read 1)
  - `SRR1039508_2.fastq.gz` (C1, read 2)
  - `SRR1039509_1.fastq.gz` (T1, read 1)
  - ... and so on for all 6 samples

Each file holds millions of 63-base paired-end reads.

---

## 10. How to read the output

The "output" of sequencing is FASTQ. You will learn to interpret it
in detail in **Chapter 04: FASTQ Format**. Briefly, each read has:

- An identifier line (`@...`)
- The nucleotide sequence
- A `+` separator
- Quality scores (Phred)

QC tools (Chapters 08-10) produce human-readable reports describing
quality, GC content, adapters, and duplication.

---

## 11. Common errors

| Error | Misconception | Correct view |
|-------|---------------|--------------|
| "RNA-seq measures protein" | It measures RNA, not protein | Post-transcriptional regulation means RNA != protein |
| "More reads = more genes detected cheaply" | Depth has diminishing returns | There is a saturation point for gene detection |
| "Poly-A selection removes all non-coding RNA" | It enriches for polyadenylated transcripts | Some ncRNA lacks poly-A and is lost |
| "Single-end is always inferior" | Paired-end is usually better, but SE can suffice | Use paired-end for splice/isoform work |

---

## 12. Limitations

- RNA is fragile; degraded input produces poor-quality libraries
  (detected by FastQC).
- Amplification during library prep introduces **duplicates** and
  **bias**.
- Poly-A selection excludes non-polyadenylated species.
- Sequencing is **relative**, not absolute; normalization is required
  to compare samples.
- It measures **steady-state abundance**, not transcription rate.

---

## 13. How our project uses it

- The pipeline's input is the FASTQ output of RNA-seq.
- Our samples come from a **poly-A selected, paired-end** library.
- The **63 bp read length** determines the STAR `sjdbOverhang`
  parameter (63 - 1 = 62) (Chapter 12).
- The **paired-end** layout enables fastp adapter detection (Chapter 09).
- Understanding library type (poly-A, non-stranded) is essential for
  interpreting strandness in alignment/quantification.

---

## 14. Official documentation

- **Illumina: RNA-seq overview**:
  https://www.illumina.com/techniques/sequencing/rna-sequencing.html
- **NCBI: RNA-seq resources**:
  https://www.ncbi.nlm.nih.gov/
- **Nature Reviews Methods Primers: RNA-seq (Stark et al. 2019)**:
  https://www.nature.com/articles/s43586-019-0002-4
- **GSE52778 on GEO**:
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52778

---

## 15. Mini exercise

1. List the six main steps of RNA-seq library preparation and
   sequencing.
2. Explain why the GSE52778 library used poly-A selection.
3. In paired-end sequencing, why does R1 and R2 overlap enable
   adapter detection without knowing the adapter sequence?
4. Why must the 63 bp read length factor into the STAR index
   parameters (think `sjdbOverhang`)?
5. Write one sentence describing the exact biological input and the
   exact data output of RNA-seq.

---

> **Next**: [Chapter 04: FASTQ Format](../02_data/fastq.md)
