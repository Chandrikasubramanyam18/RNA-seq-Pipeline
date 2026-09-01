from __future__ import annotations

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DeResultModel(Base):
    __tablename__ = "de_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    gene_id: Mapped[str] = mapped_column(String)
    symbol: Mapped[str | None] = mapped_column(String, nullable=True)
    base_mean: Mapped[float] = mapped_column(Float)
    log2_fold_change: Mapped[float] = mapped_column(Float)
    lfc_se: Mapped[float | None] = mapped_column(Float, nullable=True)
    pvalue: Mapped[float] = mapped_column(Float)
    padj: Mapped[float] = mapped_column(Float)
    significant: Mapped[bool] = mapped_column(Boolean)
    data_source: Mapped[str] = mapped_column(String)  # source_derived | synthetic_demo


class PcaPointModel(Base):
    __tablename__ = "pca_points"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sample_id: Mapped[str] = mapped_column(String)
    pc1: Mapped[float] = mapped_column(Float)
    pc2: Mapped[float] = mapped_column(Float)
    condition: Mapped[str] = mapped_column(String)


class DeAxisModel(Base):
    """PC variance-explained labels (single row)."""

    __tablename__ = "de_axes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    axis1_label: Mapped[str] = mapped_column(String)
    axis1_var: Mapped[float] = mapped_column(Float)
    axis2_label: Mapped[str] = mapped_column(String)
    axis2_var: Mapped[float] = mapped_column(Float)
