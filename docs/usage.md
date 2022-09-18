# Usage

## Help Screen

```console
❯ liitos --help
usage: liitos [-h] --facet FACET --target TARGET [--document-root DOC_ROOT] [--structure STRUCTURE] [doc_root_pos]

Splice (Finnish liitos) contributions.

positional arguments:
  doc_root_pos          Root of the document tree to visit. Optional (default: PWD)

options:
  -h, --help            show this help message and exit
  --facet FACET, -f FACET
                        facet key of target document
  --target TARGET, -t TARGET
                        target document key
  --document-root DOC_ROOT, -d DOC_ROOT
                        Root of the document tree to visit. Optional
                        (default: positional tree root value)
  --structure STRUCTURE, -s STRUCTURE
                        structure mapping file (default: structure.yml)
```

## Verification Example

All good:

```console
❯ liitos -d test/fixtures/basic -f mn -t abc
```

Target document key not present in structure (map):

```console
❯ liitos -d test/fixtures/basic -f mn -t abc-not-present
ERROR: target (abc-not-present) not in ['abc']
```

Facet key for target document not present in structure (map):

```console
❯ liitos -d test/fixtures/basic -f mn-not-present -t abc
ERROR: facet (mn-not-present) of target (abc) not in ['mn', 'opq']
```

Infvalid asset link of facet for target document key:

```console
❯ liitos -d test/fixtures/basic -f opq -t abc
ERROR: bind asset link (bind-opq.txt) for facet (opq) of target (abc) is invalid
```
