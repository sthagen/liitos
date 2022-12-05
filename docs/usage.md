# Usage

## Help Screen

```console
❯ liitos --help


 Usage: liitos [OPTIONS] COMMAND [ARGS]...

 Splice (Finnish liitos) contributions.

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version  -V        Display the application version and exit                                                    │
│ --help     -h        Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ approvals  Weave in the approvals for facet of target within document root.                                      │
│ changes    Weave in the changes for facet of target within document root.                                        │
│ concat     Concatenate the markdown tree for facet of target within render/pdf below document root.              │
│ eject      Eject a template. Enter unique part to retrieve, any unknown word to obtain the list of known         │
│            templates.                                                                                            │
│ render     Render the markdown tree for facet of target within render/pdf below document root.                   │
│ verify     Verify the structure definition against the file system.                                              │
│ version    Display the application version and exit.                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Version

```console
❯ Splice (Finnish liitos) contributions. version 2022.12.5+parent.aec13b7a
```

## Eject 

You can eject template files to modify these and provide externally per environment variables for overriding the built-in variants.

Any unique start of template name will yield, executing the command without argument provides a list of available templates (i.e. their names):

```console
❯ liitos eject
2022-12-05T19:14:56.833200+00:00 ERROR [LIITOS]: eject of template with no name requested
2022-12-05T19:14:56.833815+00:00 INFO [LIITOS]: templates known: (approvals-yaml, bookmatter-pdf, changes-yaml, driver-pdf, meta-base-yaml, meta-patch-yaml, metadata-pdf, publisher-pdf, setup-pdf, vocabulary-yaml)
```

Example fetch the approvals data file by only naming the first letter (as it is unique) of the template name:

```console
❯ liitos eject a
approvals:
- name: An Author
  role: Author
- name: A Reviewer
  role: Review
- name: An App Rover
  role: Approved

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

Similarly verifying the structural integrity of the deep example:

```console
❯ liitos verify example/deep --target prod_kind --facet deep
2022-12-05T19:18:08.986407+00:00 INFO [LIITOS]: starting verification of facet (deep) for target (prod_kind) with structure map (structure.yml) in document root (example/deep)
2022-12-05T19:18:08.987810+00:00 INFO [LIITOS]: - target (prod_kind) OK
2022-12-05T19:18:08.987840+00:00 INFO [LIITOS]: - facet (deep) of target (prod_kind) OK
2022-12-05T19:18:08.991024+00:00 INFO [LIITOS]: - assets (approvals, bind, changes, meta) for facet (deep) of target (prod_kind) OK
2022-12-05T19:18:08.991048+00:00 INFO [LIITOS]: loading signatures from signatures_path='approvals.yml'
2022-12-05T19:18:08.991548+00:00 INFO [LIITOS]: signatures=({'approvals': [{'name': 'An Author', 'role': 'Author'}, {'name': 'A Reviewer', 'role': 'Review'}, {'name': 'An App Rover', 'role': 'Approved'}]}, '')
2022-12-05T19:18:08.991569+00:00 INFO [LIITOS]: loading history from history_path='changes.yml'
2022-12-05T19:18:08.991916+00:00 INFO [LIITOS]: history=({'changes': [{'author': 'An Author', 'date': 'PUBLICATIONDATE', 'issue': '01', 'summary': 'Initial Issue'}]}, '')
2022-12-05T19:18:08.991933+00:00 INFO [LIITOS]: loading metadata from metadata_path='meta-deep.yml'
2022-12-05T19:18:08.992270+00:00 INFO [LIITOS]: info=({'document': {'import': 'meta-base.yml', 'patch': {'header_id': 'P99999', 'header_date': 'PUBLICATIONDATE'}}}, '')
2022-12-05T19:18:08.992290+00:00 INFO [LIITOS]: successful verification
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
❯ liitos render example/deep -t prod_kind -f deep
# ... - - - 8< - - - ...
2022-12-05T19:11:29.552633+00:00 INFO [LIITOS]: processing complete - SUCCESS
2022-12-05T19:11:29.552645+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:29.552701+00:00 INFO [LIITOS]: before met.weave(): /some/where/example/deep/render/pdf set doc (../../)
2022-12-05T19:11:29.552719+00:00 INFO [LIITOS]: parsed target (prod_kind) and facet (deep) from request
2022-12-05T19:11:29.552756+00:00 INFO [LIITOS]: executing prelude of command (meta) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/some/where/example/deep/render/pdf)
2022-12-05T19:11:29.553278+00:00 INFO [LIITOS]: prelude teleported processor into the document root at (/some/where/example/deep/)
2022-12-05T19:11:29.553326+00:00 INFO [LIITOS]: meta (this processor) teleported into the render/pdf location (/some/where/example/deep/render/pdf/)
2022-12-05T19:11:29.553790+00:00 INFO [LIITOS]: found single target (prod_kind) with facets (['deep'])
2022-12-05T19:11:29.553811+00:00 WARNING [LIITOS]: structure does not strictly provide the expected aspects ['approvals', 'bind', 'changes', 'meta'] for target (prod_kind) and facet (deep)
2022-12-05T19:11:29.553826+00:00 WARNING [LIITOS]: - found the following aspects instead:                   ['approvals', 'bind', 'changes', 'meta', 'render'] instead
2022-12-05T19:11:29.558008+00:00 INFO [LIITOS]: weaving in the meta data per metadata.tex.in into metadata.tex ...
2022-12-05T19:11:29.558083+00:00 INFO [LIITOS]: header_issue_revision_combined value missing ... setting default (Iss \theMetaIssCode, Rev \theMetaRevCode)
2022-12-05T19:11:29.559175+00:00 INFO [LIITOS]: weaving in the meta data per driver.tex.in into driver.tex ...
2022-12-05T19:11:29.559884+00:00 INFO [LIITOS]: weaving in the meta data per setup.tex.in into setup.tex ...
2022-12-05T19:11:29.560776+00:00 INFO [LIITOS]: before sig.weave(): /some/where/example/deep/render/pdf set doc (../../)
2022-12-05T19:11:29.560811+00:00 INFO [LIITOS]: relocated for sig.weave(): /some/where/example/deep/render/pdf with doc (../../)
2022-12-05T19:11:29.560829+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:29.560866+00:00 INFO [LIITOS]: executing prelude of command (approvals) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/some/where/example/deep/render/pdf)
2022-12-05T19:11:29.561329+00:00 INFO [LIITOS]: detected approvals channel (yaml) weaving in from (approvals.yml)
2022-12-05T19:11:29.561347+00:00 INFO [LIITOS]: loading signatures from signatures_path='approvals.yml'
2022-12-05T19:11:29.561840+00:00 INFO [LIITOS]: signatures=({'approvals': [{'name': 'An Author', 'role': 'Author'}, {'name': 'A Reviewer', 'role': 'Review'}, {'name': 'An App Rover', 'role': 'Approved'}]}, '')
2022-12-05T19:11:29.561857+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:29.561869+00:00 INFO [LIITOS]: plausibility tests for approvals ...
2022-12-05T19:11:29.561890+00:00 INFO [LIITOS]: calculated extra pushdown to be 18em
2022-12-05T19:11:29.562296+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:29.562310+00:00 INFO [LIITOS]: weaving in the approvals from approvals.yml...
2022-12-05T19:11:29.562529+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:29.562562+00:00 INFO [LIITOS]: before chg.weave(): /some/where/example/deep set doc (../../)
2022-12-05T19:11:29.562592+00:00 INFO [LIITOS]: relocated for chg.weave(): /some/where/example/deep/render/pdf with doc (../../)
2022-12-05T19:11:29.562606+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:29.562642+00:00 INFO [LIITOS]: executing prelude of command (changes) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/some/where/example/deep/render/pdf)
2022-12-05T19:11:29.563085+00:00 INFO [LIITOS]: detected changes channel (yaml) weaving in from (changes.yml)
2022-12-05T19:11:29.563101+00:00 INFO [LIITOS]: loading changes from changes_path='changes.yml'
2022-12-05T19:11:29.563445+00:00 INFO [LIITOS]: changes=({'changes': [{'author': 'An Author', 'date': 'PUBLICATIONDATE', 'issue': '01', 'summary': 'Initial Issue'}]}, '')
2022-12-05T19:11:29.563462+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:29.563475+00:00 INFO [LIITOS]: plausibility tests for changes ...
2022-12-05T19:11:29.563919+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:29.563933+00:00 INFO [LIITOS]: weaving in the changes ...
2022-12-05T19:11:29.564118+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:29.564191+00:00 INFO [LIITOS]: before chg.weave(): /some/where/example/deep set doc (../../)
2022-12-05T19:11:29.564220+00:00 INFO [LIITOS]: relocated for chg.weave(): /some/where/example/deep/render/pdf with doc (../../)
2022-12-05T19:11:29.564234+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:29.564247+00:00 INFO [LIITOS]: parsed target (prod_kind) and facet (deep) from request
2022-12-05T19:11:29.564280+00:00 INFO [LIITOS]: executing prelude of command (render) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/some/where/example/deep/render/pdf)
2022-12-05T19:11:29.564730+00:00 INFO [LIITOS]: prelude teleported processor into the document root at (/some/where/example/deep/)
2022-12-05T19:11:29.564764+00:00 INFO [LIITOS]: inspecting any patch spec file (patch.yml) ...
2022-12-05T19:11:29.565544+00:00 INFO [LIITOS]: - loaded 1 patch pair from patch spec file (patch.yml)
2022-12-05T19:11:29.565581+00:00 INFO [LIITOS]: render (this processor) teleported into the render/pdf location (/some/where/example/deep/render/pdf/)
2022-12-05T19:11:29.566023+00:00 INFO [LIITOS]: found single target (prod_kind) with facets (['deep'])
2022-12-05T19:11:29.566043+00:00 INFO [LIITOS]: found render instruction with value (True)
2022-12-05T19:11:29.566056+00:00 INFO [LIITOS]: we will render ...
2022-12-05T19:11:29.566068+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:29.566080+00:00 INFO [LIITOS]: transforming SVG assets to high resolution PNG bitmaps ...
2022-12-05T19:11:30.646089+00:00 INFO [LIITOS]: svg-to-png: /some/where/example/deep/render/pdf/diagrams/squares-and-edges.svg /some/where/example/deep/render/pdf/diagrams/squares-and-edges.png png 100% 1x 0:0:220:100 220:100
2022-12-05T19:11:30.735785+00:00 INFO [LIITOS]: svg-to-png process (['svgexport', PosixPath('diagrams/squares-and-edges.svg'), 'diagrams/squares-and-edges.png', '100%']) returned 0
2022-12-05T19:11:30.735899+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:30.735941+00:00 INFO [LIITOS]: rewriting src attribute values of SVG to PNG sources ...
2022-12-05T19:11:30.875749+00:00 INFO [LIITOS]: transform[#97]: ![Caption Text for SVG](diagrams/squares-and-edges.svg "Alt Text for SVG")
2022-12-05T19:11:30.875892+00:00 INFO [LIITOS]:      into[#97]: ![Caption Text for SVG](diagrams/squares-and-edges.png "Alt Text for SVG")
2022-12-05T19:11:30.876632+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:30.876775+00:00 INFO [LIITOS]: pandoc -f markdown+link_attributes -t latex document.md -o document.tex --filter mermaid-filter ...
2022-12-05T19:11:31.327037+00:00 INFO [LIITOS]: markdown-to-latex: [INFO] Running filter mermaid-filter
2022-12-05T19:11:31.383895+00:00 INFO [LIITOS]: markdown-to-latex: [INFO] Completed filter mermaid-filter in 2 ms
2022-12-05T19:11:31.399460+00:00 INFO [LIITOS]: markdown-to-latex process (['pandoc', '--verbose', '-f', 'markdown+link_attributes', '-t', 'latex', 'document.md', '-o', 'document.tex', '--filter', 'mermaid-filter']) returned 0
2022-12-05T19:11:31.399527+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:31.399548+00:00 INFO [LIITOS]: move any captions below tables ...
2022-12-05T19:11:31.402327+00:00 INFO [LIITOS]: start of a table environment at line #62
2022-12-05T19:11:31.402363+00:00 INFO [LIITOS]: - found the caption start at line #63
2022-12-05T19:11:31.402381+00:00 INFO [LIITOS]: - multi line caption at line #63
2022-12-05T19:11:31.402399+00:00 INFO [LIITOS]: - caption read at line #64
2022-12-05T19:11:31.402422+00:00 INFO [LIITOS]: end of table env detected at line #79
2022-12-05T19:11:31.402594+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:31.402613+00:00 INFO [LIITOS]: inject stem (derived from file name) labels ...
2022-12-05T19:11:31.402921+00:00 INFO [LIITOS]: start of a figure environment at line #41
2022-12-05T19:11:31.402942+00:00 INFO [LIITOS]: within a figure environment at line #43
2022-12-05T19:11:31.402955+00:00 INFO [LIITOS]: \includegraphics{images/blue.png}
2022-12-05T19:11:31.402971+00:00 INFO [LIITOS]: \label{fig:blue}
2022-12-05T19:11:31.402984+00:00 INFO [LIITOS]: - found the caption start at line #44
2022-12-05T19:11:31.402998+00:00 INFO [LIITOS]: end of figure env detected at line #45
2022-12-05T19:11:31.403016+00:00 INFO [LIITOS]: start of a figure environment at line #49
2022-12-05T19:11:31.403029+00:00 INFO [LIITOS]: within a figure environment at line #51
2022-12-05T19:11:31.403042+00:00 INFO [LIITOS]: \includegraphics{images/blue.png}
2022-12-05T19:11:31.403055+00:00 INFO [LIITOS]: \label{fig:blue}
2022-12-05T19:11:31.403068+00:00 INFO [LIITOS]: - found the caption start at line #52
2022-12-05T19:11:31.403080+00:00 INFO [LIITOS]: end of figure env detected at line #53
2022-12-05T19:11:31.403096+00:00 WARNING [LIITOS]: graphics include outside of a figure environment at line #55
2022-12-05T19:11:31.403122+00:00 ERROR [LIITOS]: line#55|\includegraphics{images/blue.png}
2022-12-05T19:11:31.403137+00:00 INFO [LIITOS]: trying to fix temporarily ... watch for marker MISSING-CAPTION-IN-MARKDOWN
2022-12-05T19:11:31.403150+00:00 INFO [LIITOS]: \label{fig:blue}
2022-12-05T19:11:31.403182+00:00 INFO [LIITOS]: start of a figure environment at line #108
2022-12-05T19:11:31.403604+00:00 INFO [LIITOS]: within a figure environment at line #110
2022-12-05T19:11:31.403620+00:00 INFO [LIITOS]: \includegraphics{images/yellow.png}
2022-12-05T19:11:31.403634+00:00 INFO [LIITOS]: \label{fig:yellow}
2022-12-05T19:11:31.403648+00:00 INFO [LIITOS]: - found the caption start at line #111
2022-12-05T19:11:31.403663+00:00 INFO [LIITOS]: end of figure env detected at line #112
2022-12-05T19:11:31.403679+00:00 INFO [LIITOS]: start of a figure environment at line #119
2022-12-05T19:11:31.403755+00:00 INFO [LIITOS]: within a figure environment at line #121
2022-12-05T19:11:31.403768+00:00 INFO [LIITOS]: \includegraphics{images/red.png}
2022-12-05T19:11:31.403782+00:00 INFO [LIITOS]: \label{fig:red}
2022-12-05T19:11:31.403796+00:00 INFO [LIITOS]: - found the caption start at line #122
2022-12-05T19:11:31.403811+00:00 INFO [LIITOS]: end of figure env detected at line #123
2022-12-05T19:11:31.403829+00:00 INFO [LIITOS]: start of a figure environment at line #135
2022-12-05T19:11:31.403844+00:00 INFO [LIITOS]: within a figure environment at line #137
2022-12-05T19:11:31.403857+00:00 INFO [LIITOS]: \includegraphics{images/red.png}
2022-12-05T19:11:31.403872+00:00 INFO [LIITOS]: \label{fig:red}
2022-12-05T19:11:31.403886+00:00 INFO [LIITOS]: - found the caption start at line #138
2022-12-05T19:11:31.403900+00:00 INFO [LIITOS]: end of figure env detected at line #139
2022-12-05T19:11:31.403914+00:00 INFO [LIITOS]: start of a figure environment at line #141
2022-12-05T19:11:31.403928+00:00 INFO [LIITOS]: within a figure environment at line #143
2022-12-05T19:11:31.403942+00:00 INFO [LIITOS]: \includegraphics{images/lime.png}
2022-12-05T19:11:31.403957+00:00 INFO [LIITOS]: \label{fig:lime}
2022-12-05T19:11:31.404038+00:00 INFO [LIITOS]: - found the caption start at line #144
2022-12-05T19:11:31.404194+00:00 INFO [LIITOS]: end of figure env detected at line #145
2022-12-05T19:11:31.404210+00:00 INFO [LIITOS]: start of a figure environment at line #149
2022-12-05T19:11:31.404225+00:00 INFO [LIITOS]: within a figure environment at line #151
2022-12-05T19:11:31.404238+00:00 INFO [LIITOS]: \includegraphics{diagrams/squares-and-edges.png}
2022-12-05T19:11:31.404253+00:00 INFO [LIITOS]: \label{fig:squares-and-edges}
2022-12-05T19:11:31.404326+00:00 INFO [LIITOS]: - found the caption start at line #152
2022-12-05T19:11:31.404340+00:00 INFO [LIITOS]: end of figure env detected at line #153
2022-12-05T19:11:31.407688+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:31.407710+00:00 INFO [LIITOS]: scale figures ...
2022-12-05T19:11:31.407985+00:00 INFO [LIITOS]: trigger a scale mod for the next figure environment at line #47|\scale=0.9
2022-12-05T19:11:31.408008+00:00 INFO [LIITOS]: - found the scale target start at line #51|\includegraphics{images/blue.png}
2022-12-05T19:11:31.410990+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:31.411009+00:00 INFO [LIITOS]: apply user patches ...
2022-12-05T19:11:31.411485+00:00 INFO [LIITOS]: applying patches to 157 lines of text
2022-12-05T19:11:31.411502+00:00 INFO [LIITOS]:  - trying any (,height=\textheight]) --> (]) ...
2022-12-05T19:11:31.412840+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:31.412967+00:00 INFO [LIITOS]: cp -a driver.tex this.tex ...
2022-12-05T19:11:31.413957+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:31.413982+00:00 INFO [LIITOS]: 1/3) lualatex --shell-escape this.tex ...
2022-12-05T19:11:31.636176+00:00 INFO [LIITOS]: latex-to-pdf(1/3): This is LuaHBTeX, Version 1.15.0 (TeX Live 2022)
2022-12-05T19:11:31.636339+00:00 INFO [LIITOS]: latex-to-pdf(1/3):  system commands enabled.
2022-12-05T19:11:31.656060+00:00 INFO [LIITOS]: latex-to-pdf(1/3): (./this.tex
2022-12-05T19:11:31.656124+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX2e <2022-11-01>
2022-12-05T19:11:31.794445+00:00 INFO [LIITOS]: latex-to-pdf(1/3):  L3 programming layer <2022-11-02> (./setup.tex
2022-12-05T19:11:31.794997+00:00 INFO [LIITOS]: latex-to-pdf(1/3): Document Class: scrartcl 2022/10/12 v3.38 KOMA-Script document class (article)
2022-12-05T19:11:32.219037+00:00 INFO [LIITOS]: latex-to-pdf(1/3): For additional information on amsmath, use the `?' option.
2022-12-05T19:11:32.766121+00:00 INFO [LIITOS]: latex-to-pdf(1/3): === Package selnolig, Version 0.302, Date 2015/10/26 ===
2022-12-05T19:11:32.783538+00:00 INFO [LIITOS]: latex-to-pdf(1/3): ex.sty)) (./metadata.tex)
2022-12-05T19:11:33.065342+00:00 INFO [LIITOS]: latex-to-pdf(1/3): (./this.aux (./bookmatter.aux) (./publisher.aux) (./document.aux
2022-12-05T19:11:33.065411+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX Warning: Label `fig:blue' multiply defined.
2022-12-05T19:11:33.065431+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX Warning: Label `fig:blue' multiply defined.
2022-12-05T19:11:33.065445+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX Warning: Label `fig:red' multiply defined.
2022-12-05T19:11:33.437796+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [Loading MPS to PDF converter (version 2006.09.02).]
2022-12-05T19:11:33.446174+00:00 INFO [LIITOS]: latex-to-pdf(1/3): *geometry* driver: auto-detecting
2022-12-05T19:11:33.446222+00:00 INFO [LIITOS]: latex-to-pdf(1/3): *geometry* detected driver: luatex
2022-12-05T19:11:33.472242+00:00 INFO [LIITOS]: latex-to-pdf(1/3): (./bookmatter.tex)
2022-12-05T19:11:33.521874+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [1{/usr/local/texlive/2022/texmf-var/fonts/map/pdftex/updmap/pdftex.map}</opt/l
2022-12-05T19:11:33.537298+00:00 INFO [LIITOS]: latex-to-pdf(1/3): ogo/liitos-logo.png>] (./publisher.tex
2022-12-05T19:11:33.537363+00:00 INFO [LIITOS]: latex-to-pdf(1/3): Overfull \hbox (0.5696pt too wide) in alignment at lines 8--22
2022-12-05T19:11:33.546230+00:00 INFO [LIITOS]: latex-to-pdf(1/3): warning  (pdf backend): ignoring duplicate destination with the name 'page.1'
2022-12-05T19:11:33.580110+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [1] (./this.toc)
2022-12-05T19:11:33.609781+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [2] (./document.tex
2022-12-05T19:11:33.637376+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [3<./images/blue.png>]
2022-12-05T19:11:33.646442+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [4]
2022-12-05T19:11:33.659606+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [5<./images/yellow.png><./images/red.png>])
2022-12-05T19:11:33.671400+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [6<./images/lime.png><./diagrams/squares-and-edges.png>] (./this.aux
2022-12-05T19:11:33.674309+00:00 INFO [LIITOS]: latex-to-pdf(1/3): (./bookmatter.aux) (./publisher.aux) (./document.aux))
2022-12-05T19:11:33.674349+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX Warning: There were multiply-defined labels.
2022-12-05T19:11:33.674484+00:00 INFO [LIITOS]: latex-to-pdf(1/3):  741 words of node memory still in use:
2022-12-05T19:11:33.674505+00:00 INFO [LIITOS]: latex-to-pdf(1/3):    7 hlist, 2 vlist, 2 rule, 1 local_par, 4 glue, 4 kern, 1 penalty, 3 glyph, 1
2022-12-05T19:11:33.674520+00:00 INFO [LIITOS]: latex-to-pdf(1/3): 5 attribute, 87 glue_spec, 10 attribute_list, 3 write, 1 user_defined nodes
2022-12-05T19:11:33.674536+00:00 INFO [LIITOS]: latex-to-pdf(1/3):    avail lists: 1:3,2:1944,3:357,4:128,5:147,6:170,7:2210,8:38,9:1367,10:3,11:7
2022-12-05T19:11:33.674550+00:00 INFO [LIITOS]: latex-to-pdf(1/3): 1,12:1
2022-12-05T19:11:33.702719+00:00 INFO [LIITOS]: latex-to-pdf(1/3): </usr/local/texlive/2022/texmf-dist/fonts/opentype/public/lm/lmsans12-regular.o
2022-12-05T19:11:33.712022+00:00 INFO [LIITOS]: latex-to-pdf(1/3): tf></usr/local/texlive/2022/texmf-dist/fonts/opentype/public/lm/lmsans10-bold.o
2022-12-05T19:11:33.735551+00:00 INFO [LIITOS]: latex-to-pdf(1/3): tf></opt/fonts/ITCFranklinGothicStd-Demi.otf></opt/fonts/ITCFranklinGothicStd-B
2022-12-05T19:11:33.741241+00:00 INFO [LIITOS]: latex-to-pdf(1/3): ook.otf>
2022-12-05T19:11:33.741265+00:00 INFO [LIITOS]: latex-to-pdf(1/3): Output written on this.pdf (7 pages, 29050 bytes).
2022-12-05T19:11:33.749816+00:00 INFO [LIITOS]: latex-to-pdf(1/3): Transcript written on this.log.
2022-12-05T19:11:33.799521+00:00 INFO [LIITOS]: latex-to-pdf process 1/3  (['lualatex', '--shell-escape', 'this.tex']) returned 0
2022-12-05T19:11:33.799571+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:33.799589+00:00 INFO [LIITOS]: 2/3) lualatex --shell-escape this.tex ...
2022-12-05T19:11:34.001834+00:00 INFO [LIITOS]: latex-to-pdf(2/3): This is LuaHBTeX, Version 1.15.0 (TeX Live 2022)
2022-12-05T19:11:34.002020+00:00 INFO [LIITOS]: latex-to-pdf(2/3):  system commands enabled.
2022-12-05T19:11:34.018123+00:00 INFO [LIITOS]: latex-to-pdf(2/3): (./this.tex
2022-12-05T19:11:34.018178+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX2e <2022-11-01>
2022-12-05T19:11:34.139688+00:00 INFO [LIITOS]: latex-to-pdf(2/3):  L3 programming layer <2022-11-02> (./setup.tex
2022-12-05T19:11:34.139950+00:00 INFO [LIITOS]: latex-to-pdf(2/3): Document Class: scrartcl 2022/10/12 v3.38 KOMA-Script document class (article)
2022-12-05T19:11:34.546538+00:00 INFO [LIITOS]: latex-to-pdf(2/3): For additional information on amsmath, use the `?' option.
2022-12-05T19:11:35.057847+00:00 INFO [LIITOS]: latex-to-pdf(2/3): === Package selnolig, Version 0.302, Date 2015/10/26 ===
2022-12-05T19:11:35.074255+00:00 INFO [LIITOS]: latex-to-pdf(2/3): ex.sty)) (./metadata.tex)
2022-12-05T19:11:35.336831+00:00 INFO [LIITOS]: latex-to-pdf(2/3): (./this.aux (./bookmatter.aux) (./publisher.aux) (./document.aux
2022-12-05T19:11:35.336895+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX Warning: Label `fig:blue' multiply defined.
2022-12-05T19:11:35.336916+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX Warning: Label `fig:blue' multiply defined.
2022-12-05T19:11:35.336931+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX Warning: Label `fig:red' multiply defined.
2022-12-05T19:11:35.698975+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [Loading MPS to PDF converter (version 2006.09.02).]
2022-12-05T19:11:35.706103+00:00 INFO [LIITOS]: latex-to-pdf(2/3): *geometry* driver: auto-detecting
2022-12-05T19:11:35.706129+00:00 INFO [LIITOS]: latex-to-pdf(2/3): *geometry* detected driver: luatex
2022-12-05T19:11:35.730718+00:00 INFO [LIITOS]: latex-to-pdf(2/3): (./bookmatter.tex)
2022-12-05T19:11:35.778521+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [1{/usr/local/texlive/2022/texmf-var/fonts/map/pdftex/updmap/pdftex.map}</opt/l
2022-12-05T19:11:35.793041+00:00 INFO [LIITOS]: latex-to-pdf(2/3): ogo/liitos-logo.png>] (./publisher.tex
2022-12-05T19:11:35.793111+00:00 INFO [LIITOS]: latex-to-pdf(2/3): Overfull \hbox (0.5696pt too wide) in alignment at lines 8--22
2022-12-05T19:11:35.801452+00:00 INFO [LIITOS]: latex-to-pdf(2/3): warning  (pdf backend): ignoring duplicate destination with the name 'page.1'
2022-12-05T19:11:35.835458+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [1] (./this.toc)
2022-12-05T19:11:35.865135+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [2] (./document.tex
2022-12-05T19:11:35.892910+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [3<./images/blue.png>]
2022-12-05T19:11:35.901635+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [4]
2022-12-05T19:11:35.914837+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [5<./images/yellow.png><./images/red.png>])
2022-12-05T19:11:35.926101+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [6<./images/lime.png><./diagrams/squares-and-edges.png>] (./this.aux
2022-12-05T19:11:35.928940+00:00 INFO [LIITOS]: latex-to-pdf(2/3): (./bookmatter.aux) (./publisher.aux) (./document.aux))
2022-12-05T19:11:35.928963+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX Warning: There were multiply-defined labels.
2022-12-05T19:11:35.929147+00:00 INFO [LIITOS]: latex-to-pdf(2/3):  741 words of node memory still in use:
2022-12-05T19:11:35.929178+00:00 INFO [LIITOS]: latex-to-pdf(2/3):    7 hlist, 2 vlist, 2 rule, 1 local_par, 4 glue, 4 kern, 1 penalty, 3 glyph, 1
2022-12-05T19:11:35.929197+00:00 INFO [LIITOS]: latex-to-pdf(2/3): 5 attribute, 87 glue_spec, 10 attribute_list, 3 write, 1 user_defined nodes
2022-12-05T19:11:35.929213+00:00 INFO [LIITOS]: latex-to-pdf(2/3):    avail lists: 1:3,2:1944,3:357,4:128,5:147,6:170,7:2210,8:38,9:1367,10:3,11:7
2022-12-05T19:11:35.929227+00:00 INFO [LIITOS]: latex-to-pdf(2/3): 1,12:1
2022-12-05T19:11:35.956009+00:00 INFO [LIITOS]: latex-to-pdf(2/3): </usr/local/texlive/2022/texmf-dist/fonts/opentype/public/lm/lmsans12-regular.o
2022-12-05T19:11:35.964510+00:00 INFO [LIITOS]: latex-to-pdf(2/3): tf></usr/local/texlive/2022/texmf-dist/fonts/opentype/public/lm/lmsans10-bold.o
2022-12-05T19:11:35.986800+00:00 INFO [LIITOS]: latex-to-pdf(2/3): tf></opt/fonts/ITCFranklinGothicStd-Demi.otf></opt/fonts/ITCFranklinGothicStd-B
2022-12-05T19:11:35.992464+00:00 INFO [LIITOS]: latex-to-pdf(2/3): ook.otf>
2022-12-05T19:11:35.992487+00:00 INFO [LIITOS]: latex-to-pdf(2/3): Output written on this.pdf (7 pages, 29050 bytes).
2022-12-05T19:11:36.000815+00:00 INFO [LIITOS]: latex-to-pdf(2/3): Transcript written on this.log.
2022-12-05T19:11:36.046848+00:00 INFO [LIITOS]: latex-to-pdf process 2/3  (['lualatex', '--shell-escape', 'this.tex']) returned 0
2022-12-05T19:11:36.046908+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:36.046924+00:00 INFO [LIITOS]: 3/3) lualatex --shell-escape this.tex ...
2022-12-05T19:11:36.250333+00:00 INFO [LIITOS]: latex-to-pdf(3/3): This is LuaHBTeX, Version 1.15.0 (TeX Live 2022)
2022-12-05T19:11:36.250578+00:00 INFO [LIITOS]: latex-to-pdf(3/3):  system commands enabled.
2022-12-05T19:11:36.266363+00:00 INFO [LIITOS]: latex-to-pdf(3/3): (./this.tex
2022-12-05T19:11:36.266397+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX2e <2022-11-01>
2022-12-05T19:11:36.386259+00:00 INFO [LIITOS]: latex-to-pdf(3/3):  L3 programming layer <2022-11-02> (./setup.tex
2022-12-05T19:11:36.386520+00:00 INFO [LIITOS]: latex-to-pdf(3/3): Document Class: scrartcl 2022/10/12 v3.38 KOMA-Script document class (article)
2022-12-05T19:11:36.813726+00:00 INFO [LIITOS]: latex-to-pdf(3/3): For additional information on amsmath, use the `?' option.
2022-12-05T19:11:37.336882+00:00 INFO [LIITOS]: latex-to-pdf(3/3): === Package selnolig, Version 0.302, Date 2015/10/26 ===
2022-12-05T19:11:37.353707+00:00 INFO [LIITOS]: latex-to-pdf(3/3): ex.sty)) (./metadata.tex)
2022-12-05T19:11:37.624456+00:00 INFO [LIITOS]: latex-to-pdf(3/3): (./this.aux (./bookmatter.aux) (./publisher.aux) (./document.aux
2022-12-05T19:11:37.624531+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX Warning: Label `fig:blue' multiply defined.
2022-12-05T19:11:37.624553+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX Warning: Label `fig:blue' multiply defined.
2022-12-05T19:11:37.624568+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX Warning: Label `fig:red' multiply defined.
2022-12-05T19:11:37.991952+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [Loading MPS to PDF converter (version 2006.09.02).]
2022-12-05T19:11:37.999749+00:00 INFO [LIITOS]: latex-to-pdf(3/3): *geometry* driver: auto-detecting
2022-12-05T19:11:37.999812+00:00 INFO [LIITOS]: latex-to-pdf(3/3): *geometry* detected driver: luatex
2022-12-05T19:11:38.024947+00:00 INFO [LIITOS]: latex-to-pdf(3/3): (./bookmatter.tex)
2022-12-05T19:11:38.072831+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [1{/usr/local/texlive/2022/texmf-var/fonts/map/pdftex/updmap/pdftex.map}</opt/l
2022-12-05T19:11:38.087368+00:00 INFO [LIITOS]: latex-to-pdf(3/3): ogo/liitos-logo.png>] (./publisher.tex
2022-12-05T19:11:38.087432+00:00 INFO [LIITOS]: latex-to-pdf(3/3): Overfull \hbox (0.5696pt too wide) in alignment at lines 8--22
2022-12-05T19:11:38.096003+00:00 INFO [LIITOS]: latex-to-pdf(3/3): warning  (pdf backend): ignoring duplicate destination with the name 'page.1'
2022-12-05T19:11:38.130047+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [1] (./this.toc)
2022-12-05T19:11:38.159512+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [2] (./document.tex
2022-12-05T19:11:38.187039+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [3<./images/blue.png>]
2022-12-05T19:11:38.195870+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [4]
2022-12-05T19:11:38.209254+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [5<./images/yellow.png><./images/red.png>])
2022-12-05T19:11:38.220477+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [6<./images/lime.png><./diagrams/squares-and-edges.png>] (./this.aux
2022-12-05T19:11:38.223520+00:00 INFO [LIITOS]: latex-to-pdf(3/3): (./bookmatter.aux) (./publisher.aux) (./document.aux))
2022-12-05T19:11:38.223550+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX Warning: There were multiply-defined labels.
2022-12-05T19:11:38.223709+00:00 INFO [LIITOS]: latex-to-pdf(3/3):  741 words of node memory still in use:
2022-12-05T19:11:38.223730+00:00 INFO [LIITOS]: latex-to-pdf(3/3):    7 hlist, 2 vlist, 2 rule, 1 local_par, 4 glue, 4 kern, 1 penalty, 3 glyph, 1
2022-12-05T19:11:38.223744+00:00 INFO [LIITOS]: latex-to-pdf(3/3): 5 attribute, 87 glue_spec, 10 attribute_list, 3 write, 1 user_defined nodes
2022-12-05T19:11:38.223758+00:00 INFO [LIITOS]: latex-to-pdf(3/3):    avail lists: 1:3,2:1944,3:357,4:128,5:147,6:170,7:2210,8:38,9:1367,10:3,11:7
2022-12-05T19:11:38.223771+00:00 INFO [LIITOS]: latex-to-pdf(3/3): 1,12:1
2022-12-05T19:11:38.250412+00:00 INFO [LIITOS]: latex-to-pdf(3/3): </usr/local/texlive/2022/texmf-dist/fonts/opentype/public/lm/lmsans12-regular.o
2022-12-05T19:11:38.258877+00:00 INFO [LIITOS]: latex-to-pdf(3/3): tf></usr/local/texlive/2022/texmf-dist/fonts/opentype/public/lm/lmsans10-bold.o
2022-12-05T19:11:38.281165+00:00 INFO [LIITOS]: latex-to-pdf(3/3): tf></opt/fonts/ITCFranklinGothicStd-Demi.otf></opt/fonts/ITCFranklinGothicStd-B
2022-12-05T19:11:38.286899+00:00 INFO [LIITOS]: latex-to-pdf(3/3): ook.otf>
2022-12-05T19:11:38.286930+00:00 INFO [LIITOS]: latex-to-pdf(3/3): Output written on this.pdf (7 pages, 29050 bytes).
2022-12-05T19:11:38.295566+00:00 INFO [LIITOS]: latex-to-pdf(3/3): Transcript written on this.log.
2022-12-05T19:11:38.342299+00:00 INFO [LIITOS]: latex-to-pdf process 3/3  (['lualatex', '--shell-escape', 'this.tex']) returned 0
2022-12-05T19:11:38.342359+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:38.342378+00:00 INFO [LIITOS]: Moving stuff around (result phase) ...
2022-12-05T19:11:38.351930+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:38.351976+00:00 INFO [LIITOS]: Deliverable taxonomy: ...
2022-12-05T19:11:38.362210+00:00 INFO [LIITOS]: - Ephemeral:
2022-12-05T19:11:38.362291+00:00 INFO [LIITOS]:   + name: index.pdf
2022-12-05T19:11:38.362313+00:00 INFO [LIITOS]:   + size: 29050 bytes
2022-12-05T19:11:38.362329+00:00 INFO [LIITOS]:   + date: 2022-12-05 19:11:38.351920 +00:00
2022-12-05T19:11:38.362344+00:00 INFO [LIITOS]: - Characteristic:
2022-12-05T19:11:38.362359+00:00 INFO [LIITOS]:   + Checksums:
2022-12-05T19:11:38.362372+00:00 INFO [LIITOS]:     sha512:4286b06154a6f8986ca9c0eadab11a44a72059dc41b3cb159592e8f6641ed0254577586740605bcf750cd376dbf7a6a7b43215fe35707bff473a31da25abed4b
2022-12-05T19:11:38.362388+00:00 INFO [LIITOS]:     sha256:1eb1d57f6a2b3c4e885b558695a2a7a2f2c3ec9e72a5921a1fe96c97f12dc245
2022-12-05T19:11:38.362402+00:00 INFO [LIITOS]:       sha1:29321246b7377b12bd60f9a908108a549368fabe
2022-12-05T19:11:38.362415+00:00 INFO [LIITOS]:        md5:1d6c6998f50644999182ca3ff2b7867d
2022-12-05T19:11:38.362427+00:00 INFO [LIITOS]:   + Fonts:
2022-12-05T19:11:38.437865+00:00 INFO [LIITOS]:     pdffonts: name                                 type              encoding         emb sub uni object ID
2022-12-05T19:11:38.438110+00:00 INFO [LIITOS]:     pdffonts: ------------------------------------ ----------------- ---------------- --- --- --- ---------
2022-12-05T19:11:38.438131+00:00 INFO [LIITOS]:     pdffonts: XPOFQN+ITCFranklinGothicStd-Book     CID Type 0C       Identity-H       yes yes yes      8  0
2022-12-05T19:11:38.438148+00:00 INFO [LIITOS]:     pdffonts: IKTCZX+ITCFranklinGothicStd-Demi     CID Type 0C       Identity-H       yes yes yes      9  0
2022-12-05T19:11:38.438165+00:00 INFO [LIITOS]:     pdffonts: FSKYUR+LMSans10-Bold                 CID Type 0C       Identity-H       yes yes yes     11  0
2022-12-05T19:11:38.438181+00:00 INFO [LIITOS]:     pdffonts: HPBJUX+LMSans12-Regular              CID Type 0C       Identity-H       yes yes yes     12  0
2022-12-05T19:11:38.438219+00:00 INFO [LIITOS]: pdffonts process (['pdffonts', '../index.pdf']) returned 0
2022-12-05T19:11:38.438238+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-05T19:11:38.438256+00:00 INFO [LIITOS]: done.
2022-12-05T19:11:38.438270+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

## Use Cases and Author Info

The purpose of the package / tool is to encourage convention based authoring in markdown without sacrificing tight control on the rendered results.

### Rendering

The [example/deep/](https://git.sr.ht/~sthagen/liitos/tree/default/item/example/deep) folder in the source repository 
shows how documents can be distributed across subfolders and how the linkage per the data files (in this case) works:

- structure.yml
- approvals.yml
- bind.txt
- changes.yml
- meta-base.yml
- meta-deep.yml

How to eject templates for the various data files is demonstrated above.

#### Structure

The `structure.yml` file is the single entry point for discovery and rendering per this tool for publication pipelines:

```yaml
prod_kind:
- deep:
    approvals: approvals.yml
    bind: bind.txt
    changes: changes.yml
    meta: meta-deep.yml
    render: true
```

The entries are paths to files from the folder of the structure data file itself.
To link the artificial terms in the example to our names:

> A document type `PQR` for a product named `ABC` created for a specific audience `XYZ` would have `abc_pqr`instead of `prod_kind` and `xyz` instead of `deep`
> (the names of the files being values to the keys `approvals`, `bind`, `changes`, and `meta` also differ of course as the authors choose these).

#### Approvals

The approvals file (can be of course different per facet i.e. in real world cases often "per audience") which in the example `deep` is:

```console
❯ cat deep/approvals.yml
approvals:
- name: An Author
  role: Author
- name: A Reviewer
  role: Review
- name: An App Rover
  role: Approved

```

The entries should be speaking for themselves.
Note the spelling (also case) of all keys is fixed and will lead to failures during rendering if not correct.
Also note, that the table these approvals (signature loop) entries end up in has column labels that are determined elsewhere
(namely in the metadata files or if not given there in this application (`liitos`).


#### Binder

The binder (bind file) is the top level list of files that bound in sequence (and followed all includes up to some level)
will result in the intended document target (product of kind) of that facet.
In the example the target is `prod_kind` and the facet is `deep`.

bind.txt:
```
1.md
2.md
other/b.md
```

The render command of `liitos` first discovers and collates all sub-documents in the order determined by the sequence given in the binder:

This initial phase results are placed in the folder of the rendering which is by default always in the path `render/pdf/` below every document folder in the checkout of a documentation repository.
In the case of `orga/repo/doctype/` this would be the path `orga/repo/doctype/render/pdf/` and for `orga/repo/doctype/part/` this would be `orga/repo/doctype/part/render/pdf/`.

The example log for the following call can be found further up the page:

```console
❯ liitos render deep --target prod_kind --facet deep
```

#### Changes

The changes files may of course also differ per facet (in our case often the audience) and in the example `deep` are as follows:

```console
❯ cat deep/changes.yml
changes:
- author: An Author
  date: PUBLICATIONDATE
  issue: '01'
  summary: Initial Issue
```

Again the keys in spelling and case are significant.
Also, the table column labels themselves are per meta data file or application default of `liitos`.

In YAML the dash (-) indicates a list item so this example file has only one change log entry.
Also, please quote strings with special YAML characters (otherwise the parse will fail)
and also quote strings (the issue number is best seen as an opaque string) with only digits.
Even more so, when they start with zero (0) as to preserve the leading zero.

The magical term `PUBLICATIONDATE` results in a valid form of the date of the rendering and can occur

- in the changes data file as well as
- in the meta data files (there as value to the key `header_date`)

#### Metadata

All customizing of the rendering is offered to the authors per the meta data file(s).
To reduce duplication and thereby the risk of inconsistencies the tool allows to import meta data files within meta data files
(one level only) and override or amend the imported data for an effective metadata set.

The example `deep` demonstrates this by only including `meta-deep.yml` (indicating it has specifics for the facet `deep`):

```console
❯ cat deep/meta-deep.yml
---
document:
  import: meta-base.yml
  patch:
    header_id: P99999
    header_date: PUBLICATIONDATE
```

Again the spelling and case of the keys are significant.

The top-level (object) key `document` is fixed (as it relates to the document).
There are currently the following two supported keys within the document object (dict) of meta data files that import
(specialize) base metadata files:

import
:    a valid path from the main document folder to another meta data file
(please keep the special files for now in the same folder)

patch
:    ley value pairs to add (or override) in the imported meta data from the path of the `import` key value

We see that in above example we add/overwrite

1. the document id (key `header_id` as it appears only in the header of the rendered document)
1. the publication date per `header_date` to the magical term `PUBLICATIONDATE` resulting during rendering
   in the date of rendering displayed as `DD MON YYYY` eg. on 2022-12-04 this would be `04 DEC 2022`


The base meta data files (imported by other meta data files or standing for themselves is only one meta data file is needed)
in the example `deep` provide all known keys to demonstrate the features:

```console
❯ cat deep/meta-base.yml
---
document:
  common:
    title: Ttt Tt Tt
    header_title: Ttt Tt
    sub_title: The Deep Spec
    header_type: Engineering Document
    header_id: null
    issue: '01'
    revision: '00'
    header_date: 01 DEC 2022
    header_issue_revision_combined: null
    footer_frame_note: VERY CONSEQUENTIAL
    footer_page_number_prefix: Page
    change_log_issue_label: Iss.
    change_log_revision_label: Rev.
    change_log_date_label: Date
    change_log_author_label: Author
    change_log_description_label: Description
    approvals_role_label: Approvals
    approvals_name_label: Name
    approvals_date_and_signature_label: Date and Signature
    proprietary_information: /opt/legal/proprietary_information.txt
    toc_level: 2
    list_of_figures: '%'  # empty string to enable lof
    list_of_tables: '%'  # empty string to enable lot
    font_path: /opt/fonts/
    font_suffix: .otf
    bold_font: ITCFranklinGothicStd-Demi
    italic_font: ITCFranklinGothicStd-BookIt
    bold_italic_font: ITCFranklinGothicStd-DemiIt
    main_font: ITCFranklinGothicStd-Book
    fixed_font_package: sourcecodepro
    code_fontsize: \scriptsize
    chosen_logo: /opt/logo/liitos-logo.png
```

The special value `null` indicates that either a default shall be taken or that the value on the level of the meta data file makes no sense.
Example for the latter is `header_id` in the above base file as it will be overridden by specific document meta files like `meta-deep.yml`.

All keys below the magic `common` key should be self-explanatory.

A minimal base meta data file could be (untested):

```console
❯ cat fictitious/meta-minimal.yml
---
document:
  common:
    title: Ttt Tt Tt
    footer_frame_note: DISTRIBUTION SCOPE
    proprietary_information: /opt/legal/proprietary_information.txt
```

The terseness profits from the defaults chosen in `liitos` that expect many artifacts like fonts or logo at paths available on many systems.

Leaving out `proprietary_information` would produce warnings (like other left out settings)
and also inject the text `Proprietary Information MISSING` on the second page of the rendered document.

### Including Markdown Files

First things first:

> Please be prepared to save the planet yourself and avoid cyclic includes (a including b which in turn includes a which ...)
> as we may make the discovery failsafe only later. Thanks.

There is an example file in the `deep` folder that demonstrates the two ways to include markdown files inside other markdown files
(the binder as top level inclusion is the main way of linking content).

```console
❯ cat deep/part/a.md | filter-includes --magic

Part A with again includes.

\```{.python .cb.run}
with open('a1.md') as fp:
    print(fp.read())
\```

 - - 8< - - 

\include{sub/as.md}

```

### Applying User Patches

As a last resort it may be necessary to rewrite parts of the final latex file before transforming to pdf.
One way (besides editing and calling lualatex yourself) is to provide pairs of search and replace strings
in the `patch.yml` file inside the document root as list of two-element lists.

The example in the provided folder inside the source repository:

```console
❯ cat example/deep/patch.yml
---
- - ',height=\textheight]'
  - ']'
```

Demonstrates how to ensure that no naive scaling distorting the aspect of images occurs (setting the width but
not the height in the markdown source can result in pandoc generating a rectangular scaling that over scales the height
in case of portrait mode layouts).
