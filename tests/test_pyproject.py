import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = PROJECT_ROOT / "pyproject.toml"

REQUIRED_RUNTIME_DEPS = [
    "mysqlclient",
    "sqlalchemy",
    "pydantic",
    "pydantic-settings",
]

REQUIRED_DEV_DEPS = [
    "pytest",
    "pytest-mock",
    "ruff",
]


def _parse_pyproject() -> dict:
    return tomllib.loads(PYPROJECT.read_text())


def _dependency_names(deps: list[str]) -> list[str]:
    """Return bare dependency names from PEP 508 requirement strings.

    Strips version specifiers (``>=``, ``==``) and extras (``pkg[extra]``)
    so callers can compare against plain names like ``"sqlalchemy"``.
    """
    return [d.split(">=")[0].split("==")[0].split("[")[0] for d in deps]


def test_pyproject_toml_exists() -> None:
    assert PYPROJECT.is_file(), "pyproject.toml missing from project root"


def test_requires_python_is_313_plus() -> None:
    data = _parse_pyproject()
    requires_python = data["project"]["requires-python"]
    assert "3.13" in requires_python


def test_runtime_dependencies_present() -> None:
    data = _parse_pyproject()
    dep_names = _dependency_names(data["project"]["dependencies"])
    for required in REQUIRED_RUNTIME_DEPS:
        assert required in dep_names, f"Missing runtime dependency: {required}"


def test_dev_dependencies_present() -> None:
    data = _parse_pyproject()
    dep_names = _dependency_names(data["project"]["optional-dependencies"]["dev"])
    for required in REQUIRED_DEV_DEPS:
        assert required in dep_names, f"Missing dev dependency: {required}"


def test_sqlmodel_not_a_runtime_dependency() -> None:
    """SQLModel was dropped during the db-common migration (T5)."""
    data = _parse_pyproject()
    dep_names = _dependency_names(data["project"]["dependencies"])
    assert "sqlmodel" not in dep_names, "sqlmodel should no longer be a runtime dependency"


def test_pytest_config_present() -> None:
    data = _parse_pyproject()
    assert "tool" in data
    assert "pytest" in data["tool"]
    assert "ini_options" in data["tool"]["pytest"]


def test_ruff_config_present() -> None:
    data = _parse_pyproject()
    assert "tool" in data
    assert "ruff" in data["tool"]
