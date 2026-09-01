# Chapter 29: Apptainer (Singularity)

> The rootless container technology used on HPC clusters, letting
> scientists run reproducible containers without administrator rights.

---

## 1. What is it?

**Apptainer** (formerly **Singularity**) is a container runtime
designed for **high-performance computing (HPC)**. Unlike Docker, it
runs containers **without root privileges** and integrates with shared
filesystems and schedulers (SLURM).

It can run Docker images directly (`.sif` format), so the same
reproducibility carries onto the cluster.

---

## 2. Why do we need it?

- HPC clusters typically **forbid Docker** (security: it needs root).
- Apptainer runs user-space containers safely on shared clusters.
- It supports running existing Docker images, so workflows port easily.
- Nextflow supports `-profile singularity` transparently.

---

## 3. Where does it fit?

```
Docker image (Ch 28) -> Apptainer (pull/convert to .sif) -> HPC/SLURM
                                                            |
                                      Nextflow -profile singularity
```

Apptainer brings container portability to the cluster (Ch 31).

---

## 4. Input

- A Docker image reference (e.g., `docker://nfcore/rnaseq:3.16`)
- Or a `.sif` (Apptainer) image file

---

## 5. Output

- A `.sif` **singularity image file** that runs on the cluster.

---

## 6. How it works

1. **Pull** a Docker image and convert to a single-file `.sif`:
   `apptainer pull docker://nfcore/rnaseq:3.16`
2. **Run** the tool:
   `apptainer exec rnaseq.sif fastqc reads.fastq.gz`
3. Because it's rootless and integrates with the host filesystem, it
   runs where Docker can't.

---

## 7. Biology behind it

- Reproducible tool versions on shared HPC clusters (as with Docker, Ch
  28), but permitted where Docker isn't.
- Ensures cluster-computed counts match local computed counts.

---

## 8. Command

```bash
# Pull a Docker image and convert to .sif
apptainer pull docker://nfcore/rnaseq:3.16

# Run a tool inside the container
apptainer exec rnaseq_3.16.sif fastqc data/reads.fastq.gz

# Nextflow profile
nextflow run main.nf -profile singularity
```

---

## 9. Example

On a SLURM cluster, Nextflow with `-profile singularity` runs every
process inside `.sif` images pulled from Docker Hub, without any
per-user installs.

---

## 10. How to read the output

- `apptainer exec <img>.sif <cmd>` stdout is normal tool output.
- Successful `.sif` pull = a ready-to-run portable image.

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| `.sif` not found | `apptainer pull` first |
| Root needed | Apptainer is rootless; check perms on module load |
| Docker daemon interaction | Not required; converts from registry |
| Binding host paths | Use `--bind /path` or default current dir |

---

## 12. Limitations

- Rootless design means some privileged Docker features are unavailable.
- Image conversion/pull needs a registry or a `.sif` artifact.
- Slightly different from Docker for advanced features.

---

## 13. How our project uses it

- **Future** phase: `-profile singularity` for HPC execution.
- Docker images (Ch 28) convert to `.sif` for cluster use.
- Complement to conda (Ch 27) for full portability.

---

## 14. Official documentation

- **Apptainer**:
  https://apptainer.org/
- **Singularity (legacy)**:
  https://sylabs.io/singularity/
- **Defining containers**:
  https://apptainer.org/docs/user/latest/

---

## 15. Mini exercise

1. Why can't Docker run on most HPC clusters, and why can Apptainer?
2. What is a `.sif` file?
3. How do you convert a Docker image for Apptainer use?
4. How does Nextflow integrate Apptainer?
5. Compare conda (Ch 27), Docker (Ch 28), and Apptainer.

---

**End of Reproducibility phase.**

> **Next**: [Chapter 30: Linux/HPC](../11_infrastructure/linux.md)
