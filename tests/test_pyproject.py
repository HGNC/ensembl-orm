import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = PROJECT_ROOT / "pyproject.toml"

REQUIRED_RUNTIME_DEPS = [
    "mysqlclient",
    "sqlalchemy",
    "sqlmodel",
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


def test_pyproject_toml_exists() -> None:
    assert PYPROJECT.is_file(), "pyproject.toml missing from project root"


def test_requires_python_is_313_plus() -> None:
    data = _parse_pyproject()
    requires_python = data["project"]["requires-python"]
    assert "3.13" in requires_python


def test_runtime_dependencies_present() -> None:
    data = _parse_pyproject()
    deps = data["project"]["dependencies"]
    dep_names = [d.split(">=")[0].split("==")[0].split("[")[0] for d in deps]
    for required in REQUIRED_RUNTIME_DEPS:
        assert required in dep_names, f"Missing runtime dependency: {required}"


def test_dev_dependencies_present() -> None:
    data = _parse_pyproject()
    dev_deps = data["project"]["optional-dependencies"]["dev"]
    dep_names = [d.split(">=")[0].split("==")[0].split("[")[0] for d in dev_deps]
    for required in REQUIRED_DEV_DEPS:
        assert required in dep_names, f"Missing dev dependency: {required}"


def test_pytest_config_present() -> None:
    data = _parse_pyproject()
    assert "tool" in data
    assert "pytest" in data["tool"]
    assert "ini_options" in data["tool"]["pytest"]


def test_ruff_config_present() -> None:
    data = _parse_pyproject()
    assert "tool" in data
    assert "ruff" in data["tool"]
