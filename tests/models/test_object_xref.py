import pytest
from pydantic import ValidationError
from sqlalchemy import Enum as SAEnum, Integer, String, inspect as sa_inspect

from ensembl_orm.enums import EnsemblObjectType, InfoType
from ensembl_orm.models.object_xref import ObjectXref


def test_tablename():
    assert ObjectXref.__tablename__ == "object_xref"


def test_column_count():
    mapper = sa_inspect(ObjectXref)
    assert len(list(mapper.columns)) == 7


def test_columns_present():
    mapper = sa_inspect(ObjectXref)
    names = {column.key for column in mapper.columns}
    expected = {
        "object_xref_id",
        "xref_id",
        "ensembl_id",
        "ensembl_object_type",
        "linkage_annotation",
        "analysis_id",
        "linkage_type",
    }
    assert names == expected


def test_primary_key():
    mapper = sa_inspect(ObjectXref)
    primary_keys = {column.key for column in mapper.primary_key}
    assert primary_keys == {"object_xref_id"}


def test_nullable_columns():
    mapper = sa_inspect(ObjectXref)
    nullable_columns = {column.key for column in mapper.columns if column.nullable}
    expected_nullable = {
        "linkage_annotation",
        "analysis_id",
        "linkage_type",
    }
    assert nullable_columns == expected_nullable


def test_non_nullable_columns():
    mapper = sa_inspect(ObjectXref)
    assert mapper.columns["xref_id"].nullable is False
    assert mapper.columns["ensembl_id"].nullable is False
    assert mapper.columns["ensembl_object_type"].nullable is False


def test_xref_foreign_key():
    mapper = sa_inspect(ObjectXref)
    foreign_keys = mapper.columns["xref_id"].foreign_keys
    assert len(foreign_keys) == 1
    foreign_key = next(iter(foreign_keys))
    assert str(foreign_key.target_fullname) == "xref.xref_id"


def test_column_types():
    mapper = sa_inspect(ObjectXref)
    type_map = {column.key: type(column.type) for column in mapper.columns}
    assert type_map["object_xref_id"] is Integer
    assert type_map["xref_id"] is Integer
    assert type_map["ensembl_id"] is Integer
    assert type_map["linkage_annotation"] is String
    assert type_map["analysis_id"] is Integer


def test_ensembl_object_type_enum_column():
    mapper = sa_inspect(ObjectXref)
    ensembl_object_type_column = mapper.columns["ensembl_object_type"]
    assert isinstance(ensembl_object_type_column.type, SAEnum)
    assert ensembl_object_type_column.type.enum_class is EnsemblObjectType


def test_linkage_type_enum_column():
    mapper = sa_inspect(ObjectXref)
    linkage_type_column = mapper.columns["linkage_type"]
    assert isinstance(linkage_type_column.type, SAEnum)
    assert linkage_type_column.type.enum_class is InfoType


def test_xref_relationship_exists():
    mapper = sa_inspect(ObjectXref)
    relationships = {relationship.key for relationship in mapper.relationships}
    assert "xref" in relationships


def test_valid_ensembl_object_type_value_is_accepted():
    object_xref = ObjectXref.model_validate(
        {"xref_id": 1, "ensembl_id": 10, "ensembl_object_type": EnsemblObjectType.GENE},
    )
    assert object_xref.ensembl_object_type is EnsemblObjectType.GENE


def test_valid_linkage_type_value_is_accepted():
    object_xref = ObjectXref.model_validate(
        {
            "xref_id": 1,
            "ensembl_id": 10,
            "ensembl_object_type": EnsemblObjectType.GENE,
            "linkage_type": InfoType.DIRECT,
        },
    )
    assert object_xref.linkage_type is InfoType.DIRECT


def test_invalid_ensembl_object_type_value_is_rejected():
    with pytest.raises((ValueError, ValidationError)):
        ObjectXref.model_validate(
            {"xref_id": 1, "ensembl_id": 10, "ensembl_object_type": "NOT_AN_ENSEMBL_OBJECT_TYPE"},
        )


def test_invalid_linkage_type_value_is_rejected():
    with pytest.raises((ValueError, ValidationError)):
        ObjectXref.model_validate(
            {
                "xref_id": 1,
                "ensembl_id": 10,
                "ensembl_object_type": EnsemblObjectType.GENE,
                "linkage_type": "NOT_A_LINKAGE_TYPE",
            },
        )
