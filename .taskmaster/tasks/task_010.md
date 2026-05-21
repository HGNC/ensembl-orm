# Task ID: 10

**Title:** Database discovery module implementation

**Status:** done

**Dependencies:** 9 ✓

**Priority:** high

**Description:** Implement the discover_database_name() function in discovery.py that dynamically resolves the current Ensembl homo_sapiens_core database name by fetching the release version from the Ensembl FTP server and querying MySQL with SHOW DATABASES LIKE pattern. Includes in-memory caching and error handling.

**Details:**

Implement src/ensembl_orm/discovery.py:

```python
import logging
from urllib.request import urlopen
from urllib.error import URLError
from typing import Optional

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

from ensembl_orm.config.database_settings import DatabaseSettings
from ensembl_orm.exceptions import EnsemblDiscoveryError

logger = logging.getLogger("ensembl_orm")

_cached_database_name: Optional[str] = None
VERSION_URL = "http://ftp.ensembl.org/pub/VERSION"

def _fetch_release_version() -> int:
    """Fetch current Ensembl release version number."""
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
    """Query MySQL to find the exact database name for the given version."""
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
    """Discover and cache the current Ensembl database name."""
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
    """Clear the cached database name (for testing)."""
    global _cached_database_name
    _cached_database_name = None
```

Write tests/test_discovery.py covering all scenarios from Section 8.2.

**Test Strategy:**

Mock urlopen to return version string '112', verify _fetch_release_version returns 112. Mock network error, verify EnsemblDiscoveryError raised. Mock non-integer response, verify EnsemblDiscoveryError. Mock SQLAlchemy engine/connection to return database list ['homo_sapiens_core_112_38'], verify correct name returned. Test caching: call twice, verify only one network request. Test multiple matches: log warning, use first alphabetically. Test empty matches: raise EnsemblDiscoveryError. Test settings.database set skips discovery entirely. Run: uv run pytest tests/test_discovery.py -v

## Subtasks

### 10.1. Implement _fetch_release_version with error handling

**Status:** done  
**Dependencies:** None  

Implement the _fetch_release_version() helper function that fetches the current Ensembl release version from the FTP VERSION file using urlopen. Includes timeout configuration, URLError and OSError handling, and validation that the response is a valid integer. Raises EnsemblDiscoveryError on any failure.

**Details:**

Define the module-level VERSION_URL constant as 'http://ftp.ensembl.org/pub/VERSION'. Implement _fetch_release_version() to: (1) use urlopen with a 10-second timeout to fetch the VERSION file; (2) decode and strip the response content; (3) catch URLError and OSError, wrapping them in EnsemblDiscoveryError with a descriptive message; (4) attempt int() conversion on the content, raising EnsemblDiscoveryError with the raw content repr if ValueError occurs. Import urlopen from urllib.request, URLError from urllib.error, and EnsemblDiscoveryError from ensembl_orm.exceptions. Add appropriate logger import and module-level logger setup.

### 10.2. Implement _resolve_database_name with SQLAlchemy query

**Status:** done  
**Dependencies:** None  

Implement the _resolve_database_name() helper that constructs a MySQL connection URL from DatabaseSettings, creates a temporary SQLAlchemy engine, executes SHOW DATABASES LIKE with a version-based pattern, and returns the matching database name. Includes proper engine disposal and handling for zero or multiple matches.

**Details:**

Implement _resolve_database_name(settings: DatabaseSettings, version: int) -> str. Build the connection URL as f'mysql+mysqldb://{settings.user}:{settings.password}@{settings.host}:{settings.port}/' and create an engine via create_engine(). Define the pattern as f'homo_sapiens_core_{version}%' for the LIKE clause. Execute 'SHOW DATABASES LIKE :pattern' using text() and parameterized query to avoid SQL injection. Collect results as a list of strings from row[0]. Use a try/finally block to ensure engine.dispose() is always called. If no matches found, raise EnsemblDiscoveryError. If multiple matches found, sort the list, log a warning with all matches, and return the first (sorted) result. Import create_engine and text from sqlalchemy.

### 10.3. Implement discover_database_name with caching and override

**Status:** done  
**Dependencies:** 10.1, 10.2  

Implement the main discover_database_name() public function that orchestrates the discovery process. It should return the cached database name if available, fall back to settings.database if explicitly set, or invoke _fetch_release_version and _resolve_database_name to dynamically discover the name. Cache the result in the module-level _cached_database_name variable.

**Details:**

Declare module-level _cached_database_name as Optional[str] = None. Implement discover_database_name(settings: DatabaseSettings) -> str that: (1) checks if _cached_database_name is not None and returns it immediately (in-memory cache hit); (2) checks if settings.database is truthy and returns it directly without caching (explicit override from configuration); (3) calls _fetch_release_version() to get the version, logs it via logger.info; (4) calls _resolve_database_name(settings, version) to get the database name; (5) logs the resolved name; (6) stores the result in _cached_database_name and returns it. Use 'global _cached_database_name' declaration inside the function for assignment. All logging should use the module-level logger instance.

### 10.4. Implement reset_cache and module-level initialization

**Status:** done  
**Dependencies:** 10.3  

Implement the reset_cache() utility function that clears the module-level cached database name. Also ensure all module-level initialization is correct: logger setup, type annotations for the cache variable, and proper __all__ exports if applicable.

**Details:**

Implement reset_cache() -> None that uses 'global _cached_database_name' and sets it back to None. This function is primarily intended for testing purposes to reset state between test cases. Ensure the module-level logger is properly initialized with logging.getLogger('ensembl_orm'). Verify the _cached_database_name is typed as Optional[str] and initialized to None at module load. Ensure all imports are correctly organized at the top of the file (stdlib first, third-party second, local third). The module should be importable without side effects - no auto-discovery on import.

### 10.5. Write comprehensive tests in tests/test_discovery.py

**Status:** done  
**Dependencies:** 10.1, 10.2, 10.3, 10.4  

Create tests/test_discovery.py with full test coverage for all discovery module scenarios: successful version fetch, network errors, invalid version responses, successful database resolution, no matching databases, multiple matching databases, cache behavior, settings.database override, reset_cache functionality, and proper logging verification.

**Details:**

Create test_discovery.py with pytest fixtures and test classes organized by function. Use unittest.mock.patch to mock urlopen, create_engine, and the module-level _cached_database_name. Scenarios to cover: (1) TestFetchReleaseVersion: successful fetch returns int, URLError raises EnsemblDiscoveryError, OSError raises EnsemblDiscoveryError, non-integer content raises EnsemblDiscoveryError with repr in message, timeout behavior. (2) TestResolveDatabaseName: single match returns correctly, no match raises EnsemblDiscoveryError, multiple matches returns first sorted and logs warning, engine.dispose() called even on error, parameterized query used. (3) TestDiscoverDatabaseName: cache hit returns immediately without network/DB calls, settings.database bypasses discovery, full discovery flow works end-to-end, result is properly cached for subsequent calls. (4) TestResetCache: clears cached value, idempotent. (5) TestLogging: verify appropriate info and warning messages are logged. Use reset_cache() in setup/teardown or autouse fixtures to ensure test isolation.
