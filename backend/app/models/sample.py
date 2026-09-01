from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SampleModel(Base):
    __tablename__ = "samples"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    run_id: Mapped[str] = mapped_column(String)
    gsm_id: Mapped[str | None] = mapped_column(String, nullable=True)
    donor: Mapped[str] = mapped_column(String)
    replicate: Mapped[int] = mapped_column(Integer)
    condition: Mapped[str] = mapped_column(String)
    fastq1: Mapped[str] = mapped_column(Text)
    fastq2: Mapped[str] = mapped_column(Text)
