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
