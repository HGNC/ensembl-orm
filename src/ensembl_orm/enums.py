"""Enum definitions mapping to MySQL ENUM columns in the Ensembl database."""

from enum import StrEnum, unique


@unique
class EnsemblObjectType(StrEnum):
    """Represent object types for the object_xref.ensembl_object_type column.

    Attributes:
        GENE: Represent a gene object type.
        TRANSCRIPT: Represent a transcript object type.
        TRANSLATION: Represent a translation object type.
    """

    GENE = "Gene"
    TRANSCRIPT = "Transcript"
    TRANSLATION = "Translation"


@unique
class ExternalDbStatus(StrEnum):
    """Represent status values for the external_db.status column.

    Attributes:
        KNOWN: Represent a known external database status.
        XREF: Represent a cross-reference external database status.
        DUMPED: Represent a dumped external database status.
        DEPENDENT: Represent a dependent external database status.
    """

    KNOWN = "KNOWN"
    XREF = "XREF"
    DUMPED = "DUMPED"
    DEPENDENT = "DEPENDENT"


@unique
class InfoType(StrEnum):
    """Represent info type values for the xref.info_type column.

    Attributes:
        NONE: Represent no specific info type.
        PROBE: Represent a probe info type.
        DEPENDENT: Represent a dependent info type.
        DIRECT: Represent a direct info type.
        INFERRED_PAIR: Represent an inferred pair info type.
        PROBE2TRANSCRIPT: Represent a probe-to-transcript info type.
        UNMAPPED: Represent an unmapped info type.
        CHECKSUM: Represent a checksum info type.
    """

    NONE = "NONE"
    PROBE = "PROBE"
    DEPENDENT = "DEPENDENT"
    DIRECT = "DIRECT"
    INFERRED_PAIR = "INFERRED_PAIR"
    PROBE2TRANSCRIPT = "PROBE2TRANSCRIPT"
    UNMAPPED = "UNMAPPED"
    CHECKSUM = "CHECKSUM"


@unique
class ExternalDbType(StrEnum):
    """Represent database type values for the external_db.type column.

    Attributes:
        PRIMARY: Represent a primary external database type.
        SECONDARY: Represent a secondary external database type.
        MISC: Represent a miscellaneous external database type.
        CHECKSUM: Represent a checksum external database type.
        DEPENDENT: Represent a dependent external database type.
        IMAGE_DEPICTION: Represent an image depiction external database type.
    """

    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    MISC = "MISC"
    CHECKSUM = "CHECKSUM"
    DEPENDENT = "DEPENDENT"
    IMAGE_DEPICTION = "IMAGE_DEPICTION"
