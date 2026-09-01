# Chapter 31: SLURM (HPC Scheduling)

> The workload manager used on high-performance computing (HPC)
> clusters to schedule parallel pipeline jobs across many nodes.

---

## 1. What is it?

**SLURM** (Simple Linux Utility for Resource Management) is a **job
scheduler** for HPC clusters. It queues, schedules, and manages
computational jobs on shared compute nodes, allocating CPUs, memory,
and GPUs.

Nextflow (Ch 25) can submit each pipeline step as a SLURM job,
enabling large-scale parallel execution.

---

## 2. Why do we need it?

- Real RNA-seq datasets are too big for one laptop.
- Clusters have many nodes; a scheduler fairly allocates them.
- SLURM lets you run hundreds of alignment/quant jobs in parallel.
- It tracks resource usage and handles failures across the cluster.

---

## 3. Where does it fit?

```
Linux (Ch 30) -> SLURM (schedule) -> Nextflow -> pipeline tools
```

SLURM is the scheduling layer under Nextflow on HPC.

---

## 4. Input

- A **job script** (`.sbatch`) with resource requests.
- Or a Nextflow config directed at the SLURM executor.

---

## 5. Output

- Scheduled jobs running on cluster nodes with logs and exit statuses.

---

## 6. How it works

### 6.1 Core commands

```bash
sbatch job.sh        # submit a job
squeue               # view queued/running jobs
sacct                # view completed job accounting
scancel <jobid>      # cancel a job
```

### 6.2 Job script (sbatch)

```bash
#!/bin/bash
#SBATCH --job-name=star_C1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32GB
#SBATCH --time=04:00:00
#SBATCH --output=logs/star_C1_%j.log

conda activate rnaseq-pipeline
STAR --genomeDir ... --runThreadN 8 ...
```

### 6.3 Partition & QoS

Jobs run in **partitions** (queues) with quality-of-service limits on
time and resources.

---

## 7. Biology behind it

- SLURM parallelizes per-sample steps: 6 STAR alignments, 6 Salmon
  quantifications can run **simultaneously** on different nodes.
- Faster turnaround for large cohorts without changing the biology.

---

## 8. Command

```bash
# Submit a single job
sbatch scripts/slurm/star_C1.sbatch

# Check the queue
squeue -u $USER

# After completion, check usage
sacct -j <jobid> --format=JobID,State,CPUTime,MaxRSS
```

With Nextflow:

```groovy
// nextflow.config
process {
  executor = 'slurm'
  queue    = 'normal'
  cpus     = 8
  memory   = '32 GB'
  time     = '4h'
}
```

---

## 9. Example

Submitting our 6 samples as 6 parallel STAR jobs cuts wall time
~6x versus running sequentially, each on its own node.

---

## 10. How to read the output

- `squeue` : state (PD=pending, R=running, CG=completing).
- `sacct` : exit code, CPU time, peak memory of each step.
- Job logs (`slurm-<jobid>.out`) contain tool output.

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| Job out of memory (OOM killed) | Request more `--mem` |
| Job exceeds time limit | Increase `--time` / optimize |
| Queue is full | Use different partition/QoS; wait |
| Node-level failures | Resubmit; check `sacct` for exit codes |

---

## 12. Limitations

- Requires access to an HPC cluster (not free).
- Fair-share scheduling means jobs queue.
- Resource requests must match tool needs (STAR ~30GB RAM).

---

## 13. How our project uses it

- **Future** phase: Nextflow with `executor='slurm'` on a cluster.
- Pipeline tools (STAR, Salmon, featureCounts) run as SLURM jobs.
- Apptainer (Ch 29) containers used on the cluster.

---

## 14. Official documentation

- **SLURM**:
  https://slurm.schedmd.com/
- **SLURM quickstart / command overview**:
  https://slurm.schedmd.com/quickstart.html

---

## 15. Mini exercise

1. What does SLURM do, and why is a scheduler needed on clusters?
2. What do `sbatch`, `squeue`, `sacct`, and `scancel` do?
3. Write an `#SBATCH` header requesting 8 CPUs and 32GB for 4 hours.
4. How does Nextflow submit pipeline steps to SLURM?
5. What happens if a job is killed for exceeding memory?

---

> **Next**: [Chapter 32: AWS Cloud](aws.md)
