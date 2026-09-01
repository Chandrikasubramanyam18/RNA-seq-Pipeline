from __future__ import annotations

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AlignmentStatsModel(Base):
    __tablename__ = "alignment_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sample_id: Mapped[str] = mapped_column(ForeignKey("samples.id"), unique=True)
    total_reads: Mapped[int] = mapped_column(Integer)
    uniquely_mapped_pct: Mapped[float] = mapped_column(Float)
    multi_mapped_pct: Mapped[float] = mapped_column(Float)
    unmapped_pct: Mapped[float] = mapped_column(Float)
    properly_paired_pct: Mapped[float] = mapped_column(Float)


class QuantificationModel(Base):
    __tablename__ = "quantification"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sample_id: Mapped[str] = mapped_column(ForeignKey("samples.id"), index=True)
    method: Mapped[str] = mapped_column(String)
    gene_id: Mapped[str] = mapped_column(String)
    symbol: Mapped[str | None] = mapped_column(String, nullable=True)
    tpm: Mapped[float | None] = mapped_column(Float, nullable=True)
    counts: Mapped[int | None] = mapped_column(Integer, nullable=True)
    length: Mapped[int | None] = mapped_column(Integer, nullable=True)
