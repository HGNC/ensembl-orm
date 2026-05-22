"""Tests for the session management module."""

import logging
from unittest.mock import MagicMock, patch

import pytest

from ensembl_orm.config.database_settings import DatabaseSettings
from ensembl_orm.exceptions import EnsemblSessionError


@pytest.fixture(autouse=True)
def _reset_engine():
    """Clear the global engine before and after each test."""
    import ensembl_orm.session as sess

    sess._engine = None
    yield
    sess._engine = None


@pytest.fixture()
def settings():
    """Provide DatabaseSettings with explicit database set."""
    return DatabaseSettings(
        host="localhost",
        port=3306,
        user="testuser",
        password="testpass",
        database="test_db",
    )


class TestInitializeEngine:
    """Tests for initialize_engine()."""

    def test_creates_engine_with_correct_url_and_pool_settings(self, settings):
        """initialize_engine calls create_engine with connection_url and pool args."""
        from ensembl_orm.session import initialize_engine

        mock_engine = MagicMock()
        with patch("ensembl_orm.session.create_engine", return_value=mock_engine) as mock_create:
            engine = initialize_engine(settings)

        assert engine is mock_engine
        mock_create.assert_called_once_with(
            settings.connection_url,
            pool_size=settings.pool_size,
            pool_recycle=settings.pool_recycle,
        )

    def test_calls_discover_when_database_empty(self):
        """When settings.database is empty, discover_database_name is called."""
        from ensembl_orm.session import initialize_engine

        empty_settings = DatabaseSettings(host="localhost", port=3306, user="testuser", password="testpass")
        mock_engine = MagicMock()

        with (
            patch("ensembl_orm.session.create_engine", return_value=mock_engine),
            patch("ensembl_orm.session.discover_database_name", return_value="discovered_db") as mock_discover,
        ):
            initialize_engine(empty_settings)

        mock_discover.assert_called_once_with(empty_settings)
        assert empty_settings.database == "discovered_db"

    def test_skips_discovery_when_database_set(self, settings):
        """When settings.database is already set, discover_database_name is NOT called."""
        from ensembl_orm.session import initialize_engine

        mock_engine = MagicMock()
        with (
            patch("ensembl_orm.session.create_engine", return_value=mock_engine),
            patch("ensembl_orm.session.discover_database_name") as mock_discover,
        ):
            initialize_engine(settings)

        mock_discover.assert_not_called()

    def test_idempotent_returns_same_engine(self, settings):
        """Repeated calls return the same engine without re-creating."""
        from ensembl_orm.session import initialize_engine

        mock_engine = MagicMock()
        with patch("ensembl_orm.session.create_engine", return_value=mock_engine):
            first = initialize_engine(settings)
            second = initialize_engine(settings)

        assert first is second

    def test_defaults_settings_when_none(self):
        """When settings is None, a default DatabaseSettings is created."""
        from ensembl_orm.session import initialize_engine

        mock_engine = MagicMock()
        with (
            patch("ensembl_orm.session.create_engine", return_value=mock_engine),
            patch("ensembl_orm.session.discover_database_name", return_value="auto_db"),
        ):
            engine = initialize_engine(None)

        assert engine is mock_engine

    def test_logs_debug_with_masked_password(self, settings, caplog):
        """Debug log contains masked password, not the real one."""
        from ensembl_orm.session import initialize_engine

        mock_engine = MagicMock()
        with (
            patch("ensembl_orm.session.create_engine", return_value=mock_engine),
            caplog.at_level(logging.DEBUG, logger="ensembl_orm"),
        ):
            initialize_engine(settings)

        log_messages = [r.message for r in caplog.records]
        assert any("Connection URL" in m for m in log_messages)
        assert not any("testpass" in m for m in log_messages)

    def test_stores_engine_in_global(self, settings):
        """The created engine is stored in the module-level _engine variable."""
        import ensembl_orm.session as sess

        from ensembl_orm.session import initialize_engine

        mock_engine = MagicMock()
        with patch("ensembl_orm.session.create_engine", return_value=mock_engine):
            initialize_engine(settings)

        assert sess._engine is mock_engine


class TestGetEngine:
    """Tests for get_engine()."""

    def test_returns_global_engine(self):
        """get_engine returns the initialized engine."""
        import ensembl_orm.session as sess

        from ensembl_orm.session import get_engine

        mock_engine = MagicMock()
        sess._engine = mock_engine
        assert get_engine() is mock_engine

    def test_raises_when_not_initialized(self):
        """get_engine raises EnsemblSessionError when engine is None."""
        from ensembl_orm.session import get_engine

        with pytest.raises(EnsemblSessionError, match="Engine not initialized"):
            get_engine()


class TestGetSession:
    """Tests for get_session()."""

    def test_yields_session_bound_to_engine(self):
        """get_session creates a Session with the global engine."""
        import ensembl_orm.session as sess

        from ensembl_orm.session import get_session

        mock_engine = MagicMock()
        sess._engine = mock_engine

        with patch("ensembl_orm.session.Session") as mock_session_cls:
            mock_session = MagicMock()
            mock_session_cls.return_value = mock_session
            with get_session() as session:
                assert session is mock_session
            mock_session_cls.assert_called_once_with(mock_engine)

    def test_sets_read_only_transaction(self):
        """get_session executes SET SESSION TRANSACTION READ ONLY."""
        import ensembl_orm.session as sess

        from ensembl_orm.session import get_session

        mock_engine = MagicMock()
        sess._engine = mock_engine

        with patch("ensembl_orm.session.Session") as mock_session_cls:
            mock_session = MagicMock()
            mock_session_cls.return_value = mock_session
            with get_session():
                pass

        calls = mock_session.exec.call_args_list
        assert len(calls) >= 1
        executed_sql = [c[0][0].text for c in calls]
        assert "SET SESSION TRANSACTION READ ONLY" in executed_sql

    def test_closes_session_on_exit(self):
        """session.close() is called when context exits."""
        import ensembl_orm.session as sess

        from ensembl_orm.session import get_session

        mock_engine = MagicMock()
        sess._engine = mock_engine

        with patch("ensembl_orm.session.Session") as mock_session_cls:
            mock_session = MagicMock()
            mock_session_cls.return_value = mock_session
            with get_session():
                pass

        mock_session.close.assert_called_once()

    def test_closes_session_on_exception(self):
        """session.close() is called even when an exception occurs inside the with block."""
        import ensembl_orm.session as sess

        from ensembl_orm.session import get_session

        mock_engine = MagicMock()
        sess._engine = mock_engine

        with patch("ensembl_orm.session.Session") as mock_session_cls:
            mock_session = MagicMock()
            mock_session_cls.return_value = mock_session
            with pytest.raises(ValueError):
                with get_session():
                    raise ValueError("boom")

        mock_session.close.assert_called_once()

    def test_raises_when_engine_not_initialized(self):
        """get_session propagates EnsemblSessionError if engine not initialized."""
        from ensembl_orm.session import get_session

        with pytest.raises(EnsemblSessionError, match="Engine not initialized"):
            with get_session():
                pass


class TestCloseAllSessions:
    """Tests for close_all_sessions()."""

    def test_disposes_engine_and_clears_global(self):
        """close_all_sessions calls dispose() and sets _engine to None."""
        import ensembl_orm.session as sess

        from ensembl_orm.session import close_all_sessions

        mock_engine = MagicMock()
        sess._engine = mock_engine
        close_all_sessions()

        mock_engine.dispose.assert_called_once()
        assert sess._engine is None

    def test_idempotent_when_engine_already_none(self):
        """Calling close_all_sessions when _engine is None raises no error."""
        import ensembl_orm.session as sess

        from ensembl_orm.session import close_all_sessions

        assert sess._engine is None
        close_all_sessions()
        assert sess._engine is None

    def test_logs_info_on_dispose(self, caplog):
        """Info log is emitted when engine is disposed."""
        import ensembl_orm.session as sess

        from ensembl_orm.session import close_all_sessions

        mock_engine = MagicMock()
        sess._engine = mock_engine

        with caplog.at_level(logging.INFO, logger="ensembl_orm"):
            close_all_sessions()

        assert any("Engine disposed" in r.message for r in caplog.records)


class TestPublicAPIExports:
    """Tests that the session API is importable from ensembl_orm."""

    def test_imports_from_package_root(self):
        """Session functions are importable from the top-level package."""
        from ensembl_orm import (
            close_all_sessions,
            get_engine,
            get_session,
            initialize_engine,
        )

        assert callable(initialize_engine)
        assert callable(get_engine)
        assert callable(get_session)
        assert callable(close_all_sessions)

    def test_imports_are_same_objects(self):
        """Imported objects from __init__ are the same as from the module."""
        from ensembl_orm import get_engine, get_session, initialize_engine, close_all_sessions
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
