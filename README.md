# ensembl-orm

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue.svg)](https://hgnc.github.io/ensembl-orm/)

Read-only SQLAlchemy ORM for the Ensembl `homo_sapiens_core` MySQL database.

## Installation

Add as a git-source dependency using `uv`:

```bash
uv add "git+https://github.com/HGNC/ensembl-orm.git"
```

Or with `pip`:

```bash
pip install "git+https://github.com/HGNC/ensembl-orm.git"
```

Requires Python >= 3.13.

## Quick start

```python
from sqlalchemy import select

from ensembl_orm import DatabaseSettings, Gene, get_session, initialize_engine

settings = DatabaseSettings(host="ensembldb.ensembl.org", port=5306)
initialize_engine(settings)

with get_session() as session:
    genes = session.scalars(select(Gene).limit(5)).all()
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
| `ENSEMBLDB_CHARSET` | `utf8mb4` | Connection charset enforced at connect (MySQL only) |
| `ENSEMBLDB_COLLATION` | _(empty)_ | Optional connection collation enforced at connect (MySQL only) |

> The canonical field name is `username`, so `ENSEMBLDB_USERNAME` is also
> accepted as an alias for `ENSEMBLDB_USER`.

> The `charset`/`collation` fields are inherited from `db-common` (v0.2.0+). On
> the MySQL driver, `utf8mb4` is now enforced on every pooled connection at
> connect time via `SET NAMES` (configurable through the env vars above); on
> the SQLite driver the fields are ignored.

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
