from sqlalchemy import Enum as SAEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_common import DeclarativeBase
from ensembl_orm import enums
from ensembl_orm.models.xref import Xref


class ObjectXref(DeclarativeBase):
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

    object_xref_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    xref_id: Mapped[int] = mapped_column(Integer, ForeignKey("xref.xref_id"))
    ensembl_id: Mapped[int] = mapped_column(Integer)
    ensembl_object_type: Mapped[enums.EnsemblObjectType] = mapped_column(SAEnum(enums.EnsemblObjectType))
    linkage_annotation: Mapped[str | None] = mapped_column(String(255))
    analysis_id: Mapped[int | None] = mapped_column(Integer)
    linkage_type: Mapped[enums.InfoType | None] = mapped_column(SAEnum(enums.InfoType))

    xref: Mapped[Xref | None] = relationship()
