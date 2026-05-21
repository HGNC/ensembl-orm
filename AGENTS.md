## Python Rules

### Project Structure & Style

- One class per file. Name the file after the class in snake_case (e.g., `OrderProcessor` → `order_processor.py`).
- Always use object-oriented development. Favour composition over inheritance where practical.
- Use type hints everywhere: function parameters, return types, and variable declarations. Prefer `str | None` union syntax over `Optional[str]`.
- All classes and public methods must have comprehensive, clear docstrings (Google style). Include `Args`, `Returns`, `Raises`, and a usage example where non-trivial. Use action words in docstrings ("Return the user" not "Returns the user").
- Private helper methods should still have a one-line docstring at minimum.
- Keep methods short and single-purpose. If a method exceeds ~30 lines, consider refactoring.
- Use the following decorators where appropriate: `@classmethod`, `@abstractmethod`, `@staticmethod`, `@atexit.register`, `@enum.unique`, `@enum.verify`, and `@dataclass`.

### Naming Conventions

- Variables, functions, methods, packages, modules: `lower_case_with_underscores`.
- Classes and exceptions: `CapWords`.
- Protected methods and internal functions: `_single_leading_underscore`.
- Private methods: `__double_leading_underscore`.
- Constants: `ALL_CAPS_WITH_UNDERSCORES`.
- Avoid one-letter variable names except in very short blocks where meaning is obvious from context (e.g., `for e in elements`).
- Avoid redundant labelling — do not prefix attributes with the class or module name (e.g., `audio.Core` not `audio.AudioCore`).
- Prefer reverse notation for related variables: `elements_active`, `elements_defunct` — not `active_elements`, `defunct_elements`.

### Architectural Layering

- Separate concerns into distinct layers: **Models** (data shape/validation), **Repositories** (all database access), **Services** (business logic), and **Controllers/Routes** (HTTP handling).
- Services must never contain raw SQL or ORM queries — they call repository methods with descriptive names (e.g., `get_overdue_invoices_with_line_items()`).
- Controllers/routes must never contain business logic — they validate input, call a service, and return a response.
- Use SQLAlchemy (2.0-style `select()` API) when an ORM is appropriate, but do not force it. Complex queries, reporting queries, or performance-critical operations can use raw SQL via `mysqlclient` directly.
- If you are fighting the ORM to express a query, that is the signal to drop down to raw SQL. Be pragmatic, not dogmatic.
- Regardless of whether a repository uses SQLAlchemy or raw SQL, the interface it exposes to services must remain the same — the caller should never know or care how the data was fetched.
- Inject dependencies through constructor parameters — never instantiate them internally. For example, `OrderService` receives its `OrderRepository` via `__init__`, not by creating one itself.
- In FastAPI, use `Depends()` to wire dependencies into route handlers, keeping the constructor injection pattern consistent across the application.
- Define abstract base classes (`ABC` with `@abstractmethod`) for repository and service interfaces when there are, or could be, multiple implementations. Type-hint dependencies against the abstraction, not the concrete class.

### Data Validation & Models

- Use Pydantic (`BaseModel` / `BaseSettings`) for all data structures, API request/response schemas, and configuration objects.
- Use Pydantic's `Field(...)` for validation constraints, default values, and field descriptions.
- Use `model_validator` and `field_validator` decorators for custom validation logic rather than ad-hoc checks scattered through business logic.

### Database

- Use `mysqlclient` for MySQL connections — never `mysql-connector-python`.
- Use `psycopg` (v3) for PostgreSQL connections — never `psycopg2`.
- Use parameterised queries for all database operations — never string interpolation or f-strings in SQL.
- Wrap database operations in context managers to guarantee connection/cursor cleanup.
- Application code must never execute DDL (no `CREATE`, `ALTER`, `DROP`, `TRUNCATE`). Code is limited to CRUD operations only. Schema changes are managed outside the application through migration tooling or manual processes.
- This includes SQLAlchemy's `metadata.create_all()` — never use it. Table structures are managed externally.

### Dependencies & Environment

- Use `uv` exclusively to manage and install packages (e.g., `uv add`, `uv sync`, `uv run`). Never use raw `pip install`.
- Maintain a `pyproject.toml` as the single source of truth for project metadata and dependencies.
- Target the minimum Python version specified in `pyproject.toml` — do not use syntax or stdlib features from newer versions without updating it.

### Secrets & Configuration

- Store sensitive data (API keys, DB credentials, etc.) in `.env` files that are listed in `.gitignore`. Never hard-code secrets.
- When deploying to GCP, use Secret Manager to store and retrieve secrets at runtime rather than `.env` files.
- Use Pydantic `BaseSettings` to load environment variables and secrets, providing a single typed configuration object.

### Security

- Never trust user input. All external data must pass through Pydantic validation before any processing or database operation.
- Set explicit CORS origins in FastAPI — never use `allow_origins=["*"]` in production.
- Sanitise any user-supplied data that gets rendered in responses or written to logs to prevent injection or log-forging.

### Testing (TDD)

- Follow test-driven development: Red → Green → Refactor. Write the failing test first, then the minimal code to pass, then refactor.
- Use `pytest` as the test runner and `pytest-mock` (the `mocker` fixture) for mocking.
- Test file structure must mirror source structure: `src/models/user.py` → `tests/models/test_user.py`.
- Each test method should test one behaviour and have a descriptive name: `test_create_order_raises_when_quantity_is_negative`.
- Use fixtures (`conftest.py`) for shared setup like database connections, test clients, and mock configurations.
- Aim for thorough coverage of business logic; don't write trivial tests for getters/setters or Pydantic defaults.
- Tests must be isolated — never interact with a real database or external service. Use mocks, fakes, or an in-memory test database.
- Never let incomplete tests pass silently. Mark them with `assert False, "TODO: finish me"` or `pytest.skip("Not yet implemented")` so they are impossible to miss.

### Error Handling

- Define custom exception classes for domain-specific errors rather than raising generic `ValueError` or `RuntimeError`.
- Never use bare `except:` or `except Exception:` without re-raising or logging. Catch the most specific exception possible.
- Use `logging` (not `print`) for all diagnostic output. Configure structured logging (JSON) for anything deployed to GCP.
- Use the correct logging level:
  - `debug` — internal state useful during development (variable values, query parameters).
  - `info` — significant business events (order created, user authenticated, job started/completed).
  - `warning` — something unexpected but recoverable (retry attempt, deprecated feature used, slow query).
  - `error` — something failed that needs attention (API call failed, data integrity issue).
  - `critical` — application cannot continue (database unreachable, missing required config).

### Code Quality

- Write clean code that passes `ruff`, `Pylance`, and `mypy` without errors or warnings. Only add a `# type: ignore`, `# noqa`, or suppression comment if there is genuinely no better option — and always include the specific rule code and a brief justification (e.g., `# type: ignore[override]  # covariant return required by base class`).
- Prefer f-strings for string formatting.
- Use `Enum` or `StrEnum` for fixed sets of values rather than magic strings or constants.
- Use `dataclasses` only for simple internal data containers that don't need validation; prefer Pydantic models for anything crossing a boundary (API, DB, config).
- Use `pathlib.Path` over `os.path` for all file system operations.
- Imports should be sorted and grouped: stdlib → third-party → local. Let `ruff` manage this automatically.
- Import entire modules rather than individual symbols to avoid circular imports (e.g., `from canteen import sessions` not `from canteen.sessions import get_session`). Exception: third-party libraries where documentation explicitly says to import individual symbols.
- Use list comprehensions and generator expressions over manual loops with `append` where readability is not sacrificed.
- Use `is` / `is not` for comparisons to `True`, `False`, and `None` — never `==` or `!=`.
- Always use the `with` statement (context managers) for resource handling: files, database connections, locks.
- Prefer code readability over comments. If a block needs a comment to explain _what_ it does, extract it into a well-named method instead. Reserve comments for explaining _why_ something is done.
- Never leave incomplete code without a marker. Use `assert False, "TODO: finish me"` or `raise NotImplementedError("TODO: ...")` so incomplete work is impossible to miss.
- Use parentheses for line continuations rather than backslashes.

---

## Markdown Rules

- All markdown files must pass markdownlint.
- The file .markdownlint.json must exist and contain the following:
  
``` json
{
  "MD013": {
    "line_length": 120,
    "tables": false
  },
  "MD024": {
    "siblings_only": true
  },
  "MD060": false
}
```
