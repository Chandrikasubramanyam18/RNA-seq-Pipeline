# Containers (Step 13)

Static containerization for the pinned tool stack in [`envs/rnaseq.yml`](../envs/rnaseq.yml).

> **Gate note**: Step 13 is *static authorship*. No Docker/Apptainer daemon is
> available in the development environment, so **no images have been built or
> smoke-tested here**. Build + verify on a machine with the runtime before any
> real `-profile docker` / `-profile apptainer` run.

## Files

| File             | Purpose                                                       |
|------------------|---------------------------------------------------------------|
| `Dockerfile`     | Single-image Docker build (`Micromamba` base + pinned env).   |
| `rnaseq.def`     | Apptainer/Singularity definition → `.sif` for HPC clusters.   |

Both build the *same* environment from `envs/rnaseq.yml` so every Nextflow
process (FastQC, fastp, STAR, SAMtools, RSeQC, featureCounts, salmon,
DESeq2, clusterProfiler, MultiQC) sees identical tool versions.

## Docker

Build from the repository **root** (so `envs/rnaseq.yml` is in context):

```bash
docker build -t rnaseq-pipeline:0.1.0-tutorial -f containers/Dockerfile .
```

Smoke test a tool inside the image:

```bash
docker run --rm rnaseq-pipeline:0.1.0-tutorial \
    bash -lc 'which STAR && STAR --version && fastqc --version && featureCounts -v 2>&1 | head -n 1 && Rscript --version'
```

Run the pipeline with it:

```bash
nextflow run workflow -profile docker
```

## Apptainer / Singularity

Build from the repository **root** (the `%files` staging expects
`envs/rnaseq.yml` under the build directory):

```bash
apptainer build rnaseq-pipeline_0.1.0-tutorial.sif containers/rnaseq.def
```

Smoke test:

```bash
apptainer exec rnaseq-pipeline_0.1.0-tutorial.sif \
    bash -lc 'which STAR && samtools --version | head -n 1 && multiqc --version'
```

Run on an HPC cluster (rootless):

```bash
nextflow run workflow -profile apptainer
# legacy runtime:
nextflow run workflow -profile singularity
```

## Troubleshooting

| Symptom                                   | Fix                                        |
|-------------------------------------------|--------------------------------------------|
| `envs/rnaseq.yml not found` / build fails | Ensure the build runs from the repo root.  |
| Nextflow can't pull image                 | `docker pull rnaseq-pipeline:0.1.0-tutorial` (Docker) or build the `.sif` first (Apptainer). |
| RSeQC/Python tool "not found"             | Confirm `PATH` prefix in `%environment`/`ENV` points at `${prefix}/envs/rnaseq-pipeline/bin`. |