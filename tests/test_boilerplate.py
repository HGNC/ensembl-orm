from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_BOILERPLATE_FILES = [
    ".gitignore",
    ".env.example",
    "LICENSE",
]

REQUIRED_ENV_VARS = [
    "ENSEMBLDB_HOST",
    "ENSEMBLDB_PORT",
    "ENSEMBLDB_USER",
    "ENSEMBLDB_PASSWORD",
    "ENSEMBLDB_DATABASE",
    "ENSEMBLDB_POOL_SIZE",
    "ENSEMBLDB_POOL_RECYCLE",
]

REQUIRED_GITIGNORE_ENTRIES = [
    "__pycache__",
    ".venv",
    "*.pyc",
]


def test_boilerplate_files_exist() -> None:
    for filename in REQUIRED_BOILERPLATE_FILES:
        filepath = PROJECT_ROOT / filename
        assert filepath.is_file(), f"Missing boilerplate file: {filename}"
        assert filepath.stat().st_size > 0, f"Empty boilerplate file: {filename}"


def test_env_example_contains_required_vars() -> None:
    env_example = PROJECT_ROOT / ".env.example"
    content = env_example.read_text()
    for var in REQUIRED_ENV_VARS:
        assert var in content, f"Missing env var in .env.example: {var}"


def test_gitignore_contains_python_entries() -> None:
    gitignore = PROJECT_ROOT / ".gitignore"
    content = gitignore.read_text()
    for entry in REQUIRED_GITIGNORE_ENTRIES:
        assert entry in content, f"Missing .gitignore entry: {entry}"


def test_license_contains_mit_text() -> None:
    license_file = PROJECT_ROOT / "LICENSE"
    content = license_file.read_text()
    assert "MIT" in content
