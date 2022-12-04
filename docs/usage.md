# Usage

## Help Screen

```console
❯ liitos --help

 Usage: liitos [OPTIONS] COMMAND [ARGS]...

 Splice (Finnish liitos) contributions.

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version  -V        Display the application version and exit                                                                │
│ --help     -h        Show this message and exit.                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ approvals     Weave in the approvals for facet of target within document root.                                               │
│ changes       Weave in the changes for facet of target within document root.                                                 │
│ concat        Concatenate the markdown tree for facet of target within render/pdf below document root.                       │
│ render        Render the markdown tree for facet of target within render/pdf below document root.                            │
│ verify        Verify the structure definition against the file system.                                                       │
│ version       Display the application version and exit.                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Version

```console
❯ Splice (Finnish liitos) contributions. version 2022.12.3+parent.84710d29
```

## Verification Example

All good:

```console
❯ liitos verify -d test/fixtures/basic -f mn -t abc
2022-12-04T00:23:04.410992+00:00 INFO [LIITOS]: starting verification of facet (mn) for target (abc) with structure map (structure.yml) in document root (test/fixtures/basic)
2022-12-04T00:23:04.413316+00:00 INFO [LIITOS]: - target (abc) OK
2022-12-04T00:23:04.413342+00:00 INFO [LIITOS]: - facet (mn) of target (abc) OK
2022-12-04T00:23:04.415746+00:00 INFO [LIITOS]: - assets (approvals, bind, changes, meta) for facet (mn) of target (abc) OK
2022-12-04T00:23:04.415776+00:00 INFO [LIITOS]: loading signatures from signatures_path='approvals.json'
2022-12-04T00:23:04.415834+00:00 INFO [LIITOS]: signatures=({'columns': ['Approvals', 'Name'], 'rows': [['Author', 'One Author'], ['Review', 'One Reviewer'], ['Approved', 'One Approver']]}, '')
2022-12-04T00:23:04.415852+00:00 INFO [LIITOS]: loading history from history_path='changes.json'
2022-12-04T00:23:04.415896+00:00 INFO [LIITOS]: history=({'columns': ['issue', 'author', 'date', 'summary'], 'rows': [['01', 'One Author', '31.12.2024', 'Initial Issue']]}, '')
2022-12-04T00:23:04.415911+00:00 INFO [LIITOS]: loading metadata from metadata_path='meta-mn.yml'
2022-12-04T00:23:04.416835+00:00 INFO [LIITOS]: info=({'document': {'short_title': 'The Y', 'long_title': 'The Real Y', 'sub_title': None, 'type': 'Engineering Document', 'id': 'ID-X-1234-00', 'issue': '01', 'revision': '00', 'head_iss_rev': 'Iss @issue, Rev @revision', 'date': '21 OCT 2022', 'blurb_header': 'Some Comp. Proprietary Information', 'page_count_prefix': 'Page', 'toc': True, 'lof': False, 'lot': False}}, '')
2022-12-04T00:23:04.416858+00:00 INFO [LIITOS]: successful verification
```

Target document key not present in structure (map):

```console
❯ liitos verify -d test/fixtures/basic -f mn -t no-target
2022-12-04T00:23:41.854342+00:00 INFO [LIITOS]: starting verification of facet (mn) for target (no-target) with structure map (structure.yml) in document root (test/fixtures/basic)
2022-12-04T00:23:41.856236+00:00 ERROR [LIITOS]: failed verification with: target (no-target) not in ['abc']
```

Facet key for target document not present in structure (map):

```console
❯ liitos verify -d test/fixtures/basic -f no-facet -t abc
2022-12-04T00:24:16.167166+00:00 INFO [LIITOS]: starting verification of facet (no-facet) for target (abc) with structure map (structure.yml) in document root (test/fixtures/basic)
2022-12-04T00:24:16.169116+00:00 INFO [LIITOS]: - target (abc) OK
2022-12-04T00:24:16.169151+00:00 ERROR [LIITOS]: failed verification with: facet (no-facet) of target (abc) not in ['missing', 'mn', 'opq']
```

Invalid asset link of facet for target document key:

```console
❯ liitos verify -d test/fixtures/basic -f opq -t abc
2022-12-04T00:24:38.290557+00:00 INFO [LIITOS]: starting verification of facet (opq) for target (abc) with structure map (structure.yml) in document root (test/fixtures/basic)
2022-12-04T00:24:38.292256+00:00 INFO [LIITOS]: - target (abc) OK
2022-12-04T00:24:38.292283+00:00 INFO [LIITOS]: - facet (opq) of target (abc) OK
2022-12-04T00:24:38.294568+00:00 INFO [LIITOS]: - assets (approvals, bind, changes, meta) for facet (opq) of target (abc) OK
2022-12-04T00:24:38.294594+00:00 INFO [LIITOS]: loading signatures from signatures_path='approvals.yml'
2022-12-04T00:24:38.295121+00:00 INFO [LIITOS]: signatures=({'approvals': [{'role': 'Author', 'name': 'One Author'}, {'role': 'Review', 'name': 'One Reviewer'}, {'role': 'Approved', 'name': 'One Approver'}]}, '')
2022-12-04T00:24:38.295144+00:00 INFO [LIITOS]: loading history from history_path='changes.yml'
2022-12-04T00:24:38.295513+00:00 INFO [LIITOS]: history=({'changes': [{'issue': '01', 'author': 'One Author', 'date': '31.12.2024', 'summary': 'Initial Issue'}]}, '')
2022-12-04T00:24:38.295532+00:00 INFO [LIITOS]: loading metadata from metadata_path='meta-opq.md'
2022-12-04T00:24:38.295687+00:00 INFO [LIITOS]: info=({'setting': 'special opq value'}, '')
2022-12-04T00:24:38.295704+00:00 INFO [LIITOS]: successful verification
```

## Concat

```console
❯ liitos concat example/deep -t prod_kind -f deep
2022-12-04T00:26:11.077780+00:00 INFO [LIITOS]: parsed target (prod_kind) and facet (deep) from request
2022-12-04T00:26:11.078499+00:00 INFO [LIITOS]: executing prelude of command (concat) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (example/deep) coming from (/some/where)
2022-12-04T00:26:11.079478+00:00 INFO [LIITOS]: prelude teleported processor into the document root at (/some/where/example/deep/)
2022-12-04T00:26:11.079641+00:00 INFO [LIITOS]: concatenate (this processor) teleported into the render/pdf location (/some/where/example/deep/render/pdf/)
2022-12-04T00:26:11.080159+00:00 INFO [LIITOS]: found single target (prod_kind) with facets (['deep'])
2022-12-04T00:26:11.080185+00:00 WARNING [LIITOS]: structure does not strictly provide the expected aspects ['approvals', 'bind', 'changes', 'meta'] for target (prod_kind) and facet (deep)
2022-12-04T00:26:11.080215+00:00 WARNING [LIITOS]: - found the following aspects instead:                   ['approvals', 'bind', 'changes', 'meta', 'render'] instead
2022-12-04T00:26:11.088734+00:00 INFO [LIITOS]: processing binder ...
2022-12-04T00:26:11.093026+00:00 INFO [LIITOS]: resulting tree:
2022-12-04T00:26:11.093117+00:00 INFO [LIITOS]: /
2022-12-04T00:26:11.093136+00:00 INFO [LIITOS]: ├── 1.md
2022-12-04T00:26:11.093151+00:00 INFO [LIITOS]: │   └── part/a.md
2022-12-04T00:26:11.093164+00:00 INFO [LIITOS]: │       ├── part/a1.md
2022-12-04T00:26:11.093177+00:00 INFO [LIITOS]: │       │   └── part/a2.md
2022-12-04T00:26:11.093190+00:00 INFO [LIITOS]: │       └── part/sub/as.md
2022-12-04T00:26:11.093202+00:00 INFO [LIITOS]: │           └── part/sub/as1.md
2022-12-04T00:26:11.093215+00:00 INFO [LIITOS]: ├── 2.md
2022-12-04T00:26:11.093227+00:00 INFO [LIITOS]: │   └── 3.md
2022-12-04T00:26:11.093240+00:00 INFO [LIITOS]: └── other/b.md
2022-12-04T00:26:11.093252+00:00 INFO [LIITOS]: provisioning chains for the 4 bottom up leaf paths:
2022-12-04T00:26:11.093265+00:00 INFO [LIITOS]:  0: part/a2.md -> part/a1.md -> part/a.md -> 1.md -> /
2022-12-04T00:26:11.093278+00:00 INFO [LIITOS]:  1: part/sub/as1.md -> part/sub/as.md -> part/a.md -> 1.md -> /
2022-12-04T00:26:11.093290+00:00 INFO [LIITOS]:  2: 3.md -> 2.md -> /
2022-12-04T00:26:11.093302+00:00 INFO [LIITOS]:  3: other/b.md -> /
2022-12-04T00:26:11.093314+00:00 INFO [LIITOS]: dependencies for the 9 document parts:
2022-12-04T00:26:11.093327+00:00 INFO [LIITOS]: - part 1.md <-( 1 include )-
2022-12-04T00:26:11.093339+00:00 INFO [LIITOS]:   + between lines   4 and   7 include fragment part/a.md
2022-12-04T00:26:11.093351+00:00 INFO [LIITOS]: - part part/a.md <--( 2 includes )--
2022-12-04T00:26:11.093364+00:00 INFO [LIITOS]:   + between lines   4 and   7 include fragment part/a1.md
2022-12-04T00:26:11.093376+00:00 INFO [LIITOS]:   + between lines  13 and  13 include fragment part/sub/as.md
2022-12-04T00:26:11.093389+00:00 INFO [LIITOS]: - part part/a1.md <-( 1 include )-
2022-12-04T00:26:11.093402+00:00 INFO [LIITOS]:   + between lines  12 and  15 include fragment part/a2.md
2022-12-04T00:26:11.093415+00:00 INFO [LIITOS]: - part part/a2.md (no includes)
2022-12-04T00:26:11.093428+00:00 INFO [LIITOS]:   * did concat part/a2.md document for insertion
2022-12-04T00:26:11.093441+00:00 INFO [LIITOS]: - part part/sub/as.md <-( 1 include )-
2022-12-04T00:26:11.093453+00:00 INFO [LIITOS]:   + between lines   4 and   7 include fragment part/sub/as1.md
2022-12-04T00:26:11.093466+00:00 INFO [LIITOS]: - part part/sub/as1.md (no includes)
2022-12-04T00:26:11.093478+00:00 INFO [LIITOS]:   * did concat part/sub/as1.md document for insertion
2022-12-04T00:26:11.093490+00:00 INFO [LIITOS]: - part 2.md <-( 1 include )-
2022-12-04T00:26:11.093502+00:00 INFO [LIITOS]:   + between lines   6 and   9 include fragment 3.md
2022-12-04T00:26:11.093513+00:00 INFO [LIITOS]: - part 3.md (no includes)
2022-12-04T00:26:11.093524+00:00 INFO [LIITOS]:   * did concat 3.md document for insertion
2022-12-04T00:26:11.093536+00:00 INFO [LIITOS]: - part other/b.md (no includes)
2022-12-04T00:26:11.093549+00:00 INFO [LIITOS]:   * did concat other/b.md document for insertion
2022-12-04T00:26:11.093561+00:00 INFO [LIITOS]: starting insertions bottom up for the 4 inclusion chains:
2022-12-04T00:26:11.093583+00:00 INFO [LIITOS]:   Insertion ongoing with parts (2.md, part/a1.md, part/sub/as.md) remaining
2022-12-04T00:26:11.093607+00:00 INFO [LIITOS]:   Insertion ongoing with parts (part/a.md, part/a.md) remaining
2022-12-04T00:26:11.093631+00:00 INFO [LIITOS]:   Insertion ongoing with parts (1.md, 1.md) remaining
2022-12-04T00:26:11.093651+00:00 INFO [LIITOS]: writing final concat markdown to document.md
2022-12-04T00:26:11.093891+00:00 INFO [LIITOS]: collecting assets (images and diagrams)
2022-12-04T00:26:11.100591+00:00 INFO [LIITOS]: concat result document (document.md) and artifacts are within folder (/some/where/example/deep/render/pdf/)
2022-12-04T00:26:11.100636+00:00 INFO [LIITOS]: processing complete - SUCCESS
```

## Render

```console
❯ liitos concat example/deep -t prod_kind -f deep
# ... - - - 8< - - - ...
2022-12-04T00:27:36.141418+00:00 INFO [LIITOS]: processing complete - SUCCESS
2022-12-04T00:27:36.141488+00:00 INFO [LIITOS]: before met.weave(): /some/where/example/deep/render/pdf set doc (../../)
2022-12-04T00:27:36.141508+00:00 INFO [LIITOS]: parsed target (prod_kind) and facet (deep) from request
2022-12-04T00:27:36.141545+00:00 INFO [LIITOS]: executing prelude of command (meta) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/some/where/example/deep/render/pdf)
2022-12-04T00:27:36.142099+00:00 INFO [LIITOS]: prelude teleported processor into the document root at (/some/where/example/deep/)
2022-12-04T00:27:36.142168+00:00 INFO [LIITOS]: meta (this processor) teleported into the render/pdf location (/some/where/example/deep/render/pdf/)
2022-12-04T00:27:36.142641+00:00 INFO [LIITOS]: found single target (prod_kind) with facets (['deep'])
2022-12-04T00:27:36.142666+00:00 WARNING [LIITOS]: structure does not strictly provide the expected aspects ['approvals', 'bind', 'changes', 'meta'] for target (prod_kind) and facet (deep)
2022-12-04T00:27:36.142683+00:00 WARNING [LIITOS]: - found the following aspects instead:                   ['approvals', 'bind', 'changes', 'meta', 'render'] instead
2022-12-04T00:27:36.146971+00:00 INFO [LIITOS]: weaving in the meta data ...
2022-12-04T00:27:36.147010+00:00 WARNING [LIITOS]: footer_page_number_prefix value missing ... setting default (Page)
2022-12-04T00:27:36.147036+00:00 WARNING [LIITOS]: footer_page_number_prefix value missing ... setting default (Iss \theMetaIssCode, Rev \theMetaRevCode)
2022-12-04T00:27:36.147053+00:00 WARNING [LIITOS]: proprietary_information value missing ... setting default (Proprietary Information MISSING)
2022-12-04T00:27:36.147381+00:00 INFO [LIITOS]: before sig.weave(): /some/where/example/deep/render/pdf set doc (../../)
2022-12-04T00:27:36.147424+00:00 INFO [LIITOS]: relocated for sig.weave(): /some/where/example/deep/render/pdf with doc (../../)
2022-12-04T00:27:36.147482+00:00 INFO [LIITOS]: executing prelude of command (approvals) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/some/where/example/deep/render/pdf)
2022-12-04T00:27:36.148012+00:00 INFO [LIITOS]: detected approvals channel (yaml) weaving in from (approvals.yml)
2022-12-04T00:27:36.148032+00:00 INFO [LIITOS]: loading signatures from signatures_path='approvals.yml'
2022-12-04T00:27:36.148532+00:00 INFO [LIITOS]: signatures=({'approvals': [{'name': 'An Author', 'role': 'Author'}, {'name': 'A Reviewer', 'role': 'Review'}, {'name': 'An App Rover', 'role': 'Approved'}]}, '')
2022-12-04T00:27:36.148551+00:00 INFO [LIITOS]: plausibility tests for approvals ...
2022-12-04T00:27:36.148575+00:00 INFO [LIITOS]: calculated extra pushdown to be 18em
2022-12-04T00:27:36.149016+00:00 INFO [LIITOS]: weaving in the approvals from approvals.yml...
2022-12-04T00:27:36.149304+00:00 INFO [LIITOS]: before chg.weave(): /some/where/example/deep set doc (../../)
2022-12-04T00:27:36.149338+00:00 INFO [LIITOS]: relocated for chg.weave(): /some/where/example/deep/render/pdf with doc (../../)
2022-12-04T00:27:36.149376+00:00 INFO [LIITOS]: executing prelude of command (changes) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/some/where/example/deep/render/pdf)
2022-12-04T00:27:36.149825+00:00 INFO [LIITOS]: detected changes channel (yaml) weaving in from (changes.yml)
2022-12-04T00:27:36.149843+00:00 INFO [LIITOS]: loading changes from changes_path='changes.yml'
2022-12-04T00:27:36.150188+00:00 INFO [LIITOS]: changes=({'changes': [{'author': 'An Author', 'date': 'PUBLICATIONDATE', 'issue': '01', 'summary': 'Initial Issue'}]}, '')
2022-12-04T00:27:36.150205+00:00 INFO [LIITOS]: plausibility tests for changes ...
2022-12-04T00:27:36.150568+00:00 INFO [LIITOS]: weaving in the changes ...
```
