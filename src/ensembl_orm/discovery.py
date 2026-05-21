"""Database name discovery for Ensembl."""

import logging
from typing import Optional
from urllib.error import URLError
from urllib.request import urlopen

from ensembl_orm.exceptions import EnsemblDiscoveryError

logger = logging.getLogger("ensembl_orm")

_cached_database_name: Optional[str] = None
VERSION_URL = "http://ftp.ensembl.org/pub/VERSION"


def _fetch_release_version() -> int:
    """Fetch the current Ensembl release version number from the FTP server.

    Returns:
        The release version as an integer.

    Raises:
        EnsemblDiscoveryError: If the version cannot be fetched or parsed.
    """
    try:
        with urlopen(VERSION_URL, timeout=10) as response:
            content = response.read().decode("utf-8").strip()
    except (URLError, OSError) as e:
        raise EnsemblDiscoveryError(f"Failed to fetch Ensembl version: {e}") from e

    try:
        return int(content)
    except ValueError:
        raise EnsemblDiscoveryError(f"Invalid version response: {content!r}")
