"""Database name discovery for Ensembl."""

import logging
from typing import Optional
from urllib.error import URLError
from urllib.request import urlopen

from sqlalchemy import create_engine, text

from ensembl_orm.config.database_settings import DatabaseSettings
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


def _resolve_database_name(settings: DatabaseSettings, version: int) -> str:
    """Query MySQL to find the exact database name for the given release version.

    Args:
        settings: Database connection settings.
        version: The Ensembl release version number.

    Returns:
        The full database name matching the version pattern.

    Raises:
        EnsemblDiscoveryError: If no matching database is found.
    """
    url = f"mysql+mysqldb://{settings.user}:{settings.password}@{settings.host}:{settings.port}/"
    engine = create_engine(url)
    pattern = f"homo_sapiens_core_{version}%"

    try:
        with engine.connect() as conn:
            result = conn.execute(text("SHOW DATABASES LIKE :pattern"), {"pattern": pattern})
            matches = [row[0] for row in result]
    finally:
        engine.dispose()

    if not matches:
        raise EnsemblDiscoveryError(f"No database matching pattern '{pattern}' found")

    matches.sort()
    if len(matches) > 1:
        logger.warning("Multiple databases matched: %s. Using first: %s", matches, matches[0])

    return matches[0]


def discover_database_name(settings: DatabaseSettings) -> str:
    """Discover and cache the current Ensembl database name.

    If a cached value exists, return it immediately. If ``settings.database``
    is explicitly set, return that without performing discovery. Otherwise,
    fetch the release version and resolve the database name, caching the
    result for subsequent calls.

    Args:
        settings: Database connection settings.

    Returns:
        The resolved or cached database name.

    Raises:
        EnsemblDiscoveryError: If version fetching or database resolution fails.
    """
    global _cached_database_name

    if _cached_database_name is not None:
        return _cached_database_name

    if settings.database:
        return settings.database

    version = _fetch_release_version()
    logger.info("Fetched Ensembl release version: %d", version)
    database_name = _resolve_database_name(settings, version)
    logger.info("Resolved database name: %s", database_name)
    _cached_database_name = database_name
    return database_name


def reset_cache() -> None:
    """Clear the cached database name.

    Intended for use in tests to ensure isolation between test cases.
    """
    global _cached_database_name
    _cached_database_name = None
