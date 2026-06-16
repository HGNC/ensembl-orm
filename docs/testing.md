# Testing

Tests are located in the `tests/` directory and use `pytest` with `pytest-mock`.

## Run all tests

```bash
uv run pytest tests/ -v
```

## Run with coverage

```bash
uv run pytest tests/ -v --cov=ensembl_orm --cov-report=term-missing
```

## Run a specific test file

```bash
uv run pytest tests/models/test_gene.py -v
```

## Test structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_boilerplate.py      # Project structure validation
├── test_database_settings.py # Configuration tests
├── test_directory_structure.py
├── test_discovery.py        # Database name discovery
├── test_enums.py            # Enum definition tests
├── test_implementation.py   # Import and contract tests
├── test_integration.py      # End-to-end db-common stack smoke (SQLite)
├── test_public_api_exports.py
├── test_pyproject.py        # pyproject.toml validation
├── test_session.py          # Session management tests
└── models/
    ├── test_external_db.py
    ├── test_gene.py
    ├── test_karyotype.py
    ├── test_model_exports.py
    ├── test_object_xref.py
    ├── test_seq_region.py
    ├── test_seq_region_attrib.py
    └── test_xref.py
```

All tests are fully mocked and do not require a live database connection.
