import pytest
from pydantic import ValidationError
from sqlalchemy import Enum as SAEnum, Integer, String, Text, inspect as sa_inspect

from ensembl_orm.enums import ExternalDbStatus, ExternalDbType
from ensembl_orm.models.external_db import ExternalDb


def test_tablename():
    assert ExternalDb.__tablename__ == "external_db"


def test_column_count():
    mapper = sa_inspect(ExternalDb)
    assert len(list(mapper.columns)) == 11


def test_columns_present():
    mapper = sa_inspect(ExternalDb)
    names = {column.key for column in mapper.columns}
    expected = {
        "external_db_id",
        "db_name",
        "status",
        "priority",
        "dbprimary_acc_link",
        "display_name_link",
        "db_display_name",
        "type",
        "secondary_db_name",
        "description",
        "release",
    }
    assert names == expected


def test_primary_key():
    mapper = sa_inspect(ExternalDb)
    primary_keys = {column.key for column in mapper.primary_key}
    assert primary_keys == {"external_db_id"}


def test_nullable_columns():
    mapper = sa_inspect(ExternalDb)
    nullable_columns = {column.key for column in mapper.columns if column.nullable}
    expected_nullable = {
        "status",
        "dbprimary_acc_link",
        "display_name_link",
        "db_display_name",
        "type",
        "secondary_db_name",
        "description",
        "release",
    }
    assert nullable_columns == expected_nullable


def test_non_nullable_columns():
    mapper = sa_inspect(ExternalDb)
    assert mapper.columns["db_name"].nullable is False
    assert mapper.columns["priority"].nullable is False


def test_column_types():
    mapper = sa_inspect(ExternalDb)
    type_map = {column.key: type(column.type) for column in mapper.columns}
    assert type_map["external_db_id"] is Integer
    assert type_map["db_name"] is String
    assert type_map["priority"] is Integer
    assert type_map["dbprimary_acc_link"] is String
    assert type_map["display_name_link"] is String
    assert type_map["db_display_name"] is String
    assert type_map["secondary_db_name"] is String
    assert type_map["description"] is Text
    assert type_map["release"] is String


def test_status_enum_column():
    mapper = sa_inspect(ExternalDb)
    status_column = mapper.columns["status"]
    assert isinstance(status_column.type, SAEnum)
    assert status_column.type.enum_class is ExternalDbStatus


def test_type_enum_column():
    mapper = sa_inspect(ExternalDb)
    type_column = mapper.columns["type"]
    assert isinstance(type_column.type, SAEnum)
    assert type_column.type.enum_class is ExternalDbType


def test_valid_status_value_is_accepted():
    external_db = ExternalDb.model_validate(
        {"db_name": "test_db", "priority": 1, "status": ExternalDbStatus.KNOWN},
    )
    assert external_db.status is ExternalDbStatus.KNOWN


def test_valid_type_value_is_accepted():
    external_db = ExternalDb.model_validate(
        {"db_name": "test_db", "priority": 1, "type": ExternalDbType.PRIMARY},
    )
    assert external_db.type is ExternalDbType.PRIMARY


def test_invalid_status_value_is_rejected():
    with pytest.raises((ValueError, ValidationError)):
        ExternalDb.model_validate({"db_name": "test_db", "priority": 1, "status": "NOT_A_STATUS"})


def test_invalid_type_value_is_rejected():
    with pytest.raises((ValueError, ValidationError)):
        ExternalDb.model_validate({"db_name": "test_db", "priority": 1, "type": "NOT_A_TYPE"})
