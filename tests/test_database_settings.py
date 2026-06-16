"""Tests for ``EnsemblDatabaseSettings`` (``db_common``-backed settings).

Covers the T3 contract: subclassing ``db_common.DatabaseSettings``, the
``ENSEMBLDB_`` env prefix, Ensembl defaults, env-var overrides (including the
legacy ``ENSEMBLDB_USER``), the ``user``/``username`` shim, ``connection_url``
and ``get_url()``.
"""

import pytest
from sqlalchemy import URL

import db_common

from ensembl_orm.config.database_settings import DatabaseSettings, EnsemblDatabaseSettings


@pytest.fixture
def settings() -> EnsemblDatabaseSettings:
    """Provide a fresh EnsemblDatabaseSettings instance with defaults."""
    return EnsemblDatabaseSettings()


@pytest.fixture
def settings_with_env(monkeypatch: pytest.MonkeyPatch) -> EnsemblDatabaseSettings:
    """Provide an EnsemblDatabaseSettings instance loaded from environment variables."""
    monkeypatch.setenv("ENSEMBLDB_HOST", "custom-host.example.com")
    monkeypatch.setenv("ENSEMBLDB_PORT", "3307")
    monkeypatch.setenv("ENSEMBLDB_USER", "admin")
    monkeypatch.setenv("ENSEMBLDB_PASSWORD", "s3cret")
    monkeypatch.setenv("ENSEMBLDB_DATABASE", "ensembl_homo_sapiens")
    monkeypatch.setenv("ENSEMBLDB_POOL_SIZE", "10")
    monkeypatch.setenv("ENSEMBLDB_POOL_RECYCLE", "7200")
    return EnsemblDatabaseSettings()


# -- Subclass + alias contract -------------------------------------------------


def test_subclasses_db_common_database_settings() -> None:
    """EnsemblDatabaseSettings must build on the shared db_common base."""
    assert issubclass(EnsemblDatabaseSettings, db_common.DatabaseSettings)


def test_database_settings_is_backward_compat_alias() -> None:
    """The legacy name stays importable as an alias of the new class (no churn)."""
    assert DatabaseSettings is EnsemblDatabaseSettings


def test_env_prefix_is_ensembldb() -> None:
    assert EnsemblDatabaseSettings.model_config["env_prefix"] == "ENSEMBLDB_"


# -- Ensembl defaults ----------------------------------------------------------


def test_default_host(settings: EnsemblDatabaseSettings) -> None:
    assert settings.host == "ensembldb.ensembl.org"


def test_default_port(settings: EnsemblDatabaseSettings) -> None:
    assert settings.port == 5306


def test_default_username(settings: EnsemblDatabaseSettings) -> None:
    assert settings.username == "anonymous"


def test_default_user_reads_username(settings: EnsemblDatabaseSettings) -> None:
    assert settings.user == "anonymous"


def test_default_password(settings: EnsemblDatabaseSettings) -> None:
    assert settings.password == ""


def test_default_database(settings: EnsemblDatabaseSettings) -> None:
    assert settings.database == ""


def test_default_pool_size(settings: EnsemblDatabaseSettings) -> None:
    assert settings.pool_size == 3


def test_default_pool_recycle(settings: EnsemblDatabaseSettings) -> None:
    assert settings.pool_recycle == 3600


def test_default_driver_is_mysql_mysqldb(settings: EnsemblDatabaseSettings) -> None:
    assert settings.driver == "mysql+mysqldb"


# -- Env-var overrides ---------------------------------------------------------


def test_env_override_host(settings_with_env: EnsemblDatabaseSettings) -> None:
    assert settings_with_env.host == "custom-host.example.com"


def test_env_override_port(settings_with_env: EnsemblDatabaseSettings) -> None:
    assert settings_with_env.port == 3307


def test_env_override_user_populates_username(settings_with_env: EnsemblDatabaseSettings) -> None:
    assert settings_with_env.username == "admin"
    assert settings_with_env.user == "admin"


def test_env_override_canonical_username(monkeypatch: pytest.MonkeyPatch) -> None:
    """The canonical ENSEMBLDB_USERNAME env var is also honoured."""
    monkeypatch.setenv("ENSEMBLDB_USERNAME", "canonical")
    assert EnsemblDatabaseSettings().username == "canonical"


def test_env_override_password(settings_with_env: EnsemblDatabaseSettings) -> None:
    assert settings_with_env.password == "s3cret"


def test_env_override_database(settings_with_env: EnsemblDatabaseSettings) -> None:
    assert settings_with_env.database == "ensembl_homo_sapiens"


def test_env_override_pool_size(settings_with_env: EnsemblDatabaseSettings) -> None:
    assert settings_with_env.pool_size == 10


def test_env_override_pool_recycle(settings_with_env: EnsemblDatabaseSettings) -> None:
    assert settings_with_env.pool_recycle == 7200


def test_default_username_unaffected_by_unix_user_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """The ``user`` shim must NOT leak the Unix ``$USER`` env var into the default."""
    monkeypatch.setenv("USER", "definitely-not-anonymous")
    assert EnsemblDatabaseSettings().username == "anonymous"


# -- user / username shim ------------------------------------------------------


def test_user_kwarg_constructs_username() -> None:
    """Legacy ``user=`` construction kwarg maps onto the canonical ``username`` field."""
    assert EnsemblDatabaseSettings(user="bob").username == "bob"
    assert EnsemblDatabaseSettings(user="bob").user == "bob"


def test_username_kwarg_constructs() -> None:
    """Canonical ``username=`` kwarg works (populate_by_name)."""
    assert EnsemblDatabaseSettings(username="carol").username == "carol"


def test_user_property_reads_username(settings: EnsemblDatabaseSettings) -> None:
    settings.username = "dave"
    assert settings.user == "dave"


def test_user_property_writes_username(settings: EnsemblDatabaseSettings) -> None:
    settings.user = "eve"
    assert settings.username == "eve"


# -- connection_url / get_url --------------------------------------------------


def test_connection_url_default(settings: EnsemblDatabaseSettings) -> None:
    assert settings.connection_url == "mysql+mysqldb://anonymous:@ensembldb.ensembl.org:5306/"


def test_connection_url_with_credentials(settings_with_env: EnsemblDatabaseSettings) -> None:
    expected = "mysql+mysqldb://admin:s3cret@custom-host.example.com:3307/ensembl_homo_sapiens"
    assert settings_with_env.connection_url == expected


def test_get_url_returns_sqlalchemy_url(settings: EnsemblDatabaseSettings) -> None:
    url = settings.get_url()
    assert isinstance(url, URL)
    assert url.drivername == "mysql+mysqldb"
    assert url.username == "anonymous"
    assert url.host == "ensembldb.ensembl.org"
    assert url.port == 5306


# -- Validation ----------------------------------------------------------------


def test_port_must_be_integer(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENSEMBLDB_PORT", "not_a_number")
    with pytest.raises(ValueError):
        EnsemblDatabaseSettings()
