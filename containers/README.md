# Containers (Step 13)

Static containerization (Docker + Apptainer/Singularity) for the tool stack
declared in [`envs/rnaseq.yml`](../envs/rnaseq.yml).

> **Environment type**: `envs/rnaseq.yml` is a **version-constrained
> environment specification**, not a fully locked resolution. Most core tools
> are exact-pinned (e.g. STAR `2.7.11b`, FastQC `0.12.1`, samtools `1.24`),
> while language runtimes and the Python scientific stack use version
> constraints (`>=` / ranges, e.g. `r-base>=4.5,<4.7`, `openjdk>=17`,
> `nextflow>=23.10.0`). Exact per-build resolution locking (`conda-lock` or
> equivalent) is a future reproducibility enhancement, not yet applied.

---

## Architecture (orchestrator vs. container)

```text
Host
  ↓
Nextflow                  ← workflow orchestrator (channels, tasks, retries)
  ↓
Docker / Apptainer        ← reproducible software environment (per-process)
  ↓
RNA-seq tools             ← FASTP · STAR · featureCounts · DESeq2 · ...
```

- **Nextflow** is the **orchestrator**. It runs on the host (or a local conda
  environment) and launches each process inside the container.
- **The container** is the **reproducible software environment**: the tool
  versions declared in `envs/rnaseq.yml`, frozen at build time (FastQC, fastp,
  STAR, SAMtools, RSeQC, featureCounts, salmon, DESeq2, clusterProfiler,
  MultiQC).
- The image **also contains Nextflow** because the current project
  specification (`envs/rnaseq.yml`) includes it. This is a **convenience** —
  Nextflow does **not** need to run inside the container for the workflow to
  work; `/usr/local/bin/nextflow` on the host drives containerized processes.

---

## Static validation completed

The following was completed in this repository (no container runtime required):

- [x] `containers/Dockerfile` authored (Micromamba base, installs `envs/rnaseq.yml`,
      env exposed on `PATH`, `WORKDIR /workspace`, `CMD ["bash"]`).
- [x] `containers/rnaseq.def` authored (Apptainer/Singularity definition
      bootstrapping the same Micromamba base and staging the same
      `envs/rnaseq.yml`).
- [x] Docker and Apptainer definitions describe the **same** intended
      environment and expose it on `PATH` identically.
- [x] Nextflow profiles in `workflow/nextflow.config`
      (`standard`, `conda`, `docker`, `apptainer`, `singularity`) parse and
      resolve.
- [x] Environment specification (`envs/rnaseq.yml`) reviewed; terminology is
      version-constrained, not "fully locked".
- [x] Configuration validated (YAML parses; profiles resolve).

> No image was built and no containerized pipeline run was performed as part
> of Step 13. Static authorship is the scope of this step.

---

## Runtime validation NOT completed

> **Docker and Apptainer images have not been built or executed in the current
> environment because the required container runtimes are unavailable.**

This means the Step 13 deliverables have **not** been runtime-tested. Do **not**
treat the commands below as already-passing results — they are the *instructions
and future checklist* for a machine that has Docker/Apptainer installed.

---

## Files

| File             | Purpose                                                       |
|------------------|---------------------------------------------------------------|
| `Dockerfile`     | Single-image Docker build (`Micromamba` base + env spec).     |
| `rnaseq.def`     | Apptainer/Singularity definition → `.sif` for HPC clusters.   |

Both build the *same* environment from `envs/rnaseq.yml` so every Nextflow
process (FastQC, fastp, STAR, SAMtools, RSeQC, featureCounts, salmon,
DESeq2, clusterProfiler, MultiQC) sees the same declared tool versions.

---

## Future runtime validation checklist

**All items below are NOT EXECUTED IN THIS ENVIRONMENT.** They are the steps to
run on a machine with Docker/Apptainer before any real containerized run.

### 1. Build the Docker image — NOT EXECUTED IN THIS ENVIRONMENT

Build from the repository **root** (so `envs/rnaseq.yml` is in context):

```bash
docker build -t rnaseq-pipeline:0.1.0-tutorial -f containers/Dockerfile .
```

### 2. Start a container and verify key tool versions — NOT EXECUTED IN THIS ENVIRONMENT

```bash
docker run --rm rnaseq-pipeline:0.1.0-tutorial \
    bash -lc 'which STAR && STAR --version && fastqc --version && featureCounts -v 2>&1 | head -n 1 && Rscript --version'
```

### 3. Build the Apptainer image — NOT EXECUTED IN THIS ENVIRONMENT

Build from the repository **root** (the `%files` staging expects
`envs/rnaseq.yml` under the build directory):

```bash
apptainer build rnaseq-pipeline_0.1.0-tutorial.sif containers/rnaseq.def
```

### 4. Run an Apptainer smoke test — NOT EXECUTED IN THIS ENVIRONMENT

```bash
apptainer exec rnaseq-pipeline_0.1.0-tutorial.sif \
    bash -lc 'which STAR && samtools --version | head -n 1 && multiqc --version'
```

### 5. Run a minimal Nextflow workflow with the Docker profile — NOT EXECUTED IN THIS ENVIRONMENT

```bash
nextflow run workflow -profile docker
```

### 6. Run a minimal Nextflow workflow with the Apptainer profile — NOT EXECUTED IN THIS ENVIRONMENT

```bash
nextflow run workflow -profile apptainer
# legacy runtime:
nextflow run workflow -profile singularity
```

### 7. Verify at least one expected output artifact — NOT EXECUTED IN THIS ENVIRONMENT

Confirm the containerized run produced the same expected artifacts as the
tutorial-scale runs (e.g. trimmed FASTQs, STAR BAMs, `featureCounts` count
matrix, DESeq2 results) under the configured `outdir`.

---

## Troubleshooting

| Symptom                                   | Fix                                        |
|-------------------------------------------|--------------------------------------------|
| `envs/rnaseq.yml not found` / build fails | Ensure the build runs from the repo root.  |
| Nextflow can't pull image                 | `docker pull rnaseq-pipeline:0.1.0-tutorial` (Docker) or build the `.sif` first (Apptainer). |
| RSeQC/Python tool "not found"             | Confirm `PATH` prefix in `%environment`/`ENV` points at `/opt/conda/envs/rnaseq-pipeline/bin`. |

---

## Future improvements (recorded, not implemented)

- **Exact resolution locking**: capture a fully fixed resolution of
  `envs/rnaseq.yml` (e.g. `conda-lock` / mamba lockfile) so rebuilds are
  byte-reproducible; then the environment can be described as "locked", not
  merely "version-constrained".
- **Image-size optimization**: the current image contains the full validated
  RNA-seq stack and is intentionally left uncompressed for Step 13's
  educational/reproducibility objective. Size reduction (multi-stage builds,
  removing non-essential packages, layer squashing) is deferred.
- **Runtime user/workspace check**: confirm whether the image's default user
  can write to the Nextflow work directory at runtime (untested here); adjust
  via `docker.runOptions`/Apptainer options only after a real run.