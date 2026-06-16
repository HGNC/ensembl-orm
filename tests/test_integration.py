"""End-to-end integration smoke for the migrated db-common stack (T5).

This exercises the real, migrated path end to end against an in-memory SQLite
engine — ``initialize_engine()`` + ``get_session()`` round-tripping ``SELECT 1``
through the shared ``db-common`` ``EngineFactory``/``SessionFactory``. There are
**no mocks on db-common internals**: only the Ensembl-specific
``discover_database_name`` network call is avoided, because the SQLite driver
skips discovery entirely.

The purpose is a regression guard proving that, with SQLModel removed, the
module-level session API still produces a working read-only SQLAlchemy session.
"""

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

import ensembl_orm.session as sess
from ensembl_orm.config.database_settings import DatabaseSettings
from ensembl_orm.exceptions import ReadOnlySessionError, SessionError
from ensembl_orm.session import close_all_sessions, get_engine, get_session, initialize_engine


def _reset_engine() -> None:
    """Clear the module-level engine/session factories."""
    sess._engine_factory = None
    sess._session_factory = None


def _sqlite_settings() -> DatabaseSettings:
    """Return settings that build a real in-memory SQLite engine."""
    return DatabaseSettings(driver="sqlite", database=":memory:")


def setup_function() -> None:
    """Ensure a clean module state before each test in this module."""
    _reset_engine()


def teardown_function() -> None:
    """Ensure the engine is disposed after each test in this module."""
    close_all_sessions()


def test_initialize_engine_returns_real_sqlite_engine() -> None:
    """initialize_engine() builds a real SQLAlchemy Engine via db-common."""
    engine = initialize_engine(_sqlite_settings())

    assert isinstance(engine, Engine)


def test_get_session_round_trips_select_one() -> None:
    """The migrated path yields a real session that can execute a query."""
    initialize_engine(_sqlite_settings())

    with get_session() as session:
        assert isinstance(session, Session)
        result = session.execute(text("SELECT 1")).scalar()

    assert result == 1


def test_get_session_remains_read_only() -> None:
    """The end-to-end session is still read-only (ReadOnlySessionError on commit)."""
    initialize_engine(_sqlite_settings())

    with get_session() as session:
        session.execute(text("SELECT 1"))
        try:
            session.commit()
        except ReadOnlySessionError:
            return

    raise AssertionError("commit should have raised ReadOnlySessionError")


def test_get_engine_raises_when_uninitialized() -> None:
    """get_engine() surfaces the db-common SessionError before any init."""
    try:
        get_engine()
    except SessionError:
        return

    raise AssertionError("get_engine() should have raised SessionError when uninitialized")
