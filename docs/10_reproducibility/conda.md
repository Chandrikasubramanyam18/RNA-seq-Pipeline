# Chapter 27: Conda / Environment Management

> The tool that manages software versions so every tool runs with the
> exact pinned dependency set -- the foundation of reproducibility.

---

## 1. What is it?

**Conda** (and its faster backend **Mamba**) is a package and
environment manager. It creates **isolated environments** that install
specific, pinned versions of software and their dependencies without
conflicting with the system Python or other tools.

A conda environment is defined declaratively in a `*.yml` file, making
the whole software stack **reproducible**.

---

## 2. Why do we need it?

Bioinformatics tools have complex, version-specific dependencies. A
different version of one library can silently change results. Conda:

- Pins exact versions (e.g., STAR 2.7.11b, FastQC 0.12.1)
- Isolates environments so tools don't clash
- Makes the environment **declarative and reproducible**
- Integrates with Nextflow for per-process environments

---

## 3. Where does it fit?

```
conda (create/activate env)  ->  all pipeline tools run inside it
                                        |
               environment_setup.md (docs) documents this
```

Conda provides the runtime for every tool in Ch 8-24.

---

## 4. Input

- An environment manifest file: `envs/rnaseq.yml` (pinned versions)
- The Miniforge installer (bioconda/conda-forge channels)

---

## 5. Output

- An installed conda environment named `rnaseq-pipeline` with all
  pinned tools available on `$PATH`.

---

## 6. How it works

1. **Conda solves dependencies**: reads `rnaseq.yml`, resolves a
   consistent set of packages from `conda-forge` and `bioconda`.
2. **Installs into an isolated prefix** (e.g., `~/miniforge3/envs/
   rnaseq-pipeline`).
3. **Activation** prepends the env's `bin/` to `$PATH`, exposing the
   tools.
4. Pinned versions guarantee the same stack everywhere.

Example `envs/rnaseq.yml` (from `environment_setup.md`):

```yaml
name: rnaseq-pipeline
channels:
  - conda-forge
  - bioconda
  - nodefaults
dependencies:
  - python=3.11
  - r-base>=4.5,<4.7
  - openjdk>=17
  - nextflow>=23.10.0
  - fastqc=0.12.1
  - fastp=1.3.6
  - multiqc=1.35
  - star=2.7.11b
  - samtools=1.24
  - subread=2.1.1
```

---

## 7. Biology behind it

- Version pinning prevents subtle numeric differences in aligners /
  counters from changing biological conclusions.
- Reproducible environments mean another researcher running the same
  command gets the **same counts, same DE results**.
- This is standard practice for trustworthy bioinformatics.

---

## 8. Command

```bash
# Create the environment from the manifest
mamba env create -f envs/rnaseq.yml

# Activate it (all tools now on PATH)
conda activate rnaseq-pipeline

# Verify (implemented scripts)
bash scripts/check_environment.sh
python3 scripts/python/check_environment.py
```

---

## 9. Example

After activation, `which star` shows the tool inside the env:

```
/home/user/miniforge3/envs/rnaseq-pipeline/bin/star
```

instead of a system path -- confirming the pinned version is in use.

---

## 10. How to read the output

- `conda env list` shows available environments; `*` marks active.
- `conda list` shows installed packages and versions.
- `check_environment` scripts report which tools are present/missing
  and their versions.

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| Slow solver | Use `mamba` instead of `conda` |
| Package not found (osx/linux) | Ensure correct platform in WSL2 |
| `Command not found` after activate | Check channel priority / exact name |
| Conflicting deps | Rely on the pinned manifest |

---

## 12. Limitations

- Large download/install footprint for bioinformatics stacks.
- Solver time on version conflicts (mitigated by Mamba/pinning).
- On Windows, must run inside WSL2 (native bioconda is linux-64).

---

## 13. How our project uses it

- `envs/rnaseq.yml` pins all tool versions.
- `check_environment.sh` / `check_environment.py` verify the stack
  (implemented).
- `environment_setup.md` documents WSL2/Miniforge setup.
- Future Nextflow uses the conda env (or containers, Ch 28/29).

---

## 14. Official documentation

- **Conda**:
  https://docs.conda.io/
- **Mamba**:
  https://mamba.readthedocs.io/
- **bioconda**:
  https://bioconda.github.io/

---

## 15. Mini exercise

1. Why is version pinning essential for reproducibility?
2. What is the difference between conda and mamba?
3. Where is `envs/rnaseq.yml` and what does it contain?
4. Why must Windows users run conda inside WSL2?
5. Which implemented scripts verify the environment?

---

> **Next**: [Chapter 28: Docker](docker.md)
