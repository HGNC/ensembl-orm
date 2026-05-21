"""ORM models for Ensembl database tables."""

from ensembl_orm.models.seq_region import SeqRegion
from ensembl_orm.models.gene import Gene

__all__: list[str] = ["SeqRegion", "Gene"]
