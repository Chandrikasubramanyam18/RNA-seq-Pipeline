# Benchmark RNA-seq Dataset: Airway Smooth Muscle Glucocorticoid Response

## 1. Study Overview & Biological Context

| Attribute | Specification |
| :--- | :--- |
| **Study Title** | RNA-Seq Transcriptome Profiling Identifies *CRISPLD2* as a Glucocorticoid Responsive Gene that Modulates Cytokine Function in Airway Smooth Muscle Cells |
| **Primary Publication** | Himes BE, Jiang X, Wagner P, Hu R, Wang Q, Klanderman B, Blakey J, Tantisira K, Choi AM, Lu Q, Weiss ST, Lu Q. *PLoS ONE* 9(6): e99625 (2014). [doi:10.1371/journal.pone.0099625](https://doi.org/10.1371/journal.pone.0099625) |
| **GEO Accession** | [GSE52778](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52778) |
| **BioProject** | [PRJNA229998](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA229998) |
| **SRA Study** | [SRP033325](https://trace.ncbi.nlm.nih.gov/Traces/sra/?study=SRP033325) |
| **Organism** | *Homo sapiens* (Human, NCBI Taxonomy ID: 9606) |
| **Tissue / Cell Type** | Primary Human Airway Smooth Muscle (ASM) cells |
| **Sequencing Platform** | Illumina HiSeq 2000 |
| **Library Strategy** | RNA-Seq (polyA+ enriched, non-stranded) |
| **Layout** | Paired-End ($2 \times 63$ bp) |

---

## 2. Experimental Design

Glucocorticoids (such as **dexamethasone**) are the standard-of-care anti-inflammatory treatment for asthma and chronic obstructive pulmonary disease (COPD). The study investigates the transcriptional remodeling in human ASM cells following 1-micromolar (1 $\mu\text{M}$) dexamethasone treatment for 18 hours compared to untreated vehicle controls across distinct biological donor cell lines.

We utilize 3 paired biological replicate cell lines:

| Sample ID | SRA Run ID | GEO GSM | Condition | Donor / Cell Line | Replicate | Layout |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `C1` | `SRR1039508` | GSM1275862 | `control` | N61311 | 1 | Paired-End ($2 \times 63$ bp) |
| `T1` | `SRR1039509` | GSM1275863 | `treatment` (Dex) | N61311 | 1 | Paired-End ($2 \times 63$ bp) |
| `C2` | `SRR1039512` | GSM1275866 | `control` | N052611 | 2 | Paired-End ($2 \times 63$ bp) |
| `T2` | `SRR1039513` | GSM1275867 | `treatment` (Dex) | N052611 | 2 | Paired-End ($2 \times 63$ bp) |
| `C3` | `SRR1039516` | GSM1275870 | `control` | N080611 | 3 | Paired-End ($2 \times 63$ bp) |
| `T3` | `SRR1039517` | GSM1275871 | `treatment` (Dex) | N080611 | 3 | Paired-End ($2 \times 63$ bp) |

---

## 3. Why this Dataset is Ideal for Benchmark Pipeline Engineering

1. **Standard Gold-Standard Dataset**: Widely used across the Bioconductor community (the official `airway` vignette) and DESeq2 tutorials, providing an established, published ground truth for differentially expressed genes (e.g., *CRISPLD2*, *DUSP1*, *FKBP5*).
2. **Paired Experimental Design**: Allows testing both standard two-group comparisons (`~ condition`) and paired-replicate multi-factor models (`~ donor + condition`) in DESeq2 to control for donor-to-donor baseline variability.
3. **High Quality & Realistic Size**: Real Illumina reads with biological variability, splice junctions, and standard error profiles, without synthetic artifacts.
4. **Public Access & Mirror Availability**: Fast direct downloads via EMBL-EBI European Nucleotide Archive (ENA) FTP/HTTP without requiring commercial API keys.
