# Installation

## Prerequisites

- Python >= 3.13
- A running Ensembl MySQL database (or access to the public Ensembl server)

## Install

Add as a git-source dependency using `uv`:

```bash
uv add "git+https://github.com/HGNC/ensembl-orm.git"
```

Or with `pip`:

```bash
pip install "git+https://github.com/HGNC/ensembl-orm.git"
```

## Verify

```python
import ensembl_orm
print(ensembl_orm.__doc__)
```
