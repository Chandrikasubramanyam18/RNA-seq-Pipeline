from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.pathway import PathwayEnrichmentModel
from app.schemas.models import PathwayEnrichment

router = APIRouter(prefix="/pathways", tags=["pathways"])


@router.get("", response_model=list[PathwayEnrichment])
def list_pathways(db: Session = Depends(get_db)) -> list[PathwayEnrichment]:
    rows = (
        db.scalars(select(PathwayEnrichmentModel).order_by(PathwayEnrichmentModel.padj))
        .all()
    )
    return [
        PathwayEnrichment(
            id=p.term_id,
            source=p.source,
            term=p.term,
            geneRatio=p.gene_ratio,
            pvalue=p.pvalue,
            padj=p.padj,
            genes=p.genes.split(";") if p.genes else [],
            dataSource=p.data_source,
        )
        for p in rows
    ]
