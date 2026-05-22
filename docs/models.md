# Models

The following SQLModel ORM models map directly to tables in the Ensembl `homo_sapiens_core` database.

## Gene

```python
from ensembl_orm import Gene
```

Maps to the `gene` table. Represents an Ensembl gene with stable ID, biotype, and metadata.

## SeqRegion

```python
from ensembl_orm import SeqRegion
```

Maps to the `seq_region` table. Represents a genomic sequence region (chromosome, scaffold, etc.).

## Xref

```python
from ensembl_orm import Xref
```

Maps to the `xref` table. Cross-references linking Ensembl objects to external databases.

## ObjectXref

```python
from ensembl_orm import ObjectXref
```

Maps to the `object_xref` table. Junction table linking Ensembl objects to xrefs.

## ExternalDb

```python
from ensembl_orm import ExternalDb
```

Maps to the `external_db` table. External database definitions.

## SeqRegionAttrib

```python
from ensembl_orm import SeqRegionAttrib
```

Maps to the `seq_region_attrib` table. Attributes attached to sequence regions.

## Karyotype

```python
from ensembl_orm import Karyotype
```

Maps to the `karyotype` table. Karyotype band information for chromosomes.
