# RNA-seq Platform — Backend API (Phase 3)

Read-only FastAPI + SQLite backend for the RNA-seq analysis platform
(GSE52778 dexamethasone airway smooth-muscle demonstration project).

## Stack

- FastAPI (Pydantic v2 models)
- SQLAlchemy 2.0 ORM (declarative)
- Alembic migrations
- SQLite (local file, see `backend/data/`)

## Run

```powershell
# from the repo root
python -m pip install -r backend/requirements.txt

# seed-on-startup creates/leaves tables ready
python -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

Interactive docs: http://127.0.0.1:8000/docs
Health check:    http://127.0.0.1:8000/api/v1/health

### Seeding

The database is seeded automatically on startup from the repository's real
analysis artifacts:

| Table | Source artifact | Provenance |
| --- | --- | --- |
| `projects`, `samples` | `metadata/dataset_manifest.yaml`, `samplesheet.csv`, `reference_manifest.yaml` | source-derived metadata |
| `qc_metrics`, `multiqc_summary` | `results/fastqc/raw/*.tsv`, `results/fastp/*.tsv` | FastQC/fastp summaries |
| `de_results`, `pca_points`, `de_axes` | `results/differential_expression/deseq2_results.csv`, `results/visualization/*` | source-derived DE results |
| `pathway_enrichment` | `results/pathway_analysis/*.csv` | source-derived enrichment |
| `alignment_stats`, `quantification` | none (pipeline not executed) | synthetic demo |

To force a clean re-seed:

```powershell
python -c "from app.seed.load import init_db; init_db(force=True)"
```

### Migrations

```powershell
# from backend/
python -m alembic revision --autogenerate -m "<message>"
python -m alembic upgrade head
```

Note: the app also calls `Base.metadata.create_all` on import for a
zero-config first run. Alembic is the migration source of truth for schema
evolution; both are idempotent and coexist.

## Provenance rule (locked)

The project-level `isMock` flag remains `true` because the full pipeline has
not been executed against the raw reads; only the metadata/QC/DESeq2/pathway
artifacts that genuinely exist on disk are served as source-derived, while
alignment and quantification stay synthetic-demo. Nothing is presented as
experimental output that the pipeline did not actually produce.

## Endpoints

All prefixed with `/api/v1`:

- `GET /health`
- `GET /projects`, `GET /projects/{id}`
- `GET /samples`, `GET /samples/cohorts`
- `GET /qc/metrics`, `GET /qc/multiqc`
- `GET /alignment`, `GET /quantification`
- `GET /stages`
- `GET /de/results`, `GET /de/visual`
- `GET /pathways`

CORS allows the Vite dev server (`http://localhost:5173`).
