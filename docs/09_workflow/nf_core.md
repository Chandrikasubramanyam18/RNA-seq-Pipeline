# Chapter 26: nf-core/rnaseq

> A community-standard, best-practice Nextflow pipeline for RNA-seq
> that we benchmark our own workflow against (or adopt).

---

## 1. What is it?

**nf-core/rnaseq** is a production-ready, community-maintained Nextflow
pipeline for bulk RNA-seq. It implements industry best practices for
our exact steps: QC, trimming, alignment (STAR), quantification
(Salmon), and (optionally) differential expression.

**nf-core** is a framework of conventions: standard directory layout,
`nextflow_schema.json` parameter validation, test datasets, and CI/CD.

---

## 2. Why do we need it?

- It encodes **best-practice parameters** for exactly the tools we
  studied (FastQC, fastp, STAR, Salmon, MultiQC).
- Saves reinventing the wheel; battle-tested by the community.
- Serves as a **reference implementation** to compare against our own
  pipeline.
- Its conventions (modules, config, tests) are the standard in the
  field.

---

## 3. Where does it fit?

```
Our custom workflow (Ch 25)  <->  nf-core/rnaseq (benchmark/baseline)
```

We can either adopt nf-core/rnaseq directly or pattern our modules on
it.

---

## 4. Input

- A **samplesheet** (`--input samplesheet.csv`) listing sample, fastq,
  strandness.
- A genome / references (`--genome GRCh38` via iGenomes or custom).
- Profiles (`-profile docker`, `singularity`).

---

## 5. Output

| File | Description |
|------|-------------|
| `results/multiqc/multiqc_report.html` | Aggregated QC |
| `results/star_salmon/*` | STAR/Salmon quantification |
| `results/deseq2/*` | DE results (if enabled) |
| `results/fastqc`, `results/trimgalore`, `results/rsem` etc. | Step outputs |

---

## 6. How it works

nf-core/rnaseq runs modules in sequence (DSL2):

```
inputs -> fastqc -> trimgalore(fastp) -> star -> rseqc
                                            -> salmon
         quant -> multiqc -> (deseq2 optional)
```

Each module is a separate Nextflow process with pinned container
versions. Parameters are validated against a JSON schema.

---

## 7. Biology behind it

- Best-practice parameter choices (e.g., sjdbOverhang, library types)
  are encoded to get reliable counts.
- Alignment (STAR) and quantification (Salmon) run in parallel,
  matching our architecture (Ch 25).
- The outputs feed the same downstream biology (DE, pathways).

---

## 8. Command

```bash
# Run nf-core/rnaseq (using sailfish/STAR+Salmon pipeline)
nextflow run nf-core/rnaseq \
    --input samplesheet.csv \
    --genome GRCh38 \
    -profile docker \
    -resume
```

---

## 9. Example

A minimal samplesheet header:

```
sample,fastq_1,fastq_2,strandedness
C1,data/raw/C1_R1.fastq.gz,data/raw/C1_R2.fastq.gz,unstranded
T1,data/raw/T1_R1.fastq.gz,data/raw/T1_R2.fastq.gz,unstranded
```

---

## 10. How to read the output

- **MultiQC report** summarizes all QC from every module.
- **star_salmon gene counts** feed DESeq2.
- **The workflow diagram / report** shows which steps ran and their
  status.

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| Profile/config missing | Set `-profile docker`/`singularity` |
| Samplesheet malformed | Match required headers exactly |
| Genome not in iGenomes | Provide `--fasta`/`--gtf` explicitly |
| Resource limits | Bump executor resources in config |

---

## 12. Limitations

- Large resource demands (full human STAR index, ~30 GB RAM).
- Parameter-heavy; best to rely on defaults.
- Adds nf-core conventions/boilerplate to learn.

---

## 13. How our project uses it

- nf-core/rnaseq is our **benchmark/baseline** for the future
  Nextflow phase.
- Our custom modules mirror its structure (STAR+Salmon parallel path).
- It validates that our pipeline parameters match best practice.

---

## 14. Official documentation

- **nf-core/rnaseq**:
  https://nf-co.re/rnaseq
- **nf-core framework**:
  https://nf-co.re/
- **nf-core/rnaseq docs**:
  https://nf-co.re/rnaseq/3.16/docs/usage

---

## 15. Mini exercise

1. What does nf-core provide beyond just a pipeline?
2. Which two quantification/alignment tools run in parallel in
   nf-core/rnaseq?
3. What must be correct in the samplesheet, and why does strandness
   matter?
4. How does nf-core/rnaseq validate its parameters?
5. How could our pipeline use nf-core/rnaseq as a benchmark?

---

**End of Workflow phase.**

> **Next**: [Chapter 27: Conda](../10_reproducibility/conda.md)
