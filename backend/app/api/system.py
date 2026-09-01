from fastapi import APIRouter

from app.schemas.models import Health

router = APIRouter(tags=["system"])


@router.get("/health", response_model=Health)
def health() -> Health:
    return Health(status="ok", app="rna-seq-platform-api", version="0.1.0")
