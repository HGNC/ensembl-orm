from sqlalchemy import Enum as SAEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_common import DeclarativeBase
from ensembl_orm import enums
from ensembl_orm.models.external_db import ExternalDb


class Xref(DeclarativeBase):
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

    xref_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_db_id: Mapped[int] = mapped_column(Integer, ForeignKey("external_db.external_db_id"))
    dbprimary_acc: Mapped[str | None] = mapped_column(String(255))
    display_label: Mapped[str | None] = mapped_column(String(255))
    version: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    info_type: Mapped[enums.InfoType | None] = mapped_column(SAEnum(enums.InfoType))
    info_text: Mapped[str | None] = mapped_column(String(255))

    external_db: Mapped[ExternalDb | None] = relationship()
