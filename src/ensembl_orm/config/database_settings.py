from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Configuration for Ensembl MySQL database connections.

    Loads settings from environment variables prefixed with ENSEMBLDB_.

    Attributes:
        host: Database server hostname.
        port: Database server port.
        user: Database user name.
        password: Database user password.
        database: Target database name.
        pool_size: Connection pool size.
        pool_recycle: Seconds before a connection is recycled.

    Usage::

        settings = DatabaseSettings()
        print(settings.connection_url)
    """

    host: str = "ensembldb.ensembl.org"
    port: int = 5306
    user: str = "anonymous"
    password: str = ""
    database: str = ""
    pool_size: int = 3
    pool_recycle: int = 3600

    model_config = {"env_prefix": "ENSEMBLDB_"}

    @property
    def connection_url(self) -> str:
        """Build a SQLAlchemy-compatible MySQL connection URL."""
        return f"mysql+mysqldb://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
