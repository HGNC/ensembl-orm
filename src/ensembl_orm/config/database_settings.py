"""Ensembl database connection settings backed by the shared ``db-common`` library."""

from typing import Any

import db_common
from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import SettingsConfigDict


class EnsemblDatabaseSettings(db_common.DatabaseSettings):
    """Connection and pooling settings for the public Ensembl MySQL database.

    Subclass the shared :class:`db_common.DatabaseSettings`, overriding only the
    Ensembl specifics: the ``ENSEMBLDB_`` env prefix, the public Ensembl server
    defaults, and the MySQL (mysqlclient) driver. URL building and pooling come
    from ``db-common`` via :meth:`get_url`.

    Backward-compatibility shims keep legacy callers working without churn:

    * ``user`` — a read/write property over the canonical ``username`` field.
      It is *also* accepted as a construction kwarg (mapped onto ``username``)
      and read from the legacy ``ENSEMBLDB_USER`` env var, in addition to the
      canonical ``ENSEMBLDB_USERNAME``.
    * ``connection_url`` — a literal, password-bearing URL derived from
      :meth:`get_url` (for :func:`create_engine`; password shown, not masked).
    * ``DatabaseSettings`` — a module alias of this class (see below).

    Usage::

        settings = EnsemblDatabaseSettings()
        print(settings.connection_url)  # mysql+mysqldb://anonymous:@ensembldb.ensembl.org:5306/

    Note:
        A bare ``"user"`` validation alias is deliberately **not** used: under
        case-insensitive env reading it would leak the Unix ``$USER`` variable
        into the default. The ``user=`` kwarg is handled by a ``before`` model
        validator instead.
    """

    model_config = SettingsConfigDict(env_prefix="ENSEMBLDB_", populate_by_name=True)

    # mysqlclient driver, matching the historical connection URL.
    driver: str = "mysql+mysqldb"
    host: str | None = "ensembldb.ensembl.org"
    port: int | None = 5306
    username: str | None = Field(
        default="anonymous",
        validation_alias=AliasChoices("ENSEMBLDB_USER", "ENSEMBLDB_USERNAME"),
    )
    password: str | None = ""
    database: str | None = ""
    pool_size: int = 3
    pool_recycle: int = 3600

    @model_validator(mode="before")
    @classmethod
    def _map_legacy_user_kwarg(cls, data: Any) -> Any:
        """Map the legacy ``user=`` construction kwarg onto ``username``."""
        if isinstance(data, dict) and "user" in data:
            data.setdefault("username", data.pop("user"))
        return data

    @property
    def user(self) -> str | None:
        """Alias for :attr:`username` (legacy callers read/write ``user``)."""
        return self.username

    @user.setter
    def user(self, value: str | None) -> None:
        self.username = value

    @property
    def connection_url(self) -> str:
        """Return the literal MySQL connection URL for :func:`create_engine`.

        ``str(get_url())`` masks the password (``***``), which would break engine
        creation, so render with the password shown.
        """
        return str(self.get_url().render_as_string(hide_password=False))


# Backward-compat alias: the class was historically named ``DatabaseSettings``
# and is imported under that name throughout the codebase (discovery.py,
# session.py, ensembl_orm/__init__.py, config/__init__.py, conftest.py, and
# several test modules). Keeping the alias avoids touching those callers.
DatabaseSettings = EnsemblDatabaseSettings
