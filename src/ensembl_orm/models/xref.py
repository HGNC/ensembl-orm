from sqlalchemy import Column, Enum as SAEnum, ForeignKey, Integer, String, Text
from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from ensembl_orm import enums
from ensembl_orm.models.external_db import ExternalDb


class Xref(SQLModel, table=True):
    """Represent an xref row in the Ensembl schema.

    Attributes:
        xref_id: Primary key.
        external_db_id: Foreign key to external_db.external_db_id.
        dbprimary_acc: Primary accession identifier.
        display_label: User-facing label for the cross-reference.
        version: Version string for the reference.
        description: Free-text description of the reference.
        info_type: Information type classification.
        info_text: Additional information text.
        external_db: Related external database row.
    """

    __tablename__ = "xref"

    xref_id: int | None = Field(default=None, sa_column=Column(Integer, primary_key=True))
    external_db_id: int = Field(
        sa_column=Column(Integer, ForeignKey("external_db.external_db_id"), nullable=False),
    )
    dbprimary_acc: str | None = Field(default=None, sa_column=Column(String(255), nullable=True))
    display_label: str | None = Field(default=None, sa_column=Column(String(255), nullable=True))
    version: str | None = Field(default=None, sa_column=Column(String(255), nullable=True))
    description: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
    info_type: enums.InfoType | None = Field(default=None, sa_column=Column(SAEnum(enums.InfoType), nullable=True))
    info_text: str | None = Field(default=None, sa_column=Column(String(255), nullable=True))

    external_db: ExternalDb | None = Relationship()

    @field_validator("info_type", mode="before")
    @classmethod
    def _validate_info_type(cls, value: enums.InfoType | str | None) -> enums.InfoType | None:
        """Validate info_type against InfoType enum values."""
        if value is None or isinstance(value, enums.InfoType):
            return value
        return enums.InfoType(value)
