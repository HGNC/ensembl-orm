# Task ID: 12

**Title:** Enum definitions for Ensembl column types

**Status:** pending

**Dependencies:** 9 ✓

**Priority:** medium

**Description:** Define the four StrEnum classes (EnsemblObjectType, ExternalDbStatus, InfoType, ExternalDbType) that map to MySQL ENUM columns in the Ensembl database, placed in enums.py.

**Details:**

Create src/ensembl_orm/enums.py:

```python
from enum import StrEnum, unique

@unique
class EnsemblObjectType(StrEnum):
    """Represent object types for the object_xref.ensembl_object_type column.

    Attributes:
        GENE: Represent a gene object type.
        TRANSCRIPT: Represent a transcript object type.
        TRANSLATION: Represent a translation object type.
    """
    GENE = "Gene"
    TRANSCRIPT = "Transcript"
    TRANSLATION = "Translation"

@unique
class ExternalDbStatus(StrEnum):
    """Represent status values for the external_db.status column.

    Attributes:
        KNOWN: Represent a known external database status.
        XREF: Represent a cross-reference external database status.
        DUMPED: Represent a dumped external database status.
        DEPENDENT: Represent a dependent external database status.
    """
    KNOWN = "KNOWN"
    XREF = "XREF"
    DUMPED = "DUMPED"
    DEPENDENT = "DEPENDENT"

@unique
class InfoType(StrEnum):
    """Represent info type values for the xref.info_type column.

    Attributes:
        NONE: Represent no specific info type.
        PROBE: Represent a probe info type.
        DEPENDENT: Represent a dependent info type.
        DIRECT: Represent a direct info type.
        INFERRED_PAIR: Represent an inferred pair info type.
        PROBE2TRANSCRIPT: Represent a probe-to-transcript info type.
        UNMAPPED: Represent an unmapped info type.
        CHECKSUM: Represent a checksum info type.
    """
    NONE = "NONE"
    PROBE = "PROBE"
    DEPENDENT = "DEPENDENT"
    DIRECT = "DIRECT"
    INFERRED_PAIR = "INFERRED_PAIR"
    PROBE2TRANSCRIPT = "PROBE2TRANSCRIPT"
    UNMAPPED = "UNMAPPED"
    CHECKSUM = "CHECKSUM"

@unique
class ExternalDbType(StrEnum):
    """Represent database type values for the external_db.type column.

    Attributes:
        PRIMARY: Represent a primary external database type.
        SECONDARY: Represent a secondary external database type.
        MISC: Represent a miscellaneous external database type.
        CHECKSUM: Represent a checksum external database type.
        DEPENDENT: Represent a dependent external database type.
        IMAGE_DEPICTION: Represent an image depiction external database type.
    """
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    MISC = "MISC"
    CHECKSUM = "CHECKSUM"
    DEPENDENT = "DEPENDENT"
    IMAGE_DEPICTION = "IMAGE_DEPICTION"
```

Note: EnsemblObjectType uses mixed-case values (Gene, Transcript, Translation) to match the actual MySQL ENUM column definitions, while others use uppercase. All classes use the `@unique` decorator per AGENTS.md guidelines. All docstrings follow Google style and use action verbs ("Represent" not "Represents"). Update src/ensembl_orm/__init__.py (the main package) to re-export enums via `__all__`. Enums are not models and should not be exported from models/__init__.py.

**Test Strategy:**

Verify each enum has exactly the specified members with correct string values. Test that StrEnum values are strings (isinstance check). Test that invalid values raise ValueError when constructing from string. Test EnsemblObjectType('Gene') == 'Gene'. Test all enum members are accessible and iterable. Verify no duplicate values across unrelated enums don't cause conflicts. Verify @unique decorator is applied by confirming no duplicate values exist within each enum. Test string comparison equality critical for SQLAlchemy queries: assert EnsemblObjectType.GENE == "Gene" evaluates to True for all members across all enums. Test that enum classes work with sqlalchemy.Enum() column type (e.g., sqlalchemy.Enum(EnsemblObjectType) can be instantiated and used in column definitions) since the purpose is ORM column mapping. Run: uv run pytest tests/test_enums.py -v (create this test file)

## Subtasks

### 12.1. Create tests/test_enums.py to validate enum behavior (RED phase)

**Status:** pending  
**Dependencies:** None  

Create the test module FIRST with failing tests that define the expected behavior of all four StrEnum classes. This is the Red phase of TDD — tests must fail because enums.py does not yet exist. Tests cover: correct members and values, string comparison equality, construction from strings, invalid value handling, iteration, @unique enforcement, and SQLAlchemy Enum column type integration.

**Details:**

Create tests/test_enums.py (flat structure, consistent with tests/test_discovery.py, tests/test_session.py).

Import all four enums from their public path: `from ensembl_orm.enums import EnsemblObjectType, ExternalDbStatus, InfoType, ExternalDbType`. These imports WILL FAIL in the Red phase because enums.py does not exist yet — that is expected and correct.

Test cases to implement:

1. **Member completeness and values** (parametrized for each enum):
   - EnsemblObjectType members: {GENE="Gene", TRANSCRIPT="Transcript", TRANSLATION="Translation"}
   - ExternalDbStatus members: {KNOWN="KNOWN", XREF="XREF", DUMPED="DUMPED", DEPENDENT="DEPENDENT"}
   - InfoType members: {NONE="NONE", PROBE="PROBE", DEPENDENT="DEPENDENT", DIRECT="DIRECT", INFERRED_PAIR="INFERRED_PAIR", PROBE2TRANSCRIPT="PROBE2TRANSCRIPT", UNMAPPED="UNMAPPED", CHECKSUM="CHECKSUM"}
   - ExternalDbType members: {PRIMARY="PRIMARY", SECONDARY="SECONDARY", MISC="MISC", CHECKSUM="CHECKSUM", DEPENDENT="DEPENDENT", IMAGE_DEPICTION="IMAGE_DEPICTION"}
   - Assert `{m.name for m in EnumClass}` matches expected names.
   - Assert each member's `.value` equals the expected string.
   - Assert `isinstance(member.value, str)` for all members.

2. **String comparison equality** (critical for SQLAlchemy queries):
   - For every member of every enum, assert `member == member.value` (e.g., `EnsemblObjectType.GENE == "Gene"`).
   - This ensures SQLAlchemy filter expressions like `session.query(X).where(X.type == EnsemblObjectType.GENE)` work correctly.

3. **Construction from valid strings** (parametrized):
   - `assert EnsemblObjectType("Gene") is EnsemblObjectType.GENE`
   - `assert EnsemblObjectType("Gene").value == "Gene"`
   - At least one representative member per enum.

4. **Invalid value handling** (parametrized):
   - `pytest.raises(ValueError)` for each enum with "INVALID"
   - `pytest.raises(ValueError)` for wrong case (e.g., `EnsemblObjectType("gene")`)

5. **Iteration and len**:
   - `assert len(EnsemblObjectType) == 3`, etc.
   - `assert list(EnsemblObjectType)` returns all members.

6. **@unique enforcement**:
   - Confirm no duplicate values within each enum by checking `len(set(m.value for m in EnumClass)) == len(EnumClass)`.

7. **SQLAlchemy Enum integration**:
   - `from sqlalchemy import Enum as SAEnum`
   - `SAEnum(EnsemblObjectType)` instantiates without error for all four enum classes.
   - Optionally: define a minimal Column with the SAEnum type to verify ORM column definition works.

8. **Public API re-export**:
   - `from ensembl_orm import EnsemblObjectType, ExternalDbStatus, InfoType, ExternalDbType` succeeds.
   - Imported objects are the same as from `ensembl_orm.enums`.

Use pytest.mark.parametrize extensively to reduce duplication. Organize into test classes or descriptive function names like `test_ensembl_object_type_members`, `test_string_comparison_equality`, etc.

Completion criteria: All tests are written and FAIL because enums.py does not exist. Running `uv run pytest tests/test_enums.py` shows import errors or collection failures.

### 12.2. Implement src/ensembl_orm/enums.py and re-export from __init__.py (GREEN phase)

**Status:** pending  
**Dependencies:** 12.1  

Implement src/ensembl_orm/enums.py with the four StrEnum classes to make all tests from subtask 12.1 pass. This is the Green phase of TDD — write the minimal code to satisfy the failing tests. Then update src/ensembl_orm/__init__.py to re-export the enums. Enums are NOT models and must NOT be exported from models/__init__.py.

**Details:**

1. Create src/ensembl_orm/enums.py.
2. Import StrEnum and unique from the standard library: `from enum import StrEnum, unique`.
3. Define EnsemblObjectType(StrEnum) with the `@unique` decorator and members:
   - GENE = "Gene"
   - TRANSCRIPT = "Transcript"
   - TRANSLATION = "Translation"
   Include a comprehensive Google-style docstring using action verbs ("Represent" not "Represents") documenting each attribute. Preserve the mixed-case string values to match the MySQL ENUM.
4. Define ExternalDbStatus(StrEnum) with the `@unique` decorator, members KNOWN="KNOWN", XREF="XREF", DUMPED="DUMPED", DEPENDENT="DEPENDENT", and a comprehensive Google-style docstring with action verbs.
5. Define InfoType(StrEnum) with the `@unique` decorator, members NONE="NONE", PROBE="PROBE", DEPENDENT="DEPENDENT", DIRECT="DIRECT", INFERRED_PAIR="INFERRED_PAIR", PROBE2TRANSCRIPT="PROBE2TRANSCRIPT", UNMAPPED="UNMAPPED", CHECKSUM="CHECKSUM", and a comprehensive Google-style docstring with action verbs.
6. Define ExternalDbType(StrEnum) with the `@unique` decorator, members PRIMARY="PRIMARY", SECONDARY="SECONDARY", MISC="MISC", CHECKSUM="CHECKSUM", DEPENDENT="DEPENDENT", IMAGE_DEPICTION="IMAGE_DEPICTION", and a comprehensive Google-style docstring with action verbs.
7. Ensure each enum uses explicit string values, the `@unique` decorator, and no additional helper methods, keeping the API simple and predictable for ORM usage.
8. Update src/ensembl_orm/__init__.py (the main package) to re-export these enums. Do NOT update models/__init__.py — enums are not models. Add:
   - `from ensembl_orm.enums import EnsemblObjectType, ExternalDbStatus, InfoType, ExternalDbType`
   - Add all four to `__all__` following the existing project pattern.
9. Run `uv run pytest tests/test_enums.py -v` to confirm all tests pass (Green phase).
10. Run `uv run ruff check src/ensembl_orm/enums.py` to verify lint compliance.

Completion criteria: All tests in tests/test_enums.py pass. `from ensembl_orm import EnsemblObjectType` works. `uv run ruff check` passes clean.
