"""Create tables and load seed data into the database."""

from __future__ import annotations

import random

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import Base, engine
from app.models.alignment import AlignmentStatsModel, QuantificationModel
from app.models.de import DeAxisModel, DeResultModel, PcaPointModel
from app.models.pathway import PathwayEnrichmentModel
from app.models.project import ProjectModel
from app.models.qc import MultiQcSummaryModel, PerBaseQualityModel, QcMetricModel
from app.models.sample import SampleModel
from app.seed import seed_data


def _rng(seed: int):
    return random.Random(seed)


def _synthetic_de(count: int, seed: int) -> list[dict]:
    r = _rng(seed)
    rows = []
    for i in range(count):
        log2fc = (r.random() - 0.5) * 4
        base_mean = round(50 + r.random() * 8000)
        if r.random() < 0.06:
            padj = 10 ** (-(3 + r.random() * 10))
        else:
            padj = 0.1 + r.random() * 0.9
        significant = padj < 0.05 and abs(log2fc) >= 1
        rows.append(
            {
                "geneId": f"DEMO{i}",
                "symbol": None,
                "baseMean": base_mean,
                "log2FoldChange": round(log2fc, 2),
                "lfcSE": None,
                "pvalue": min(1.0, padj * (0.5 + r.random())),
                "padj": min(1.0, padj),
                "significant": significant,
                "dataSource": "synthetic_demo",
            }
        )
    return rows


def init_db(force: bool = False) -> None:
    """Create tables and seed them if empty (or force re-seed)."""
    if force:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        exists = db.scalars(select(ProjectModel).limit(1)).first()
        if exists and not force:
            return
        _seed(db)
        db.commit()


def _seed(db: Session) -> None:
    project_fields = seed_data.build_project_fields()
    db.add(ProjectModel(**project_fields))

    samples = seed_data.build_sample_fields()
    db.add_all(SampleModel(**s) for s in samples)

    qc_rows = seed_data.build_qc_fields()
    for q in qc_rows:
        per_base = q.pop("per_base")
        gc_model = QcMetricModel(**q)
        gc_model.per_base = [PerBaseQualityModel(**pb) for pb in per_base]
        db.add(gc_model)

    multiqc = seed_data.build_multiqc_fields(qc_rows)
    db.add_all(MultiQcSummaryModel(**m) for m in multiqc)

    alignment = seed_data.build_alignment_fields(samples)
    db.add_all(AlignmentStatsModel(**a) for a in alignment)

    quant = seed_data.build_quantification_fields()
    db.add_all(QuantificationModel(**q) for q in quant)

    de = seed_data.build_de_fields()
    db.add_all(DeResultModel(**d) for d in de)

    pca = seed_data.build_pca_points(samples)
    db.add_all(PcaPointModel(**p) for p in pca)

    axes = seed_data.build_de_axes()
    db.add(DeAxisModel(**axes))

    pathways = seed_data.build_pathway_fields()
    db.add_all(PathwayEnrichmentModel(**p) for p in pathways)


def synthetic_de_seeds() -> dict[str, list[dict]]:
    """Synthetic background for volcano/MA demonstration (never in DB)."""
    return {
        "volcano": _synthetic_de(280, 42),
        "ma": _synthetic_de(280, 1337),
    }
