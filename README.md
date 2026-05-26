# ensembl-orm

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue.svg)](https://hgnc.github.io/ensembl-orm/)

Read-only SQLModel ORM for the Ensembl `homo_sapiens_core` MySQL database.

## Installation

Add as a git-source dependency using `uv`:

```bash
uv add "git+https://github.com/your-org/ensembl-orm.git"
```

Or with `pip`:

```bash
pip install "git+https://github.com/your-org/ensembl-orm.git"
```

Requires Python >= 3.13.

## Quick start

```python
from ensembl_orm import DatabaseSettings, initialize_engine, get_session, Gene

settings = DatabaseSettings(host="ensembldb.ensembl.org", port=5306)
initialize_engine(settings)

with get_session() as session:
    genes = session.query(Gene).limit(5).all()
    for gene in genes:
        print(gene.gene_id, gene.stable_id)
```

## Configuration

Settings are loaded from environment variables with the `ENSEMBLDB_` prefix.

| Variable | Default | Description |
| --- | --- | --- |
| `ENSEMBLDB_HOST` | `ensembldb.ensembl.org` | Database server hostname |
| `ENSEMBLDB_PORT` | `5306` | Database server port |
| `ENSEMBLDB_USER` | `anonymous` | Database user name |
| `ENSEMBLDB_PASSWORD` | _(empty)_ | Database user password |
| `ENSEMBLDB_DATABASE` | _(empty)_ | Target database name (auto-discovered if empty) |
| `ENSEMBLDB_POOL_SIZE` | `3` | Connection pool size |
| `ENSEMBLDB_POOL_RECYCLE` | `3600` | Seconds before a connection is recycled |

## Development

```bash
# Create virtual environment and install dev dependencies
uv sync --extra dev

# Run linter
uv run ruff check src/ tests/

# Run formatter
uv run ruff format src/ tests/

# Run tests
uv run pytest tests/ -v
```

## License

MIT
