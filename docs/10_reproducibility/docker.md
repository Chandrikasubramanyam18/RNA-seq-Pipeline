# Chapter 28: Docker

> A containerization technology that packages each pipeline tool with
> its entire runtime into a portable, run-anywhere image.

---

## 1. What is it?

**Docker** packages an application (tool) plus all its dependencies
(libraries, OS layers) into a **container image**. A container runs
that image in an isolated environment, so "it runs on my machine" is no
longer an excuse.

Each pipeline process (STAR, Salmon, DESeq2, ...) can have its own
image, guaranteeing identical execution anywhere.

---

## 2. Why do we need it?

- Conda (Ch 27) pins versions but still relies on the host OS.
- Docker captures the **entire runtime** (OS + libs + tool) in one
  image.
- Nextflow (Ch 25) can pull each process's container automatically.
- Enables HPC/cloud portability (Ch 31/32).

---

## 3. Where does it fit?

```
Conda (env) ---+---> Docker (immutable image) ---> Nextflow (per-process)
Build scripts          |
Dockerfile          registry (pull)
```

Docker images wrap the conda environments so Nextflow runs them
consistently.

---

## 4. Input

- A `Dockerfile` (optional; many use `nf-core/rnaseq:latest` or
  `staphb/*` images)
- The conda env can be exported into an image

---

## 5. Output

- A **container image** (e.g., `nfcore/rnaseq:3.16`) that Nextflow
  runs.

---

## 6. How it works

1. A `Dockerfile` defines the image: base OS, install tools, set
   entrypoint.
2. `docker build` creates the image from the Dockerfile.
3. `docker run` executes a container from the image; process isolation,
   same behavior everywhere.
4. Nextflow's `process.container` specifies which image each process
   uses; Nextflow pulls and runs it.

Example:

```dockerfile
FROM continuumio/miniconda3
RUN conda install -c bioconda -c conda-forge fastqc=0.12.1
```

---

## 7. Biology behind it

- Containerizing tools ensures the **same aligner/counter versions**
  run in production as in testing.
- This guarantees numeric reproducibility of counts and DE, so
  biological findings aren't artifacts of software drift.

---

## 8. Command

```bash
# Build an image
docker build -t rnaseq-tools:latest .

# Run a tool in a container
docker run --rm -v "$PWD":/data rnaseq-tools fastqc data/reads.fastq.gz

# Nextflow uses containers automatically via config
# process.container = 'nfcore/rnaseq:latest'
```

---

## 9. Example

Using nf-core's official image (Ch 26), Nextflow runs STAR inside a
container without local install:

```
[fastqc] process > staphb/fastqc
[star]   process > nfcore/rnaseq:latest
```

---

## 10. How to read the output

- `docker images` lists locally available images.
- `docker ps -a` shows running/stopped containers.
- Nextflow logs show which container image a process used.

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| Image not found | `docker pull` / correct registry tag |
| Permission denied | Add user to `docker` group / Docker Desktop running |
| Out of disk | `docker system prune` |
| Container can't see files | Mount volumes with `-v` |

---

## 12. Limitations

- Requires Docker Desktop (or WSL2) on Windows.
- Image build/pull adds overhead and disk usage.
- Some HPC clusters forbid Docker (root); use Apptainer (Ch 29).

---

## 13. How our project uses it

- **Future** phase: Nextflow run with `-profile docker`.
- Images derived from conda envs / nf-core base images.
- WSL2/Docker Desktop documented in `environment_setup.md`.

---

## 14. Official documentation

- **Docker**:
  https://docs.docker.com/
- **Dockerfile reference**:
  https://docs.docker.com/reference/dockerfile/
- **Docker Hub**:
  https://hub.docker.com/

---

## 15. Mini exercise

1. What is a container image vs a running container?
2. Why does Docker capture more than conda (Ch 27)?
3. How does Nextflow use images for each process?
4. Why do some HPC clusters prefer Apptainer over Docker?
5. Write a minimal Dockerfile that installs FastQC.

---

> **Next**: [Chapter 29: Apptainer](apptainer.md)
