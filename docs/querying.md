# Querying

`get_session()` yields a standard SQLAlchemy 2.0
[`Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html), so you query
with the `select()` API exactly as you would with any SQLAlchemy ORM. Every
session is read-only — `ensembl-orm` exposes no read-write sessions.

## Basic queries

```python
from sqlalchemy import select

from ensembl_orm import Gene, get_session

with get_session() as session:
    # Get a single gene by primary key
    gene = session.get(Gene, 1)

    # Query with filters
    genes = session.scalars(
        select(Gene).where(Gene.biotype == "protein_coding").limit(10)
    ).all()
```

## Relationships and joins

Models declare SQLAlchemy `relationship()` attributes, so related rows load
lazily from a gene:

```python
from sqlalchemy import select

from ensembl_orm import Gene, get_session

with get_session() as session:
    gene = session.scalars(select(Gene).limit(1)).first()
    print(gene.seq_region.name)  # related SeqRegion row
```

For explicit joins across tables, select both entities:

```python
from sqlalchemy import select

from ensembl_orm import Gene, SeqRegion, get_session

with get_session() as session:
    results = session.execute(select(Gene, SeqRegion).join(SeqRegion)).all()
```

## Read-only enforcement

Sessions from `get_session()` are read-only by design. The shared `db-common`
library attaches a SQLAlchemy `before_commit` event listener to each session that
raises `ReadOnlySessionError` the moment a commit is attempted, so any write path
is rejected before it reaches the database:

```python
from ensembl_orm import ReadOnlySessionError, get_session

with get_session() as session:
    genes = session.scalars(select(Gene).limit(5)).all()
    session.commit()  # raises ensembl_orm.ReadOnlySessionError
```
