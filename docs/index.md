# ensembl-orm

Read-only SQLAlchemy ORM for the Ensembl `homo_sapiens_core` MySQL database.

## Features

- Type-safe SQLAlchemy ORM models mapping Ensembl database tables
- Read-only session with automatic transaction enforcement
- Auto-discovery of database name from Ensembl release version
- Python Enum types matching MySQL ENUM columns
- Configuration via environment variables with Pydantic validation

## Quick Example

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
