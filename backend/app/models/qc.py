from __future__ import annotations

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class QcMetricModel(Base):
    __tablename__ = "qc_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sample_id: Mapped[str] = mapped_column(
        ForeignKey("samples.id"), unique=True, index=True
    )
    total_reads: Mapped[int] = mapped_column(Integer)
    gc_percent: Mapped[float] = mapped_column(Float)
    q20_rate: Mapped[float] = mapped_column(Float)
    q30_rate: Mapped[float] = mapped_column(Float)
    adapter_content_pct: Mapped[float] = mapped_column(Float)
    duplication_pct: Mapped[float] = mapped_column(Float)
    retention_pct: Mapped[float] = mapped_column(Float)

    per_base: Mapped[list["PerBaseQualityModel"]] = relationship(
        back_populates="qc", cascade="all, delete-orphan", order_by="PerBaseQualityModel.position"
    )


class PerBaseQualityModel(Base):
    __tablename__ = "per_base_quality"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    qc_id: Mapped[int] = mapped_column(ForeignKey("qc_metrics.id"), index=True)
    position: Mapped[int] = mapped_column(Integer)
    mean_q: Mapped[float] = mapped_column(Float)

    qc: Mapped[QcMetricModel] = relationship(back_populates="per_base")


class MultiQcSummaryModel(Base):
    __tablename__ = "multiqc_summary"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sample_id: Mapped[str] = mapped_column(ForeignKey("samples.id"), unique=True)
    pct_dups: Mapped[float] = mapped_column(Float)
    pct_gc: Mapped[float] = mapped_column(Float)
    mil_seqs: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String)  # PASS | WARN | FAIL
