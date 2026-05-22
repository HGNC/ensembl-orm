# Querying

## Basic queries

```python
from ensembl_orm import get_session, Gene
from sqlmodel import select

with get_session() as session:
    # Get a single gene by primary key
    gene = session.get(Gene, 1)

    # Query with filters
    genes = session.exec(
        select(Gene).where(Gene.biotype == "protein_coding").limit(10)
    ).all()
```

## Joins

```python
from ensembl_orm import get_session, Gene, SeqRegion
from sqlmodel import select

with get_session() as session:
    results = session.exec(
        select(Gene, SeqRegion).join(SeqRegion)
    ).all()
```

## Read-only enforcement

All sessions created via `get_session()` automatically run `SET SESSION TRANSACTION READ ONLY`. Any attempt to write will raise a database error.
