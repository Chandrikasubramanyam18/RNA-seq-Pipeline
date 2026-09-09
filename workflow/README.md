# Nextflow Workflow — `workflow/`

This directory contains the **Nextflow DSL2** re-expression of the Phase-4 analytical pipeline (Step 12), wrapping the exact tools and committed R/Python entry points validated in Steps 3–9:

```text
FastQC (raw) → fastp → FastQC (clean) → STAR index/align → SAMtools/RSeQC
→ featureCounts → DESeq2 → visualization → clusterProfiler → MultiQC
```

It is a **portable orchestration layer** over the same steps that were executed with the real tools at tutorial scale (see `reports/phase4_integration.md` for the exact boundary).

---

## Requirements

- POSIX environment (Linux / WSL2)
- Java 17+ and [Nextflow](https://www.nextflow.io/) `>= 23.10.0` (per `nextflow.config` manifest)
- For a **real run** (not `-stub`): the tools/scripts from `envs/rnaseq.yml` (e.g. via the `conda` profile or a container built from `containers/`)

---

## Inputs (params)

| param | default | purpose |
|---|---|---|
| `--samplesheet` | `metadata/samplesheet.csv` | sample table (`sample,fastq_1,fastq_2,condition,replicate`) |
| `--fasta` | `data/reference/mini_real/mini_genome.fa` | reference genome |
| `--gtf` | `data/reference/mini_real/mini_genes.gtf` | gene annotation |
| `--rseqc_bed` | `data/reference/mini_real/refgene.bed12` | RSeQC transcript BED12 |
| `--outdir` | `results_nextflow/` | output root |

Reference paths are resolved relative to the repo root (see `workflow/main.nf`). Override any of them on the command line:

```bash
nextflow run workflow \
  --samplesheet metadata/samplesheet.csv \
  --fasta data/reference/mini_real/mini_genome.fa \
  --gtf data/reference/mini_real/mini_genes.gtf \
  --rseqc_bed data/reference/mini_real/refgene.bed12 \
  --outdir results_nextflow
```

---

## Profiles

All configured in `workflow/nextflow.config`:

| profile | runtime | notes |
|---|---|---|
| `standard` | local executor, no env | used for `-stub` topology validation |
| `conda` | conda env from `envs/rnaseq.yml` | for a real local run |
| `docker` | container `rnaseq-pipeline:0.1.0-tutorial` | needs image built (see `containers/`) |
| `apptainer` | container `rnaseq-pipeline_0.1.0-tutorial.sif` | needs image built (see `containers/`) |
| `singularity` | alias for the Apptainer runtime | legacy name |

Docker/Apptainer/Singularity runtimes require building the images **before** use; a runtime-validation checklist is in `containers/README.md`.

---

## Validate topology (`-stub`)

`-stub` proves **workflow topology only** (process graph, channel wiring, publish layout) without executing STAR/featureCounts/DESeq2 on real data:

```bash
nextflow run workflow -stub -profile standard \
  --outdir results_nextflow
```

Expected: all tasks succeed (54/54 at tutorial scale) and key artifacts are published under `--outdir`, e.g. `counts/gene_counts.txt` and `multiqc/multiqc_report.html`. This is exercised automatically by `tests/integration/test_nextflow_stub.py` (marker `nextflow`).

> ⚠️ **Important**: a `-stub` run is **not** a real analysis. A **real** run executes the same validated commands but at tutorial scale (3-gene mini-reference), so its results are **not publication-grade** either.

---

## Real run

```bash
nextflow run workflow -profile conda \
  --outdir results_nextflow
```

For reproducibility, prefer a container profile once the image exists. Real-run outputs land under `--outdir` (counts, differential expression, visualization, pathway, multiqc, fastqc/fastp, processed reads, alignment + alignment QC).

---

## Tests

```bash
# integration smoke test (requires nextflow on PATH)
pytest tests/integration -q -m nextflow
```

The integration test generates valid synthetic FASTQ fixtures at runtime (under `tests/integration/fixtures/`, git-ignored), runs `-stub -profile standard`, and asserts the key artifacts are published.
