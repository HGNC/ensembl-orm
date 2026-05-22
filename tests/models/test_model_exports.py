def test_models_package_exports_new_models():
    from ensembl_orm.models import ExternalDb, ObjectXref, Xref

    assert ExternalDb.__tablename__ == "external_db"
    assert Xref.__tablename__ == "xref"
    assert ObjectXref.__tablename__ == "object_xref"
