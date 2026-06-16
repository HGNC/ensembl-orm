from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db_common import DeclarativeBase


class SeqRegion(DeclarativeBase):
    """Represent a seq_region row from the Ensembl database.

    Attributes:
        seq_region_id: Unique identifier for the sequence region.
        name: Name of the sequence region (e.g., chromosome name).
        coord_system_id: Foreign key to the coordinate system.
        length: Length of the sequence region in base pairs.
    """

    __tablename__ = "seq_region"

    seq_region_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    coord_system_id: Mapped[int] = mapped_column(Integer)
    length: Mapped[int] = mapped_column(Integer)
