from sqlalchemy import Integer, String, inspect as sa_inspect

from db_common import DeclarativeBase
from ensembl_orm.models.karyotype import Karyotype
from ensembl_orm.models.seq_region import SeqRegion


def test_tablename():
    assert Karyotype.__tablename__ == "karyotype"


def test_column_count():
    mapper = sa_inspect(Karyotype)
    assert len(list(mapper.columns)) == 6


def test_columns_present():
    mapper = sa_inspect(Karyotype)
    column_names = {column.key for column in mapper.columns}
    expected = {
        "karyotype_id",
        "seq_region_id",
        "seq_region_start",
        "seq_region_end",
        "band",
        "stain",
    }
    assert column_names == expected


def test_primary_key():
    mapper = sa_inspect(Karyotype)
    primary_keys = {column.key for column in mapper.primary_key}
    assert primary_keys == {"karyotype_id"}


def test_nullable_columns():
    mapper = sa_inspect(Karyotype)
    nullable_columns = {column.key for column in mapper.columns if column.nullable}
    expected_nullable = {
        "band",
        "stain",
    }
    assert nullable_columns == expected_nullable


def test_column_types():
    mapper = sa_inspect(Karyotype)
    type_map = {column.key: type(column.type) for column in mapper.columns}
    assert type_map["karyotype_id"] is Integer
    assert type_map["seq_region_id"] is Integer
    assert type_map["seq_region_start"] is Integer
    assert type_map["seq_region_end"] is Integer
    assert type_map["band"] is String
    assert type_map["stain"] is String


def test_string_lengths():
    mapper = sa_inspect(Karyotype)
    assert mapper.columns["band"].type.length == 255
    assert mapper.columns["stain"].type.length == 255


def test_seq_region_foreign_key():
    mapper = sa_inspect(Karyotype)
    foreign_keys = mapper.columns["seq_region_id"].foreign_keys
    assert len(foreign_keys) == 1
    foreign_key = next(iter(foreign_keys))
    assert str(foreign_key.target_fullname) == "seq_region.seq_region_id"


def test_seq_region_relationship_exists():
    mapper = sa_inspect(Karyotype)
    relationship_names = {relationship.key for relationship in mapper.relationships}
    assert "seq_region" in relationship_names


def test_seq_region_relationship_targets_seq_region_model():
    mapper = sa_inspect(Karyotype)
    seq_region_relationship = mapper.relationships["seq_region"]
    assert seq_region_relationship.mapper.class_ is SeqRegion


def test_subclasses_db_common_declarative_base():
    """Models are plain SQLAlchemy on db_common.DeclarativeBase (not SQLModel)."""
    assert issubclass(Karyotype, DeclarativeBase)
