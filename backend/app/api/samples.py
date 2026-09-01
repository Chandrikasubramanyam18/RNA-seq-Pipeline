from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.sample import SampleModel
from app.schemas.models import Cohort, Sample

router = APIRouter(prefix="/samples", tags=["samples"])


@router.get("", response_model=list[Sample])
def list_samples(db: Session = Depends(get_db)) -> list[Sample]:
    rows = db.scalars(select(SampleModel))
    return [
        Sample(
            id=s.id,
            runId=s.run_id,
            gsmId=s.gsm_id,
            donor=s.donor,
            replicate=s.replicate,
            condition=s.condition,
            fastq1=s.fastq1,
            fastq2=s.fastq2,
        )
        for s in rows
    ]


@router.get("/cohorts", response_model=list[Cohort])
def list_cohorts(db: Session = Depends(get_db)) -> list[Cohort]:
    rows = db.scalars(select(SampleModel)).all()
    control = [s.id for s in rows if s.condition == "control"]
    treatment = [s.id for s in rows if s.condition == "treatment"]
    return [
        Cohort(condition="control", label="Control", sampleIds=control),
        Cohort(condition="treatment", label="Dexamethasone", sampleIds=treatment),
    ]

