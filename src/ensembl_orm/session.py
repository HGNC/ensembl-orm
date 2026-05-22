"""Session management for Ensembl database connections."""

import logging
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlmodel import Session

from ensembl_orm.config.database_settings import DatabaseSettings
from ensembl_orm.discovery import discover_database_name
from ensembl_orm.exceptions import EnsemblSessionError

logger = logging.getLogger("ensembl_orm")

_engine: Optional[Engine] = None


def initialize_engine(settings: Optional[DatabaseSettings] = None) -> Engine:
    """Create the global engine, running discovery if needed.

    Args:
        settings: Database connection settings. If None, defaults are used.

    Returns:
        The global SQLAlchemy Engine instance.

    Usage::

        engine = initialize_engine(DatabaseSettings(host="localhost"))
    """
    global _engine

    if _engine is not None:
        return _engine

    if settings is None:
        settings = DatabaseSettings()

    if not settings.database:
        settings.database = discover_database_name(settings)

    url = settings.connection_url
    logger.debug(
        "Connection URL: %s",
        url.replace(settings.password, "***") if settings.password else url,
    )

    _engine = create_engine(
        url,
        pool_size=settings.pool_size,
        pool_recycle=settings.pool_recycle,
    )
    logger.info("Engine initialized for database: %s", settings.database)
    return _engine


def get_engine() -> Engine:
    """Return the global engine.

    Returns:
        The initialized SQLAlchemy Engine.

    Raises:
        EnsemblSessionError: If the engine has not been initialized.
    """
    if _engine is None:
        raise EnsemblSessionError("Engine not initialized. Call initialize_engine() first.")
    return _engine


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Context manager yielding a read-only session.

    Yields:
        A SQLModel Session with read-only transaction enforcement.

    Usage::

        with get_session() as session:
            result = session.exec(text("SELECT 1"))
    """
    engine = get_engine()
    session = Session(engine)
    try:
        session.execute(text("SET SESSION TRANSACTION READ ONLY"))
        yield session
    finally:
        session.close()


def close_all_sessions() -> None:
    """Dispose the global engine and clear the reference."""
    global _engine
    if _engine is not None:
        _engine.dispose()
        _engine = None
        logger.info("Engine disposed and cleared")
