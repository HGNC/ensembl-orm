from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_common import DeclarativeBase
from ensembl_orm.models.seq_region import SeqRegion


class Karyotype(DeclarativeBase):
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

    karyotype_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    seq_region_id: Mapped[int] = mapped_column(Integer, ForeignKey("seq_region.seq_region_id"))
    seq_region_start: Mapped[int] = mapped_column(Integer)
    seq_region_end: Mapped[int] = mapped_column(Integer)
    band: Mapped[str | None] = mapped_column(String(255))
    stain: Mapped[str | None] = mapped_column(String(255))

    seq_region: Mapped[SeqRegion | None] = relationship()
