from sqlalchemy import Integer, String, inspect as sa_inspect

from ensembl_orm.models.seq_region_attrib import SeqRegionAttrib


def test_tablename():
    assert SeqRegionAttrib.__tablename__ == "seq_region_attrib"


def test_column_count():
    mapper = sa_inspect(SeqRegionAttrib)
    assert len(list(mapper.columns)) == 3


def test_columns_present():
    mapper = sa_inspect(SeqRegionAttrib)
    names = {column.key for column in mapper.columns}
    assert names == {"seq_region_id", "attrib_type_id", "value"}


def test_composite_primary_key_columns():
    mapper = sa_inspect(SeqRegionAttrib)
    primary_keys = {column.key for column in mapper.primary_key}
    assert primary_keys == {"seq_region_id", "attrib_type_id"}


def test_column_types():
    mapper = sa_inspect(SeqRegionAttrib)
    type_map = {column.key: type(column.type) for column in mapper.columns}
    assert type_map["seq_region_id"] is Integer
    assert type_map["attrib_type_id"] is Integer
    assert type_map["value"] is String


def test_value_length():
    mapper = sa_inspect(SeqRegionAttrib)
    assert mapper.columns["value"].type.length == 255


def test_column_nullability():
    mapper = sa_inspect(SeqRegionAttrib)
    assert mapper.columns["seq_region_id"].nullable is False
    assert mapper.columns["attrib_type_id"].nullable is False
    assert mapper.columns["value"].nullable is True
