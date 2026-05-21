from ensembl_orm.config.database_settings import DatabaseSettings
from ensembl_orm.exceptions import EnsemblDiscoveryError, EnsemblSessionError

import pytest


@pytest.fixture
def database_settings() -> DatabaseSettings:
    """Provide a fresh DatabaseSettings instance with defaults."""
    return DatabaseSettings()


@pytest.fixture
def ensembl_discovery_error() -> EnsemblDiscoveryError:
    """Provide an EnsemblDiscoveryError instance."""
    return EnsemblDiscoveryError("test discovery failure")


@pytest.fixture
def ensembl_session_error() -> EnsemblSessionError:
    """Provide an EnsemblSessionError instance."""
    return EnsemblSessionError("test session failure")
