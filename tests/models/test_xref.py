import pytest
from pydantic import ValidationError
from sqlalchemy import Enum as SAEnum, Integer, String, Text, inspect as sa_inspect

from ensembl_orm.enums import InfoType
from ensembl_orm.models.xref import Xref


def test_tablename():
    assert Xref.__tablename__ == "xref"


def test_column_count():
    mapper = sa_inspect(Xref)
    assert len(list(mapper.columns)) == 8


def test_columns_present():
    mapper = sa_inspect(Xref)
    names = {column.key for column in mapper.columns}
    expected = {
        "xref_id",
        "external_db_id",
        "dbprimary_acc",
        "display_label",
        "version",
        "description",
        "info_type",
        "info_text",
    }
    assert names == expected


def test_primary_key():
    mapper = sa_inspect(Xref)
    primary_keys = {column.key for column in mapper.primary_key}
    assert primary_keys == {"xref_id"}


def test_nullable_columns():
    mapper = sa_inspect(Xref)
    nullable_columns = {column.key for column in mapper.columns if column.nullable}
    expected_nullable = {
        "dbprimary_acc",
        "display_label",
        "version",
        "description",
        "info_type",
        "info_text",
    }
    assert nullable_columns == expected_nullable


def test_external_db_id_is_non_nullable():
    mapper = sa_inspect(Xref)
    assert mapper.columns["external_db_id"].nullable is False


def test_external_db_foreign_key():
    mapper = sa_inspect(Xref)
    foreign_keys = mapper.columns["external_db_id"].foreign_keys
    assert len(foreign_keys) == 1
    foreign_key = next(iter(foreign_keys))
    assert str(foreign_key.target_fullname) == "external_db.external_db_id"


def test_column_types():
    mapper = sa_inspect(Xref)
    type_map = {column.key: type(column.type) for column in mapper.columns}
    assert type_map["xref_id"] is Integer
    assert type_map["external_db_id"] is Integer
    assert type_map["dbprimary_acc"] is String
    assert type_map["display_label"] is String
    assert type_map["version"] is String
    assert type_map["description"] is Text
    assert type_map["info_text"] is String


def test_info_type_enum_column():
    mapper = sa_inspect(Xref)
    info_type_column = mapper.columns["info_type"]
    assert isinstance(info_type_column.type, SAEnum)
    assert info_type_column.type.enum_class is InfoType


def test_external_db_relationship_exists():
    mapper = sa_inspect(Xref)
    relationships = {relationship.key for relationship in mapper.relationships}
    assert "external_db" in relationships


def test_valid_info_type_value_is_accepted():
    xref = Xref.model_validate({"external_db_id": 1, "info_type": InfoType.DIRECT})
    assert xref.info_type is InfoType.DIRECT


def test_invalid_info_type_value_is_rejected():
    with pytest.raises((ValueError, ValidationError)):
        Xref.model_validate({"external_db_id": 1, "info_type": "NOT_AN_INFO_TYPE"})
