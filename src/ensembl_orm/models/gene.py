from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlmodel import Field, Relationship, SQLModel

from ensembl_orm.models.seq_region import SeqRegion


class Gene(SQLModel, table=True):
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

    gene_id: int | None = Field(default=None, sa_column=Column(Integer, primary_key=True))
    biotype: str = Field(sa_column=Column(String(255), nullable=False))
    analysis_id: int = Field(sa_column=Column(Integer, nullable=False))
    seq_region_id: int = Field(
        sa_column=Column(Integer, ForeignKey("seq_region.seq_region_id"), nullable=False),
    )
    seq_region_start: int = Field(sa_column=Column(Integer, nullable=False))
    seq_region_end: int = Field(sa_column=Column(Integer, nullable=False))
    seq_region_strand: int = Field(sa_column=Column(Integer, nullable=False))
    display_xref_id: int | None = Field(default=None, sa_column=Column(Integer, nullable=True))
    source: str = Field(sa_column=Column(String(255), nullable=False))
    description: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
    is_current: bool = Field(sa_column=Column(Boolean, nullable=False))
    canonical_transcript_id: int | None = Field(
        default=None, sa_column=Column(Integer, nullable=True)
    )
    canonical_translation_id: int | None = Field(
        default=None, sa_column=Column(Integer, nullable=True)
    )
    stable_id: str | None = Field(default=None, sa_column=Column(String(128), nullable=True))
    version: int | None = Field(default=None, sa_column=Column(Integer, nullable=True))
    created_date: datetime | None = Field(default=None, sa_column=Column(DateTime, nullable=True))
    modified_date: datetime | None = Field(default=None, sa_column=Column(DateTime, nullable=True))

    seq_region: SeqRegion | None = Relationship()
