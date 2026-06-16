import importlib


EXPECTED_PUBLIC_API: list[str] = [
    "DatabaseSettings",
    "initialize_engine",
    "get_engine",
    "get_session",
    "close_all_sessions",
    "discover_database_name",
    "EnsemblDiscoveryError",
    "SessionError",
    "ReadOnlySessionError",
    "EnsemblObjectType",
    "ExternalDbStatus",
    "ExternalDbType",
    "InfoType",
    "Gene",
    "SeqRegion",
    "Xref",
    "ObjectXref",
    "ExternalDb",
    "SeqRegionAttrib",
    "Karyotype",
]


def test_top_level_docstring_matches_public_api_contract() -> None:
    import ensembl_orm

    expected_docstring = "Read-only SQLModel ORM for the Ensembl homo_sapiens_core MySQL database."
    assert ensembl_orm.__doc__ == expected_docstring


def test_top_level_all_matches_public_api_contract() -> None:
    import ensembl_orm

    assert ensembl_orm.__all__ == EXPECTED_PUBLIC_API


def test_top_level_public_symbols_are_accessible() -> None:
    import ensembl_orm

    for symbol_name in EXPECTED_PUBLIC_API:
        assert hasattr(ensembl_orm, symbol_name), f"Missing public symbol: {symbol_name}"


def test_star_import_exports_only_expected_symbols() -> None:
    namespace: dict[str, object] = {}

    exec("from ensembl_orm import *", namespace)

    exported_symbols = sorted(name for name in namespace if not name.startswith("__"))
    assert exported_symbols == sorted(EXPECTED_PUBLIC_API)


def test_importing_top_level_package_does_not_initialize_engine(mocker) -> None:
    module = importlib.import_module("ensembl_orm")
    initialize_engine_spy = mocker.spy(module, "initialize_engine")

    importlib.reload(module)

    initialize_engine_spy.assert_not_called()
