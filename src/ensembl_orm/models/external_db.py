from sqlalchemy import Column, Enum as SAEnum, Integer, String, Text
from pydantic import field_validator
from sqlmodel import Field, SQLModel

from ensembl_orm import enums


class ExternalDb(SQLModel, table=True):
    """Represent an external_db row in the Ensembl schema.

    Attributes:
        external_db_id: Primary key.
        db_name: Name of the external database.
        status: Status of the external database mapping.
        priority: Ordering priority for the external database.
        dbprimary_acc_link: URL pattern for primary accession links.
        display_name_link: URL pattern for display-name links.
        db_display_name: Display name used for the external database.
        type: Classification type for the external database.
        secondary_db_name: Secondary external database name.
        description: Free-text description.
        release: Release label or version string.
    """

    __tablename__ = "external_db"

    external_db_id: int | None = Field(default=None, sa_column=Column(Integer, primary_key=True))
    db_name: str = Field(sa_column=Column(String(255), nullable=False))
    status: enums.ExternalDbStatus | None = Field(
        default=None,
        sa_column=Column(SAEnum(enums.ExternalDbStatus), nullable=True),
    )
    priority: int = Field(sa_column=Column(Integer, nullable=False))
    dbprimary_acc_link: str | None = Field(default=None, sa_column=Column(String(255), nullable=True))
    display_name_link: str | None = Field(default=None, sa_column=Column(String(255), nullable=True))
    db_display_name: str | None = Field(default=None, sa_column=Column(String(255), nullable=True))
    type: enums.ExternalDbType | None = Field(
        default=None,
        sa_column=Column(SAEnum(enums.ExternalDbType), nullable=True),
    )
    secondary_db_name: str | None = Field(default=None, sa_column=Column(String(255), nullable=True))
    description: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
    release: str | None = Field(default=None, sa_column=Column(String(255), nullable=True))

    @field_validator("status", mode="before")
    @classmethod
    def _validate_status(cls, value: enums.ExternalDbStatus | str | None) -> enums.ExternalDbStatus | None:
        """Validate status against ExternalDbStatus enum values."""
        if value is None or isinstance(value, enums.ExternalDbStatus):
            return value
        return enums.ExternalDbStatus(value)

    @field_validator("type", mode="before")
    @classmethod
    def _validate_type(cls, value: enums.ExternalDbType | str | None) -> enums.ExternalDbType | None:
        """Validate type against ExternalDbType enum values."""
        if value is None or isinstance(value, enums.ExternalDbType):
            return value
        return enums.ExternalDbType(value)
