# Chapter 30: Linux / HPC Command Line

> The operating system and shell skills needed to actually run
> bioinformatics pipelines -- essential for anything beyond toy
> datasets.

---

## 1. What is it?

**Linux** is the standard operating system for bioinformatics.
Bioinformatics tools (STAR, SAMtools, Nextflow) are native Linux
binaries, and HPC clusters (Ch 31) run Linux. You interact with it via
the **command line / shell** (typically Bash).

This chapter covers the core Linux skills used throughout the
pipeline: navigation, files, permissions, pipes, background jobs, and
resource awareness.

---

## 2. Why do we need it?

- All our tools run on Linux (native binaries).
- WSL2 (see `environment_setup.md`) gives Windows users Linux.
- Real datasets and clusters require command-line fluency.
- Understanding Linux is prerequisite to HPC and cloud (Ch 31/32).

---

## 3. Where does it fit?

```
Linux (OS)  ->  shell commands  ->  run all pipeline tools (Ch 8-24)
```

Linux is the foundation layer under everything.

---

## 4. Input

- A Linux environment (Ubuntu via WSL2, or a remote cluster).

---

## 5. Output

- The ability to navigate files, run tools, manage processes, and
  monitor resources.

---

## 6. How it works

### 6.1 Navigation & files

```bash
pwd          # print working directory
ls -la       # list files (long, all)
cd path      # change directory
mkdir -p d   # create directory (and parents)
cp / mv / rm # copy, move, remove
```

### 6.2 Permissions

```bash
chmod +x script.sh   # make executable
ls -l                # view permissions
```

### 6.3 Pipes & redirection

```bash
command1 | command2      # pipe output
> out.txt                # redirect to file
< in.txt                 # input from file
```

### 6.4 Processes & resources

```bash
top / htop     # monitor CPU/memory
free -h        # memory usage
df -h          # disk usage
nohup cmd &    # run in background
```

### 6.5 Finding & searching

```bash
grep pattern file          # search text
find . -name "*.fastq.gz"  # find files
```

---

## 7. Biology behind it

- Linux skills let you move large FASTQ/BAM files, run resource-heavy
  alignments, and interpret logs -- directly supporting the biology
  (counts, DE, pathways).
- The commands you run *are* the computational biology.

---

## 8. Command (examples)

```bash
# Navigate to project in WSL2
cd "/mnt/c/Chandrika/RNA-seq  Pipeline"

# Check a FASTQ file
zcat data/raw/C1_R1.fastq.gz | head -8

# Run a script in the background, log output
nohup bash scripts/run_fastqc.sh \
  --input data/raw --output results/fastqc/raw --threads 4 \
  > logs/fastqc.log 2>&1 &

# Monitor while it runs
top
```

---

## 9. Example

A typical real workflow in WSL2:

```bash
conda activate rnaseq-pipeline
bash scripts/run_fastp.sh --samplesheet metadata/samplesheet.csv ...
```

---

## 10. How to read the output

- `head`/`tail` preview streamed data.
- `ls -la` reveals file sizes/permissions.
- `top`/`free -h` show whether the machine can handle the next step.
- Logs (redirected with `>` / `2>&1`) capture tool messages.

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| `command not found` | Activate env / check PATH |
| Permission denied | `chmod +x` script |
| Out of memory | Check `.wslconfig`; smaller reference |
| Disk full | `df -h`; clean work dir |
| `cannot access /mnt/c` | Open WSL2 from the project folder |

---

## 12. Limitations

- Steep learning curve; easy to make operational mistakes.
- Windows users must use WSL2 (not native PowerShell).
- Managing huge files manually is error-prone (Nextflow helps, Ch 25).

---

## 13. How our project uses it

- All `scripts/*.sh` run under Bash in WSL2/Linux.
- `environment_setup.md` documents WSL2 setup.
- The pipeline is executed from the command line.
- Future Nextflow orchestration runs the same commands.

---

## 14. Official documentation

- **Ubuntu / WSL2**:
  https://learn.microsoft.com/en-us/windows/wsl/
- **The Linux Command Line (free book)**:
  https://linuxcommand.org/tlcl.php
- **GNU Bash manual**:
  https://www.gnu.org/software/bash/manual/

---

## 15. Mini exercise

1. What does `ls -la | wc -l` do?
2. How do you make a shell script executable and give it permission?
3. What does `2>&1` mean in a command?
4. How would you run a long alignment in the background and log it?
5. Why must Windows users run the pipeline in WSL2?

---

> **Next**: [Chapter 31: SLURM HPC](slurm.md)
