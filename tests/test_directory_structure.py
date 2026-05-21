from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DIRS = [
    "src",
    "src/ensembl_orm",
    "src/ensembl_orm/config",
    "src/ensembl_orm/models",
    "tests",
    "tests/models",
]


def test_required_directory_structure_exists() -> None:
    for relative_path in REQUIRED_DIRS:
        directory = PROJECT_ROOT / relative_path
        assert directory.is_dir(), f"Missing required directory: {relative_path}"
