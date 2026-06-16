from sqlalchemy import inspect as sa_inspect

from db_common import DeclarativeBase
from ensembl_orm.models.gene import Gene


def test_tablename():
    assert Gene.__tablename__ == "gene"


def test_column_count():
    mapper = sa_inspect(Gene)
    assert len(list(mapper.columns)) == 17


def test_all_columns_present():
    mapper = sa_inspect(Gene)
    col_names = {c.key for c in mapper.columns}
    expected = {
        "gene_id",
        "biotype",
        "analysis_id",
        "seq_region_id",
        "seq_region_start",
        "seq_region_end",
        "seq_region_strand",
        "display_xref_id",
        "source",
        "description",
        "is_current",
        "canonical_transcript_id",
        "canonical_translation_id",
        "stable_id",
        "version",
        "created_date",
        "modified_date",
    }
    assert col_names == expected


def test_nullable_fields():
    mapper = sa_inspect(Gene)
    nullable = {c.key for c in mapper.columns if c.nullable}
    expected_nullable = {
        "display_xref_id",
        "description",
        "canonical_transcript_id",
        "canonical_translation_id",
        "stable_id",
        "version",
        "created_date",
        "modified_date",
    }
    assert nullable == expected_nullable


def test_seq_region_foreign_key():
    mapper = sa_inspect(Gene)
    fk_set = mapper.columns["seq_region_id"].foreign_keys
    assert len(fk_set) == 1
    fk = next(iter(fk_set))
    assert str(fk.target_fullname) == "seq_region.seq_region_id"


def test_primary_key():
    mapper = sa_inspect(Gene)
    pk_cols = {c.key for c in mapper.primary_key}
    assert pk_cols == {"gene_id"}


def test_seq_region_relationship_exists():
    mapper = sa_inspect(Gene)
    rel_names = {r.key for r in mapper.relationships}
    assert "seq_region" in rel_names


def test_models_package_imports():
    from ensembl_orm.models import Gene as ImportedGene
    from ensembl_orm.models import SeqRegion as ImportedSeqRegion

    assert ImportedGene.__tablename__ == "gene"
    assert ImportedSeqRegion.__tablename__ == "seq_region"


def test_subclasses_db_common_declarative_base():
    """Models are plain SQLAlchemy on db_common.DeclarativeBase (not SQLModel)."""
    assert issubclass(Gene, DeclarativeBase)
