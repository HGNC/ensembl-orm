# Task ID: 13

**Title:** Gene and SeqRegion model implementations

**Status:** pending

**Dependencies:** 11 ✓

**Priority:** high

**Description:** Implement the Gene and SeqRegion SQLModel table models with correct column mappings, types, nullable constraints, and the Gene->SeqRegion many-to-one relationship.

**Details:**

Create src/ensembl_orm/models/gene.py:

```python
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime

class Gene(SQLModel, table=True):
    __tablename__ = "gene"

    gene_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True),
    )
    biotype: str = Field(sa_column=Column(String(255), nullable=False))
    analysis_id: int = Field(sa_column=Column(Integer, nullable=False))
    seq_region_id: int = Field(sa_column=Column(Integer, nullable=False))
    seq_region_start: int = Field(sa_column=Column(Integer, nullable=False))
    seq_region_end: int = Field(sa_column=Column(Integer, nullable=False))
    seq_region_strand: int = Field(sa_column=Column(Integer, nullable=False))
    display_xref_id: Optional[int] = Field(default=None, sa_column=Column(Integer, nullable=True))
    source: str = Field(sa_column=Column(String(255), nullable=False))
    description: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
    is_current: bool = Field(sa_column=Column(Boolean, nullable=False))
    canonical_transcript_id: Optional[int] = Field(default=None, sa_column=Column(Integer, nullable=True))
    canonical_translation_id: Optional[int] = Field(default=None, sa_column=Column(Integer, nullable=True))
    stable_id: Optional[str] = Field(default=None, sa_column=Column(String(128), nullable=True))
    version: Optional[int] = Field(default=None, sa_column=Column(Integer, nullable=True))
    created_date: Optional[datetime] = Field(default=None, sa_column=Column(DateTime, nullable=True))
    modified_date: Optional[datetime] = Field(default=None, sa_column=Column(DateTime, nullable=True))

    # Relationship
    seq_region: Optional["SeqRegion"] = Relationship()
```

Create src/ensembl_orm/models/seq_region.py:

```python
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String

class SeqRegion(SQLModel, table=True):
    __tablename__ = "seq_region"

    seq_region_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True),
    )
    name: str = Field(sa_column=Column(String(255), nullable=False))
    coord_system_id: int = Field(sa_column=Column(Integer, nullable=False))
    length: int = Field(sa_column=Column(Integer, nullable=False))
```

Update models/__init__.py to export Gene and SeqRegion. Note: Gene.seq_region relationship requires a ForeignKey declaration pointing to SeqRegion.seq_region_id via sa_column=Column(Integer, ForeignKey('seq_region.seq_region_id'), nullable=False) on the seq_region_id field.

Write tests/models/test_gene.py and tests/models/test_seq_region.py.

**Test Strategy:**

Test Gene.__tablename__ == 'gene'. Test Gene has all 17 columns with correct types. Test nullable fields (description, stable_id, etc.) accept None. Test non-nullable fields are required. Test Gene.seq_region relationship is defined. Test SeqRegion.__tablename__ == 'seq_region'. Test SeqRegion has all 4 columns with correct types. Verify SQLModel metadata reflects correct column types. Verify no DDL generation occurs (metadata.create_all never called). Run: uv run pytest tests/models/test_gene.py tests/models/test_seq_region.py -v

## Subtasks

### 13.1. Implement SeqRegion SQLModel table in src/ensembl_orm/models/seq_region.py

**Status:** pending  
**Dependencies:** None  

Create the SeqRegion SQLModel table model with correct table name, primary key, columns, types, and nullability.

**Details:**

Add src/ensembl_orm/models/seq_region.py defining class SeqRegion(SQLModel, table=True) with __tablename__ = 'seq_region'. Implement seq_region_id as an optional int primary key using Field with sa_column=Column(Integer, primary_key=True). Define name as a non-nullable String(255), coord_system_id as a non-nullable Integer, and length as a non-nullable Integer using Field(sa_column=Column(..., nullable=False)). Ensure imports for SQLModel, Field, and the relevant SQLAlchemy Column and type classes are present and consistent with project style.

### 13.2. Implement Gene SQLModel table with columns and seq_region_id ForeignKey

**Status:** pending  
**Dependencies:** 13.1  

Create the Gene SQLModel table model with all specified columns, types, nullability, and a ForeignKey from seq_region_id to SeqRegion.seq_region_id.

**Details:**

Add src/ensembl_orm/models/gene.py defining class Gene(SQLModel, table=True) with __tablename__ = 'gene'. Implement gene_id as an optional int primary key. Add all required columns: biotype, analysis_id, seq_region_id, seq_region_start, seq_region_end, seq_region_strand, display_xref_id, source, description, is_current, canonical_transcript_id, canonical_translation_id, stable_id, version, created_date, modified_date using Field(sa_column=Column(...)) with correct SQLAlchemy types and nullable flags per the specification. For seq_region_id, configure sa_column=Column(Integer, ForeignKey('seq_region.seq_region_id'), nullable=False) to enforce the many-to-one FK. Import ForeignKey from sqlalchemy and ensure no relationship configuration is added or modified yet (that will be handled separately).

### 13.3. Configure Gene.seq_region Relationship and update model exports

**Status:** pending  
**Dependencies:** 13.1, 13.2  

Define the Gene.seq_region Relationship to SeqRegion, handle forward references cleanly, and export both models from the models package.

**Details:**

In gene.py, add or finalize the attribute seq_region: Optional['SeqRegion'] = Relationship() to represent the many-to-one link from Gene to SeqRegion. Ensure SQLModel/SQLAlchemy can resolve the forward reference by either using from __future__ import annotations or wrapping imports in a TYPE_CHECKING block, e.g., if TYPE_CHECKING: from ensembl_orm.models.seq_region import SeqRegion. Confirm there is no circular import at runtime. Optionally configure Relationship arguments (e.g., back_populates) if a reciprocal relationship is later desired, but keep scope to the required Gene->SeqRegion navigation for now. In src/ensembl_orm/models/__init__.py, import and expose Gene and SeqRegion so they are part of the models public API, taking care not to introduce import cycles.

### 13.4. Write tests for SeqRegion and Gene models, including relationships

**Status:** pending  
**Dependencies:** 13.1, 13.2, 13.3  

Create tests for SeqRegion and Gene models covering table names, columns, nullability, foreign key, and the Gene->SeqRegion relationship.

**Details:**

Add tests/models/test_seq_region.py to validate the SeqRegion model and tests/models/test_gene.py to validate the Gene model. For SeqRegion, test __tablename__, presence and types of seq_region_id, name, coord_system_id, and length, and that the primary key and nullability align with the schema. For Gene, test __tablename__, that all configured columns exist with correct types and nullable flags, and that seq_region_id has a ForeignKey to seq_region.seq_region_id. Add tests that constructing model instances respects required vs optional fields and that nullable fields accept None. Using a temporary database and SQLModel Session, insert a SeqRegion and a Gene referencing it, commit, and assert that querying Gene and accessing gene.seq_region yields the associated SeqRegion instance. Keep tests consistent with existing project testing patterns and fixtures.
