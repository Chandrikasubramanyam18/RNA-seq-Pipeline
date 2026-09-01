from __future__ import annotations

from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PathwayEnrichmentModel(Base):
    __tablename__ = "pathway_enrichment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    term_id: Mapped[str] = mapped_column(String)  # e.g. "GO:0071356"
    source: Mapped[str] = mapped_column(String)  # GO | KEGG | ...
    term: Mapped[str] = mapped_column(Text)
    gene_ratio: Mapped[float | None] = mapped_column(Float, nullable=True)
    pvalue: Mapped[float] = mapped_column(Float)
    padj: Mapped[float] = mapped_column(Float)
    genes: Mapped[str] = mapped_column(Text)  # comma-separated symbols
    data_source: Mapped[str] = mapped_column(String)
