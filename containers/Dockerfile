# =============================================================================
#  rna-seq-pipeline — Docker image
# =============================================================================
#
#  Builds a single runtime image that contains the *exact* conda environment
#  defined in envs/rnaseq.yml (the pinned, validated tool stack used for the
#  tutorial-scale run: FastQC, fastp, STAR, SAMtools, RSeQC, featureCounts,
#  DESeq2, clusterProfiler, visualization, MultiQC, plus Nextflow itself).
#
#  Usage (build from the repository ROOT so envs/rnaseq.yml is in context):
#
#     docker build -t rnaseq-pipeline:<tag> -f containers/Dockerfile .
#
#  Nextflow then runs every process in this image via:
#
#     nextflow run workflow -profile docker
#     (or set process.container = 'rnaseq-pipeline:<tag>' + docker.enabled = true)
#
#  NOTE (Step 13 gate): this file is authored but NOT built in this
#  environment (no Docker daemon), so it is static/untested here. Follow the
#  build + smoke-test commands in containers/README.md on a machine with
#  Docker before running the `-profile docker` pipeline for real.
# =============================================================================

# --- Base image: Micromamba (conda-forge) --------------------------------
# Slim, fast, rootless-friendly; installs the pinned stack below.
FROM mambaorg/micromamba:2

# --- Metadata ------------------------------------------------------------
LABEL org.opencontainers.image.title="rna-seq-pipeline"
LABEL org.opencontainers.image.description="Tutorial-scale RNA-seq pipeline runtime (GSE52778, 3-gene mini-reference): FastQC -> fastp -> STAR -> SAMtools/RSeQC -> featureCounts -> DESeq2 -> visualization -> pathway -> MultiQC"
LABEL org.opencontainers.image.source="https://github.com/Chandrikasubramanyam18/RNA-seq-Pipeline"
LABEL org.opencontainers.image.version="0.1.0-tutorial"
LABEL org.opencontainers.image.licenses="MIT"

ARG CONDA_ENV_FILE=envs/rnaseq.yml

# --- Install the pinned conda environment --------------------------------
# envs/rnaseq.yml is at the repo root; the build context MUST be the repo root.
COPY --chown=$MAMBA_USER:$MAMBA_USER "$CONDA_ENV_FILE" /tmp/rnaseq.yml

RUN micromamba create -y -f /tmp/rnaseq.yml \
    && micromamba clean -ay \
    && rm -f /tmp/rnaseq.yml

# --- Activate the env + put tools on PATH --------------------------------
ENV PATH="/opt/conda/envs/rnaseq-pipeline/bin:${PATH}" \
    CONDA_DEFAULT_ENV=rnaseq-pipeline \
    TZ=Etc/UTC

# --- Working directory for Nextflow task dirs ----------------------------
# Nextflow mounts its per-task work directory at the process working dir; a
# predictable WORKDIR keeps `pwd` stable for tool calls that write relative
# paths (mirrors how the validated commands run in scripts/).
WORKDIR /workspace

# A plain `exec` keeps Nextflow's `containerOptions`/shell handling simple.
CMD ["bash"]