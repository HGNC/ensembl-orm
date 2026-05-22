from sqlalchemy import Column, Integer, PrimaryKeyConstraint, String
from sqlmodel import Field, SQLModel


class SeqRegionAttrib(SQLModel, table=True):
    """Represent a seq_region_attrib row from the Ensembl database.

    Attributes:
        seq_region_id: Identifier of the related sequence region.
        attrib_type_id: Identifier of the attribute type.
        value: Attribute value associated with the sequence region.
    """

    __tablename__ = "seq_region_attrib"
    __table_args__ = (PrimaryKeyConstraint("seq_region_id", "attrib_type_id"),)

    seq_region_id: int = Field(sa_column=Column(Integer, nullable=False))
    attrib_type_id: int = Field(sa_column=Column(Integer, nullable=False))
    value: str | None = Field(default=None, sa_column=Column(String(255), nullable=True))
