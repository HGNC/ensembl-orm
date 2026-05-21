from sqlalchemy import Column, Integer, String
from sqlmodel import Field, SQLModel


class SeqRegion(SQLModel, table=True):
    """Represent a seq_region row from the Ensembl database.

    Attributes:
        seq_region_id: Unique identifier for the sequence region.
        name: Name of the sequence region (e.g., chromosome name).
        coord_system_id: Foreign key to the coordinate system.
        length: Length of the sequence region in base pairs.
    """

    __tablename__ = "seq_region"

    seq_region_id: int | None = Field(default=None, sa_column=Column(Integer, primary_key=True))
    name: str = Field(sa_column=Column(String(255), nullable=False))
    coord_system_id: int = Field(sa_column=Column(Integer, nullable=False))
    length: int = Field(sa_column=Column(Integer, nullable=False))
