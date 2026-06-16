from unittest.mock import MagicMock

import pytest

from ensembl_orm.config.database_settings import DatabaseSettings
from ensembl_orm.exceptions import EnsemblDiscoveryError


@pytest.fixture
def mock_settings() -> DatabaseSettings:
    """Provide a DatabaseSettings instance pointed at a fake local database."""
    return DatabaseSettings(
        host="localhost",
        port=3306,
        user="testuser",
        password="testpass",
        database="test_homo_sapiens_core_112_38",
    )


@pytest.fixture
def database_settings() -> DatabaseSettings:
    """Provide a fresh DatabaseSettings instance with defaults."""
    return DatabaseSettings()


@pytest.fixture
def mock_engine() -> MagicMock:
    """Provide a mocked SQLAlchemy engine with a connectable mock connection."""
    mock_conn = MagicMock()
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)

    engine = MagicMock()
    engine.connect.return_value = mock_conn
    engine.dispose = MagicMock()

    return engine


@pytest.fixture
def mock_version_response() -> MagicMock:
    """Mock the HTTP response body for the Ensembl release version endpoint."""
    mock_body = MagicMock()
    mock_body.read.return_value = b"112\n"
    mock_body.__enter__ = MagicMock(return_value=mock_body)
    mock_body.__exit__ = MagicMock(return_value=False)
    return mock_body


@pytest.fixture
def mock_show_databases_result() -> MagicMock:
    """Mock the result of SHOW DATABASES LIKE for database name discovery."""
    mock_result = MagicMock()
    mock_result.__iter__ = MagicMock(return_value=iter([("homo_sapiens_core_112_38",)]))
    return mock_result


@pytest.fixture
def ensembl_discovery_error() -> EnsemblDiscoveryError:
    """Provide an EnsemblDiscoveryError instance."""
    return EnsemblDiscoveryError("test discovery failure")
