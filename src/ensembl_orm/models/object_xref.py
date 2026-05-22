from sqlalchemy import Column, Enum as SAEnum, ForeignKey, Integer, String
from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from ensembl_orm import enums
from ensembl_orm.models.xref import Xref


class ObjectXref(SQLModel, table=True):
    """Represent an object_xref row in the Ensembl schema.

    Attributes:
        object_xref_id: Primary key.
        xref_id: Foreign key to xref.xref_id.
        ensembl_id: Identifier of the related Ensembl object.
        ensembl_object_type: Type of related Ensembl object.
        linkage_annotation: Annotation text describing linkage evidence.
        analysis_id: Related analysis identifier.
        linkage_type: Linkage type classification.
        xref: Related xref row.
    """

    __tablename__ = "object_xref"

    object_xref_id: int | None = Field(default=None, sa_column=Column(Integer, primary_key=True))
    xref_id: int = Field(sa_column=Column(Integer, ForeignKey("xref.xref_id"), nullable=False))
    ensembl_id: int = Field(sa_column=Column(Integer, nullable=False))
    ensembl_object_type: enums.EnsemblObjectType = Field(
        sa_column=Column(SAEnum(enums.EnsemblObjectType), nullable=False),
    )
    linkage_annotation: str | None = Field(default=None, sa_column=Column(String(255), nullable=True))
    analysis_id: int | None = Field(default=None, sa_column=Column(Integer, nullable=True))
    linkage_type: enums.InfoType | None = Field(default=None, sa_column=Column(SAEnum(enums.InfoType), nullable=True))

    xref: Xref | None = Relationship()

    @field_validator("ensembl_object_type", mode="before")
    @classmethod
    def _validate_ensembl_object_type(
        cls,
        value: enums.EnsemblObjectType | str,
    ) -> enums.EnsemblObjectType:
        """Validate ensembl_object_type against EnsemblObjectType enum values."""
        if isinstance(value, enums.EnsemblObjectType):
            return value
        return enums.EnsemblObjectType(value)

    @field_validator("linkage_type", mode="before")
    @classmethod
    def _validate_linkage_type(cls, value: enums.InfoType | str | None) -> enums.InfoType | None:
        """Validate linkage_type against InfoType enum values."""
        if value is None or isinstance(value, enums.InfoType):
            return value
        return enums.InfoType(value)
