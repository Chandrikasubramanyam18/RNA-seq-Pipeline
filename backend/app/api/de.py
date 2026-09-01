from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.de import DeAxisModel, DeResultModel, PcaPointModel
from app.schemas.models import DeResult, DeVisualData
from app.seed.load import synthetic_de_seeds

router = APIRouter(prefix="/de", tags=["differential-expression"])


def _de_to_schema(d: DeResultModel) -> DeResult:
    return DeResult(
        geneId=d.gene_id,
        symbol=d.symbol,
        baseMean=d.base_mean,
        log2FoldChange=d.log2_fold_change,
        lfcSE=d.lfc_se,
        pvalue=d.pvalue,
        padj=d.padj,
        significant=d.significant,
        dataSource=d.data_source,
    )


@router.get("/results", response_model=list[DeResult])
def list_de_results(db: Session = Depends(get_db)) -> list[DeResult]:
    """All DE results: real source_derived genes from deseq2_results.csv plus
    synthetic_demo background used to demonstrate the charts."""
    rows = db.scalars(select(DeResultModel)).all()
    demo = synthetic_de_seeds()["volcano"]
    return [_de_to_schema(r) for r in rows] + [DeResult(**d) for d in demo]


@router.get("/visual", response_model=DeVisualData)
def de_visual_data(db: Session = Depends(get_db)) -> DeVisualData:
    de_rows = db.scalars(select(DeResultModel)).all()
    pca_rows = db.scalars(select(PcaPointModel)).all()
    axes = db.scalar(select(DeAxisModel).limit(1))

    source = [_de_to_schema(r) for r in de_rows]
    seeds = synthetic_de_seeds()

    from app.schemas.models import PcaAxisInfo, PcaPoint

    return DeVisualData(
        pca=[
            PcaPoint(
                sampleId=p.sample_id,
                pc1=p.pc1,
                pc2=p.pc2,
                condition=p.condition,
            )
            for p in pca_rows
        ],
        pcaAxis1=PcaAxisInfo(label=axes.axis1_label, varianceExplained=axes.axis1_var),
        pcaAxis2=PcaAxisInfo(label=axes.axis2_label, varianceExplained=axes.axis2_var),
        volcano=source + [DeResult(**d) for d in seeds["volcano"]],
        ma=source + [DeResult(**d) for d in seeds["ma"]],
        sourceDerived=source,
    )

