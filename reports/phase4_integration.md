# Phase 4 — Final Integration & Boundary Document

**Purpose**: Demonstrate that all Phase 4 components form **one coherent prototype**, and precisely document the boundary between the six Phase-4 dimensions so the project never overstates what is real, what is orchestrated, what is validated, and what remains to be done.

**Project**: Airway Smooth Muscle Glucocorticoid Response — GSE52778 (tutorial scale)
**Generated**: Step 15 (final Phase-4 integration gate)
**Status**: PHASE 4 COMPLETE — prototype is coherent end-to-end. **Not** genome-wide biological inference; not a full GSE52778 re-analysis.

---

## 1. The six Phase-4 dimensions

Phase 4 integrates six distinct capabilities, each with its own maturity level. This document is the authoritative statement of **what each dimension is**, **where it lives**, **how it was proven**, and **its honest current status**.

| # | Dimension | Primary location(s) | Status |
|---|---|---|---|
| 1 | Real tutorial-scale execution | `results/` (`real_*`), `scripts/R/`, `scripts/python/` | **DONE** (real tools, tutorial scale) |
| 2 | Workflow orchestration | `workflow/` (Nextflow DSL2) | **DONE** (stub-validated topology) |
| 3 | UI/backend integration | `backend/`, `ui/` | **DONE** (serves real artifacts; `isMock` correctly true) |
| 4 | Reproducibility infrastructure | `envs/rnaseq.yml`, `containers/`, `metadata/` | **DONE** (static/pinned; container runtime pending) |
| 5 | CI validation | `.github/workflows/ci.yml`, `tests/` | **DONE** (authored + locally validated; Actions run pending) |
| 6 | Full genome-wide GSE52778 analysis | — | **NOT DONE** (separate research milestone) |

---

## 2. One coherent prototype — how the parts connect

The prototype is a single pipeline whose stages feed one another, and whose outputs are surfaced through the UI/API while being reproducible and validated by CI.

```text
                    ┌─────────────────────────────────────────────────────────┐
                    │ REPRODUCIBILITY INFRASTRUCTURE (dim 4)                  │
                    │  envs/rnaseq.yml ──► containers/Dockerfile · rnaseq.def │
                    └───────────────┬─────────────────────────────────────────┘
                                    │ pinned tool versions
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ REAL TUTORIAL-SCALE EXECUTION (dim 1)  60k-scale, real-loci 3-gene reference │
│  FastQC ─► fastp ─► FastQC ─► STAR ─► SAMtools/RSeQC ─► featureCounts ─►     │
│  DESeq2 ─► visualization ─► clusterProfiler                                   │
└──────────────┬───────────────────▲───────────────────────────────────────────┘
               │ 6 real BAMs       │ real count matrix / DE / pathway files
               ▼                   │ (results/real_*)
┌──────────────────────────┐  ┌────┴───────────────────────────────────────────┐
│ WORKFLOW ORCHESTRATION   │  │ UI/BACKEND INTEGRATION (dim 3)                 │
│ (dim 2) workflow/ DSL2    │  │  backend seeds/TESTS from results/real_*       │
│  re-expresses the SAME    │  │  FastAPI (/api/v1) ──► React UI               │
│  steps as portable Nextflow│  │  isMock:true · executionReal:true            │
└──────────────────────────┘  └────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ CI VALIDATION (dim 5)  GitHub Actions: unit · ui build · config parse ·      │
│  nextflow-stub · metadata  +  tests/unit + tests/integration (locally green) │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Coherence argument**: The same analytical steps were first executed with the **real tools** against the real (subsampled) dataset (dimension 1), then **re-expressed as a portable Nextflow DSL2 pipeline** whose modules wrap those exact tools and scripts (dimension 2). The real outputs are **served to a UI/API** (dimension 3) with provenance flags that keep the distinction honest. The environment and tools are **captured in a version-constrained conda env and container defs** (dimension 4) so the executable path is reproducible. Everything is **guarded by unit, integration, and CI checks** (dimension 5).

The result is a prototype that is traceable from raw FASTQ → real DESeq2 → UI, with a documented, reproducible, CI-checked path — while the **full biological analysis (dimension 6) is explicitly the next research milestone, not yet attempted.**

---

## 3. Boundary — precisely what is real vs orchestrated vs pending

This section is the authoritative boundary statement. Every claim below is traceable to committed artifacts.

### 3.1 Dimension 1 — Real tutorial-scale execution (DONE)

- **Real tools executed**: FastQC 0.12.1, fastp 1.3.6, STAR 2.7.x, SAMtools 1.24, RSeQC 5.0.5, featureCounts 2.1.1, DESeq2 1.50.2 (R 4.5.3), clusterProfiler 4.18.4, MultiQC 1.35.
- **Real data**: first 50,000 read pairs/sample from the genuine GSE52778 SRA accessions (6 samples, PE 2×63).
- **Reference**: real-loci mini-reference (`data/reference/mini_real/`) containing 3 genes (CRISPLD2, GAPDH, ACTB) — **not** the full genome.
- **Honest results**: CRISPLD2 is the single DEG; genuine zero GO/KEGG enrichment at this scale; low genome-mapping % documented as expected for a 3-gene reference.
- **Evidence**: `reports/step4…step9` gate reports + `reports/final_report/real_pipeline_report.md`.
- **Boundary**: This is **tutorial-scale execution integrity, not publication-grade inference**.

### 3.2 Dimension 2 — Workflow orchestration (DONE, stub-validated)

- `workflow/main.nf` + 11 modules + 4 subworkflows re-express the same steps as a portable Nextflow DSL2 pipeline.
- `-stub -profile standard` validates **topology only** (54/54 tasks, correct fan-out, published artifacts) — it does **not** execute STAR/featureCounts/DESeq2 on real data.
- A **real** run executes the same validated commands, but at the same tutorial scale (3-gene reference) → still not publication analysis.
- See `workflow/README.md` for run instructions.
- **Boundary**: Orchestration is proven for topology; containerized/runtime execution remains unverified (dimension 4).

### 3.3 Dimension 3 — UI/backend integration (DONE)

- Backend seeds from `results/real_*` (counts, DE, pathway, QC, alignment, visualization) and serves them via `/api/v1`; UI renders them (with mock-data fallback if the API is unreachable).
- **Locked provenance semantics**: `executionReal: true` · `analysisScope: "tutorial_mini_reference"` · `isMock: true`. These coexist because real tools ran at tutorial scale (artifacts are `source_derived`) but this is **not** publication/full biological analysis.
- **Boundary**: `isMock` stays **true** until a full/publication analysis exists. The UI is **read-only**; it cannot trigger analysis.

### 3.4 Dimension 4 — Reproducibility infrastructure (DONE, static)

- `envs/rnaseq.yml`: version-constrained environment (exact-pinned core tools; constrained runtimes/scientific stack).
- `containers/Dockerfile` + `containers/rnaseq.def`: build `rnaseq-pipeline:0.1.0-tutorial` (docker) and `rnaseq-pipeline_0.1.0-tutorial.sif` (Apptainer/Singularity) — **authored statically**.
- `metadata/*.yaml`: dataset + reference provenance and checksums.
- **Boundary**: Images are **not built** and container runtime (docker/apptainer/singularity) execution is **not performed** in this environment. A 7-item runtime-validation checklist is documented in `containers/README.md` but **NOT EXECUTED**. Exact per-build resolution locking (e.g. `conda-lock`) is a future enhancement.

### 3.5 Dimension 5 — CI validation (DONE, authored + locally validated)

- `.github/workflows/ci.yml`: 5 jobs (unit-tests, ui, config-parse, nextflow-stub, metadata-validation), container-free, trigger `push → main`.
- `tests/unit/` (20 stdlib-only tests) and `tests/integration/test_nextflow_stub.py` (stub smoke test with valid synthetic FASTQ fixtures).
- **Locally validated in this environment**: 20 unit tests pass, integration stub passes, 5/5 profiles parse, UI typecheck+build clean, metadata validated, ci.yml YAML valid, staged diff clean.
- **Boundary**: The workflow is **authored and locally checked**, but **GitHub Actions has not run** in this environment (no runner / no `gh` CLI). Do **not** report CI as "passed" until the Actions run is observed. Backend is **intentionally excluded** from CI (import-time seeding from gitignored `results/*`).

### 3.6 Dimension 6 — Full genome-wide GSE52778 research analysis (NOT DONE)

- **Not attempted** in this project phase. Requires a full genome reference + annotation, the complete (non-subsampled) dataset, genome-wide DESeq2, and full ORA/GSEA.
- Completion of dimension 6 is the precondition to flipping `isMock: true → false` and to any publication-grade claim.
- **Boundary**: This is the **explicitly deferred** research milestone — the prototype's execution integrity, orchestration, integration, reproducibility, and CI are all demonstrated *independent of* dimension 6's outcome.

---

## 4. The boundary is provenance discipline, not a bug

The simultaneous truth of `executionReal: true` **and** `isMock: true` is deliberate and correct:

| Claim | Value | Why |
|---|---|---|
| Real tools ran? | Yes | true execution of fastp/STAR/DESeq2/… at tutorial scale |
| Tutorial scale? | Yes | 6 samples × 50k read pairs, 3-gene mini-reference |
| Publication/full analysis? | No | 3-gene panel ≠ genome-wide biological inference |
| `isMock` | `true` | signals "not publication-grade", per locked semantics |
| artifacts labeled | `source_derived` | they genuinely derive from real tool output |

Keeping the boundary precise here is what makes the prototype scientifically honest rather than overstated.

---

## 5. Phase 4 gate summary

| Step | Component | Outcome |
|---|---|---|
| 11 | Real artifact → UI/API integration | ✅ PASS |
| 12 | Nextflow DSL2 workflow | ✅ PASS (stub-validated) |
| 13 | Docker + Apptainer authorship | ✅ PASS (static; runtime pending) |
| 14 | CI/CD + automated validation | ✅ PASS (locally validated; Actions pending) |
| 15 | Phase-4 integration & boundary | ✅ PASS (this document) |

---

## 6. Post-Phase-4 robustness fixes (real-pipeline discovery)

Two workflow issues were discovered and fixed during the first full real-pipeline run (`-profile conda` on `~/RNA-seq-Pipeline`). Both are minor robustness corrections, not behavioral changes to the analysis.

| Commit | Fix | Evidence |
|---|---|---|
| `fd12e4a` | Remove unused STAR `.bai` output emit and publish pattern (only `.bam` published) | Stub 54/54 ✔; live run published 6 BAMs, 0 BAIs |
| `1dcf92a` | Create `results/differential_expression` directory in DESEQ2 real script block | Stub 54/54 ✔; live run DESEQ2 1/1 with real CSV output |

**What they are**: Workflow-only module corrections — the R script (`scripts/R/run_deseq2_fittype_mean.R`) was always correct; the Nextflow process wrapper needed matching `mkdir -p` in the real (non-stub) path. The STAR bai removal cleans an unused output channel that never connected to any consumer.

**What they are not**: No change to the analysis logic, reference data, or published real artifacts (the real DESeq2 CSV and 6 BAMs were already correct before the commit). Both repos (Windows and Linux) are now synced at `1dcf92a`.

---

**Overall**: All Phase-4 components form one coherent prototype with a documented, honest boundary. The full genome-wide GSE52778 research analysis remains the explicit, separate next milestone.
