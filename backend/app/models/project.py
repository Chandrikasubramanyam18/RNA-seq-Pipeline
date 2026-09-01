"""ORM models for the RNA-seq platform.

The schema is denormalised for simple read-only serving: each table maps to a
single response resource. FK references use the project accession as a stable
natural key.
"""

from __future__ import annotations

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ProjectModel(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # e.g. "gse52778"
    accession: Mapped[str] = mapped_column(String, unique=True, index=True)

    bioproject: Mapped[str] = mapped_column(String)
    sra_study: Mapped[str] = mapped_column(String)
    organism: Mapped[str] = mapped_column(String)
    taxonomy_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(Text)
    publication: Mapped[str] = mapped_column(String)
    platform: Mapped[str] = mapped_column(String)
    library_strategy: Mapped[str] = mapped_column(String)
    library_selection: Mapped[str] = mapped_column(String)
    library_layout: Mapped[str] = mapped_column(String)
    read_length: Mapped[int] = mapped_column(Integer)
    reference_genome: Mapped[str] = mapped_column(String)
    annotation_source: Mapped[str] = mapped_column(String)
    source: Mapped[str] = mapped_column(String)
    download_date: Mapped[str | None] = mapped_column(String, nullable=True)

    name: Mapped[str] = mapped_column(String)
    design_description: Mapped[str] = mapped_column(Text)
    is_mock: Mapped[bool] = mapped_column(Boolean, default=True)

    genome_assembly: Mapped[str] = mapped_column(String)
    reference_release: Mapped[str] = mapped_column(String)
    sjdb_overhang: Mapped[int] = mapped_column(Integer)
    genome_sa_index_nbases: Mapped[int] = mapped_column(Integer)
    salmon_kmer_length: Mapped[int] = mapped_column(Integer)
    genome_fasta: Mapped[str] = mapped_column(String)
    annotation_gtf: Mapped[str] = mapped_column(String)
    transcriptome_fasta: Mapped[str] = mapped_column(String)
