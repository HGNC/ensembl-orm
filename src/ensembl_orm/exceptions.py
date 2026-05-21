"""Custom exceptions for the ensembl_orm package."""


class EnsemblDiscoveryError(Exception):
    """Raised when database name discovery fails."""


class EnsemblSessionError(Exception):
    """Raised when session operations fail due to an uninitialized engine."""
