"""Tests for the database discovery module."""

from unittest.mock import MagicMock, patch
from urllib.error import URLError

import pytest

from ensembl_orm.exceptions import EnsemblDiscoveryError


class TestFetchReleaseVersion:
    """Tests for _fetch_release_version()."""

    def test_returns_integer_version_on_success(self):
        """Successful response with '112\\n' body returns int 112."""
        from ensembl_orm.discovery import _fetch_release_version

        mock_body = MagicMock()
        mock_body.read.return_value = b"112\n"
        mock_body.__enter__ = MagicMock(return_value=mock_body)
        mock_body.__exit__ = MagicMock(return_value=False)

        with patch("ensembl_orm.discovery.urlopen", return_value=mock_body):
            result = _fetch_release_version()

        assert result is 112

    def test_raises_discovery_error_on_url_error(self):
        """URLError from urlopen is wrapped in EnsemblDiscoveryError."""
        from ensembl_orm.discovery import _fetch_release_version

        with patch("ensembl_orm.discovery.urlopen", side_effect=URLError("timeout")):
            with pytest.raises(EnsemblDiscoveryError, match="Failed to fetch Ensembl version"):
                _fetch_release_version()

    def test_raises_discovery_error_on_os_error(self):
        """OSError from urlopen is wrapped in EnsemblDiscoveryError."""
        from ensembl_orm.discovery import _fetch_release_version

        with patch("ensembl_orm.discovery.urlopen", side_effect=OSError("network down")):
            with pytest.raises(EnsemblDiscoveryError, match="Failed to fetch Ensembl version"):
                _fetch_release_version()

    def test_raises_discovery_error_on_non_integer_body(self):
        """Non-integer response body raises EnsemblDiscoveryError with raw content."""
        from ensembl_orm.discovery import _fetch_release_version

        mock_body = MagicMock()
        mock_body.read.return_value = b"not-a-number"
        mock_body.__enter__ = MagicMock(return_value=mock_body)
        mock_body.__exit__ = MagicMock(return_value=False)

        with patch("ensembl_orm.discovery.urlopen", return_value=mock_body):
            with pytest.raises(EnsemblDiscoveryError, match="Invalid version response"):
                _fetch_release_version()

    def test_strips_whitespace_before_parsing(self):
        """Leading/trailing whitespace is stripped before integer parsing."""
        from ensembl_orm.discovery import _fetch_release_version

        mock_body = MagicMock()
        mock_body.read.return_value = b"  115  \n"
        mock_body.__enter__ = MagicMock(return_value=mock_body)
        mock_body.__exit__ = MagicMock(return_value=False)

        with patch("ensembl_orm.discovery.urlopen", return_value=mock_body):
            result = _fetch_release_version()

        assert result is 115


class TestResolveDatabaseName:
    """Tests for _resolve_database_name()."""

    @pytest.fixture()
    def settings(self):
        """Provide default DatabaseSettings for tests."""
        from ensembl_orm.config.database_settings import DatabaseSettings

        return DatabaseSettings(
            host="localhost",
            port=3306,
            user="testuser",
            password="testpass",
        )

    def _make_mock_engine(self, database_names: list[str]):
        """Build a mock SQLAlchemy engine that returns the given database names."""
        mock_result = MagicMock()
        mock_result.__iter__ = MagicMock(return_value=iter([(name,) for name in database_names]))

        mock_conn = MagicMock()
        mock_conn.execute.return_value = mock_result
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        mock_engine = MagicMock()
        mock_engine.connect.return_value = mock_conn
        mock_engine.dispose = MagicMock()

        return mock_engine

    def test_returns_single_match(self, settings):
        """When one database matches, that name is returned."""
        from ensembl_orm.discovery import _resolve_database_name

        mock_engine = self._make_mock_engine(["homo_sapiens_core_112_38"])

        with patch("ensembl_orm.discovery.create_engine", return_value=mock_engine):
            result = _resolve_database_name(settings, 112)

        assert result == "homo_sapiens_core_112_38"

    def test_engine_disposed_after_query(self, settings):
        """Engine.dispose() is always called, even on success."""
        from ensembl_orm.discovery import _resolve_database_name

        mock_engine = self._make_mock_engine(["homo_sapiens_core_112_38"])

        with patch("ensembl_orm.discovery.create_engine", return_value=mock_engine):
            _resolve_database_name(settings, 112)

        mock_engine.dispose.assert_called_once()

    def test_raises_when_no_matches(self, settings):
        """EnsemblDiscoveryError raised when SHOW DATABASES returns no matches."""
        from ensembl_orm.discovery import _resolve_database_name

        mock_engine = self._make_mock_engine([])

        with patch("ensembl_orm.discovery.create_engine", return_value=mock_engine):
            with pytest.raises(EnsemblDiscoveryError, match="No database matching pattern"):
                _resolve_database_name(settings, 112)

        mock_engine.dispose.assert_called_once()

    def test_returns_first_alphabetically_on_multiple_matches(self, settings):
        """When multiple databases match, the lexicographically first is returned."""
        from ensembl_orm.discovery import _resolve_database_name

        mock_engine = self._make_mock_engine([
            "homo_sapiens_core_112_39",
            "homo_sapiens_core_112_38",
        ])

        with patch("ensembl_orm.discovery.create_engine", return_value=mock_engine):
            result = _resolve_database_name(settings, 112)

        assert result == "homo_sapiens_core_112_38"

    def test_logs_warning_on_multiple_matches(self, settings, caplog):
        """A warning is logged when multiple databases match."""
        import logging

        from ensembl_orm.discovery import _resolve_database_name

        mock_engine = self._make_mock_engine([
            "homo_sapiens_core_112_39",
            "homo_sapiens_core_112_38",
        ])

        with patch("ensembl_orm.discovery.create_engine", return_value=mock_engine), \
             caplog.at_level(logging.WARNING, logger="ensembl_orm"):
            _resolve_database_name(settings, 112)

        assert any("Multiple databases matched" in record.message for record in caplog.records)

    def test_show_databases_called_with_correct_pattern(self, settings):
        """SHOW DATABASES LIKE is called with the correct version-based pattern."""
        from sqlalchemy import text

        from ensembl_orm.discovery import _resolve_database_name

        mock_engine = self._make_mock_engine(["homo_sapiens_core_112_38"])

        with patch("ensembl_orm.discovery.create_engine", return_value=mock_engine):
            _resolve_database_name(settings, 112)

        mock_conn = mock_engine.connect.return_value.__enter__.return_value
        call_args = mock_conn.execute.call_args
        compiled = call_args[0][0].text
        assert "SHOW DATABASES LIKE" in compiled
        assert call_args[0][1] == {"pattern": "homo_sapiens_core_112%"} or \
               call_args[1].get("parameters") == {"pattern": "homo_sapiens_core_112%"}
