# Task ID: 14

**Title:** Xref, ObjectXref, and ExternalDb model implementations

**Status:** pending

**Dependencies:** 13

**Priority:** high

**Description:** Implement the ExternalDb, Xref, and ObjectXref SQLModel table models with correct column mappings, enum types, nullable constraints, and the Xref->ExternalDb and ObjectXref->Xref many-to-one relationships.

**Details:**

Create src/ensembl_orm/models/external_db.py:

```python
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, Text, Enum as SAEnum
from ensembl_orm.enums import ExternalDbStatus, ExternalDbType

class ExternalDb(SQLModel, table=True):
    __tablename__ = "external_db"

    external_db_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True),
    )
    db_name: str = Field(sa_column=Column(String(255), nullable=False))
    status: Optional[ExternalDbStatus] = Field(
        default=None,
        sa_column=Column(SAEnum(ExternalDbStatus), nullable=True),
    )
    priority: int = Field(sa_column=Column(Integer, nullable=False))
    dbprimary_acc_link: Optional[str] = Field(default=None, sa_column=Column(String(255), nullable=True))
    display_name_link: Optional[str] = Field(default=None, sa_column=Column(String(255), nullable=True))
    db_display_name: Optional[str] = Field(default=None, sa_column=Column(String(255), nullable=True))
    type: Optional[ExternalDbType] = Field(
        default=None,
        sa_column=Column(SAEnum(ExternalDbType), nullable=True),
    )
    secondary_db_name: Optional[str] = Field(default=None, sa_column=Column(String(255), nullable=True))
    description: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
    release: Optional[str] = Field(default=None, sa_column=Column(String(255), nullable=True))
```

Create src/ensembl_orm/models/xref.py with Xref model including external_db relationship (ForeignKey to external_db.external_db_id), using InfoType enum for info_type column.

Create src/ensembl_orm/models/object_xref.py with ObjectXref model including xref relationship (ForeignKey to xref.xref_id), using EnsemblObjectType enum for ensembl_object_type column.

Update models/__init__.py to export all three models. Write corresponding test files.

**Test Strategy:**

Test each model maps to correct __tablename__. Test ExternalDb has 11 columns with correct types and enum fields. Test Xref has 8 columns with InfoType enum for info_type. Test ObjectXref has 7 columns with EnsemblObjectType enum. Test enum fields accept valid values and reject invalid ones. Test Xref.external_db relationship defined with ForeignKey. Test ObjectXref.xref relationship defined with ForeignKey. Test all nullable columns accept None. Run: uv run pytest tests/models/test_external_db.py tests/models/test_xref.py tests/models/test_object_xref.py -v

## Subtasks

### 14.1. Implement ExternalDb SQLModel with enum-backed status and type fields

**Status:** pending  
**Dependencies:** None  

Create the ExternalDb SQLModel table model with correct __tablename__, columns, enum-backed status/type fields, and nullability settings.

**Details:**

Add src/ensembl_orm/models/external_db.py implementing the ExternalDb class as a SQLModel table. Use the provided skeleton: set __tablename__ = "external_db"; define external_db_id as an Optional[int] primary key with sa_column=Column(Integer, primary_key=True). Implement db_name (String(255), nullable=False), status (SAEnum(ExternalDbStatus), nullable=True), priority (Integer, nullable=False), dbprimary_acc_link, display_name_link, db_display_name, secondary_db_name, release (all String(255), nullable=True), description (Text, nullable=True), and type (SAEnum(ExternalDbType), nullable=True). Ensure Optional[...] typing matches nullable=True columns and that SAEnum uses the enum types from ensembl_orm.enums. Keep this model self-contained without relationships for now, ready to be referenced by Xref.

### 14.2. Implement Xref SQLModel with ExternalDb ForeignKey and InfoType enum

**Status:** pending  
**Dependencies:** 14.1  

Create the Xref SQLModel table model including ForeignKey to external_db.external_db_id, InfoType enum-backed info_type column, and relationship to ExternalDb.

**Details:**

Add src/ensembl_orm/models/xref.py defining class Xref(SQLModel, table=True) with __tablename__ = "xref". Define xref_id primary key (Optional[int], Column(Integer, primary_key=True)). Add columns matching schema (e.g. external_db_id, dbprimary_acc, display_label, version, description, info_type, info_text) with correct String/Text/Integer types and nullability per the Ensembl xref table. Use sa_column=Column(Integer, ForeignKey("external_db.external_db_id"), nullable=False) for external_db_id. Import InfoType enum from ensembl_orm.enums and map info_type using SAEnum(InfoType) with appropriate Optional typing/nullability. Add a Relationship to ExternalDb: external_db: Optional["ExternalDb"] = Relationship(back_populates="xrefs") and in ExternalDb add a matching xrefs: list["Xref"] = Relationship(back_populates="external_db") once both models are available. Ensure forward references are handled (string annotations and potential update_forward_refs in __init__ or module import order).

### 14.3. Implement ObjectXref SQLModel with Xref ForeignKey and EnsemblObjectType enum

**Status:** pending  
**Dependencies:** 14.2  

Create the ObjectXref SQLModel table model including ForeignKey to xref.xref_id, EnsemblObjectType enum-backed ensembl_object_type column, and relationship to Xref.

**Details:**

Add src/ensembl_orm/models/object_xref.py defining class ObjectXref(SQLModel, table=True) with __tablename__ = "object_xref". Implement primary key (e.g. object_xref_id: Optional[int] = Field(sa_column=Column(Integer, primary_key=True))) according to the schema used in the project. Add xref_id column as Integer with sa_column=Column(Integer, ForeignKey("xref.xref_id"), nullable=False) to link to Xref. Add ensembl_id (Integer, nullable=False) and ensembl_object_type using SAEnum(EnsemblObjectType) from ensembl_orm.enums with correct Optional typing/nullability. Include any additional columns (e.g. linkage_annotation, analysis_id, etc.) as required by the Ensembl object_xref schema, respecting nullability. Define relationship xref: Optional["Xref"] = Relationship(back_populates="object_xrefs") and add the inverse relationship object_xrefs: list["ObjectXref"] = Relationship(back_populates="xref") in the Xref model. Use string-based type hints for forward references and rely on import ordering or update_forward_refs as needed.

### 14.4. Update models package __init__ and handle forward references

**Status:** pending  
**Dependencies:** 14.1, 14.2, 14.3  

Export ExternalDb, Xref, and ObjectXref from the models package and ensure forward references in relationships are correctly resolved.

**Details:**

Edit src/ensembl_orm/models/__init__.py to import and expose ExternalDb, Xref, and ObjectXref (e.g. from .external_db import ExternalDb; from .xref import Xref; from .object_xref import ObjectXref; and define __all__ accordingly). Ensure import order does not cause circular import problems: either import models within __init__ in an order that lets SQLModel/SQLAlchemy resolve relationships, or, if needed, call SQLModel.metadata or model-specific update_forward_refs() once all three classes are imported. Confirm that external_db.xrefs, xref.external_db, xref.object_xrefs, and object_xref.xref relationship attributes can be imported from ensembl_orm.models without raising NameError or circular import issues. Keep __init__ consistent with how Gene and SeqRegion models are exported.

### 14.5. Create and run model tests for ExternalDb, Xref, and ObjectXref

**Status:** pending  
**Dependencies:** 14.1, 14.2, 14.3, 14.4  

Add pytest test modules to validate tablenames, columns, enums, relationships, and nullability for ExternalDb, Xref, and ObjectXref models.

**Details:**

Create tests/models/test_external_db.py to assert ExternalDb.__tablename__ == "external_db"; verify the expected number of columns (e.g. 11), column names, SQLAlchemy types, primary key, and that status/type columns use SAEnum(ExternalDbStatus/ExternalDbType) with correct nullability. Create tests/models/test_xref.py to assert Xref.__tablename__, count and names of columns, that info_type uses SAEnum(InfoType), external_db_id has a ForeignKey to external_db.external_db_id, and that the external_db relationship works (e.g. creating ExternalDb and Xref rows in a test database and accessing xref.external_db and external_db.xrefs). Create tests/models/test_object_xref.py to validate ObjectXref.__tablename__, columns (including xref_id, ensembl_id, ensembl_object_type), that ensembl_object_type uses SAEnum(EnsemblObjectType), and that the xref relationship is functional. Use a temporary in-memory SQLite or dedicated test database via the existing session/engine helpers. Include tests that enums accept valid values and raise on invalid assignments (either via Pydantic validation or database-level errors). Run pytest to ensure the new tests pass and do not interfere with existing suites.
