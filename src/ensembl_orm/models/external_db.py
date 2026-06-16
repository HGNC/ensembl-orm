from sqlalchemy import Enum as SAEnum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db_common import DeclarativeBase
from ensembl_orm import enums


class ExternalDb(DeclarativeBase):
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

    external_db_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    db_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[enums.ExternalDbStatus | None] = mapped_column(SAEnum(enums.ExternalDbStatus))
    priority: Mapped[int] = mapped_column(Integer)
    dbprimary_acc_link: Mapped[str | None] = mapped_column(String(255))
    display_name_link: Mapped[str | None] = mapped_column(String(255))
    db_display_name: Mapped[str | None] = mapped_column(String(255))
    type: Mapped[enums.ExternalDbType | None] = mapped_column(SAEnum(enums.ExternalDbType))
    secondary_db_name: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    release: Mapped[str | None] = mapped_column(String(255))
