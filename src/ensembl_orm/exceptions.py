"""Custom exceptions for the ensembl_orm package.

The session-management errors come from the shared ``db-common`` hierarchy
(:class:`db_common.SessionError` / :class:`db_common.ReadOnlySessionError`)
and are re-exported here so callers can import them from ``ensembl_orm``.
``EnsemblDiscoveryError`` stays Ensembl-specific.
"""

from db_common import ReadOnlySessionError, SessionError

__all__ = ["EnsemblDiscoveryError", "SessionError", "ReadOnlySessionError"]


class EnsemblDiscoveryError(Exception):
    """Raised when database name discovery fails."""
