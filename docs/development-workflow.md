# Development Workflow

## Setup

```bash
# Install dependencies
uv sync --extra dev
```

## Linting

```bash
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/
```

## Formatting

```bash
uv run ruff format src/ tests/
```

## Running tests

```bash
uv run pytest tests/ -v
```

## CI

All pushes to `main` trigger the CI, lint, and test workflows automatically.
