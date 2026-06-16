from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_common import DeclarativeBase
from ensembl_orm.models.seq_region import SeqRegion


class Gene(DeclarativeBase):
    """Represent a gene row from the Ensembl database.

    Attributes:
        gene_id: Primary key.
        biotype: Biotype classification (e.g., protein_coding).
        analysis_id: Foreign key to the analysis table.
        seq_region_id: Foreign key to seq_region.
        seq_region_start: Start position on the sequence region.
        seq_region_end: End position on the sequence region.
        seq_region_strand: Strand orientation (1 or -1).
        display_xref_id: Foreign key to the xref table for display name.
        source: Source of the gene annotation.
        description: Human-readable gene description.
        is_current: Whether this is the current version of the gene.
        canonical_transcript_id: Foreign key to the canonical transcript.
        canonical_translation_id: Foreign key to the canonical translation.
        stable_id: Stable identifier (e.g., ENSG00000139618).
        version: Version number of the stable ID.
        created_date: Timestamp when the record was created.
        modified_date: Timestamp when the record was last modified.
    """

    __tablename__ = "gene"

    gene_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    biotype: Mapped[str] = mapped_column(String(255))
    analysis_id: Mapped[int] = mapped_column(Integer)
    seq_region_id: Mapped[int] = mapped_column(Integer, ForeignKey("seq_region.seq_region_id"))
    seq_region_start: Mapped[int] = mapped_column(Integer)
    seq_region_end: Mapped[int] = mapped_column(Integer)
    seq_region_strand: Mapped[int] = mapped_column(Integer)
    display_xref_id: Mapped[int | None] = mapped_column(Integer)
    source: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    is_current: Mapped[bool] = mapped_column(Boolean)
    canonical_transcript_id: Mapped[int | None] = mapped_column(Integer)
    canonical_translation_id: Mapped[int | None] = mapped_column(Integer)
    stable_id: Mapped[str | None] = mapped_column(String(128))
    version: Mapped[int | None] = mapped_column(Integer)
    created_date: Mapped[datetime | None] = mapped_column(DateTime)
    modified_date: Mapped[datetime | None] = mapped_column(DateTime)

    seq_region: Mapped[SeqRegion | None] = relationship()
