from sqlalchemy import Column, ForeignKey, Integer, String
from sqlmodel import Field, Relationship, SQLModel

from ensembl_orm.models.seq_region import SeqRegion


class Karyotype(SQLModel, table=True):
    """Represent a karyotype row from the Ensembl database.

    Attributes:
        karyotype_id: Primary key.
        seq_region_id: Foreign key to seq_region.seq_region_id.
        seq_region_start: Start coordinate on the sequence region.
        seq_region_end: End coordinate on the sequence region.
        band: Cytogenetic band name.
        stain: Staining classification label.
        seq_region: Related sequence region row.
    """

    __tablename__ = "karyotype"

    karyotype_id: int | None = Field(default=None, sa_column=Column(Integer, primary_key=True))
    seq_region_id: int = Field(
        sa_column=Column(Integer, ForeignKey("seq_region.seq_region_id"), nullable=False),
    )
    seq_region_start: int = Field(sa_column=Column(Integer, nullable=False))
    seq_region_end: int = Field(sa_column=Column(Integer, nullable=False))
    band: str | None = Field(default=None, sa_column=Column(String(255), nullable=True))
    stain: str | None = Field(default=None, sa_column=Column(String(255), nullable=True))

    seq_region: SeqRegion | None = Relationship()
