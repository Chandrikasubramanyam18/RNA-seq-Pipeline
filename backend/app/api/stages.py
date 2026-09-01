from pathlib import Path

from fastapi import APIRouter

from app.core.config import RESULTS_DIR, settings
from app.schemas.models import RunStage

router = APIRouter(prefix="/stages", tags=["pipeline"])

# Stage statuses are derived from whether genuine result artifacts exist on
# disk (source of truth). deseq2_results.csv exists, so that stage is 'done';
# alignment/salmon/counts outputs are not present, so they remain 'pending'
# and can never be mistaken for real results.
_STAGE_DEFS = [
    ("metadata", "Metadata", settings.samplesheet_path, "Samplesheet validated (6 samples, 2 conditions)"),
    ("raw_qc", "Raw QC", settings.fastqc_summary_path, "FastQC output present"),
    ("preprocessing", "Preprocessing", settings.fastp_summary_path, "fastp trimming summary present"),
    ("alignment", "Alignment", RESULTS_DIR / "alignment" / "Log.final.out", "STAR alignment - not executed"),
    ("quantification", "Quantification", RESULTS_DIR / "salmon" / "quant.sf", "Salmon / featureCounts - not executed"),
    ("deseq2", "DESeq2", settings.deseq2_results_path, "DESeq2 results table present"),
]


def _exists(path: Path) -> bool:
    return path.exists()


@router.get("", response_model=list[RunStage])
def list_stages() -> list[RunStage]:
    out = []
    for key, label, path, detail in _STAGE_DEFS:
        done = _exists(path)
        status = "done" if done else "pending"
        note = detail if done else f"{label} - not executed"
        out.append(RunStage(key=key, label=label, status=status, detail=note))
    return out
