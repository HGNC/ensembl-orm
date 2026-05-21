# Task ID: 16

**Title:** Integration verification, public API finalization, and documentation

**Status:** pending

**Dependencies:** 15

**Priority:** medium

**Description:** Finalize the public API exports in __init__.py, verify all models import correctly, run full test suite, apply linting/formatting with ruff, write README.md with installation and usage examples, and ensure package is installable as a git-source dependency.

**Details:**

1. Finalize src/ensembl_orm/__init__.py with all public exports:
```python
"""Read-only SQLModel ORM for the Ensembl homo_sapiens_core MySQL database."""

from ensembl_orm.config.database_settings import DatabaseSettings
from ensembl_orm.session import initialize_engine, get_engine, get_session, close_all_sessions
from ensembl_orm.exceptions import EnsemblDiscoveryError, EnsemblSessionError
from ensembl_orm.discovery import discover_database_name

from ensembl_orm.models.gene import Gene
from ensembl_orm.models.seq_region import SeqRegion
from ensembl_orm.models.xref import Xref
from ensembl_orm.models.object_xref import ObjectXref
from ensembl_orm.models.external_db import ExternalDb
from ensembl_orm.models.seq_region_attrib import SeqRegionAttrib
from ensembl_orm.models.karyotype import Karyotype

__all__ = [
    # Configuration
    "DatabaseSettings",
    # Session management
    "initialize_engine",
    "get_engine",
    "get_session",
    "close_all_sessions",
    # Discovery
    "discover_database_name",
    # Exceptions
    "EnsemblDiscoveryError",
    "EnsemblSessionError",
    # Models
    "Gene",
    "SeqRegion",
    "Xref",
    "ObjectXref",
    "ExternalDb",
    "SeqRegionAttrib",
    "Karyotype",
]
```

2. Finalize src/ensembl_orm/models/__init__.py to re-export all models.
3. Run ruff check src/ tests/ and ruff format src/ tests/ - fix any issues.
4. Run full test suite: uv run pytest tests/ -v --tb=short
5. Write README.md with:
   - Project description
   - Installation via git-source dependency (uv syntax)
   - Quick start example (matching Section 5.2 API)
   - Configuration (environment variables table)
   - Development setup
   - License (MIT)
6. Verify package metadata in pyproject.toml is complete and correct.
7. Test that `import ensembl_orm` works without errors (mock any DB connections).
8. Add conftest.py fixtures for mock_settings, mock_engine, mock_session, mock_version_response, mock_show_databases_result.

**Test Strategy:**

Run complete test suite: uv run pytest tests/ -v --tb=short. Verify all tests pass with 100% of specified test cases covered. Run ruff check src/ tests/ for linting issues. Run ruff format --check src/ tests/ for formatting. Verify `import ensembl_orm` succeeds and all __all__ members are accessible. Verify models can be used in SQLModel select() statements (construct queries without executing). Test that the package structure matches Section 2.3 exactly. Verify README.md examples are syntactically correct.

## Subtasks

### 16.1. Finalize top-level public API and __all__ in src/ensembl_orm/__init__.py

**Status:** pending  
**Dependencies:** None  

Complete the package-level __init__.py so that it exposes the intended public API, including configuration, session helpers, discovery utilities, exceptions, and core models via explicit imports and a well-defined __all__ list.

**Details:**

Edit src/ensembl_orm/__init__.py to match the proposed public API:
- Import DatabaseSettings, initialize_engine, get_engine, get_session, close_all_sessions, discover_database_name, EnsemblDiscoveryError, EnsemblSessionError.
- Import all core models (Gene, SeqRegion, Xref, ObjectXref, ExternalDb, SeqRegionAttrib, Karyotype) from src/ensembl_orm/models/.
- Define __all__ to list only the supported public symbols, in logical sections (config, session, discovery, exceptions, models).
- Ensure the module docstring concisely describes the package (read-only SQLModel ORM for Ensembl homo_sapiens_core).
Acceptance criteria:
- `from ensembl_orm import *` exposes exactly the names listed in __all__.
- `from ensembl_orm import DatabaseSettings, Gene, initialize_engine` works without ImportError.
- No top-level import in __init__.py attempts to connect to the database when imported (import is side-effect free aside from symbol loading).

### 16.2. Finalize src/ensembl_orm/models/__init__.py re-exports for all models

**Status:** pending  
**Dependencies:** None  

Create or refine the models package __init__.py so that it re-exports all SQLModel table classes that should be part of the public model API, using explicit imports and __all__ if appropriate.

**Details:**

Edit src/ensembl_orm/models/__init__.py to:
- Import each model class from its module, at minimum Gene, SeqRegion, Xref, ObjectXref, ExternalDb, SeqRegionAttrib, Karyotype.
- Optionally include other table models that exist in the project and are intended to be public.
- Define __all__ = ["Gene", "SeqRegion", "Xref", "ObjectXref", "ExternalDb", "SeqRegionAttrib", "Karyotype", ...] so star-imports from ensembl_orm.models are controlled.
- Avoid circular import issues; if necessary, structure imports so that models.__init__ only re-exports already-defined classes from individual modules rather than defining anything new.
Acceptance criteria:
- `from ensembl_orm.models import Gene, SeqRegion` works without ImportError.
- `from ensembl_orm.models import *` yields only the intended model symbols.
- Top-level import of ensembl_orm (which indirectly imports models) is still free of circular import errors.

### 16.3. Add and refine shared pytest fixtures in tests/conftest.py for DB and discovery mocking

**Status:** pending  
**Dependencies:** 16.1, 16.2  

Define reusable pytest fixtures in tests/conftest.py to provide mock DatabaseSettings, engine, session, and discovery responses so tests and smoke checks can run without connecting to a real Ensembl database.

**Details:**

Edit or create tests/conftest.py with fixtures such as:
- mock_settings: returns a DatabaseSettings instance pointed at a fake host/database or uses monkeypatch to override environment variables.
- mock_engine: provides a mocked SQLAlchemy engine (e.g., using create_engine with an in-memory SQLite URL or a MagicMock) that mimics the required interface.
- mock_session: yields a SQLModel Session or mock session object bound to mock_engine.
- mock_version_response: mocks the response of any version-discovery query (e.g., SHOW VARIABLES LIKE or SELECT VERSION()).
- mock_show_databases_result: mocks the SHOW DATABASES query used by discover_database_name so tests do not hit a real MySQL instance.
Ensure all fixtures are placed in tests/conftest.py to be globally available.
Acceptance criteria:
- Existing and new tests that rely on DB interactions can run without a live database.
- discover_database_name and session-related code paths can be tested using these fixtures.
- No test opens a real network connection to ensembldb.ensembl.org when using the default test configuration.

### 16.4. Run ruff check and ruff format on src/ and tests/ and resolve issues

**Status:** pending  
**Dependencies:** 16.1, 16.2, 16.3  

Execute ruff linting and formatting across the src/ and tests/ directories, then update code to satisfy all configured rules and formatting standards.

**Details:**

From the project root, run:
- `ruff check src/ tests/` to identify lint issues.
- `ruff format src/ tests/` to apply the configured code style.
Resolve any remaining warnings or errors manually, including import order, unused imports, and type-annotation style, while ensuring that changes do not alter behavior.
Re-run ruff after fixes to confirm a clean result.
Acceptance criteria:
- `ruff check src/ tests/` exits with status 0 and no reported violations.
- `ruff format src/ tests/` makes no further changes when run a second time (idempotent formatting).
- Imports and style in __init__.py files, models, and tests conform to the configured project style.

### 16.5. Run full pytest suite and fix integration issues across models and API

**Status:** pending  
**Dependencies:** 16.1, 16.2, 16.3, 16.4  

Execute the complete pytest suite, diagnose any failures related to model imports, fixtures, or public API usage, and apply fixes until all tests pass.

**Details:**

From the project root, run `uv run pytest tests/ -v --tb=short`.
Investigate and fix any failing tests or errors, focusing on:
- Import paths using the finalized public API (ensembl_orm and ensembl_orm.models).
- Tests that require updated fixtures from tests/conftest.py.
- Model relationship definitions and metadata consistency (e.g., Gene.seq_region foreign key definitions).
- Any regressions introduced by refactoring or formatting.
Iterate until the full test run is green.
Acceptance criteria:
- `uv run pytest tests/ -v --tb=short` completes successfully with exit code 0.
- No tests are skipped due to missing fixtures or misconfigured imports, unless explicitly and intentionally marked xfail/skip with justification.
- Coverage of API surface (config, session, discovery, models) is consistent with the project’s expectations.

### 16.6. Verify pyproject.toml metadata and git-source installability

**Status:** pending  
**Dependencies:** 16.5  

Review and update pyproject.toml to ensure all required metadata is present and that the project can be installed as a git-source dependency using tools like uv or pip.

**Details:**

Open pyproject.toml and verify that:
- The [project] table includes correct name, version, description, authors, license, readme, dependencies, and Python version (>=3.13).
- Optional dev dependencies (pytest, pytest-mock, ruff, etc.) are correctly listed under the appropriate section.
- Classifiers, URLs, and package layout (src/ensembl_orm) are correctly configured.
Then test installation:
- Use a local path or test repository URL to run `uv add --dev git+<repo-url>#egg=ensembl-orm` or equivalent pip command, ensuring the package installs and exposes the ensembl_orm top-level package.
Acceptance criteria:
- pyproject.toml passes any basic validation (e.g., `uv build` or `python -m build` succeeds if used).
- Installing from a git URL or local VCS checkout results in a working environment where `python -c "import ensembl_orm"` succeeds.
- The installed package version and metadata match expectations when inspected via `import importlib.metadata` or `pip show ensembl-orm`.

### 16.7. Write and align README.md with final public API and installation methods

**Status:** pending  
**Dependencies:** 16.1, 16.2, 16.6  

Create or update README.md to describe the project, document installation via git-source dependency, provide a quick-start example aligning with the finalized API, and include configuration, development, and license sections.

**Details:**

Edit README.md at the project root to include:
- A clear project description summarizing ensembl_orm as a read-only SQLModel ORM for the Ensembl homo_sapiens_core MySQL database.
- Installation instructions using git-source dependency syntax for uv (and optionally pip), referencing the correct project name and minimum Python version.
- A quick-start usage example that imports from ensembl_orm using the finalized API (e.g., DatabaseSettings, initialize_engine, get_session, Gene) and demonstrates a simple read-only query.
- A configuration section with a table documenting ENSEMBLDB_ environment variables used by DatabaseSettings, including defaults and meanings.
- A development setup section describing how to create a virtual environment, install dev dependencies, run ruff, and run pytest.
- A license section stating that the project uses the MIT license.
Acceptance criteria:
- README.md renders cleanly in Markdown viewers and contains no references to outdated module paths or APIs.
- The quick-start code block runs successfully when copied into a Python file in a correctly configured environment.
- Installation and configuration instructions align with pyproject.toml settings and actual behavior of DatabaseSettings and session helpers.

### 16.8. Perform final smoke test of import, basic query construction, and document limitations

**Status:** pending  
**Dependencies:** 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7  

Run a final integration smoke test to ensure `import ensembl_orm` works, core symbols from __all__ are accessible, and basic SQLModel query construction functions as expected without requiring a live database, then capture any known limitations for future work.

**Details:**

In a clean environment where the package has been installed from the git source, perform the following:
- Start a Python REPL or script and run `import ensembl_orm`.
- Verify access to key exports: DatabaseSettings, initialize_engine, get_engine, get_session, close_all_sessions, discover_database_name, EnsemblDiscoveryError, EnsemblSessionError, and core models like Gene and SeqRegion via both `ensembl_orm.Gene` and `from ensembl_orm import Gene`.
- Using a mocked or in-memory engine/session (e.g., via the fixtures design), construct a simple SQLModel query such as a select on Gene filtered by gene_id and ensure it compiles or executes against the mock backend without raising ORM-level errors.
- Confirm that import and basic usage do not trigger unintended side effects like immediate real DB connections.
- Note any remaining limitations or TODOs (e.g., unsupported tables, partial relationship coverage) and, if appropriate, add a short “Limitations / Future work” section in README.md or project documentation.
Acceptance criteria:
- All symbols listed in ensembl_orm.__all__ are importable and usable without AttributeError.
- Basic SQLModel queries involving the public models can be constructed and run against a test or mocked backend without schema mismatches.
- Any known limitations are documented in code comments or README.md so users understand the current scope of the library.
