from sqlalchemy import Integer, String, inspect as sa_inspect

from ensembl_orm.models.seq_region import SeqRegion


def test_tablename():
    assert SeqRegion.__tablename__ == "seq_region"


def test_columns_exist():
    mapper = sa_inspect(SeqRegion)
    col_names = {c.key for c in mapper.columns}
    expected = {"seq_region_id", "name", "coord_system_id", "length"}
    assert col_names == expected


def test_primary_key():
    mapper = sa_inspect(SeqRegion)
    pk_cols = {c.key for c in mapper.primary_key}
    assert pk_cols == {"seq_region_id"}


def test_non_nullable_columns():
    mapper = sa_inspect(SeqRegion)
    for col in mapper.columns:
        if col.key == "seq_region_id":
            continue
        assert not col.nullable, f"Column '{col.key}' should be non-nullable"


def test_column_types():
    mapper = sa_inspect(SeqRegion)
    type_map = {c.key: type(c.type) for c in mapper.columns}
    assert type_map["seq_region_id"] is Integer
    assert type_map["name"] is String
    assert type_map["coord_system_id"] is Integer
    assert type_map["length"] is Integer
