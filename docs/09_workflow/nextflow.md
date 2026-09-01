# Chapter 25: Nextflow

> A workflow language that orchestrates the entire RNA-seq pipeline as
> a set of reproducible, scalable, resumable processes.

---

## 1. What is it?

**Nextflow** is a workflow manager (Groovy/DSL) that runs
bioinformatics pipelines as a graph of **processes**, each with its own
containerized environment. It handles:

- Orchestration (FastQC -> fastp -> STAR -> ... -> DESeq2)
- Parallelization and scaling (local, SLURM, cloud)
- Resume from where a run stopped
- Containerized reproducibility (Docker/Apptainer, Ch 28/29)

---

## 2. Why do we need it?

- Our pipeline has many steps (Ch 8-24) that need to run in sequence.
- We need reproducibility (same versions, same result).
- We want to scale from the local laptop to an HPC cluster.
- Resume capability saves time after failures.

---

## 3. Where does it fit?

Nextflow **wraps** all the tools we've learned:

```
FastQC -> fastp -> FastQC(clean) -> MultiQC
                     |
                 STAR -> SAMtools -> featureCounts -> DESeq2 -> pathways
                     |
                 Salmon (parallel quantification)
```

Nextflow is the conductor of the whole orchestra.

---

## 4. Input

- A `main.nf` (workflow script)
- A `nextflow.config` (params, containers, executors)
- A samplesheet (sample metadata)
- The reference files (Ch 11)

---

## 5. Output

- Final results files (counts, DE tables, plots) plus:
- A **work directory** with per-process outputs and logs
- An execution report (`*_report.html`) and timeline

---

## 6. How it works

### 6.1 Processes and channels

A `process` encapsulates one tool command. **Channels** pass data
between processes:

```groovy
process FASTQC {
  container 'staphb/fastqc'
  input:  tuple val(sample), path(reads)
  output: path("*_fastqc.html"), path("*_fastqc.zip")
  script: "fastqc $reads"
}
```

### 6.2 DSL2 modularity

Nextflow DSL2 lets you split the pipeline into reusable **modules** and
**sub-workflows**, promoted by nf-core (Ch 26).

### 6.3 Resumability

`-resume` skips completed processes (using cached work-dir outputs),
so a failure mid-pipeline doesn't restart from scratch.

### 6.4 Executors

Nextflow runs the same script on:
- **local** (your machine)
- **SLURM/PBS** (HPC, Ch 31)
- **AWS Batch / cloud** (Ch 32)

via `process.executor`.

---

## 7. Biology behind it

- Nextflow itself does no biology; it just runs the bioinformatics
  tools.
- The biological interpretation still comes from the output (counts,
  DE, pathways).
- It ensures the steps are run in the correct order with correct
  inputs.

---

## 8. Command

```bash
# Run a pipeline (nf-core rnaseq, Ch 26, or custom)
nextflow run main.nf \
    --input samplesheet.csv \
    --genome GRCh38 \
    -profile docker \
    -resume
```

---

## 9. Example

A run with `-resume` after fixing one failed sample: only the failed
step re-runs; all completed steps are cached and skipped.

---

## 10. How to read the output

- **Execution report**: per-process resource usage and status.
- **Work dir** (`work/`): intermediate files; used for resume/debug.
- **`.nextflow.log`**: full run log for troubleshooting.
- **Trace**: timing per process.

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| Container not found | Check container registry/name & config |
| Process fails (exit 1) | Check the tool command/log; use resume |
| Channel mismatch | Input/output declarations must align |
| No profile match | Define your executor profile in config |

---

## 12. Limitations

- Learning curve (DSL, channels).
- Adds orchestration overhead vs a plain shell script.
- Requires containerized envs (Docker/Apptainer) for full
  reproducibility.

---

## 13. How our project uses it

- **Future** phase: wrap the whole pipeline in a Nextflow workflow.
- The existing `scripts/*.sh` become Nextflow module bodies.
- Follows nf-core conventions (Ch 26) for structure.
- Enables reproducibility and HPC/cloud scaling.

---

## 14. Official documentation

- **Nextflow**:
  https://www.nextflow.io/
- **Nextflow documentation**:
  https://www.nextflow.io/docs/latest/
- **Nextflow DSL2**:
  https://www.nextflow.io/docs/latest/dsl2.html

---

## 15. Mini exercise

1. List 4 things Nextflow handles for a pipeline.
2. What is a "process" and what is a "channel"?
3. What does `-resume` do, and why is it valuable?
4. How can the same Nextflow script run locally and on SLURM/AWS?
5. Why is containerizing each process important for reproducibility?

---

> **Next**: [Chapter 26: nf-core/rnaseq](nf_core.md)
