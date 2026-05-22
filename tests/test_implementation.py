from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_import_database_settings() -> None:
    from ensembl_orm.config.database_settings import DatabaseSettings

    assert DatabaseSettings is not None


def test_import_exceptions() -> None:
    from ensembl_orm.exceptions import EnsemblDiscoveryError, EnsemblSessionError

    assert issubclass(EnsemblDiscoveryError, Exception)
    assert issubclass(EnsemblSessionError, Exception)


def test_import_from_top_level_package() -> None:
    from ensembl_orm import DatabaseSettings, EnsemblDiscoveryError, EnsemblSessionError

    assert DatabaseSettings is not None
    assert EnsemblDiscoveryError is not None
    assert EnsemblSessionError is not None


def test_database_settings_defaults() -> None:
    from ensembl_orm.config.database_settings import DatabaseSettings

    settings = DatabaseSettings()
    assert settings.host == "ensembldb.ensembl.org"
    assert settings.port == 5306
    assert settings.user == "anonymous"
    assert settings.password == ""
    assert settings.database == ""
    assert settings.pool_size == 3
    assert settings.pool_recycle == 3600


def test_connection_url_format() -> None:
    from ensembl_orm.config.database_settings import DatabaseSettings

    settings = DatabaseSettings()
    assert settings.connection_url == "mysql+mysqldb://anonymous:@ensembldb.ensembl.org:5306/"


def test_connection_url_with_password_and_database() -> None:
    from ensembl_orm.config.database_settings import DatabaseSettings

    settings = DatabaseSettings(
        user="testuser",
        password="secret",
        host="db.example.com",
        port=3306,
        database="mydb",
    )
    assert settings.connection_url == "mysql+mysqldb://testuser:secret@db.example.com:3306/mydb"


def test_env_prefix_ensembldb() -> None:
    from ensembl_orm.config.database_settings import DatabaseSettings

    config = DatabaseSettings.model_config
    assert config.get("env_prefix") == "ENSEMBLDB_"
