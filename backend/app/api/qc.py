from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.models.qc import MultiQcSummaryModel, QcMetricModel
from app.schemas.models import MultiQcSummary, QcMetric

router = APIRouter(prefix="/qc", tags=["qc"])


@router.get("/metrics", response_model=list[QcMetric])
def list_qc_metrics(db: Session = Depends(get_db)) -> list[QcMetric]:
    rows = (
        db.scalars(select(QcMetricModel).options(selectinload(QcMetricModel.per_base)))
        .unique()
        .all()
    )
    return [
        QcMetric(
            sampleId=q.sample_id,
            totalReads=q.total_reads,
            gcPercent=q.gc_percent,
            q20Rate=q.q20_rate,
            q30Rate=q.q30_rate,
            adapterContentPct=q.adapter_content_pct,
            duplicationPct=q.duplication_pct,
            retentionPct=q.retention_pct,
            perBaseQuality=[
                {"position": pb.position, "meanQ": pb.mean_q} for pb in q.per_base
            ],
        )
        for q in rows
    ]


@router.get("/multiqc", response_model=list[MultiQcSummary])
def list_multiqc(db: Session = Depends(get_db)) -> list[MultiQcSummary]:
    rows = db.scalars(select(MultiQcSummaryModel)).all()
    return [
        MultiQcSummary(
            sampleId=m.sample_id,
            pctDups=m.pct_dups,
            pctGC=m.pct_gc,
            milSeqs=m.mil_seqs,
            status=m.status,
        )
        for m in rows
    ]

