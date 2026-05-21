from unittest.mock import patch

import pytest

from ensembl_orm.config.database_settings import DatabaseSettings


@pytest.fixture
def settings() -> DatabaseSettings:
    """Provide a fresh DatabaseSettings instance with defaults."""
    return DatabaseSettings()


@pytest.fixture
def settings_with_env(monkeypatch: pytest.MonkeyPatch) -> DatabaseSettings:
    """Provide a DatabaseSettings instance loaded from environment variables."""
    monkeypatch.setenv("ENSEMBLDB_HOST", "custom-host.example.com")
    monkeypatch.setenv("ENSEMBLDB_PORT", "3307")
    monkeypatch.setenv("ENSEMBLDB_USER", "admin")
    monkeypatch.setenv("ENSEMBLDB_PASSWORD", "s3cret")
    monkeypatch.setenv("ENSEMBLDB_DATABASE", "ensembl_homo_sapiens")
    monkeypatch.setenv("ENSEMBLDB_POOL_SIZE", "10")
    monkeypatch.setenv("ENSEMBLDB_POOL_RECYCLE", "7200")
    return DatabaseSettings()


def test_default_host(settings: DatabaseSettings) -> None:
    assert settings.host == "ensembldb.ensembl.org"


def test_default_port(settings: DatabaseSettings) -> None:
    assert settings.port == 5306


def test_default_user(settings: DatabaseSettings) -> None:
    assert settings.user == "anonymous"


def test_default_password(settings: DatabaseSettings) -> None:
    assert settings.password == ""


def test_default_database(settings: DatabaseSettings) -> None:
    assert settings.database == ""


def test_default_pool_size(settings: DatabaseSettings) -> None:
    assert settings.pool_size == 3


def test_default_pool_recycle(settings: DatabaseSettings) -> None:
    assert settings.pool_recycle == 3600


def test_env_override_host(settings_with_env: DatabaseSettings) -> None:
    assert settings_with_env.host == "custom-host.example.com"


def test_env_override_port(settings_with_env: DatabaseSettings) -> None:
    assert settings_with_env.port == 3307


def test_env_override_user(settings_with_env: DatabaseSettings) -> None:
    assert settings_with_env.user == "admin"


def test_env_override_password(settings_with_env: DatabaseSettings) -> None:
    assert settings_with_env.password == "s3cret"


def test_env_override_database(settings_with_env: DatabaseSettings) -> None:
    assert settings_with_env.database == "ensembl_homo_sapiens"


def test_env_override_pool_size(settings_with_env: DatabaseSettings) -> None:
    assert settings_with_env.pool_size == 10


def test_env_override_pool_recycle(settings_with_env: DatabaseSettings) -> None:
    assert settings_with_env.pool_recycle == 7200


def test_connection_url_default(settings: DatabaseSettings) -> None:
    assert settings.connection_url == "mysql+mysqldb://anonymous:@ensembldb.ensembl.org:5306/"


def test_connection_url_with_credentials(settings_with_env: DatabaseSettings) -> None:
    expected = "mysql+mysqldb://admin:s3cret@custom-host.example.com:3307/ensembl_homo_sapiens"
    assert settings_with_env.connection_url == expected


def test_env_prefix_is_ensembldb() -> None:
    assert DatabaseSettings.model_config["env_prefix"] == "ENSEMBLDB_"


def test_port_must_be_integer(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENSEMBLDB_PORT", "not_a_number")
    with pytest.raises(ValueError):
        DatabaseSettings()
