"""Session management for Ensembl database connections.

Engine and session creation are delegated to the shared ``db-common`` library:
module-level :class:`db_common.EngineFactory` and
:class:`db_common.SessionFactory` singletons hold the cached engine, and
:func:`get_session` yields a read-only session via
:meth:`db_common.SessionFactory.get_readonly_session`.
"""

import logging
from contextlib import contextmanager
from typing import Generator

from db_common import EngineFactory, SessionFactory
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from ensembl_orm.config.database_settings import DatabaseSettings
from ensembl_orm.discovery import discover_database_name
from ensembl_orm.exceptions import SessionError

logger = logging.getLogger("ensembl_orm")

_engine_factory: EngineFactory | None = None
_session_factory: SessionFactory | None = None


def initialize_engine(settings: DatabaseSettings | None = None) -> Engine:
    """Create and cache the global engine, running discovery when required.

    Args:
        settings: Database connection settings. If ``None``, the default
            :class:`DatabaseSettings` is used.

    Returns:
        The cached SQLAlchemy :class:`~sqlalchemy.engine.Engine`.

    Raises:
        EnsemblDiscoveryError: If ``settings.database`` is empty, the driver is
            not SQLite, and database-name discovery fails.

    Usage::

        engine = initialize_engine(DatabaseSettings(host="localhost"))
    """
    global _engine_factory, _session_factory

    if _engine_factory is not None:
        return _engine_factory.get_engine()

    if settings is None:
        settings = DatabaseSettings()

    # Discovery hits the public Ensembl server and only makes sense for the
    # MySQL backend; SQLite (the test/local driver) always skips it.
    if not settings.database and settings.driver != "sqlite":
        settings.database = discover_database_name(settings)

    _engine_factory = EngineFactory(settings)
    _session_factory = SessionFactory(_engine_factory)
    engine = _engine_factory.get_engine()
    logger.info("Engine initialized for database: %s", settings.database)
    return engine


def get_engine() -> Engine:
    """Return the cached global engine.

    Returns:
        The initialized SQLAlchemy :class:`~sqlalchemy.engine.Engine`.

    Raises:
        SessionError: If the engine has not been initialized.
    """
    if _engine_factory is None:
        raise SessionError("Engine not initialized. Call initialize_engine() first.")
    return _engine_factory.get_engine()


@contextmanager
def get_session() -> Generator[Session]:
    """Context manager yielding a read-only session.

    The session is a :class:`sqlalchemy.orm.Session` obtained from the shared
    :class:`db_common.SessionFactory`. Any attempt to commit raises
    :class:`ReadOnlySessionError` (ensembl-orm is a read-only ORM).

    Yields:
        A read-only SQLAlchemy :class:`~sqlalchemy.orm.Session`.

    Raises:
        SessionError: If the engine has not been initialized.

    Usage::

        with get_session() as session:
            result = session.execute(text("SELECT 1")).scalar()
    """
    if _session_factory is None:
        raise SessionError("Engine not initialized. Call initialize_engine() first.")
    with _session_factory.get_readonly_session() as session:
        yield session


def close_all_sessions() -> None:
    """Close all open sessions, dispose the engine, and clear the singletons."""
    global _engine_factory, _session_factory

    if _engine_factory is None:
        return

    if _session_factory is not None:
        _session_factory.close_all_sessions()
        _session_factory.dispose_engine()

    _session_factory = None
    _engine_factory = None
    logger.info("Engine disposed and cleared")
