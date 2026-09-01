from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.alignment import AlignmentStatsModel, QuantificationModel
from app.schemas.models import AlignmentStats, Quantification

router = APIRouter(tags=["expression"])


@router.get("/alignment", response_model=list[AlignmentStats])
def list_alignment(db: Session = Depends(get_db)) -> list[AlignmentStats]:
    rows = db.scalars(select(AlignmentStatsModel)).all()
    return [
        AlignmentStats(
            sampleId=a.sample_id,
            totalReads=a.total_reads,
            uniquelyMappedPct=a.uniquely_mapped_pct,
            multiMappedPct=a.multi_mapped_pct,
            unmappedPct=a.unmapped_pct,
            properlyPairedPct=a.properly_paired_pct,
        )
        for a in rows
    ]


@router.get("/quantification", response_model=list[Quantification])
def list_quantification(db: Session = Depends(get_db)) -> list[Quantification]:
    rows = db.scalars(select(QuantificationModel)).all()
    return [
        Quantification(
            sampleId=q.sample_id,
            method=q.method,
            geneId=q.gene_id,
            symbol=q.symbol,
            tpm=q.tpm,
            counts=q.counts,
            length=q.length,
        )
        for q in rows
    ]

