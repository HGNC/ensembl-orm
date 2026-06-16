"""Read-only SQLModel ORM for the Ensembl homo_sapiens_core MySQL database."""

from ensembl_orm.config.database_settings import DatabaseSettings
from ensembl_orm.discovery import discover_database_name
from ensembl_orm.enums import EnsemblObjectType, ExternalDbStatus, ExternalDbType, InfoType
from ensembl_orm.exceptions import EnsemblDiscoveryError, ReadOnlySessionError, SessionError
from ensembl_orm.models.external_db import ExternalDb
from ensembl_orm.models.gene import Gene
from ensembl_orm.models.karyotype import Karyotype
from ensembl_orm.models.object_xref import ObjectXref
from ensembl_orm.models.seq_region import SeqRegion
from ensembl_orm.models.seq_region_attrib import SeqRegionAttrib
from ensembl_orm.models.xref import Xref
from ensembl_orm.session import close_all_sessions, get_engine, get_session, initialize_engine

__all__: list[str] = [
    "DatabaseSettings",
    "initialize_engine",
    "get_engine",
    "get_session",
    "close_all_sessions",
    "discover_database_name",
    "EnsemblDiscoveryError",
    "SessionError",
    "ReadOnlySessionError",
    "EnsemblObjectType",
    "ExternalDbStatus",
    "ExternalDbType",
    "InfoType",
    "Gene",
    "SeqRegion",
    "Xref",
    "ObjectXref",
    "ExternalDb",
    "SeqRegionAttrib",
    "Karyotype",
]
# Autopilot commit marker
