"""Tests for the session management module.

Engine/session creation is delegated to the shared ``db-common`` library, so
these tests exercise the public ``ensembl_orm.session`` API against a real
in-memory SQLite engine (no mocks on db-common internals). Only the
Ensembl-specific ``discover_database_name`` is patched, because it hits the
network.
"""

import logging
from contextlib import contextmanager
from unittest.mock import patch

import pytest
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

import ensembl_orm.session as sess
from ensembl_orm.config.database_settings import DatabaseSettings
from ensembl_orm.exceptions import ReadOnlySessionError, SessionError
from ensembl_orm.session import close_all_sessions, get_engine, get_session, initialize_engine


@pytest.fixture(autouse=True)
def _reset_engine():
    """Clear the module-level engine/session factories before and after each test."""
    sess._engine_factory = None
    sess._session_factory = None
    yield
    sess._engine_factory = None
    sess._session_factory = None


def _sqlite_settings() -> DatabaseSettings:
    """Return settings that build a real in-memory SQLite engine.

    The ``sqlite`` driver makes db-common use ``sqlite:///:memory:`` with a
    :class:`~sqlalchemy.pool.StaticPool`, so the same in-memory connection is
    shared across sessions within a test.
    """
    return DatabaseSettings(driver="sqlite", database=":memory:")


@contextmanager
def _stub_engine_factories():
    """Stub the db-common EngineFactory/SessionFactory so no driver is loaded.

    The discovery-branch tests use the MySQL driver to exercise the non-SQLite
    code path, but mysqlclient's native ``libmysqlclient`` is not available in
    every environment. Patching the delegation boundary keeps these as focused
    unit tests of ``initialize_engine``'s discovery *decision* (whether
    ``discover_database_name`` is called), which is the behaviour under test.
    """
    with patch("ensembl_orm.session.EngineFactory") as ef, patch("ensembl_orm.session.SessionFactory") as sf:
        yield ef, sf


class TestInitializeEngine:
    """Tests for initialize_engine()."""

    def test_returns_real_sqlite_engine(self):
        """initialize_engine constructs and returns a SQLAlchemy Engine."""
        engine = initialize_engine(_sqlite_settings())

        assert isinstance(engine, Engine)

    def test_idempotent_returns_same_engine(self):
        """Repeated calls return the cached engine without re-creating."""
        first = initialize_engine(_sqlite_settings())
        second = initialize_engine(_sqlite_settings())

        assert first is second

    def test_defaults_settings_when_none(self):
        """When settings is None, default DatabaseSettings is used and discovery runs."""
        with (
            patch("ensembl_orm.session.discover_database_name", return_value="discovered_db") as mock_discover,
            _stub_engine_factories(),
        ):
            initialize_engine(None)

        used_settings = mock_discover.call_args[0][0]
        assert used_settings.host == "ensembldb.ensembl.org"
        assert used_settings.port == 5306

    def test_skips_discovery_when_database_set(self):
        """When settings.database is set (non-SQLite), discover_database_name is NOT called."""
        settings = DatabaseSettings(
            driver="mysql+mysqldb",
            host="db.example.com",
            port=3306,
            username="u",
            password="p",
            database="mydb",
        )

        with (
            patch("ensembl_orm.session.discover_database_name") as mock_discover,
            _stub_engine_factories(),
        ):
            initialize_engine(settings)

        mock_discover.assert_not_called()
        assert settings.database == "mydb"

    def test_skips_discovery_for_sqlite_driver(self):
        """SQLite driver skips discovery even when database is empty."""
        settings = DatabaseSettings(driver="sqlite")

        with patch("ensembl_orm.session.discover_database_name") as mock_discover:
            initialize_engine(settings)

        mock_discover.assert_not_called()

    def test_runs_discovery_when_database_empty_and_not_sqlite(self):
        """When database is empty and driver is not SQLite, discovery runs and fills database."""
        settings = DatabaseSettings(
            driver="mysql+mysqldb",
            host="db.example.com",
            port=3306,
            username="u",
            password="p",
            database="",
        )

        with (
            patch("ensembl_orm.session.discover_database_name", return_value="discovered_db") as mock_discover,
            _stub_engine_factories(),
        ):
            initialize_engine(settings)

        mock_discover.assert_called_once_with(settings)
        assert settings.database == "discovered_db"

    def test_logs_info_on_init(self, caplog):
        """Info log is emitted when the engine is initialized."""
        with caplog.at_level(logging.INFO, logger="ensembl_orm"):
            initialize_engine(_sqlite_settings())

        assert any("initialized" in r.message.lower() for r in caplog.records)


class TestGetEngine:
    """Tests for get_engine()."""

    def test_returns_initialized_engine(self):
        """get_engine returns the same engine initialize_engine built."""
        engine = initialize_engine(_sqlite_settings())

        assert get_engine() is engine

    def test_raises_session_error_when_uninitialized(self):
        """get_engine raises db_common SessionError when never initialized."""
        with pytest.raises(SessionError, match="not initialized"):
            get_engine()


class TestGetSession:
    """Tests for get_session() (the read-only delegation contract)."""

    def test_yields_real_session_executing_select(self):
        """get_session yields a real Session that can execute a query (SQLite)."""
        initialize_engine(_sqlite_settings())

        with get_session() as session:
            assert isinstance(session, Session)
            assert session.execute(text("SELECT 1")).scalar() == 1

    def test_commit_raises_read_only_session_error(self):
        """Committing inside a read-only session raises ReadOnlySessionError."""
        initialize_engine(_sqlite_settings())

        with get_session() as session:
            session.execute(text("SELECT 1"))
            with pytest.raises(ReadOnlySessionError):
                session.commit()

    def test_session_is_bound_to_the_engine(self):
        """The yielded session is bound to the initialized engine."""
        engine = initialize_engine(_sqlite_settings())

        with get_session() as session:
            assert session.bind is engine

    def test_raises_session_error_when_uninitialized(self):
        """get_session raises SessionError if the engine was never initialized."""
        with pytest.raises(SessionError, match="not initialized"):
            with get_session():
                pass


class TestCloseAllSessions:
    """Tests for close_all_sessions()."""

    def test_disposes_engine_and_clears_globals(self):
        """close_all_sessions disposes the engine and clears the module singletons."""
        initialize_engine(_sqlite_settings())
        assert sess._engine_factory is not None
        assert sess._session_factory is not None

        close_all_sessions()

        assert sess._engine_factory is None
        assert sess._session_factory is None

    def test_idempotent_when_uninitialized(self):
        """Calling close_all_sessions before any init raises no error."""
        assert sess._engine_factory is None

        close_all_sessions()

        assert sess._engine_factory is None

    def test_allows_reinit_after_close(self):
        """A fresh engine is built when initialize_engine runs after close."""
        first = initialize_engine(_sqlite_settings())
        close_all_sessions()
        second = initialize_engine(_sqlite_settings())

        assert first is not second

    def test_logs_info_on_dispose(self, caplog):
        """Info log is emitted when the engine is disposed."""
        initialize_engine(_sqlite_settings())

        with caplog.at_level(logging.INFO, logger="ensembl_orm"):
            close_all_sessions()

        assert any("disposed" in r.message.lower() for r in caplog.records)


class TestPublicAPIExports:
    """Tests that the session API is importable from ensembl_orm."""

    def test_imports_from_package_root(self):
        """Session functions are importable from the top-level package."""
        from ensembl_orm import close_all_sessions, get_engine, get_session, initialize_engine

        assert callable(initialize_engine)
        assert callable(get_engine)
        assert callable(get_session)
        assert callable(close_all_sessions)

    def test_imports_are_same_objects(self):
        """Imported objects from __init__ are the same as from the module."""
        from ensembl_orm import close_all_sessions, get_engine, get_session, initialize_engine
        from ensembl_orm.session import (
            close_all_sessions as sess_close,
            get_engine as sess_get_engine,
            get_session as sess_get_session,
            initialize_engine as sess_init,
        )

        assert initialize_engine is sess_init
        assert get_engine is sess_get_engine
        assert get_session is sess_get_session
        assert close_all_sessions is sess_close
