from sqlalchemy import Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from db_common import DeclarativeBase


class SeqRegionAttrib(DeclarativeBase):
    """Represent a seq_region_attrib row from the Ensembl database.

    Attributes:
        seq_region_id: Identifier of the related sequence region.
        attrib_type_id: Identifier of the attribute type.
        value: Attribute value associated with the sequence region.
    """

    __tablename__ = "seq_region_attrib"
    __table_args__ = (PrimaryKeyConstraint("seq_region_id", "attrib_type_id"),)

    seq_region_id: Mapped[int] = mapped_column(Integer)
    attrib_type_id: Mapped[int] = mapped_column(Integer)
    value: Mapped[str | None] = mapped_column(String(255))
