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
❯ Splice (Finnish liitos) contributions. version 2022.12.4+parent.84710d29
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
2022-12-04T21:15:36.878503+00:00 INFO [LIITOS]: processing complete - SUCCESS
2022-12-04T21:15:36.878516+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:36.878564+00:00 INFO [LIITOS]: before met.weave(): /some/where/example/deep/render/pdf set doc (../../)
2022-12-04T21:15:36.878580+00:00 INFO [LIITOS]: parsed target (prod_kind) and facet (deep) from request
2022-12-04T21:15:36.878617+00:00 INFO [LIITOS]: executing prelude of command (meta) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/some/where/example/deep/render/pdf)
2022-12-04T21:15:36.879153+00:00 INFO [LIITOS]: prelude teleported processor into the document root at (/some/where/example/deep/)
2022-12-04T21:15:36.879201+00:00 INFO [LIITOS]: meta (this processor) teleported into the render/pdf location (/some/where/example/deep/render/pdf/)
2022-12-04T21:15:36.879696+00:00 INFO [LIITOS]: found single target (prod_kind) with facets (['deep'])
2022-12-04T21:15:36.879719+00:00 WARNING [LIITOS]: structure does not strictly provide the expected aspects ['approvals', 'bind', 'changes', 'meta'] for target (prod_kind) and facet (deep)
2022-12-04T21:15:36.879735+00:00 WARNING [LIITOS]: - found the following aspects instead:                   ['approvals', 'bind', 'changes', 'meta', 'render'] instead
2022-12-04T21:15:36.883839+00:00 INFO [LIITOS]: weaving in the meta data per metadata.tex.in into metadata.tex ...
2022-12-04T21:15:36.883916+00:00 INFO [LIITOS]: header_issue_revision_combined value missing ... setting default (Iss \theMetaIssCode, Rev \theMetaRevCode)
2022-12-04T21:15:36.884430+00:00 INFO [LIITOS]: weaving in the meta data per driver.tex.in into driver.tex ...
2022-12-04T21:15:36.884913+00:00 INFO [LIITOS]: weaving in the meta data per setup.tex.in into setup.tex ...
2022-12-04T21:15:36.886306+00:00 INFO [LIITOS]: before sig.weave(): /some/where/example/deep/render/pdf set doc (../../)
2022-12-04T21:15:36.886359+00:00 INFO [LIITOS]: relocated for sig.weave(): /some/where/example/deep/render/pdf with doc (../../)
2022-12-04T21:15:36.886380+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:36.886428+00:00 INFO [LIITOS]: executing prelude of command (approvals) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/some/where/example/deep/render/pdf)
2022-12-04T21:15:36.886937+00:00 INFO [LIITOS]: detected approvals channel (yaml) weaving in from (approvals.yml)
2022-12-04T21:15:36.886957+00:00 INFO [LIITOS]: loading signatures from signatures_path='approvals.yml'
2022-12-04T21:15:36.887457+00:00 INFO [LIITOS]: signatures=({'approvals': [{'name': 'An Author', 'role': 'Author'}, {'name': 'A Reviewer', 'role': 'Review'}, {'name': 'An App Rover', 'role': 'Approved'}]}, '')
2022-12-04T21:15:36.887475+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:36.887488+00:00 INFO [LIITOS]: plausibility tests for approvals ...
2022-12-04T21:15:36.887512+00:00 INFO [LIITOS]: calculated extra pushdown to be 18em
2022-12-04T21:15:36.887740+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:36.887764+00:00 INFO [LIITOS]: weaving in the approvals from approvals.yml...
2022-12-04T21:15:36.888306+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:36.888344+00:00 INFO [LIITOS]: before chg.weave(): /some/where/example/deep set doc (../../)
2022-12-04T21:15:36.888376+00:00 INFO [LIITOS]: relocated for chg.weave(): /some/where/example/deep/render/pdf with doc (../../)
2022-12-04T21:15:36.888391+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:36.888428+00:00 INFO [LIITOS]: executing prelude of command (changes) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/some/where/example/deep/render/pdf)
2022-12-04T21:15:36.888897+00:00 INFO [LIITOS]: detected changes channel (yaml) weaving in from (changes.yml)
2022-12-04T21:15:36.888915+00:00 INFO [LIITOS]: loading changes from changes_path='changes.yml'
2022-12-04T21:15:36.889271+00:00 INFO [LIITOS]: changes=({'changes': [{'author': 'An Author', 'date': 'PUBLICATIONDATE', 'issue': '01', 'summary': 'Initial Issue'}]}, '')
2022-12-04T21:15:36.889288+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:36.889301+00:00 INFO [LIITOS]: plausibility tests for changes ...
2022-12-04T21:15:36.889417+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:36.889432+00:00 INFO [LIITOS]: weaving in the changes ...
2022-12-04T21:15:36.889669+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:36.889702+00:00 INFO [LIITOS]: before chg.weave(): /some/where/example/deep set doc (../../)
2022-12-04T21:15:36.889733+00:00 INFO [LIITOS]: relocated for chg.weave(): /some/where/example/deep/render/pdf with doc (../../)
2022-12-04T21:15:36.889749+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:36.889762+00:00 INFO [LIITOS]: parsed target (prod_kind) and facet (deep) from request
2022-12-04T21:15:36.889796+00:00 INFO [LIITOS]: executing prelude of command (render) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/some/where/example/deep/render/pdf)
2022-12-04T21:15:36.890261+00:00 INFO [LIITOS]: prelude teleported processor into the document root at (/some/where/example/deep/)
2022-12-04T21:15:36.890316+00:00 INFO [LIITOS]: render (this processor) teleported into the render/pdf location (/some/where/example/deep/render/pdf/)
2022-12-04T21:15:36.890762+00:00 INFO [LIITOS]: found single target (prod_kind) with facets (['deep'])
2022-12-04T21:15:36.890783+00:00 INFO [LIITOS]: found render instruction with value (True)
2022-12-04T21:15:36.890797+00:00 INFO [LIITOS]: we will render ...
2022-12-04T21:15:36.890809+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:36.890822+00:00 INFO [LIITOS]: transforming SVG assets to high resolution PNG bitmaps ...
2022-12-04T21:15:37.649044+00:00 INFO [LIITOS]: svg-to-png: /some/where/example/deep/render/pdf/diagrams/squares-and-edges.svg /some/where/example/deep/render/pdf/diagrams/squares-and-edges.png png 100% 1x 0:0:220:100 220:100
2022-12-04T21:15:37.673577+00:00 INFO [LIITOS]: svg-to-png process (['svgexport', PosixPath('diagrams/squares-and-edges.svg'), 'diagrams/squares-and-edges.png', '100%']) returned 0
2022-12-04T21:15:37.673673+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:37.673703+00:00 INFO [LIITOS]: rewriting src attribute values of SVG to PNG sources ...
2022-12-04T21:15:37.674505+00:00 INFO [LIITOS]: transform[#97]: ![Caption Text for SVG](diagrams/squares-and-edges.svg "Alt Text for SVG")
2022-12-04T21:15:37.674564+00:00 INFO [LIITOS]:      into[#97]: ![Caption Text for SVG](diagrams/squares-and-edges.png "Alt Text for SVG")
2022-12-04T21:15:37.674850+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:37.674882+00:00 INFO [LIITOS]: pandoc -f markdown+link_attributes -t latex document.md -o document.tex --filter mermaid-filter ...
2022-12-04T21:15:37.715436+00:00 INFO [LIITOS]: markdown-to-latex: [INFO] Running filter mermaid-filter
2022-12-04T21:15:37.770329+00:00 INFO [LIITOS]: markdown-to-latex: [INFO] Completed filter mermaid-filter in 1 ms
2022-12-04T21:15:37.777913+00:00 INFO [LIITOS]: markdown-to-latex process (['pandoc', '--verbose', '-f', 'markdown+link_attributes', '-t', 'latex', 'document.md', '-o', 'document.tex', '--filter', 'mermaid-filter']) returned 0
2022-12-04T21:15:37.777962+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:37.777982+00:00 INFO [LIITOS]: move any captions below tables ...
2022-12-04T21:15:37.779973+00:00 INFO [LIITOS]: start of a table environment at line #62
2022-12-04T21:15:37.780005+00:00 INFO [LIITOS]: - found the caption start at line #63
2022-12-04T21:15:37.780023+00:00 INFO [LIITOS]: - multi line caption at line #63
2022-12-04T21:15:37.780041+00:00 INFO [LIITOS]: - caption read at line #64
2022-12-04T21:15:37.780065+00:00 INFO [LIITOS]: end of table env detected at line #79
2022-12-04T21:15:37.780196+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:37.780215+00:00 INFO [LIITOS]: inject stem (derived from file name) labels ...
2022-12-04T21:15:37.781894+00:00 INFO [LIITOS]: start of a figure environment at line #41
2022-12-04T21:15:37.781916+00:00 INFO [LIITOS]: within a figure environment at line #43
2022-12-04T21:15:37.781931+00:00 INFO [LIITOS]: \includegraphics{images/blue.png}
2022-12-04T21:15:37.781948+00:00 INFO [LIITOS]: \label{fig:blue}
2022-12-04T21:15:37.781965+00:00 INFO [LIITOS]: - found the caption start at line #44
2022-12-04T21:15:37.781980+00:00 INFO [LIITOS]: end of figure env detected at line #45
2022-12-04T21:15:37.781999+00:00 INFO [LIITOS]: start of a figure environment at line #49
2022-12-04T21:15:37.782015+00:00 INFO [LIITOS]: within a figure environment at line #51
2022-12-04T21:15:37.782029+00:00 INFO [LIITOS]: \includegraphics{images/blue.png}
2022-12-04T21:15:37.782044+00:00 INFO [LIITOS]: \label{fig:blue}
2022-12-04T21:15:37.782058+00:00 INFO [LIITOS]: - found the caption start at line #52
2022-12-04T21:15:37.782073+00:00 INFO [LIITOS]: end of figure env detected at line #53
2022-12-04T21:15:37.782089+00:00 WARNING [LIITOS]: graphics include outside of a figure environment at line #55
2022-12-04T21:15:37.782116+00:00 ERROR [LIITOS]: line#55|\includegraphics{images/blue.png}
2022-12-04T21:15:37.782132+00:00 INFO [LIITOS]: trying to fix temporarily ... watch for marker MISSING-CAPTION-IN-MARKDOWN
2022-12-04T21:15:37.782147+00:00 INFO [LIITOS]: \label{fig:blue}
2022-12-04T21:15:37.782181+00:00 INFO [LIITOS]: start of a figure environment at line #108
2022-12-04T21:15:37.782196+00:00 INFO [LIITOS]: within a figure environment at line #110
2022-12-04T21:15:37.782210+00:00 INFO [LIITOS]: \includegraphics{images/yellow.png}
2022-12-04T21:15:37.782224+00:00 INFO [LIITOS]: \label{fig:yellow}
2022-12-04T21:15:37.782238+00:00 INFO [LIITOS]: - found the caption start at line #111
2022-12-04T21:15:37.782253+00:00 INFO [LIITOS]: end of figure env detected at line #112
2022-12-04T21:15:37.782269+00:00 INFO [LIITOS]: start of a figure environment at line #119
2022-12-04T21:15:37.782284+00:00 INFO [LIITOS]: within a figure environment at line #121
2022-12-04T21:15:37.782297+00:00 INFO [LIITOS]: \includegraphics{images/red.png}
2022-12-04T21:15:37.782311+00:00 INFO [LIITOS]: \label{fig:red}
2022-12-04T21:15:37.782326+00:00 INFO [LIITOS]: - found the caption start at line #122
2022-12-04T21:15:37.782342+00:00 INFO [LIITOS]: end of figure env detected at line #123
2022-12-04T21:15:37.782360+00:00 INFO [LIITOS]: start of a figure environment at line #135
2022-12-04T21:15:37.782375+00:00 INFO [LIITOS]: within a figure environment at line #137
2022-12-04T21:15:37.782389+00:00 INFO [LIITOS]: \includegraphics{images/red.png}
2022-12-04T21:15:37.782403+00:00 INFO [LIITOS]: \label{fig:red}
2022-12-04T21:15:37.782416+00:00 INFO [LIITOS]: - found the caption start at line #138
2022-12-04T21:15:37.782431+00:00 INFO [LIITOS]: end of figure env detected at line #139
2022-12-04T21:15:37.782445+00:00 INFO [LIITOS]: start of a figure environment at line #141
2022-12-04T21:15:37.782460+00:00 INFO [LIITOS]: within a figure environment at line #143
2022-12-04T21:15:37.782473+00:00 INFO [LIITOS]: \includegraphics{images/lime.png}
2022-12-04T21:15:37.782486+00:00 INFO [LIITOS]: \label{fig:lime}
2022-12-04T21:15:37.782499+00:00 INFO [LIITOS]: - found the caption start at line #144
2022-12-04T21:15:37.782514+00:00 INFO [LIITOS]: end of figure env detected at line #145
2022-12-04T21:15:37.782530+00:00 INFO [LIITOS]: start of a figure environment at line #149
2022-12-04T21:15:37.782545+00:00 INFO [LIITOS]: within a figure environment at line #151
2022-12-04T21:15:37.782558+00:00 INFO [LIITOS]: \includegraphics{diagrams/squares-and-edges.png}
2022-12-04T21:15:37.782572+00:00 INFO [LIITOS]: \label{fig:squares-and-edges}
2022-12-04T21:15:37.782586+00:00 INFO [LIITOS]: - found the caption start at line #152
2022-12-04T21:15:37.782600+00:00 INFO [LIITOS]: end of figure env detected at line #153
2022-12-04T21:15:37.782700+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:37.782718+00:00 INFO [LIITOS]: scale figures ...
2022-12-04T21:15:37.784731+00:00 INFO [LIITOS]: trigger a scale mod for the next figure environment at line #47|\scale=0.9
2022-12-04T21:15:37.784761+00:00 INFO [LIITOS]: - found the scale target start at line #51|\includegraphics{images/blue.png}
2022-12-04T21:15:37.784890+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:37.784907+00:00 INFO [LIITOS]: cp -a driver.tex this.tex ...
2022-12-04T21:15:37.785317+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:37.785335+00:00 INFO [LIITOS]: 1/3) lualatex --shell-escape this.tex ...
2022-12-04T21:15:37.988950+00:00 INFO [LIITOS]: latex-to-pdf(1/3): This is LuaHBTeX, Version 1.15.0 (TeX Live 2022)
2022-12-04T21:15:37.989133+00:00 INFO [LIITOS]: latex-to-pdf(1/3):  system commands enabled.
2022-12-04T21:15:38.005180+00:00 INFO [LIITOS]: latex-to-pdf(1/3): (./this.tex
2022-12-04T21:15:38.005243+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX2e <2022-11-01>
2022-12-04T21:15:38.130198+00:00 INFO [LIITOS]: latex-to-pdf(1/3):  L3 programming layer <2022-11-02> (./setup.tex
2022-12-04T21:15:38.130467+00:00 INFO [LIITOS]: latex-to-pdf(1/3): Document Class: scrartcl 2022/10/12 v3.38 KOMA-Script document class (article)
2022-12-04T21:15:38.530488+00:00 INFO [LIITOS]: latex-to-pdf(1/3): For additional information on amsmath, use the `?' option.
2022-12-04T21:15:39.050107+00:00 INFO [LIITOS]: latex-to-pdf(1/3): === Package selnolig, Version 0.302, Date 2015/10/26 ===
2022-12-04T21:15:39.067773+00:00 INFO [LIITOS]: latex-to-pdf(1/3): ex.sty)) (./metadata.tex)
2022-12-04T21:15:39.333981+00:00 INFO [LIITOS]: latex-to-pdf(1/3): (./this.aux (./bookmatter.aux) (./publisher.aux) (./document.aux
2022-12-04T21:15:39.334043+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX Warning: Label `fig:blue' multiply defined.
2022-12-04T21:15:39.334063+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX Warning: Label `fig:blue' multiply defined.
2022-12-04T21:15:39.334085+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX Warning: Label `fig:red' multiply defined.
2022-12-04T21:15:39.702871+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [Loading MPS to PDF converter (version 2006.09.02).]
2022-12-04T21:15:39.711167+00:00 INFO [LIITOS]: latex-to-pdf(1/3): *geometry* driver: auto-detecting
2022-12-04T21:15:39.711208+00:00 INFO [LIITOS]: latex-to-pdf(1/3): *geometry* detected driver: luatex
2022-12-04T21:15:39.737296+00:00 INFO [LIITOS]: latex-to-pdf(1/3): (./bookmatter.tex)
2022-12-04T21:15:39.786278+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [1{/usr/local/texlive/2022/texmf-var/fonts/map/pdftex/updmap/pdftex.map}</opt/l
2022-12-04T21:15:39.800985+00:00 INFO [LIITOS]: latex-to-pdf(1/3): ogo/liitos-logo.png>] (./publisher.tex
2022-12-04T21:15:39.801047+00:00 INFO [LIITOS]: latex-to-pdf(1/3): Overfull \hbox (0.5696pt too wide) in alignment at lines 8--22
2022-12-04T21:15:39.809367+00:00 INFO [LIITOS]: latex-to-pdf(1/3): warning  (pdf backend): ignoring duplicate destination with the name 'page.1'
2022-12-04T21:15:39.843362+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [1] (./this.toc)
2022-12-04T21:15:39.873198+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [2] (./document.tex
2022-12-04T21:15:39.900408+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [3<./images/blue.png>]
2022-12-04T21:15:39.909276+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [4]
2022-12-04T21:15:39.922607+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [5<./images/yellow.png><./images/red.png>])
2022-12-04T21:15:39.933920+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [6<./images/lime.png><./diagrams/squares-and-edges.png>] (./this.aux
2022-12-04T21:15:39.936779+00:00 INFO [LIITOS]: latex-to-pdf(1/3): (./bookmatter.aux) (./publisher.aux) (./document.aux))
2022-12-04T21:15:39.936810+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX Warning: There were multiply-defined labels.
2022-12-04T21:15:39.936989+00:00 INFO [LIITOS]: latex-to-pdf(1/3):  741 words of node memory still in use:
2022-12-04T21:15:39.937008+00:00 INFO [LIITOS]: latex-to-pdf(1/3):    7 hlist, 2 vlist, 2 rule, 1 local_par, 4 glue, 4 kern, 1 penalty, 3 glyph, 1
2022-12-04T21:15:39.937023+00:00 INFO [LIITOS]: latex-to-pdf(1/3): 5 attribute, 87 glue_spec, 10 attribute_list, 3 write, 1 user_defined nodes
2022-12-04T21:15:39.937037+00:00 INFO [LIITOS]: latex-to-pdf(1/3):    avail lists: 1:3,2:1944,3:357,4:128,5:147,6:170,7:2210,8:38,9:1367,10:3,11:7
2022-12-04T21:15:39.937051+00:00 INFO [LIITOS]: latex-to-pdf(1/3): 1,12:1
2022-12-04T21:15:39.964625+00:00 INFO [LIITOS]: latex-to-pdf(1/3): </usr/local/texlive/2022/texmf-dist/fonts/opentype/public/lm/lmsans12-regular.o
2022-12-04T21:15:39.973447+00:00 INFO [LIITOS]: latex-to-pdf(1/3): tf></usr/local/texlive/2022/texmf-dist/fonts/opentype/public/lm/lmsans10-bold.o
2022-12-04T21:15:39.996821+00:00 INFO [LIITOS]: latex-to-pdf(1/3): tf></opt/fonts/ITCFranklinGothicStd-Demi.otf></opt/fonts/ITCFranklinGothicStd-B
2022-12-04T21:15:40.002503+00:00 INFO [LIITOS]: latex-to-pdf(1/3): ook.otf>
2022-12-04T21:15:40.002527+00:00 INFO [LIITOS]: latex-to-pdf(1/3): Output written on this.pdf (7 pages, 29050 bytes).
2022-12-04T21:15:40.012566+00:00 INFO [LIITOS]: latex-to-pdf(1/3): Transcript written on this.log.
2022-12-04T21:15:40.058232+00:00 INFO [LIITOS]: latex-to-pdf process 1/3  (['lualatex', '--shell-escape', 'this.tex']) returned 0
2022-12-04T21:15:40.058296+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:40.058318+00:00 INFO [LIITOS]: 2/3) lualatex --shell-escape this.tex ...
2022-12-04T21:15:40.258666+00:00 INFO [LIITOS]: latex-to-pdf(2/3): This is LuaHBTeX, Version 1.15.0 (TeX Live 2022)
2022-12-04T21:15:40.258930+00:00 INFO [LIITOS]: latex-to-pdf(2/3):  system commands enabled.
2022-12-04T21:15:40.274791+00:00 INFO [LIITOS]: latex-to-pdf(2/3): (./this.tex
2022-12-04T21:15:40.274834+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX2e <2022-11-01>
2022-12-04T21:15:40.392250+00:00 INFO [LIITOS]: latex-to-pdf(2/3):  L3 programming layer <2022-11-02> (./setup.tex
2022-12-04T21:15:40.392526+00:00 INFO [LIITOS]: latex-to-pdf(2/3): Document Class: scrartcl 2022/10/12 v3.38 KOMA-Script document class (article)
2022-12-04T21:15:40.793096+00:00 INFO [LIITOS]: latex-to-pdf(2/3): For additional information on amsmath, use the `?' option.
2022-12-04T21:15:41.290041+00:00 INFO [LIITOS]: latex-to-pdf(2/3): === Package selnolig, Version 0.302, Date 2015/10/26 ===
2022-12-04T21:15:41.306319+00:00 INFO [LIITOS]: latex-to-pdf(2/3): ex.sty)) (./metadata.tex)
2022-12-04T21:15:41.565959+00:00 INFO [LIITOS]: latex-to-pdf(2/3): (./this.aux (./bookmatter.aux) (./publisher.aux) (./document.aux
2022-12-04T21:15:41.566023+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX Warning: Label `fig:blue' multiply defined.
2022-12-04T21:15:41.566042+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX Warning: Label `fig:blue' multiply defined.
2022-12-04T21:15:41.566057+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX Warning: Label `fig:red' multiply defined.
2022-12-04T21:15:41.928001+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [Loading MPS to PDF converter (version 2006.09.02).]
2022-12-04T21:15:41.935226+00:00 INFO [LIITOS]: latex-to-pdf(2/3): *geometry* driver: auto-detecting
2022-12-04T21:15:41.935264+00:00 INFO [LIITOS]: latex-to-pdf(2/3): *geometry* detected driver: luatex
2022-12-04T21:15:41.959753+00:00 INFO [LIITOS]: latex-to-pdf(2/3): (./bookmatter.tex)
2022-12-04T21:15:42.007201+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [1{/usr/local/texlive/2022/texmf-var/fonts/map/pdftex/updmap/pdftex.map}</opt/l
2022-12-04T21:15:42.021575+00:00 INFO [LIITOS]: latex-to-pdf(2/3): ogo/liitos-logo.png>] (./publisher.tex
2022-12-04T21:15:42.021634+00:00 INFO [LIITOS]: latex-to-pdf(2/3): Overfull \hbox (0.5696pt too wide) in alignment at lines 8--22
2022-12-04T21:15:42.029932+00:00 INFO [LIITOS]: latex-to-pdf(2/3): warning  (pdf backend): ignoring duplicate destination with the name 'page.1'
2022-12-04T21:15:42.063455+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [1] (./this.toc)
2022-12-04T21:15:42.092327+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [2] (./document.tex
2022-12-04T21:15:42.119971+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [3<./images/blue.png>]
2022-12-04T21:15:42.128606+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [4]
2022-12-04T21:15:42.141986+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [5<./images/yellow.png><./images/red.png>])
2022-12-04T21:15:42.153246+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [6<./images/lime.png><./diagrams/squares-and-edges.png>] (./this.aux
2022-12-04T21:15:42.156130+00:00 INFO [LIITOS]: latex-to-pdf(2/3): (./bookmatter.aux) (./publisher.aux) (./document.aux))
2022-12-04T21:15:42.156154+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX Warning: There were multiply-defined labels.
2022-12-04T21:15:42.156352+00:00 INFO [LIITOS]: latex-to-pdf(2/3):  741 words of node memory still in use:
2022-12-04T21:15:42.156369+00:00 INFO [LIITOS]: latex-to-pdf(2/3):    7 hlist, 2 vlist, 2 rule, 1 local_par, 4 glue, 4 kern, 1 penalty, 3 glyph, 1
2022-12-04T21:15:42.156384+00:00 INFO [LIITOS]: latex-to-pdf(2/3): 5 attribute, 87 glue_spec, 10 attribute_list, 3 write, 1 user_defined nodes
2022-12-04T21:15:42.156408+00:00 INFO [LIITOS]: latex-to-pdf(2/3):    avail lists: 1:3,2:1944,3:357,4:128,5:147,6:170,7:2210,8:38,9:1367,10:3,11:7
2022-12-04T21:15:42.156423+00:00 INFO [LIITOS]: latex-to-pdf(2/3): 1,12:1
2022-12-04T21:15:42.183203+00:00 INFO [LIITOS]: latex-to-pdf(2/3): </usr/local/texlive/2022/texmf-dist/fonts/opentype/public/lm/lmsans12-regular.o
2022-12-04T21:15:42.191774+00:00 INFO [LIITOS]: latex-to-pdf(2/3): tf></usr/local/texlive/2022/texmf-dist/fonts/opentype/public/lm/lmsans10-bold.o
2022-12-04T21:15:42.214429+00:00 INFO [LIITOS]: latex-to-pdf(2/3): tf></opt/fonts/ITCFranklinGothicStd-Demi.otf></opt/fonts/ITCFranklinGothicStd-B
2022-12-04T21:15:42.220091+00:00 INFO [LIITOS]: latex-to-pdf(2/3): ook.otf>
2022-12-04T21:15:42.220116+00:00 INFO [LIITOS]: latex-to-pdf(2/3): Output written on this.pdf (7 pages, 29050 bytes).
2022-12-04T21:15:42.228585+00:00 INFO [LIITOS]: latex-to-pdf(2/3): Transcript written on this.log.
2022-12-04T21:15:42.274800+00:00 INFO [LIITOS]: latex-to-pdf process 2/3  (['lualatex', '--shell-escape', 'this.tex']) returned 0
2022-12-04T21:15:42.274862+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:42.274880+00:00 INFO [LIITOS]: 3/3) lualatex --shell-escape this.tex ...
2022-12-04T21:15:42.471545+00:00 INFO [LIITOS]: latex-to-pdf(3/3): This is LuaHBTeX, Version 1.15.0 (TeX Live 2022)
2022-12-04T21:15:42.471737+00:00 INFO [LIITOS]: latex-to-pdf(3/3):  system commands enabled.
2022-12-04T21:15:42.488565+00:00 INFO [LIITOS]: latex-to-pdf(3/3): (./this.tex
2022-12-04T21:15:42.488602+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX2e <2022-11-01>
2022-12-04T21:15:42.609542+00:00 INFO [LIITOS]: latex-to-pdf(3/3):  L3 programming layer <2022-11-02> (./setup.tex
2022-12-04T21:15:42.609806+00:00 INFO [LIITOS]: latex-to-pdf(3/3): Document Class: scrartcl 2022/10/12 v3.38 KOMA-Script document class (article)
2022-12-04T21:15:43.012191+00:00 INFO [LIITOS]: latex-to-pdf(3/3): For additional information on amsmath, use the `?' option.
2022-12-04T21:15:43.511024+00:00 INFO [LIITOS]: latex-to-pdf(3/3): === Package selnolig, Version 0.302, Date 2015/10/26 ===
2022-12-04T21:15:43.526752+00:00 INFO [LIITOS]: latex-to-pdf(3/3): ex.sty)) (./metadata.tex)
2022-12-04T21:15:43.785462+00:00 INFO [LIITOS]: latex-to-pdf(3/3): (./this.aux (./bookmatter.aux) (./publisher.aux) (./document.aux
2022-12-04T21:15:43.785544+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX Warning: Label `fig:blue' multiply defined.
2022-12-04T21:15:43.785563+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX Warning: Label `fig:blue' multiply defined.
2022-12-04T21:15:43.785582+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX Warning: Label `fig:red' multiply defined.
2022-12-04T21:15:44.146648+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [Loading MPS to PDF converter (version 2006.09.02).]
2022-12-04T21:15:44.153576+00:00 INFO [LIITOS]: latex-to-pdf(3/3): *geometry* driver: auto-detecting
2022-12-04T21:15:44.153610+00:00 INFO [LIITOS]: latex-to-pdf(3/3): *geometry* detected driver: luatex
2022-12-04T21:15:44.178060+00:00 INFO [LIITOS]: latex-to-pdf(3/3): (./bookmatter.tex)
2022-12-04T21:15:44.225388+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [1{/usr/local/texlive/2022/texmf-var/fonts/map/pdftex/updmap/pdftex.map}</opt/l
2022-12-04T21:15:44.239408+00:00 INFO [LIITOS]: latex-to-pdf(3/3): ogo/liitos-logo.png>] (./publisher.tex
2022-12-04T21:15:44.239471+00:00 INFO [LIITOS]: latex-to-pdf(3/3): Overfull \hbox (0.5696pt too wide) in alignment at lines 8--22
2022-12-04T21:15:44.247927+00:00 INFO [LIITOS]: latex-to-pdf(3/3): warning  (pdf backend): ignoring duplicate destination with the name 'page.1'
2022-12-04T21:15:44.282382+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [1] (./this.toc)
2022-12-04T21:15:44.311935+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [2] (./document.tex
2022-12-04T21:15:44.339380+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [3<./images/blue.png>]
2022-12-04T21:15:44.348219+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [4]
2022-12-04T21:15:44.362293+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [5<./images/yellow.png><./images/red.png>])
2022-12-04T21:15:44.374020+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [6<./images/lime.png><./diagrams/squares-and-edges.png>] (./this.aux
2022-12-04T21:15:44.376950+00:00 INFO [LIITOS]: latex-to-pdf(3/3): (./bookmatter.aux) (./publisher.aux) (./document.aux))
2022-12-04T21:15:44.376983+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX Warning: There were multiply-defined labels.
2022-12-04T21:15:44.377183+00:00 INFO [LIITOS]: latex-to-pdf(3/3):  741 words of node memory still in use:
2022-12-04T21:15:44.377202+00:00 INFO [LIITOS]: latex-to-pdf(3/3):    7 hlist, 2 vlist, 2 rule, 1 local_par, 4 glue, 4 kern, 1 penalty, 3 glyph, 1
2022-12-04T21:15:44.377218+00:00 INFO [LIITOS]: latex-to-pdf(3/3): 5 attribute, 87 glue_spec, 10 attribute_list, 3 write, 1 user_defined nodes
2022-12-04T21:15:44.377233+00:00 INFO [LIITOS]: latex-to-pdf(3/3):    avail lists: 1:3,2:1944,3:357,4:128,5:147,6:170,7:2210,8:38,9:1367,10:3,11:7
2022-12-04T21:15:44.377249+00:00 INFO [LIITOS]: latex-to-pdf(3/3): 1,12:1
2022-12-04T21:15:44.404516+00:00 INFO [LIITOS]: latex-to-pdf(3/3): </usr/local/texlive/2022/texmf-dist/fonts/opentype/public/lm/lmsans12-regular.o
2022-12-04T21:15:44.412994+00:00 INFO [LIITOS]: latex-to-pdf(3/3): tf></usr/local/texlive/2022/texmf-dist/fonts/opentype/public/lm/lmsans10-bold.o
2022-12-04T21:15:44.435290+00:00 INFO [LIITOS]: latex-to-pdf(3/3): tf></opt/fonts/ITCFranklinGothicStd-Demi.otf></opt/fonts/ITCFranklinGothicStd-B
2022-12-04T21:15:44.440961+00:00 INFO [LIITOS]: latex-to-pdf(3/3): ook.otf>
2022-12-04T21:15:44.440988+00:00 INFO [LIITOS]: latex-to-pdf(3/3): Output written on this.pdf (7 pages, 29050 bytes).
2022-12-04T21:15:44.449403+00:00 INFO [LIITOS]: latex-to-pdf(3/3): Transcript written on this.log.
2022-12-04T21:15:44.494377+00:00 INFO [LIITOS]: latex-to-pdf process 3/3  (['lualatex', '--shell-escape', 'this.tex']) returned 0
2022-12-04T21:15:44.494433+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:44.494450+00:00 INFO [LIITOS]: Moving stuff around (result phase) ...
2022-12-04T21:15:44.503523+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:44.503567+00:00 INFO [LIITOS]: Deliverable taxonomy: ...
2022-12-04T21:15:44.513396+00:00 INFO [LIITOS]: - Ephemeral:
2022-12-04T21:15:44.513429+00:00 INFO [LIITOS]:   + name: index.pdf
2022-12-04T21:15:44.513446+00:00 INFO [LIITOS]:   + size: 29050 bytes
2022-12-04T21:15:44.513461+00:00 INFO [LIITOS]:   + date: 2022-12-04 21:15:44.503513 +00:00
2022-12-04T21:15:44.513475+00:00 INFO [LIITOS]: - Characteristic:
2022-12-04T21:15:44.513489+00:00 INFO [LIITOS]:   + Checksums:
2022-12-04T21:15:44.513505+00:00 INFO [LIITOS]:     sha512:f17808b7f73cd3877381711394000388bd7f57d3d3369a95945c382b070601c9a2659a3fbcf8593b84192e7af501d6cb8e212d175303306b520ba13c321a1cdb
2022-12-04T21:15:44.513521+00:00 INFO [LIITOS]:     sha256:f7b4ce14d233dc41977615df773f27c6acb569550f311cc0a538f2a6f25f69e5
2022-12-04T21:15:44.513538+00:00 INFO [LIITOS]:       sha1:ec982108353df88c35e8a1e2e199ebc4f53055cc
2022-12-04T21:15:44.513551+00:00 INFO [LIITOS]:        md5:870aed0f12e5a71a5a2b137ce6c4ddd1
2022-12-04T21:15:44.513567+00:00 INFO [LIITOS]:   + Fonts:
2022-12-04T21:15:44.534271+00:00 INFO [LIITOS]:     pdffonts: name                                 type              encoding         emb sub uni object ID
2022-12-04T21:15:44.534469+00:00 INFO [LIITOS]:     pdffonts: ------------------------------------ ----------------- ---------------- --- --- --- ---------
2022-12-04T21:15:44.534492+00:00 INFO [LIITOS]:     pdffonts: XPOFQN+ITCFranklinGothicStd-Book     CID Type 0C       Identity-H       yes yes yes      8  0
2022-12-04T21:15:44.534509+00:00 INFO [LIITOS]:     pdffonts: IKTCZX+ITCFranklinGothicStd-Demi     CID Type 0C       Identity-H       yes yes yes      9  0
2022-12-04T21:15:44.534525+00:00 INFO [LIITOS]:     pdffonts: FSKYUR+LMSans10-Bold                 CID Type 0C       Identity-H       yes yes yes     11  0
2022-12-04T21:15:44.534541+00:00 INFO [LIITOS]:     pdffonts: HPBJUX+LMSans12-Regular              CID Type 0C       Identity-H       yes yes yes     12  0
2022-12-04T21:15:44.534585+00:00 INFO [LIITOS]: pdffonts process (['pdffonts', '../index.pdf']) returned 0
2022-12-04T21:15:44.534604+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2022-12-04T21:15:44.534621+00:00 INFO [LIITOS]: done.
2022-12-04T21:15:44.534635+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -```
