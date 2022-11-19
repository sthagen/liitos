# Usage

## Help Screen

```console
❯ liitos --help
usage: liitos [-h] --facet FACET --target TARGET [--document-root DOC_ROOT]
              [--structure STRUCTURE] [--verbose] [doc_root_pos]

Splice (Finnish liitos) contributions.

positional arguments:
  doc_root_pos          Root of the document tree to visit. Optional
                        (default: empty for PWD)

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
  --verbose, -v         work logging more information along the way
                        (default: False)
```

## Verification Example

All good:

```console
❯ liitos -d test/fixtures/basic -f mn -t abc
2022-11-02T21:16:48.477818+00:00 INFO [LIITOS]: Starting verification of facet (mn) for target (abc) with structure map (structure.yml) in document root (test/fixtures/basic)
2022-11-02T21:16:48.479516+00:00 INFO [LIITOS]: - target (abc) OK
2022-11-02T21:16:48.479546+00:00 INFO [LIITOS]: - facet (mn) of target (abc) OK
2022-11-02T21:16:48.481667+00:00 INFO [LIITOS]: - assets (approvals, bind, changes, meta) for facet (mn) of target (abc) OK
2022-11-02T21:16:48.481692+00:00 INFO [LIITOS]: Loading signatures from signatures_path='approvals.json'
2022-11-02T21:16:48.481741+00:00 INFO [LIITOS]: signatures=({'columns': ['Approvals', 'Name'], 'rows': [['Author', 'One Author'], ['Review', 'One Reviewer'], ['Approved', 'One Approver']]}, '')
2022-11-02T21:16:48.481760+00:00 INFO [LIITOS]: Loading history from history_path='changes.json'
2022-11-02T21:16:48.481801+00:00 INFO [LIITOS]: history=({'columns': ['issue', 'author', 'date', 'summary'], 'rows': [['01', 'One Author', '31.12.2024', 'Initial Issue']]}, '')
2022-11-02T21:16:48.481819+00:00 INFO [LIITOS]: Loading metadata from metadata_path='meta-mn.yml'
2022-11-02T21:16:48.482799+00:00 INFO [LIITOS]: info=({'document': {'short_title': 'The Y', 'long_title': 'The Real Y', 'sub_title': None, 'type': 'Engineering Document', 'id': 'ID-X-1234-00', 'issue': '01', 'revision': '00', 'head_iss_rev': 'Iss @issue, Rev @revision', 'date': '21 OCT 2022', 'blurb_header': 'Some Comp. Proprietary Information', 'page_count_prefix': 'Page', 'toc': True, 'lof': False, 'lot': False}}, '')
2022-11-02T21:16:48.482822+00:00 INFO [LIITOS]: Successful verification
```

Target document key not present in structure (map):

```console
❯ liitos -d test/fixtures/basic -f mn -t no-target
2022-09-18T13:38:40.716237+00:00 INFO [LIITOS]: Starting verification of facet (mn) for target (no-target) with structure map (structure.yml) in document root (test/fixtures/basic)
2022-09-18T13:38:40.717347+00:00 ERROR [LIITOS]: Failed verification with: target (no-target) not in ['abc']
```

Facet key for target document not present in structure (map):

```console
❯ liitos -d test/fixtures/basic -f no-facet -t abc
2022-09-18T13:38:48.084175+00:00 INFO [LIITOS]: Starting verification of facet (no-facet) for target (abc) with structure map (structure.yml) in document root (test/fixtures/basic)
2022-09-18T13:38:48.085339+00:00 INFO [LIITOS]: - target (abc) OK
2022-09-18T13:38:48.085371+00:00 ERROR [LIITOS]: Failed verification with: facet (no-facet) of target (abc) not in ['mn', 'opq']
```

Invalid asset link of facet for target document key:

```console
❯ liitos -d test/fixtures/basic -f opq -t abc
2022-09-18T13:38:53.405740+00:00 INFO [LIITOS]: Starting verification of facet (opq) for target (abc) with structure map (structure.yml) in document root (test/fixtures/basic)
2022-09-18T13:38:53.406907+00:00 INFO [LIITOS]: - target (abc) OK
2022-09-18T13:38:53.406937+00:00 INFO [LIITOS]: - facet (opq) of target (abc) OK
2022-09-18T13:38:53.406978+00:00 ERROR [LIITOS]: Failed verification with: bind asset link (bind-opq.txt) for facet (opq) of target (abc) is invalid
```
