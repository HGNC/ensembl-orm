# CHANGELOG


## v0.5.1 (2026-06-17)


## v0.5.0 (2026-06-16)

### Bug Fixes

- **ci**: Pin setup-uv to v8.2.0 instead of non-existent v8 tag
  ([`9472fe3`](https://github.com/HGNC/ensembl-orm/commit/9472fe3487c5512ae1f7bd0500004c0dc83aefe7))

The astral-sh/setup-uv v8 major tag was never published (HTTP 404 on the git ref), causing all
  workflows to fail with 'unable to find version v8'. Pin to the latest real release v8.2.0 instead.

- **ci**: Restore green CI after the db-common migration
  ([`86ecb66`](https://github.com/HGNC/ensembl-orm/commit/86ecb66852a650e6eaeb0fc61bfa85dee3219d24))

docs.yml installed via `pip install -e .`, which can't resolve db-common (it's a git source, not on
  PyPI); switch to `uv sync --extra docs` and add a docs extra. Delete the redundant ci.yml (it
  duplicated lint.yml + test.yml) and fold its Codecov upload into test.yml.

The lint mypy job was red: db_common's wheel ships no py.typed marker, so mypy sees its API as Any;
  bridge it with a typed helper in session.py.

Also modernize the uv bootstrap to astral-sh/setup-uv@v8, bump actions-gh-pages to v4, and ignore
  the MkDocs /site/ build output.

### Build System

- **deps**: Pin db-common v0.1.0 as a git dependency (Task T1)
  ([`b9bc838`](https://github.com/HGNC/ensembl-orm/commit/b9bc838a5515da6376b5fa1829e99418a97ab6a7))

### Features

- **config**: Replace DatabaseSettings with EnsemblDatabaseSettings(db_common.DatabaseSettings)
  (Task T3)
  ([`2f01fff`](https://github.com/HGNC/ensembl-orm/commit/2f01fffc36c9e0c15404d2012fcfb08496624272))

### Refactoring

- **models**: Convert all 7 models to SQLAlchemy on db_common.DeclarativeBase (Task T2)
  ([`69f2f58`](https://github.com/HGNC/ensembl-orm/commit/69f2f585b601704e52f7ccb51bccfcb0a03ec23c))

Rewrite every mapped model from SQLModel to plain SQLAlchemy 2.0 on db_common.DeclarativeBase, using
  Mapped[...]/mapped_column(...) and relationship(...). Convert in foreign-key order within this
  single commit (seq_region → external_db → xref → object_xref → karyotype/gene/seq_region_attrib)
  so relationships never span a SQLModel↔SQLAlchemy boundary. Drop the pydantic @field_validator
  hooks on external_db, xref, and object_xref — they don't run on plain SQLAlchemy models and the
  MySQL ENUM still enforces validity on write.

The SQL mapper contract is preserved byte-for-byte: column count/names/ types/nullability, primary
  and foreign keys, __table_args__ (incl. SeqRegionAttrib composite PK), string lengths,
  SAEnum(enum_class), and relationship existence + target class — all pinned by the existing
  sqlalchemy.inspect tests, which stay green and unchanged. Single autoincrement PKs use Mapped[int]
  (db-common's own idiom) so the column resolves nullable=False, matching the prior Core Column
  behavior; the naive Mapped[int | None] mirror would wrongly mark PKs nullable.

Tests: add test_subclasses_db_common_declarative_base to all 7 model test files; in
  test_external_db/test_xref/test_object_xref replace each model_validate/ValidationError pair with
  a single direct-construction test for a valid enum value; drop the now-unused
  pytest/ValidationError imports.

sqlmodel remains installed and session.py still imports it — that removal is T5's scope,
  intentionally untouched here.

249 passed; ruff check + format clean.

- **session**: Delegate engine/session to db-common and re-export its exceptions (Task T4)
  ([`7a6d232`](https://github.com/HGNC/ensembl-orm/commit/7a6d23262fbd3b65a5dbe0f7caef625d539bd594))

Migrate session and exception infrastructure onto the shared db-common library, completing Phase 2
  of the db-common migration.

Source: - exceptions.py: drop EnsemblSessionError; re-export db_common.SessionError and
  ReadOnlySessionError (EnsemblDiscoveryError stays Ensembl-specific). - session.py: rewrite to
  module-level db_common.EngineFactory/SessionFactory singletons. The four public signatures are
  preserved — initialize_engine (defaults when None, runs discover_database_name only when database
  is empty and driver != sqlite), get_engine (raises SessionError if uninitialized), get_session
  (delegates to get_readonly_session, so commits raise ReadOnlySessionError via db-common's
  before_commit hook), and close_all_sessions (close_all + dispose_engine). SQLModel import removed;
  modernized to X | None / Generator[Session] per AGENTS.md. - __init__.py: drop
  EnsemblSessionError, export SessionError/ReadOnlySessionError. Docstring left as "SQLModel" for T5
  (lockstep with its test assertion).

Tests: - test_session.py: rewritten to exercise the real SQLite path (SELECT 1, ReadOnlySessionError
  on commit); MySQL discovery-branch unit tests stub EngineFactory/SessionFactory since
  mysqlclient's libmysqlclient is not loadable in CI. - test_implementation.py,
  test_public_api_exports.py: EnsemblSessionError -> SessionError/ReadOnlySessionError;
  EXPECTED_PUBLIC_API updated. - conftest.py: drop the now-removed EnsemblSessionError import and
  its unused ensembl_session_error fixture.

Public API change: EnsemblSessionError is removed; callers move to the re-exported db_common
  exceptions (SessionError derives from DatabaseError). Full suite green (260 passed); ruff clean.

- **tests**: Use pytest.raises and dedupe dependency-name parsing
  ([`d61a355`](https://github.com/HGNC/ensembl-orm/commit/d61a3553ebed91cec461bbc0334e88eb506c31b3))


## v0.4.0 (2026-05-26)


## v0.3.0 (2026-05-22)

### Features

- Add documentation badge to README
  ([`24e535d`](https://github.com/HGNC/ensembl-orm/commit/24e535d8f35251b9a7e4a189f08c7f071517db1c))


## v0.2.0 (2026-05-22)

### Features

- Add initial documentation files for API, configuration, development workflow, installation,
  querying, models, testing, and styles
  ([`a6f7550`](https://github.com/HGNC/ensembl-orm/commit/a6f7550eebd7f62fb73e6f7f65df91753fb022c2))

- Add MkDocs configuration for project documentation
  ([`13a5274`](https://github.com/HGNC/ensembl-orm/commit/13a52747d2d4f61c6af2a8c0966df604d4fe0072))


## v0.1.0 (2026-05-22)

### Bug Fixes

- **opencode**: Correct environment key and format API keys in opencode.json
  ([`cec9038`](https://github.com/HGNC/ensembl-orm/commit/cec9038c1a8b4cc9a10da4be9e05b4852888a805))

- **release**: Update semantic release configuration for GitHub Actions
  ([`9ac2e8d`](https://github.com/HGNC/ensembl-orm/commit/9ac2e8df72287e10dfd5655027bb94e28a542ed6))

- **tasks**: Change task IDs from strings to integers for consistency
  ([`035594d`](https://github.com/HGNC/ensembl-orm/commit/035594d8a446dc88a88a140264f782c7bdffd76a))

### Chores

- Remove CI badge links from README.md
  ([`c3935ed`](https://github.com/HGNC/ensembl-orm/commit/c3935ed6354570f97dceb389972e2507adae2d28))

- Update task 13 status
  ([`6db9229`](https://github.com/HGNC/ensembl-orm/commit/6db92297f12c1e69c5f1713a6ae3ddefd0ab3f05))

- Update task statuses for task 10 completion
  ([`1382a18`](https://github.com/HGNC/ensembl-orm/commit/1382a18c901d4f2b5c01fa56d8e945aee9283830))

- Update task-master state
  ([`010817a`](https://github.com/HGNC/ensembl-orm/commit/010817a7f41b977405d95d92bbc869af5c129c9a))

- **autopilot**: Complete commit cycle for subtask 16.1
  ([`5af5c69`](https://github.com/HGNC/ensembl-orm/commit/5af5c69ae198ef414831ee41d4ce3a2a8acc36ea))

- **taskmaster**: Mark task 14 subtasks done
  ([`d34f994`](https://github.com/HGNC/ensembl-orm/commit/d34f994f6ea97058eaed8b57ba3be6e81f710c99))

- **taskmaster**: Mark task 15 subtasks done
  ([`464f7e2`](https://github.com/HGNC/ensembl-orm/commit/464f7e22dd1ddbd311ece21155e6a45cacdc63a2))

- **taskmaster**: Sync task 15 workflow state
  ([`dcc6794`](https://github.com/HGNC/ensembl-orm/commit/dcc67942a2e3e52c22b641bcc4e44fbad085350e))

- **taskmaster**: Sync workflow state for task 14
  ([`b894565`](https://github.com/HGNC/ensembl-orm/commit/b89456531a5e4f8844b2f4ba6a4fd298bf315131))

### Code Style

- Ruff format gene.py
  ([`ba814a7`](https://github.com/HGNC/ensembl-orm/commit/ba814a77312959381ea48a6424a4f2004a9fa40a))

### Features

- Add enum definitions for Ensembl column types (task 12)
  ([`aae4a64`](https://github.com/HGNC/ensembl-orm/commit/aae4a647cf30e2bbdb1e3989047dfabf64b9b40c))

- Add src/ensembl_orm/enums.py with four StrEnum classes: EnsemblObjectType, ExternalDbStatus,
  InfoType, ExternalDbType - Re-export enums from src/ensembl_orm/__init__.py - Add
  tests/test_enums.py with 95 passing tests covering: member values, string comparison,
  construction, invalid input, iteration, @unique enforcement, SQLAlchemy Enum integration, and
  public API re-exports

- Update task 12 status to done and increment completed count
  ([`8369fbf`](https://github.com/HGNC/ensembl-orm/commit/8369fbfe7545dc076368d30218857dd035e05129))

- **api**: Finalize top-level public API and __all__ in ensembl_orm/__init__.py
  ([`93f2bbf`](https://github.com/HGNC/ensembl-orm/commit/93f2bbf832a5ca6d62939e563361567e8da01fd2))

- Update module docstring to describe read-only SQLModel ORM for Ensembl homo_sapiens_core - Export
  discover_database_name at package root - Export all model classes (Gene, SeqRegion, Xref,
  ObjectXref, ExternalDb, SeqRegionAttrib, Karyotype) at package root - Replace __all__ with exact
  public API contract - Add tests/test_public_api_exports.py contract tests

Task: 16.1 (GREEN phase)

- **config**: Add GOOGLE_API_KEY to environment variables in opencode.json
  ([`ba0fac6`](https://github.com/HGNC/ensembl-orm/commit/ba0fac62fe0a26455f091dc493380e9ca53413a6))

- **config**: Implement DatabaseSettings, exceptions module, and package __init__.py stubs
  ([`010ead8`](https://github.com/HGNC/ensembl-orm/commit/010ead8d26258473aa42b068a92983236335bd5f))

Task: 9

Phase: COMMIT

Tests: 7 passing, 0 failing

- **repo**: Configure Gene.seq_region Relationship and update model exports
  ([`0b43a3a`](https://github.com/HGNC/ensembl-orm/commit/0b43a3aa4f7a8122bb4fff231450fb4975ff3a63))

Task: 13

Phase: COMMIT

Tests: 13 passing, 0 failing

- **repo**: Create base project directory structure
  ([`0f68c0b`](https://github.com/HGNC/ensembl-orm/commit/0f68c0b2ceee6c404d974a12113ee48b6f75e9d1))

Task: 9

Phase: COMMIT

Tests: 1 passing, 0 failing

- **repo**: Create project boilerplate and configuration files
  ([`200c5d4`](https://github.com/HGNC/ensembl-orm/commit/200c5d4c7cddc30aa73991366047693f6472c840))

Task: 9

Phase: COMMIT

Tests: 5 passing, 0 failing

- **repo**: Finalize top-level public API and __all__ in src/ensembl_orm/__init__.py
  ([`6e6cd89`](https://github.com/HGNC/ensembl-orm/commit/6e6cd8919512253b8b6d87685a67dad8cc40586b))

Task: 16

Phase: COMMIT

Tests: 5 passing, 0 failing

[taskId:16]

[subtaskId:1]

[phase:COMMIT]

[tddCycle:complete]

- **repo**: Implement _fetch_release_version with robust HTTP error handling
  ([`66658d2`](https://github.com/HGNC/ensembl-orm/commit/66658d267d69a6c3f86ec7588ebfa30fb92b1ffa))

Task: 10

Phase: COMMIT

Tests: 5 passing, 0 failing

- **repo**: Implement _resolve_database_name using SQLAlchemy and SHOW DATABASES LIKE
  ([`9798699`](https://github.com/HGNC/ensembl-orm/commit/9798699f33c61907ab7a9e5d1891938e2cef54e4))

Task: 10

Phase: COMMIT

Tests: 6 passing, 0 failing

- **repo**: Implement discover_database_name with caching, overrides, and logging
  ([`e006697`](https://github.com/HGNC/ensembl-orm/commit/e0066971ae3f2e81e37417b772db8adbc9e454a0))

Task: 10

Phase: COMMIT

Tests: 6 passing, 0 failing

- **repo**: Implement Gene SQLModel table with columns and seq_region_id ForeignKey
  ([`c6fd4f7`](https://github.com/HGNC/ensembl-orm/commit/c6fd4f7e5b68a48f1f1778d13bf2c0e191a14c8f))

Task: 13

Phase: COMMIT

Tests: 6 passing, 0 failing

- **repo**: Implement global engine state and initialize_engine in session.py
  ([`aed0f56`](https://github.com/HGNC/ensembl-orm/commit/aed0f56b16ed2f79943f661250f775b65908c61f))

Task: 11

Phase: COMMIT

Tests: 19 passing, 0 failing

- **repo**: Implement Karyotype SQLModel with SeqRegion ForeignKey and Relationship
  ([`0e6bf17`](https://github.com/HGNC/ensembl-orm/commit/0e6bf17a052a0592f8ea0ecd8ba92b4e3d3f08f3))

Task: 15

Phase: COMMIT

Tests: 10 passing, 0 failing

- **repo**: Implement reset_cache and module-level initialization for discovery
  ([`3721023`](https://github.com/HGNC/ensembl-orm/commit/3721023758da51633c829835c70176146de163c4))

Task: 10

Phase: COMMIT

Tests: 3 passing, 0 failing

- **repo**: Implement SeqRegion SQLModel table in src/ensembl_orm/models/seq_region.py
  ([`bbbbfec`](https://github.com/HGNC/ensembl-orm/commit/bbbbfec2d9d4a0c9b4183947b477f1faf2d31e59))

Task: 13

Phase: COMMIT

Tests: 5 passing, 0 failing

- **repo**: Session management module with initialize_engine, get_engine, get_session,
  close_all_sessions
  ([`d51e420`](https://github.com/HGNC/ensembl-orm/commit/d51e420bb3d58fc4fff47468d491b4e674db1831))

Task: 11

Subtasks: 11.1-11.6 done

Tests: 19 passing (76 total suite)

- **repo**: Update models __init__.py and run full test suite (Refactor phase)
  ([`f4bb88c`](https://github.com/HGNC/ensembl-orm/commit/f4bb88c1ebbc57f4a40e31eb990f4a02bec073b4))

Task: 14

Phase: COMMIT

Tests: 54 passing, 0 failing

- **repo**: Update models/__init__.py exports and forward-reference handling
  ([`5955dba`](https://github.com/HGNC/ensembl-orm/commit/5955dba61c5225334c168ffc510bc47e5e919948))

Task: 15

Phase: COMMIT

Tests: 12 passing, 0 failing

- **repo**: Update task descriptions and statuses for project scaffolding and database discovery
  ([`6d48dfc`](https://github.com/HGNC/ensembl-orm/commit/6d48dfcfef579a5d95e161336639a9749bbb679b))

- **repo**: Write failing tests for ExternalDb, Xref, and ObjectXref models (Red phase)
  ([`2a138a3`](https://github.com/HGNC/ensembl-orm/commit/2a138a3e2acda85770dffc4192f80e3ac448ac83))

Task: 14

Phase: COMMIT

Tests: 40 passing, 0 failing

- **tests**: Add DatabaseSettings tests and shared pytest fixtures
  ([`b4210ff`](https://github.com/HGNC/ensembl-orm/commit/b4210ff25ab87a72c810970eb49d8b7df1dce5ce))

### Refactoring

- Remove unused markdownlint JSON validation from tests
  ([`e499f9f`](https://github.com/HGNC/ensembl-orm/commit/e499f9f32b0ad56838fbcff9896fcddff5537ea7))
