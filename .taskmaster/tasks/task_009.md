# Task ID: 9

**Title:** Project scaffolding and DatabaseSettings configuration

**Status:** done

**Dependencies:** None

**Priority:** high

**Description:** Create the project directory structure, pyproject.toml with all dependencies, and implement the DatabaseSettings Pydantic BaseSettings class with ENSEMBLDB_ prefixed environment variable support. Includes custom exceptions module, __init__.py public API stubs, and all project boilerplate files.

**Details:**

1. Create the full directory tree as specified in Section 2.3:
   - src/ensembl_orm/config/, src/ensembl_orm/models/, tests/models/
2. Write pyproject.toml exactly as specified in Section 9.1 with:
   - Python >=3.13 requirement
   - Dependencies: mysqlclient>=2.2.0, sqlalchemy>=2.0.46, sqlmodel>=0.0.33, pydantic>=2.12.5, pydantic-settings>=2.12.0
   - Dev dependencies: pytest>=9.0.3, pytest-mock>=3.14.0, ruff>=0.15.12
   - pytest and ruff configuration sections
3. Create .gitignore (Python project template), .env.example (ENSEMBLDB_HOST/PORT/USER/PASSWORD), .markdownlint.json, LICENSE (MIT)
4. Implement src/ensembl_orm/config/database_settings.py:
```python
from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    host: str = "ensembldb.ensembl.org"
    port: int = 5306
    user: str = "anonymous"
    password: str = ""
    database: str = ""
    pool_size: int = 3
    pool_recycle: int = 3600

    model_config = {"env_prefix": "ENSEMBLDB_"}

    @property
    def connection_url(self) -> str:
        return f"mysql+mysqldb://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
```
5. Create src/ensembl_orm/exceptions.py:
```python
class EnsemblDiscoveryError(Exception):
    """Raised when database name discovery fails."""

class EnsemblSessionError(Exception):
    """Raised when session operations fail due to uninitialized engine."""
```
6. Create stub __init__.py files for config/, models/, and the main package with placeholder public API exports.
7. Create tests/conftest.py with shared fixtures.
8. Write tests/test_database_settings.py.

**Test Strategy:**

Test DatabaseSettings defaults load correctly (host=ensembldb.ensembl.org, port=5306, user=anonymous, password='', database='', pool_size=3, pool_recycle=3600). Test environment variable override using monkeypatch. Test connection_url property formats correctly with and without password. Test port validation rejects non-integer values. Verify ENSEMBLDB_ prefix is required. Run: uv run pytest tests/test_database_settings.py -v

## Subtasks

### 9.1. Create full directory tree structure

**Status:** done  
**Dependencies:** None  

Create the complete project directory hierarchy including src/ensembl_orm/, src/ensembl_orm/config/, src/ensembl_orm/models/, tests/, and tests/models/ directories. Create empty __init__.py files where needed to establish the package structure.

**Details:**

Create the following directory tree:
- src/ensembl_orm/ (main package)
- src/ensembl_orm/config/ (configuration subpackage)
- src/ensembl_orm/models/ (models subpackage)
- tests/ (test directory)
- tests/models/ (model tests subdirectory)

Create placeholder __init__.py files in:
- src/ensembl_orm/__init__.py
- src/ensembl_orm/config/__init__.py
- src/ensembl_orm/models/__init__.py
- tests/__init__.py
- tests/models/__init__.py

Completion criteria: All directories exist and Python can recognize each directory as a package via __init__.py files.

### 9.2. Author pyproject.toml with dependencies and tool configs

**Status:** done  
**Dependencies:** 9.1  

Write the pyproject.toml file at the project root with exact Python >=3.13 requirement, runtime dependencies (mysqlclient>=2.2.0, sqlalchemy>=2.0.46, sqlmodel>=0.0.33, pydantic>=2.12.5, pydantic-settings>=2.12.0), dev dependencies (pytest>=9.0.3, pytest-mock>=3.14.0, ruff>=0.15.12), and pytest and ruff configuration sections.

**Details:**

File: pyproject.toml (project root)

Must include:
- [build-system] with hatchling backend
- [project] section with name='ensembl-orm', version, python requirement '>=3.13'
- dependencies list: mysqlclient>=2.2.0, sqlalchemy>=2.0.46, sqlmodel>=0.0.33, pydantic>=2.12.5, pydantic-settings>=2.12.0
- [project.optional-dependencies] dev section: pytest>=9.0.3, pytest-mock>=3.14.0, ruff>=0.15.12
- [tool.pytest.ini_options] with testpaths=['tests'] and appropriate settings
- [tool.ruff] configuration with line length, target-version, and selected rules
- [tool.hatch.build.targets.wheel] pointing packages to src layout

Completion criteria: File parses correctly with 'tomllib' or 'python -c import tomllib'. All dependency versions match specification exactly.

### 9.3. Create project boilerplate files

**Status:** done  
**Dependencies:** 9.1  

Create all project boilerplate files: .gitignore (Python project template), .env.example (with ENSEMBLDB_ prefixed environment variables), .markdownlint.json, LICENSE (MIT), and any initial README stub.

**Details:**

Files to create at project root:

1. .gitignore - Standard Python project template including:
   - __pycache__/, *.py[cod], *$py.class
   - *.egg-info/, dist/, build/
   - .eggs/, *.egg
   - .tox/, .nox/
   - .pytest_cache/
   - .ruff_cache/
   - .env (actual env file with secrets)
   - .venv/, venv/
   - *.so

2. .env.example - Template with commented examples:
   ENSEMBLDB_HOST=ensembldb.ensembl.org
   ENSEMBLDB_PORT=5306
   ENSEMBLDB_USER=anonymous
   ENSEMBLDB_PASSWORD=
   ENSEMBLDB_DATABASE=

3. .markdownlint.json - Standard markdown linting configuration

4. LICENSE - MIT License text with copyright holder and year

5. README.md - Initial stub with project name, brief description, and placeholder sections

Completion criteria: All 5 files exist at project root with appropriate content.

### 9.4. Implement DatabaseSettings, exceptions, and package __init__.py stubs

**Status:** done  
**Dependencies:** 9.1  

Implement the DatabaseSettings Pydantic BaseSettings class in config/database_settings.py with ENSEMBLDB_ env prefix, create the exceptions module with EnsemblDiscoveryError and EnsemblSessionError, and update all __init__.py files with placeholder public API exports.

**Details:**

Files to create/modify:

1. src/ensembl_orm/config/database_settings.py:
   - Import BaseSettings from pydantic_settings
   - Define DatabaseSettings(BaseSettings) with fields:
     * host: str = 'ensembldb.ensembl.org'
     * port: int = 5306
     * user: str = 'anonymous'
     * password: str = ''
     * database: str = ''
     * pool_size: int = 3
     * pool_recycle: int = 3600
   - model_config = {'env_prefix': 'ENSEMBLDB_'}
   - @property connection_url returning 'mysql+mysqldb://{user}:{password}@{host}:{port}/{database}'

2. src/ensembl_orm/exceptions.py:
   - class EnsemblDiscoveryError(Exception) with docstring
   - class EnsemblSessionError(Exception) with docstring

3. Update __init__.py files with exports:
   - src/ensembl_orm/__init__.py: Export DatabaseSettings, exceptions
   - src/ensembl_orm/config/__init__.py: Export DatabaseSettings
   - src/ensembl_orm/models/__init__.py: Placeholder for future model exports

Completion criteria: DatabaseSettings instantiates with defaults, reads ENSEMBLDB_ prefixed env vars, and connection_url property formats correctly.

### 9.5. Write tests for DatabaseSettings and create conftest.py

**Status:** done  
**Dependencies:** 9.2, 9.4  

Create tests/conftest.py with shared fixtures and tests/test_database_settings.py covering default values, environment variable overrides via monkeypatch, connection_url property formatting, port validation, and empty password handling.

**Details:**

Files to create:

1. tests/conftest.py:
   - Shared fixtures for DatabaseSettings instances
   - Fixtures for monkeypatching environment variables
   - Common test utilities

2. tests/test_database_settings.py:
   Test cases:
   - test_default_settings: Verify default values (host=ensembldb.ensembl.org, port=5306, user=anonymous, password='', database='', pool_size=3, pool_recycle=3600)
   - test_env_override_host: Using monkeypatch to set ENSEMBLDB_HOST and verify override
   - test_env_override_port: Using monkeypatch to set ENSEMBLDB_PORT and verify override
   - test_env_override_multiple: Override multiple env vars simultaneously
   - test_connection_url_format: Verify 'mysql+mysqldb://user:password@host:port/database' format
   - test_connection_url_no_password: Verify correct format when password is empty
   - test_port_validation: Verify port accepts valid integers from env
   - test_pool_settings_override: Verify pool_size and pool_recycle can be overridden

Completion criteria: All tests pass with 'pytest tests/test_database_settings.py'. Tests cover default loading, env override, and connection_url formatting.
