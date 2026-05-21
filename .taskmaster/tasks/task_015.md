# Task ID: 15

**Title:** SeqRegionAttrib and Karyotype model implementations

**Status:** pending

**Dependencies:** 14

**Priority:** medium

**Description:** Implement the SeqRegionAttrib model with composite primary key and the Karyotype model with its SeqRegion relationship, completing all 7 Ensembl table mappings.

**Details:**

Create src/ensembl_orm/models/seq_region_attrib.py:

```python
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint

class SeqRegionAttrib(SQLModel, table=True):
    __tablename__ = "seq_region_attrib"
    __table_args__ = (
        PrimaryKeyConstraint("seq_region_id", "attrib_type_id"),
    )

    seq_region_id: int = Field(sa_column=Column(Integer, nullable=False))
    attrib_type_id: int = Field(sa_column=Column(Integer, nullable=False))
    value: Optional[str] = Field(default=None, sa_column=Column(String(255), nullable=True))
```

Create src/ensembl_orm/models/karyotype.py:

```python
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, String, ForeignKey

class Karyotype(SQLModel, table=True):
    __tablename__ = "karyotype"

    karyotype_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True),
    )
    seq_region_id: int = Field(
        sa_column=Column(Integer, ForeignKey("seq_region.seq_region_id"), nullable=False)
    )
    seq_region_start: int = Field(sa_column=Column(Integer, nullable=False))
    seq_region_end: int = Field(sa_column=Column(Integer, nullable=False))
    band: Optional[str] = Field(default=None, sa_column=Column(String(255), nullable=True))
    stain: Optional[str] = Field(default=None, sa_column=Column(String(255), nullable=True))

    # Relationship
    seq_region: Optional["SeqRegion"] = Relationship()
```

Update models/__init__.py to export SeqRegionAttrib and Karyotype. Write tests/models/test_seq_region_attrib.py and tests/models/test_karyotype.py.

Ensure forward references are handled by updating models/__init__.py to import all models in correct order, using UPDATE_FORWARD_REFS if needed.

**Test Strategy:**

Test SeqRegionAttrib.__tablename__ == 'seq_region_attrib'. Test composite primary key is configured correctly via __table_args__. Test SeqRegionAttrib has 3 columns with correct types. Test Karyotype.__tablename__ == 'karyotype'. Test Karyotype has 6 columns with correct types. Test Karyotype.seq_region relationship is defined with ForeignKey. Test nullable columns (band, stain) accept None. Verify composite PK prevents duplicate (seq_region_id, attrib_type_id) pairs conceptually. Run: uv run pytest tests/models/test_seq_region_attrib.py tests/models/test_karyotype.py -v

## Subtasks

### 15.1. Implement SeqRegionAttrib SQLModel with composite primary key

**Status:** pending  
**Dependencies:** None  

Create the SeqRegionAttrib ORM model with the correct table name, composite primary key, and columns matching the Ensembl seq_region_attrib table.

**Details:**

Add src/ensembl_orm/models/seq_region_attrib.py defining class SeqRegionAttrib(SQLModel, table=True) with __tablename__ = 'seq_region_attrib'. Configure __table_args__ to use PrimaryKeyConstraint('seq_region_id', 'attrib_type_id') to represent the composite primary key. Implement three fields: seq_region_id: int, attrib_type_id: int (both non-nullable Integer), and value: Optional[str] with String(255) and nullable=True. Ensure imports are from sqlmodel (SQLModel, Field) and sqlalchemy (Column, Integer, String, PrimaryKeyConstraint). Include a brief class docstring describing the mapping.

### 15.2. Implement Karyotype SQLModel with SeqRegion ForeignKey and Relationship

**Status:** pending  
**Dependencies:** None  

Create the Karyotype ORM model with correct columns, ForeignKey to seq_region.seq_region_id, and a Relationship to the existing SeqRegion model.

**Details:**

Add src/ensembl_orm/models/karyotype.py defining class Karyotype(SQLModel, table=True) with __tablename__ = 'karyotype'. Implement columns: karyotype_id Optional[int] as primary key Integer, seq_region_id: int with ForeignKey('seq_region.seq_region_id'), seq_region_start: int, seq_region_end: int, band: Optional[str] = String(255), and stain: Optional[str] = String(255). Define seq_region: Optional['SeqRegion'] = Relationship() to represent the many-to-one link to SeqRegion. Explicitly note the dependency on the existing SeqRegion model (implemented in Task 13) being available as ensembl_orm.models.seq_region.SeqRegion; keep the type annotation as a forward reference string to be resolved in __init__.py.

### 15.3. Update models/__init__.py exports and forward-reference handling

**Status:** pending  
**Dependencies:** 15.1, 15.2  

Wire SeqRegionAttrib and Karyotype into the models package exports and ensure forward references to SeqRegion are resolved correctly.

**Details:**

Edit src/ensembl_orm/models/__init__.py to import and re-export SeqRegionAttrib and Karyotype alongside existing models (including the pre-existing SeqRegion model from Task 13). Update __all__ (or equivalent export list) to include 'SeqRegionAttrib' and 'Karyotype'. Ensure that the import order or explicit forward-reference resolution (e.g., using a project-level UPDATE_FORWARD_REFS helper or direct Karyotype.update_forward_refs(SeqRegion=SeqRegion)) correctly binds the 'SeqRegion' forward reference in the Karyotype.seq_region Relationship. Explicitly document that Karyotype depends on the existing SeqRegion model and that models.__init__ is responsible for making that relationship resolvable on import.

### 15.4. Write tests for SeqRegionAttrib model definition

**Status:** pending  
**Dependencies:** 15.1  

Create tests/models/test_seq_region_attrib.py to validate table name, composite primary key, and column definitions for SeqRegionAttrib.

**Details:**

Implement tests/models/test_seq_region_attrib.py. Add tests to assert SeqRegionAttrib.__tablename__ == 'seq_region_attrib'; that the SQLAlchemy table has a composite primary key over seq_region_id and attrib_type_id via __table_args__; and that the mapped columns are exactly seq_region_id, attrib_type_id (both non-nullable Integer) and value (nullable String with length 255). Use SQLModel.metadata.tables or SQLAlchemy inspection to verify primary key configuration and column metadata rather than relying only on annotations.

### 15.5. Write tests for Karyotype model columns and SeqRegion relationship

**Status:** pending  
**Dependencies:** 15.2, 15.3  

Create tests/models/test_karyotype.py to validate the Karyotype table mapping, column constraints, and the relationship to the existing SeqRegion model.

**Details:**

Implement tests/models/test_karyotype.py. Add tests to assert Karyotype.__tablename__ == 'karyotype'; verify the presence and types of karyotype_id, seq_region_id, seq_region_start, seq_region_end, band, and stain fields; and check nullability constraints (karyotype_id primary key, seq_region_id/start/end non-nullable, band and stain nullable with String(255)). Add tests that import both Karyotype and SeqRegion (from ensembl_orm.models) and verify that Karyotype.seq_region is configured as a Relationship targeting the SeqRegion class, confirming the explicit dependency on the existing SeqRegion model and that forward references were resolved via models.__init__.
