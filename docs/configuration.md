# Configuration

Settings are loaded from environment variables with the `ENSEMBLDB_` prefix.

| Variable | Default | Description |
| --- | --- | --- |
| `ENSEMBLDB_HOST` | `ensembldb.ensembl.org` | Database server hostname |
| `ENSEMBLDB_PORT` | `5306` | Database server port |
| `ENSEMBLDB_USER` | `anonymous` | Database user name |

> The canonical field name is `username`, so `ENSEMBLDB_USERNAME` is also
> accepted as an alias for `ENSEMBLDB_USER`.
| `ENSEMBLDB_PASSWORD` | _(empty)_ | Database user password |
| `ENSEMBLDB_DATABASE` | _(empty)_ | Target database name (auto-discovered if empty) |
| `ENSEMBLDB_POOL_SIZE` | `3` | Connection pool size |
| `ENSEMBLDB_POOL_RECYCLE` | `3600` | Seconds before a connection is recycled |

## Using defaults

The defaults point at the public Ensembl server with anonymous access:

```python
from ensembl_orm import DatabaseSettings, initialize_engine

settings = DatabaseSettings()
initialize_engine(settings)
```

## Using a .env file

Create a `.env` file (see `.env.example`):

```bash
ENSEMBLDB_HOST=ensembldb.ensembl.org
ENSEMBLDB_PORT=5306
ENSEMBLDB_USER=anonymous
ENSEMBLDB_PASSWORD=
ENSEMBLDB_DATABASE=
```

## Auto-discovery

When `ENSEMBLDB_DATABASE` is left empty, the library fetches the current Ensembl release
version and resolves the correct database name automatically
(e.g. `homo_sapiens_core_112_38`).
