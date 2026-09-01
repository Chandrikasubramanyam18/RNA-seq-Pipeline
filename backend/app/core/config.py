from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Repository root (backend/ -> repo).
REPO_ROOT = Path(__file__).resolve().parents[3]
BACKEND_DIR = REPO_ROOT / "backend"
RESULTS_DIR = REPO_ROOT / "results"
METADATA_DIR = REPO_ROOT / "metadata"


class Settings(BaseSettings):
    """Runtime settings for the API, overridable via env vars / .env.

    The SQLite database defaults to ``backend/data/rna_seq.db`` (git-ignored).
    """

    app_name: str = "RNA-seq Analysis Platform API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"

    # SQLite DSN. Use "sqlite:///./backend/data/rna_seq.db" relative or absolute.
    database_url: str = f"sqlite:///{(BACKEND_DIR / 'data' / 'rna_seq.db').as_posix()}"

    # CORS origins for the Vite dev server and any local build preview.
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # Seed source paths (the repository artifacts that ground the data).
    samplesheet_path: Path = METADATA_DIR / "samplesheet.csv"
    dataset_manifest_path: Path = METADATA_DIR / "dataset_manifest.yaml"
    reference_manifest_path: Path = METADATA_DIR / "reference_manifest.yaml"
    fastqc_summary_path: Path = RESULTS_DIR / "fastqc" / "raw" / "fastqc_summary.tsv"
    fastp_summary_path: Path = RESULTS_DIR / "fastp" / "fastp_summary.tsv"
    deseq2_results_path: Path = RESULTS_DIR / "differential_expression" / "deseq2_results.csv"
    pathway_results_path: Path = RESULTS_DIR / "pathway_analysis" / "pathway_enrichment_results.csv"

    model_config = SettingsConfigDict(
        env_prefix="RNAQ_",
        env_file=BACKEND_DIR / ".env",
        extra="ignore",
    )


settings = Settings()
