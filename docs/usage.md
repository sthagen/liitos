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
❯ Splice (Finnish liitos) contributions. version 2023.1.21+parent.85ecfd90
```

## Eject 

You can eject template files to modify these and provide externally per environment variables for overriding the built-in variants.

Any unique start of template name will yield, executing the command without argument provides a list of available templates (i.e. their names):

```console
❯ liitos eject
2023-01-14T20:13:40.724659+00:00 ERROR [LIITOS]: eject of template with no name requested
2023-01-14T20:13:40.726042+00:00 INFO [LIITOS]: templates known: (approvals-yaml, bookmatter-pdf, changes-yaml, driver-pdf, meta-base-yaml, meta-patch-yaml, metadata-pdf, mkdocs-yaml, publisher-pdf, setup-pdf, vocabulary-yaml)
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
2023-01-14T20:14:05.278964+00:00 INFO [LIITOS]: starting verification of facet (mn) for target (abc) with structure map (structure.yml) in document root (test/fixtures/basic)
2023-01-14T20:14:05.281152+00:00 INFO [LIITOS]: - target (abc) OK
2023-01-14T20:14:05.281183+00:00 INFO [LIITOS]: - facet (mn) of target (abc) OK
2023-01-14T20:14:05.283696+00:00 INFO [LIITOS]: - assets (approvals, bind, changes, meta) for facet (mn) of target (abc) OK
2023-01-14T20:14:05.283717+00:00 INFO [LIITOS]: loading signatures from signatures_path='approvals.json'
2023-01-14T20:14:05.283766+00:00 INFO [LIITOS]: signatures=({'columns': ['Approvals', 'Name'], 'rows': [['Author', 'One Author'], ['Review', 'One Reviewer'], ['Approved', 'One Approver']]}, '')
2023-01-14T20:14:05.283784+00:00 INFO [LIITOS]: loading history from history_path='changes.json'
2023-01-14T20:14:05.283824+00:00 INFO [LIITOS]: history=({'columns': ['issue', 'author', 'date', 'summary'], 'rows': [['01', 'One Author', '31.12.2024', 'Initial Issue']]}, '')
2023-01-14T20:14:05.283840+00:00 INFO [LIITOS]: loading metadata from metadata_path='meta-mn.yml'
2023-01-14T20:14:05.284711+00:00 INFO [LIITOS]: info=({'document': {'short_title': 'The Y', 'long_title': 'The Real Y', 'sub_title': None, 'type': 'Engineering Document', 'id': 'ID-X-1234-00', 'issue': '01', 'revision': '00', 'head_iss_rev': 'Iss @issue, Rev @revision', 'date': '21 OCT 2022', 'blurb_header': 'Some Comp. Proprietary Information', 'page_count_prefix': 'Page', 'toc': True, 'lof': False, 'lot': False}}, '')
2023-01-14T20:14:05.284729+00:00 INFO [LIITOS]: successful verification
```

Similarly verifying the structural integrity of the deep example:

```console
❯ liitos verify example/deep --target prod_kind --facet deep
2023-01-14T20:14:31.540469+00:00 INFO [LIITOS]: starting verification of facet (deep) for target (prod_kind) with structure map (structure.yml) in document root (example/deep)
2023-01-14T20:14:31.541906+00:00 INFO [LIITOS]: - target (prod_kind) OK
2023-01-14T20:14:31.541934+00:00 INFO [LIITOS]: - facet (deep) of target (prod_kind) OK
2023-01-14T20:14:31.544819+00:00 INFO [LIITOS]: - assets (approvals, bind, changes, meta) for facet (deep) of target (prod_kind) OK
2023-01-14T20:14:31.544845+00:00 INFO [LIITOS]: loading signatures from signatures_path='approvals.yml'
2023-01-14T20:14:31.545356+00:00 INFO [LIITOS]: signatures=({'approvals': [{'name': 'An Author', 'role': 'Author'}, {'name': 'A Reviewer', 'role': 'Review'}, {'name': 'An App Rover', 'role': 'Approved'}]}, '')
2023-01-14T20:14:31.545379+00:00 INFO [LIITOS]: loading history from history_path='changes.yml'
2023-01-14T20:14:31.545735+00:00 INFO [LIITOS]: history=({'changes': [{'author': 'An Author', 'date': 'PUBLICATIONDATE', 'issue': '01', 'summary': 'Initial Issue'}]}, '')
2023-01-14T20:14:31.545754+00:00 INFO [LIITOS]: loading metadata from metadata_path='meta-deep.yml'
2023-01-14T20:14:31.546280+00:00 INFO [LIITOS]: info=({'document': {'import': 'meta-base.yml', 'patch': {'header_id': 'P99999', 'header_date': 'PUBLICATIONDATE', 'toc_level': 3, 'list_of_figures': '', 'list_of_tables': ''}}}, '')
2023-01-14T20:14:31.546300+00:00 INFO [LIITOS]: successful verification
```
Target document key not present in structure (map):

```console
❯ liitos verify -d test/fixtures/basic -f mn -t no-target
2023-01-14T20:14:59.716205+00:00 INFO [LIITOS]: starting verification of facet (mn) for target (no-target) with structure map (structure.yml) in document root (test/fixtures/basic)
2023-01-14T20:14:59.718148+00:00 ERROR [LIITOS]: failed verification with: target (no-target) not in ['abc']
```

Facet key for target document not present in structure (map):

```console
❯ liitos verify -d test/fixtures/basic -f no-facet -t abc
2023-01-14T20:15:22.509602+00:00 INFO [LIITOS]: starting verification of facet (no-facet) for target (abc) with structure map (structure.yml) in document root (test/fixtures/basic)
2023-01-14T20:15:22.511442+00:00 INFO [LIITOS]: - target (abc) OK
2023-01-14T20:15:22.511475+00:00 ERROR [LIITOS]: failed verification with: facet (no-facet) of target (abc) not in ['missing', 'mn', 'opq']
```

Invalid asset link of facet for target document key:

```console
❯ liitos verify -d test/fixtures/basic -f opq -t abc
2023-01-14T20:15:39.656353+00:00 INFO [LIITOS]: starting verification of facet (opq) for target (abc) with structure map (structure.yml) in document root (test/fixtures/basic)
2023-01-14T20:15:39.658452+00:00 INFO [LIITOS]: - target (abc) OK
2023-01-14T20:15:39.658477+00:00 INFO [LIITOS]: - facet (opq) of target (abc) OK
2023-01-14T20:15:39.661172+00:00 INFO [LIITOS]: - assets (approvals, bind, changes, meta) for facet (opq) of target (abc) OK
2023-01-14T20:15:39.661194+00:00 INFO [LIITOS]: loading signatures from signatures_path='approvals.yml'
2023-01-14T20:15:39.661708+00:00 INFO [LIITOS]: signatures=({'approvals': [{'role': 'Author', 'name': 'One Author'}, {'role': 'Review', 'name': 'One Reviewer'}, {'role': 'Approved', 'name': 'One Approver'}]}, '')
2023-01-14T20:15:39.661726+00:00 INFO [LIITOS]: loading history from history_path='changes.yml'
2023-01-14T20:15:39.662090+00:00 INFO [LIITOS]: history=({'changes': [{'issue': '01', 'author': 'One Author', 'date': '31.12.2024', 'summary': 'Initial Issue'}]}, '')
2023-01-14T20:15:39.662111+00:00 INFO [LIITOS]: loading metadata from metadata_path='meta-opq.md'
2023-01-14T20:15:39.662265+00:00 INFO [LIITOS]: info=({'setting': 'special opq value'}, '')
2023-01-14T20:15:39.662282+00:00 INFO [LIITOS]: successful verification
```

## Concat

```console
❯ liitos concat example/deep -t prod_kind -f deep
2023-01-14T20:16:09.761532+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:16:09.762162+00:00 INFO [LIITOS]: parsed target (prod_kind) and facet (deep) from request
2023-01-14T20:16:09.762230+00:00 INFO [LIITOS]: executing prelude of command (concat) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (example/deep) coming from (/some/where)
2023-01-14T20:16:09.763988+00:00 INFO [LIITOS]: prelude teleported processor into the document root at (/some/where/example/deep/)
2023-01-14T20:16:09.764127+00:00 INFO [LIITOS]: concatenate (this processor) teleported into the render/pdf location (/some/where/example/deep/render/pdf/)
2023-01-14T20:16:09.764612+00:00 INFO [LIITOS]: found single target (prod_kind) with facets (['deep'])
2023-01-14T20:16:09.764641+00:00 WARNING [LIITOS]: structure does not strictly provide the expected aspects ['approvals', 'bind', 'changes', 'meta'] for target (prod_kind) and facet (deep)
2023-01-14T20:16:09.764657+00:00 WARNING [LIITOS]: - found the following aspects instead:                   ['approvals', 'bind', 'changes', 'meta', 'render'] instead
2023-01-14T20:16:09.772604+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:16:09.772630+00:00 INFO [LIITOS]: processing binder ...
2023-01-14T20:16:09.773043+00:00 INFO [LIITOS]: - parsing the markdown image text line ...
2023-01-14T20:16:09.773325+00:00 INFO [LIITOS]: ==> belte-og-seler: ->>![Caption Text Yellow](images/yellow.png "Alt Text Yellow")<<-
2023-01-14T20:16:09.774215+00:00 INFO [LIITOS]: - parsing the markdown image text line ...
2023-01-14T20:16:09.774293+00:00 INFO [LIITOS]: images/blue.png <--- OK? --- part/images/blue.png
2023-01-14T20:16:09.774316+00:00 INFO [LIITOS]: ==> belte-og-seler: ->>![Caption Text Blue](images/blue.png "Alt Text Blue")<<-
2023-01-14T20:16:09.774337+00:00 INFO [LIITOS]: - parsing the markdown image text line ...
2023-01-14T20:16:09.774402+00:00 INFO [LIITOS]: images/blue.png <--- OK? --- part/images/blue.png
2023-01-14T20:16:09.774417+00:00 INFO [LIITOS]: ==> belte-og-seler: ->>![Caption Text Blue Repeated Image](images/blue.png "Alt Text Blue Same Repeated Image")<<-
2023-01-14T20:16:09.774436+00:00 INFO [LIITOS]: - parsing the markdown image text line ...
2023-01-14T20:16:09.774452+00:00 WARNING [LIITOS]: - INCOMPLETE-MD-IMG_LINE::CAP-MISS-INJECTED <<![](images/blue.png  "Alt Text Blue Same Repeated Image Caption Missing")>>
2023-01-14T20:16:09.774513+00:00 INFO [LIITOS]: images/blue.png <--- OK? --- part/images/blue.png
2023-01-14T20:16:09.774528+00:00 INFO [LIITOS]: ==> belte-og-seler: ->>![INJECTED-CAP-TEXT-TO-MARK-MISSING-CAPTION-IN-OUTPUT](images/blue.png "Alt Text Blue Same Repeated Image Caption Missing")<<-
2023-01-14T20:16:09.774593+00:00 INFO [LIITOS]: - parsing the markdown image text line ...
2023-01-14T20:16:09.774652+00:00 INFO [LIITOS]: images/blue.png <--- OK? --- part/images/blue.png
2023-01-14T20:16:09.774670+00:00 INFO [LIITOS]: ==> belte-og-seler: ->>![Caption Text Blue](images/blue.png "Alt Text Blue")<<-
2023-01-14T20:16:09.774689+00:00 INFO [LIITOS]: - parsing the markdown image text line ...
2023-01-14T20:16:09.774746+00:00 INFO [LIITOS]: images/blue.png <--- OK? --- part/images/blue.png
2023-01-14T20:16:09.774761+00:00 INFO [LIITOS]: ==> belte-og-seler: ->>![Caption Text Blue Repeated Image](images/blue.png "Alt Text Blue Same Repeated Image")<<-
2023-01-14T20:16:09.774778+00:00 INFO [LIITOS]: - parsing the markdown image text line ...
2023-01-14T20:16:09.774793+00:00 WARNING [LIITOS]: - INCOMPLETE-MD-IMG_LINE::CAP-MISS-INJECTED <<![](images/blue.png  "Alt Text Blue Same Repeated Image Caption Missing")>>
2023-01-14T20:16:09.774847+00:00 INFO [LIITOS]: images/blue.png <--- OK? --- part/images/blue.png
2023-01-14T20:16:09.774861+00:00 INFO [LIITOS]: ==> belte-og-seler: ->>![INJECTED-CAP-TEXT-TO-MARK-MISSING-CAPTION-IN-OUTPUT](images/blue.png "Alt Text Blue Same Repeated Image Caption Missing")<<-
2023-01-14T20:16:09.775213+00:00 WARNING [LIITOS]: - INCOMPLETE-MD-IMG_LINE::QU-TOK-CNT-LOW <<![Caption for dot dot images in blue](../images/blue.png) <!-- no alt text ... and a comment eol -->>>
2023-01-14T20:16:09.775232+00:00 INFO [LIITOS]: - SUSPICIOUS-MD-IMG_LINE::MAY-HAVE-UPWARDS-PATH <<![Caption for dot dot images in blue](../images/blue.png) <!-- no alt text ... and a comment eol -->>>
2023-01-14T20:16:09.775245+00:00 INFO [LIITOS]: - parsing the markdown image text line ...
2023-01-14T20:16:09.775310+00:00 INFO [LIITOS]: images/blue.png <--- OK? --- part/images/blue.png
2023-01-14T20:16:09.775326+00:00 INFO [LIITOS]: ==> belte-og-seler: ->>![Caption for dot dot images in blue](images/blue.png "INJECTED-ALT-TEXT-TO-TRIGGER-FIGURE-ENVIRONMENT-AROUND-IMAGE-IN-PANDOC") <!-- no alt text ... and a comment eol --><<-
2023-01-14T20:16:09.776144+00:00 INFO [LIITOS]: - parsing the markdown image text line ...
2023-01-14T20:16:09.776211+00:00 INFO [LIITOS]: images/red.png <--- OK? --- other/images/red.png
2023-01-14T20:16:09.776227+00:00 INFO [LIITOS]: ==> belte-og-seler: ->>![Caption Text Sting Red](images/red.png "Alt Text Sting Red")<<-
2023-01-14T20:16:09.776842+00:00 INFO [LIITOS]: - parsing the markdown image text line ...
2023-01-14T20:16:09.776904+00:00 INFO [LIITOS]: images/red.png <--- OK? --- other/images/red.png
2023-01-14T20:16:09.776919+00:00 INFO [LIITOS]: ==> belte-og-seler: ->>![Caption Text Red](images/red.png "Alt Text Red")<<-
2023-01-14T20:16:09.776937+00:00 INFO [LIITOS]: - SUSPICIOUS-MD-IMG_LINE::MAY-HAVE-UPWARDS-PATH <<![Caption Text Dot Dot Lime](../images/lime.png "Alt Text Dot Dot Lime")>>
2023-01-14T20:16:09.776950+00:00 INFO [LIITOS]: - parsing the markdown image text line ...
2023-01-14T20:16:09.777028+00:00 INFO [LIITOS]: ==> belte-og-seler: ->>![Caption Text Dot Dot Lime](images/lime.png "Alt Text Dot Dot Lime")<<-
2023-01-14T20:16:09.777047+00:00 INFO [LIITOS]: - parsing the markdown image text line ...
2023-01-14T20:16:09.777105+00:00 INFO [LIITOS]: diagrams/squares-and-edges.svg <--- OK? --- other/diagrams/squares-and-edges.svg
2023-01-14T20:16:09.777121+00:00 INFO [LIITOS]: ==> belte-og-seler: ->>![Caption Text for SVG](diagrams/squares-and-edges.svg "Alt Text for SVG")<<-
2023-01-14T20:16:09.777140+00:00 INFO [LIITOS]: - parsing the markdown image text line ...
2023-01-14T20:16:09.777196+00:00 INFO [LIITOS]: diagrams/nuts-and-bolts.app.svg <--- OK? --- other/diagrams/nuts-and-bolts.app.svg
2023-01-14T20:16:09.777212+00:00 INFO [LIITOS]: ==> belte-og-seler: ->>![Caption Text for app specific SVG](diagrams/nuts-and-bolts.app.svg "Alt Text for app specific SVG")<<-
2023-01-14T20:16:09.777255+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:16:09.777271+00:00 INFO [LIITOS]: resulting tree:
2023-01-14T20:16:09.777340+00:00 INFO [LIITOS]: /
2023-01-14T20:16:09.777356+00:00 INFO [LIITOS]: ├── 1.md
2023-01-14T20:16:09.777369+00:00 INFO [LIITOS]: │   └── part/a.md
2023-01-14T20:16:09.777382+00:00 INFO [LIITOS]: │       ├── part/a1.md
2023-01-14T20:16:09.777395+00:00 INFO [LIITOS]: │       │   └── part/a2.md
2023-01-14T20:16:09.777408+00:00 INFO [LIITOS]: │       └── part/sub/as.md
2023-01-14T20:16:09.777420+00:00 INFO [LIITOS]: │           └── part/sub/as1.md
2023-01-14T20:16:09.777432+00:00 INFO [LIITOS]: ├── 2.md
2023-01-14T20:16:09.777446+00:00 INFO [LIITOS]: │   └── 3.md
2023-01-14T20:16:09.777458+00:00 INFO [LIITOS]: └── other/b.md
2023-01-14T20:16:09.777471+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:16:09.777485+00:00 INFO [LIITOS]: provisioning chains for the 4 bottom up leaf paths:
2023-01-14T20:16:09.777498+00:00 INFO [LIITOS]:  0: part/a2.md -> part/a1.md -> part/a.md -> 1.md -> /
2023-01-14T20:16:09.777512+00:00 INFO [LIITOS]:  1: part/sub/as1.md -> part/sub/as.md -> part/a.md -> 1.md -> /
2023-01-14T20:16:09.777525+00:00 INFO [LIITOS]:  2: 3.md -> 2.md -> /
2023-01-14T20:16:09.777538+00:00 INFO [LIITOS]:  3: other/b.md -> /
2023-01-14T20:16:09.777551+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:16:09.777563+00:00 INFO [LIITOS]: dependencies for the 9 document parts:
2023-01-14T20:16:09.777576+00:00 INFO [LIITOS]: - part 1.md <-( 1 include )-
2023-01-14T20:16:09.777590+00:00 INFO [LIITOS]:   + between lines   4 and   7 include fragment part/a.md
2023-01-14T20:16:09.777604+00:00 INFO [LIITOS]: - part part/a.md <--( 2 includes )--
2023-01-14T20:16:09.777617+00:00 INFO [LIITOS]:   + between lines   4 and   7 include fragment part/a1.md
2023-01-14T20:16:09.777631+00:00 INFO [LIITOS]:   + between lines  13 and  13 include fragment part/sub/as.md
2023-01-14T20:16:09.777644+00:00 INFO [LIITOS]: - part part/a1.md <-( 1 include )-
2023-01-14T20:16:09.777658+00:00 INFO [LIITOS]:   + between lines  38 and  41 include fragment part/a2.md
2023-01-14T20:16:09.777671+00:00 INFO [LIITOS]: - part part/a2.md (no includes)
2023-01-14T20:16:09.777685+00:00 INFO [LIITOS]:   * did concat part/a2.md document for insertion
2023-01-14T20:16:09.777699+00:00 INFO [LIITOS]: - part part/sub/as.md <-( 1 include )-
2023-01-14T20:16:09.777712+00:00 INFO [LIITOS]:   + between lines   4 and   7 include fragment part/sub/as1.md
2023-01-14T20:16:09.777725+00:00 INFO [LIITOS]: - part part/sub/as1.md (no includes)
2023-01-14T20:16:09.777738+00:00 INFO [LIITOS]:   * did concat part/sub/as1.md document for insertion
2023-01-14T20:16:09.777751+00:00 INFO [LIITOS]: - part 2.md <-( 1 include )-
2023-01-14T20:16:09.777764+00:00 INFO [LIITOS]:   + between lines   6 and   9 include fragment 3.md
2023-01-14T20:16:09.777777+00:00 INFO [LIITOS]: - part 3.md (no includes)
2023-01-14T20:16:09.777790+00:00 INFO [LIITOS]:   * did concat 3.md document for insertion
2023-01-14T20:16:09.777803+00:00 INFO [LIITOS]: - part other/b.md (no includes)
2023-01-14T20:16:09.777815+00:00 INFO [LIITOS]:   * did concat other/b.md document for insertion
2023-01-14T20:16:09.777829+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:16:09.777842+00:00 INFO [LIITOS]: starting insertions bottom up for the 4 inclusion chains:
2023-01-14T20:16:09.777859+00:00 INFO [LIITOS]:   Insertion ongoing with parts (2.md, part/a1.md, part/sub/as.md) remaining
2023-01-14T20:16:09.777890+00:00 INFO [LIITOS]:   Insertion ongoing with parts (part/a.md, part/a.md) remaining
2023-01-14T20:16:09.777915+00:00 INFO [LIITOS]:   Insertion ongoing with parts (1.md, 1.md) remaining
2023-01-14T20:16:09.777934+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:16:09.777948+00:00 INFO [LIITOS]: writing final concat markdown to document.md
2023-01-14T20:16:09.778162+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:16:09.778178+00:00 INFO [LIITOS]: collecting assets (images and diagrams)
2023-01-14T20:16:09.786023+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:16:09.786078+00:00 INFO [LIITOS]: concat result document (document.md) and artifacts are within folder (/some/where/example/deep/render/pdf/)
2023-01-14T20:16:09.786098+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:16:09.786112+00:00 INFO [LIITOS]: processing complete - SUCCESS
2023-01-14T20:16:09.786126+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

## Render

Note: Since version 2023.1.21 an optional `-l,--label` parameter allows to provide a call string for 
labeling the resulting pdf file. Example: `... --label 'etiketti --enforce'`
(that could be using the [`etiketti` script from the package with the same name](https://pypi.org/project/etiketti/)).

```console
❯ liitos render example/deep -t prod_kind -f deep
# ... - - - 8< - - - ...
2023-01-14T20:18:18.111055+00:00 INFO [LIITOS]: processing complete - SUCCESS
2023-01-14T20:18:18.111069+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:18.111165+00:00 INFO [LIITOS]: before met.weave(): /some/where/example/deep/render/pdf set doc (../../)
2023-01-14T20:18:18.111184+00:00 INFO [LIITOS]: parsed target (prod_kind) and facet (deep) from request
2023-01-14T20:18:18.111218+00:00 INFO [LIITOS]: executing prelude of command (meta) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/Usome/where/example/deep/render/pdf)
2023-01-14T20:18:18.111713+00:00 INFO [LIITOS]: prelude teleported processor into the document root at (/some/where/example/deep/)
2023-01-14T20:18:18.111759+00:00 INFO [LIITOS]: meta (this processor) teleported into the render/pdf location (/some/where/example/deep/render/pdf/)
2023-01-14T20:18:18.112215+00:00 INFO [LIITOS]: found single target (prod_kind) with facets (['deep'])
2023-01-14T20:18:18.112237+00:00 WARNING [LIITOS]: structure does not strictly provide the expected aspects ['approvals', 'bind', 'changes', 'meta'] for target (prod_kind) and facet (deep)
2023-01-14T20:18:18.112252+00:00 WARNING [LIITOS]: - found the following aspects instead:                   ['approvals', 'bind', 'changes', 'meta', 'render'] instead
2023-01-14T20:18:18.116960+00:00 INFO [LIITOS]: weaving in the meta data per metadata.tex.in into metadata.tex ...
2023-01-14T20:18:18.117005+00:00 INFO [LIITOS]: header_id_show not set - considering header_id_label ...
2023-01-14T20:18:18.117021+00:00 WARNING [LIITOS]: header_id_label value missing ... setting default(Doc. ID:)
2023-01-14T20:18:18.117039+00:00 INFO [LIITOS]: header_id_show not set - considering header_id ...
2023-01-14T20:18:18.117060+00:00 INFO [LIITOS]: header_date_show not set - considering header_date_label ...
2023-01-14T20:18:18.117073+00:00 WARNING [LIITOS]: header_date_label value missing ... setting default(Date:)
2023-01-14T20:18:18.117089+00:00 INFO [LIITOS]: header_date_show not set - considering header_date ...
2023-01-14T20:18:18.117151+00:00 INFO [LIITOS]: header_issue_revision_combined_show not set - considering header_issue_revision_combined_label ...
2023-01-14T20:18:18.117168+00:00 WARNING [LIITOS]: header_issue_revision_combined_label value missing ... setting default(Issue, Revision:)
2023-01-14T20:18:18.117185+00:00 INFO [LIITOS]: header_issue_revision_combined_show not set - considering header_issue_revision_combined ...
2023-01-14T20:18:18.117200+00:00 INFO [LIITOS]: header_issue_revision_combined value missing ... setting default (Iss \theMetaIssCode, Rev \theMetaRevCode)
2023-01-14T20:18:18.118365+00:00 INFO [LIITOS]: weaving in the meta data per driver.tex.in into driver.tex ...
2023-01-14T20:18:18.118954+00:00 INFO [LIITOS]: weaving in the meta data per setup.tex.in into setup.tex ...
2023-01-14T20:18:18.119586+00:00 INFO [LIITOS]: before sig.weave(): /some/where/example/deep/render/pdf set doc (../../)
2023-01-14T20:18:18.119622+00:00 INFO [LIITOS]: relocated for sig.weave(): /some/where/example/deep/render/pdf with doc (../../)
2023-01-14T20:18:18.119639+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:18.119674+00:00 INFO [LIITOS]: executing prelude of command (approvals) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/some/where/example/deep/render/pdf)
2023-01-14T20:18:18.120141+00:00 INFO [LIITOS]: detected approvals channel (yaml) weaving in from (approvals.yml)
2023-01-14T20:18:18.120162+00:00 INFO [LIITOS]: loading signatures from signatures_path='approvals.yml'
2023-01-14T20:18:18.120652+00:00 INFO [LIITOS]: signatures=({'approvals': [{'name': 'An Author', 'role': 'Author'}, {'name': 'A Reviewer', 'role': 'Review'}, {'name': 'An App Rover', 'role': 'Approved'}]}, '')
2023-01-14T20:18:18.120673+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:18.120686+00:00 INFO [LIITOS]: plausibility tests for approvals ...
2023-01-14T20:18:18.120710+00:00 INFO [LIITOS]: calculated extra pushdown to be 18em
2023-01-14T20:18:18.121109+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:18.121125+00:00 INFO [LIITOS]: weaving in the approvals from approvals.yml...
2023-01-14T20:18:18.121329+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:18.121362+00:00 INFO [LIITOS]: before chg.weave(): /some/where/example/deep set doc (../../)
2023-01-14T20:18:18.121395+00:00 INFO [LIITOS]: relocated for chg.weave(): /some/where/example/deep/render/pdf with doc (../../)
2023-01-14T20:18:18.121410+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:18.121443+00:00 INFO [LIITOS]: executing prelude of command (changes) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/some/where/example/deep/render/pdf)
2023-01-14T20:18:18.121882+00:00 INFO [LIITOS]: detected changes channel (yaml) weaving in from (changes.yml)
2023-01-14T20:18:18.121900+00:00 INFO [LIITOS]: loading changes from changes_path='changes.yml'
2023-01-14T20:18:18.122240+00:00 INFO [LIITOS]: changes=({'changes': [{'author': 'An Author', 'date': 'PUBLICATIONDATE', 'issue': '01', 'summary': 'Initial Issue'}]}, '')
2023-01-14T20:18:18.122257+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:18.122271+00:00 INFO [LIITOS]: plausibility tests for changes ...
2023-01-14T20:18:18.122691+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:18.122711+00:00 INFO [LIITOS]: weaving in the changes ...
2023-01-14T20:18:18.122983+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:18.123015+00:00 INFO [LIITOS]: before chg.weave(): /some/where/example/deep set doc (../../)
2023-01-14T20:18:18.123045+00:00 INFO [LIITOS]: relocated for chg.weave(): /some/where/example/deep/render/pdf with doc (../../)
2023-01-14T20:18:18.123061+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:18.123074+00:00 INFO [LIITOS]: parsed target (prod_kind) and facet (deep) from request
2023-01-14T20:18:18.123108+00:00 INFO [LIITOS]: executing prelude of command (render) for facet (deep) of target (prod_kind) with structure map (structure.yml) in document root (../..) coming from (/some/where/example/deep/render/pdf)
2023-01-14T20:18:18.123561+00:00 INFO [LIITOS]: prelude teleported processor into the document root at (/some/where/example/deep/)
2023-01-14T20:18:18.123598+00:00 INFO [LIITOS]: inspecting any patch spec file (patch.yml) ...
2023-01-14T20:18:18.124337+00:00 INFO [LIITOS]: - loaded 1 patch pair from patch spec file (patch.yml)
2023-01-14T20:18:18.124371+00:00 INFO [LIITOS]: render (this processor) teleported into the render/pdf location (/some/where/example/deep/render/pdf/)
2023-01-14T20:18:18.124387+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:18.124400+00:00 INFO [LIITOS]: Assessing the local version control status (compared to upstream) ...
2023-01-14T20:18:18.124413+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:18.183456+00:00 INFO [LIITOS]: Root     (/some/where)
2023-01-14T20:18:18.183626+00:00 INFO [LIITOS]: Analysis (2023-01-14 20:18:18 UTC)
2023-01-14T20:18:18.183647+00:00 INFO [LIITOS]: State    (UP TO DATE)
2023-01-14T20:18:18.183662+00:00 INFO [LIITOS]: Branch   (default)
2023-01-14T20:18:18.183676+00:00 INFO [LIITOS]: Commit   (4d375c3329d5d0284eadc9b60c49215c6f215e5f)
2023-01-14T20:18:18.183690+00:00 INFO [LIITOS]: List of locally modified files:
2023-01-14T20:18:18.183703+00:00 INFO [LIITOS]:  - docs/usage.md
2023-01-14T20:18:18.183721+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:18.184334+00:00 INFO [LIITOS]: found single target (prod_kind) with facets (['deep'])
2023-01-14T20:18:18.184360+00:00 INFO [LIITOS]: found render instruction with value (True)
2023-01-14T20:18:18.184374+00:00 INFO [LIITOS]: we will render ...
2023-01-14T20:18:18.184385+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:18.184398+00:00 INFO [LIITOS]: transforming SVG assets to high resolution PNG bitmaps ...
2023-01-14T20:18:19.008492+00:00 INFO [LIITOS]: svg-to-png: /some/where/example/deep/render/pdf/diagrams/squares-and-edges.svg /some/where/example/deep/render/pdf/diagrams/squares-and-edges.png png 100% 1x 0:0:220:100 220:100
2023-01-14T20:18:19.150802+00:00 INFO [LIITOS]: svg-to-png process (['svgexport', PosixPath('diagrams/squares-and-edges.svg'), 'diagrams/squares-and-edges.png', '100%']) returned 0
2023-01-14T20:18:19.910893+00:00 INFO [LIITOS]: svg-to-png: /some/where/example/deep/render/pdf/diagrams/nuts-and-bolts.app.svg /some/where/deep/render/pdf/diagrams/nuts-and-bolts.app.png png 100% 1x 0:0:220:100 220:100
2023-01-14T20:18:19.934926+00:00 INFO [LIITOS]: svg-to-png process (['svgexport', PosixPath('diagrams/nuts-and-bolts.app.svg'), 'diagrams/nuts-and-bolts.app.png', '100%']) returned 0
2023-01-14T20:18:19.935078+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:19.935118+00:00 INFO [LIITOS]: rewriting src attribute values of SVG to PNG sources ...
2023-01-14T20:18:19.935665+00:00 INFO [LIITOS]:   transform[#132]: ![Caption Text for SVG](diagrams/squares-and-edges.svg "Alt Text for SVG")
2023-01-14T20:18:19.935726+00:00 INFO [LIITOS]:        into[#132]: ![Caption Text for SVG](diagrams/squares-and-edges.png "Alt Text for SVG")
2023-01-14T20:18:19.935788+00:00 INFO [LIITOS]: - parsing the markdown image text line ...
2023-01-14T20:18:19.935850+00:00 INFO [LIITOS]: - removing application indicator (app) from src ...
2023-01-14T20:18:19.935883+00:00 INFO [LIITOS]:   transform[#136]: ![Caption Text for app specific SVG](diagrams/nuts-and-bolts.app.svg "Alt Text for app specific SVG")
2023-01-14T20:18:19.935909+00:00 INFO [LIITOS]:        into[#136]: ![Caption Text for app specific SVG](diagrams/nuts-and-bolts.png "Alt Text for app specific SVG")
2023-01-14T20:18:19.935937+00:00 INFO [LIITOS]: post-action[#136]: adding to queue for sync move: (diagrams/nuts-and-bolts.app.png) -> (diagrams/nuts-and-bolts.png)
2023-01-14T20:18:19.936279+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:19.936314+00:00 INFO [LIITOS]: ensure diagram files can be found when patched ...
2023-01-14T20:18:19.936396+00:00 INFO [LIITOS]: - moving: (diagrams/nuts-and-bolts.app.png) -> (diagrams/nuts-and-bolts.png)
2023-01-14T20:18:19.936450+00:00 INFO [LIITOS]:   + resource (diagrams/nuts-and-bolts.app.png) is present at (diagrams/nuts-and-bolts.app.png) - attempt 1 of 10 ...
2023-01-14T20:18:19.937735+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:19.937803+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:19.937842+00:00 INFO [LIITOS]: pandoc -f markdown+link_attributes -t latex document.md -o document.tex --filter mermaid-filter ...
2023-01-14T20:18:20.187763+00:00 INFO [LIITOS]: markdown-to-latex: [INFO] Running filter mermaid-filter
2023-01-14T20:18:20.235150+00:00 INFO [LIITOS]: markdown-to-latex: [INFO] Completed filter mermaid-filter in 2 ms
2023-01-14T20:18:20.254946+00:00 INFO [LIITOS]: markdown-to-latex: [INFO] Not rendering RawInline (Format "html") "<!-- no alt text ... and a comment eol -->"
2023-01-14T20:18:20.259047+00:00 INFO [LIITOS]: markdown-to-latex process (['pandoc', '--verbose', '-f', 'markdown+link_attributes', '-t', 'latex', 'document.md', '-o', 'document.tex', '--filter', 'mermaid-filter']) returned 0
2023-01-14T20:18:20.259130+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:20.259152+00:00 INFO [LIITOS]: move any captions below tables ...
2023-01-14T20:18:20.261344+00:00 INFO [LIITOS]: start of a table environment at line #99
2023-01-14T20:18:20.261368+00:00 INFO [LIITOS]: - found the caption start at line #100
2023-01-14T20:18:20.261384+00:00 INFO [LIITOS]: - multi line caption at line #100
2023-01-14T20:18:20.261399+00:00 INFO [LIITOS]: - caption read at line #101
2023-01-14T20:18:20.261419+00:00 INFO [LIITOS]: end of table env detected at line #116
2023-01-14T20:18:20.261546+00:00 INFO [LIITOS]: diff of the (captions-below-tables) filter result:
2023-01-14T20:18:20.261563+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:20.261794+00:00 INFO [LIITOS]: --- before
2023-01-14T20:18:20.261813+00:00 INFO [LIITOS]: +++ after
2023-01-14T20:18:20.261829+00:00 INFO [LIITOS]: @@ -97,8 +97,6 @@
2023-01-14T20:18:20.261843+00:00 INFO [LIITOS]:  Tables maybe:
2023-01-14T20:18:20.261856+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.261869+00:00 INFO [LIITOS]:  \begin{longtable}[]{@{}lcr@{}}
2023-01-14T20:18:20.261882+00:00 INFO [LIITOS]: -\caption{A caption for a table
2023-01-14T20:18:20.261895+00:00 INFO [LIITOS]: -\label{table:left-middle-right}}\tabularnewline
2023-01-14T20:18:20.261908+00:00 INFO [LIITOS]:  \toprule()
2023-01-14T20:18:20.261921+00:00 INFO [LIITOS]:  Left & Middle & Right \\
2023-01-14T20:18:20.261933+00:00 INFO [LIITOS]:  \midrule()
2023-01-14T20:18:20.261949+00:00 INFO [LIITOS]: @@ -113,6 +111,9 @@
2023-01-14T20:18:20.261962+00:00 INFO [LIITOS]:  L10 & M11 & R12 \\
2023-01-14T20:18:20.261975+00:00 INFO [LIITOS]:  L13 & M14 & R15 \\
2023-01-14T20:18:20.261987+00:00 INFO [LIITOS]:  \bottomrule()
2023-01-14T20:18:20.262000+00:00 INFO [LIITOS]: +\rowcolor{white}
2023-01-14T20:18:20.262012+00:00 INFO [LIITOS]: +\caption{A caption for a table
2023-01-14T20:18:20.262024+00:00 INFO [LIITOS]: +\label{table:left-middle-right}}\tabularnewline
2023-01-14T20:18:20.262037+00:00 INFO [LIITOS]:  \end{longtable}
2023-01-14T20:18:20.262049+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.262062+00:00 INFO [LIITOS]:  \hypertarget{aa}{%
2023-01-14T20:18:20.262078+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:20.262094+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:20.262107+00:00 INFO [LIITOS]: inject stem (derived from file name) labels ...
2023-01-14T20:18:20.262290+00:00 INFO [LIITOS]: start of a figure environment at line #74
2023-01-14T20:18:20.262306+00:00 INFO [LIITOS]: within a figure environment at line #76
2023-01-14T20:18:20.262318+00:00 INFO [LIITOS]: \includegraphics{images/blue.png}
2023-01-14T20:18:20.262332+00:00 INFO [LIITOS]: \label{fig:blue}
2023-01-14T20:18:20.262345+00:00 INFO [LIITOS]: - found the caption start at line #77
2023-01-14T20:18:20.262358+00:00 INFO [LIITOS]: end of figure env detected at line #78
2023-01-14T20:18:20.262373+00:00 INFO [LIITOS]: start of a figure environment at line #82
2023-01-14T20:18:20.262386+00:00 INFO [LIITOS]: within a figure environment at line #84
2023-01-14T20:18:20.262399+00:00 INFO [LIITOS]: \includegraphics{images/blue.png}
2023-01-14T20:18:20.262412+00:00 INFO [LIITOS]: \label{fig:blue}
2023-01-14T20:18:20.262424+00:00 INFO [LIITOS]: - found the caption start at line #85
2023-01-14T20:18:20.262436+00:00 INFO [LIITOS]: end of figure env detected at line #86
2023-01-14T20:18:20.262450+00:00 INFO [LIITOS]: start of a figure environment at line #88
2023-01-14T20:18:20.262462+00:00 INFO [LIITOS]: within a figure environment at line #90
2023-01-14T20:18:20.262475+00:00 INFO [LIITOS]: \includegraphics{images/blue.png}
2023-01-14T20:18:20.262487+00:00 INFO [LIITOS]: \label{fig:blue}
2023-01-14T20:18:20.262500+00:00 INFO [LIITOS]: - found the caption start at line #91
2023-01-14T20:18:20.262511+00:00 INFO [LIITOS]: end of figure env detected at line #92
2023-01-14T20:18:20.262540+00:00 WARNING [LIITOS]: graphics include outside of a figure environment at line #140
2023-01-14T20:18:20.262562+00:00 ERROR [LIITOS]: line#140|\includegraphics{images/blue.png}
2023-01-14T20:18:20.262575+00:00 INFO [LIITOS]: trying to fix temporarily ... watch for marker MISSING-CAPTION-IN-MARKDOWN
2023-01-14T20:18:20.262588+00:00 INFO [LIITOS]: \label{fig:blue}
2023-01-14T20:18:20.262605+00:00 INFO [LIITOS]: start of a figure environment at line #156
2023-01-14T20:18:20.262618+00:00 INFO [LIITOS]: within a figure environment at line #158
2023-01-14T20:18:20.262630+00:00 INFO [LIITOS]: \includegraphics{images/yellow.png}
2023-01-14T20:18:20.262642+00:00 INFO [LIITOS]: \label{fig:yellow}
2023-01-14T20:18:20.262655+00:00 INFO [LIITOS]: - found the caption start at line #159
2023-01-14T20:18:20.262677+00:00 INFO [LIITOS]: end of figure env detected at line #160
2023-01-14T20:18:20.262694+00:00 INFO [LIITOS]: start of a figure environment at line #167
2023-01-14T20:18:20.262707+00:00 INFO [LIITOS]: within a figure environment at line #169
2023-01-14T20:18:20.262719+00:00 INFO [LIITOS]: \includegraphics{images/red.png}
2023-01-14T20:18:20.262732+00:00 INFO [LIITOS]: \label{fig:red}
2023-01-14T20:18:20.262744+00:00 INFO [LIITOS]: - found the caption start at line #170
2023-01-14T20:18:20.262757+00:00 INFO [LIITOS]: end of figure env detected at line #171
2023-01-14T20:18:20.262774+00:00 INFO [LIITOS]: start of a figure environment at line #183
2023-01-14T20:18:20.262788+00:00 INFO [LIITOS]: within a figure environment at line #185
2023-01-14T20:18:20.262800+00:00 INFO [LIITOS]: \includegraphics{images/red.png}
2023-01-14T20:18:20.262812+00:00 INFO [LIITOS]: \label{fig:red}
2023-01-14T20:18:20.262825+00:00 INFO [LIITOS]: - found the caption start at line #186
2023-01-14T20:18:20.262838+00:00 INFO [LIITOS]: end of figure env detected at line #187
2023-01-14T20:18:20.262851+00:00 INFO [LIITOS]: start of a figure environment at line #189
2023-01-14T20:18:20.262863+00:00 INFO [LIITOS]: within a figure environment at line #191
2023-01-14T20:18:20.262876+00:00 INFO [LIITOS]: \includegraphics{images/lime.png}
2023-01-14T20:18:20.262887+00:00 INFO [LIITOS]: \label{fig:lime}
2023-01-14T20:18:20.262899+00:00 INFO [LIITOS]: - found the caption start at line #192
2023-01-14T20:18:20.262911+00:00 INFO [LIITOS]: end of figure env detected at line #193
2023-01-14T20:18:20.262924+00:00 INFO [LIITOS]: start of a figure environment at line #197
2023-01-14T20:18:20.262936+00:00 INFO [LIITOS]: within a figure environment at line #199
2023-01-14T20:18:20.262947+00:00 INFO [LIITOS]: \includegraphics{diagrams/squares-and-edges.png}
2023-01-14T20:18:20.262959+00:00 INFO [LIITOS]: \label{fig:squares-and-edges}
2023-01-14T20:18:20.262970+00:00 INFO [LIITOS]: - found the caption start at line #200
2023-01-14T20:18:20.262983+00:00 INFO [LIITOS]: end of figure env detected at line #201
2023-01-14T20:18:20.262997+00:00 INFO [LIITOS]: start of a figure environment at line #205
2023-01-14T20:18:20.263009+00:00 INFO [LIITOS]: within a figure environment at line #207
2023-01-14T20:18:20.263023+00:00 INFO [LIITOS]: \includegraphics{diagrams/nuts-and-bolts.png}
2023-01-14T20:18:20.263035+00:00 INFO [LIITOS]: \label{fig:nuts-and-bolts}
2023-01-14T20:18:20.263047+00:00 INFO [LIITOS]: - found the caption start at line #208
2023-01-14T20:18:20.263059+00:00 INFO [LIITOS]: end of figure env detected at line #209
2023-01-14T20:18:20.265511+00:00 INFO [LIITOS]: diff of the (inject-stem-derived-labels) filter result:
2023-01-14T20:18:20.265579+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:20.265817+00:00 INFO [LIITOS]: --- before
2023-01-14T20:18:20.265834+00:00 INFO [LIITOS]: +++ after
2023-01-14T20:18:20.265849+00:00 INFO [LIITOS]: @@ -74,7 +74,7 @@
2023-01-14T20:18:20.265862+00:00 INFO [LIITOS]:  \begin{figure}
2023-01-14T20:18:20.265875+00:00 INFO [LIITOS]:  \centering
2023-01-14T20:18:20.265888+00:00 INFO [LIITOS]:  \includegraphics{images/blue.png}
2023-01-14T20:18:20.265900+00:00 INFO [LIITOS]: -\caption{Caption Text Blue}
2023-01-14T20:18:20.265913+00:00 INFO [LIITOS]: +\caption{Caption Text Blue \label{fig:blue}}
2023-01-14T20:18:20.265925+00:00 INFO [LIITOS]:  \end{figure}
2023-01-14T20:18:20.265937+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.265949+00:00 INFO [LIITOS]:  \scale=0.9
2023-01-14T20:18:20.265964+00:00 INFO [LIITOS]: @@ -82,13 +82,13 @@
2023-01-14T20:18:20.265977+00:00 INFO [LIITOS]:  \begin{figure}
2023-01-14T20:18:20.265989+00:00 INFO [LIITOS]:  \centering
2023-01-14T20:18:20.266001+00:00 INFO [LIITOS]:  \includegraphics{images/blue.png}
2023-01-14T20:18:20.266013+00:00 INFO [LIITOS]: -\caption{Caption Text Blue Repeated Image}
2023-01-14T20:18:20.266026+00:00 INFO [LIITOS]: -\end{figure}
2023-01-14T20:18:20.266038+00:00 INFO [LIITOS]: -
2023-01-14T20:18:20.266050+00:00 INFO [LIITOS]: -\begin{figure}
2023-01-14T20:18:20.266062+00:00 INFO [LIITOS]: -\centering
2023-01-14T20:18:20.266074+00:00 INFO [LIITOS]: -\includegraphics{images/blue.png}
2023-01-14T20:18:20.266086+00:00 INFO [LIITOS]: -\caption{INJECTED-CAP-TEXT-TO-MARK-MISSING-CAPTION-IN-OUTPUT}
2023-01-14T20:18:20.266098+00:00 INFO [LIITOS]: +\caption{Caption Text Blue Repeated Image \label{fig:blue}}
2023-01-14T20:18:20.266110+00:00 INFO [LIITOS]: +\end{figure}
2023-01-14T20:18:20.266123+00:00 INFO [LIITOS]: +
2023-01-14T20:18:20.266135+00:00 INFO [LIITOS]: +\begin{figure}
2023-01-14T20:18:20.266147+00:00 INFO [LIITOS]: +\centering
2023-01-14T20:18:20.266160+00:00 INFO [LIITOS]: +\includegraphics{images/blue.png}
2023-01-14T20:18:20.266172+00:00 INFO [LIITOS]: +\caption{INJECTED-CAP-TEXT-TO-MARK-MISSING-CAPTION-IN-OUTPUT \label{fig:blue}}
2023-01-14T20:18:20.266185+00:00 INFO [LIITOS]:  \end{figure}
2023-01-14T20:18:20.266197+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.266210+00:00 INFO [LIITOS]:  \hypertarget{a2-level-four}{%
2023-01-14T20:18:20.266224+00:00 INFO [LIITOS]: @@ -137,7 +137,12 @@
2023-01-14T20:18:20.266237+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.266249+00:00 INFO [LIITOS]:  Funny image reference from upstream:
2023-01-14T20:18:20.266261+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.266273+00:00 INFO [LIITOS]: -\includegraphics{images/blue.png}
2023-01-14T20:18:20.266286+00:00 INFO [LIITOS]: +
2023-01-14T20:18:20.266298+00:00 INFO [LIITOS]: +\begin{figure}
2023-01-14T20:18:20.266310+00:00 INFO [LIITOS]: +\centering
2023-01-14T20:18:20.266322+00:00 INFO [LIITOS]: +\includegraphics{images/blue.png}
2023-01-14T20:18:20.266335+00:00 INFO [LIITOS]: +\caption{MISSING-CAPTION-IN-MARKDOWN \label{fig:blue}}
2023-01-14T20:18:20.266347+00:00 INFO [LIITOS]: +\end{figure}
2023-01-14T20:18:20.266360+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.266372+00:00 INFO [LIITOS]:  The parser survives the comment but:
2023-01-14T20:18:20.266384+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.266399+00:00 INFO [LIITOS]: @@ -156,7 +161,7 @@
2023-01-14T20:18:20.266411+00:00 INFO [LIITOS]:  \begin{figure}
2023-01-14T20:18:20.266423+00:00 INFO [LIITOS]:  \centering
2023-01-14T20:18:20.266435+00:00 INFO [LIITOS]:  \includegraphics{images/yellow.png}
2023-01-14T20:18:20.266448+00:00 INFO [LIITOS]: -\caption{Caption Text Yellow}
2023-01-14T20:18:20.266460+00:00 INFO [LIITOS]: +\caption{Caption Text Yellow \label{fig:yellow}}
2023-01-14T20:18:20.266472+00:00 INFO [LIITOS]:  \end{figure}
2023-01-14T20:18:20.266484+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.266496+00:00 INFO [LIITOS]:  \hypertarget{section-1}{%
2023-01-14T20:18:20.266511+00:00 INFO [LIITOS]: @@ -167,7 +172,7 @@
2023-01-14T20:18:20.266523+00:00 INFO [LIITOS]:  \begin{figure}
2023-01-14T20:18:20.266535+00:00 INFO [LIITOS]:  \centering
2023-01-14T20:18:20.266547+00:00 INFO [LIITOS]:  \includegraphics{images/red.png}
2023-01-14T20:18:20.266559+00:00 INFO [LIITOS]: -\caption{Caption Text Sting Red}
2023-01-14T20:18:20.266572+00:00 INFO [LIITOS]: +\caption{Caption Text Sting Red \label{fig:red}}
2023-01-14T20:18:20.266584+00:00 INFO [LIITOS]:  \end{figure}
2023-01-14T20:18:20.266597+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.266610+00:00 INFO [LIITOS]:  \hypertarget{section-2}{%
2023-01-14T20:18:20.266624+00:00 INFO [LIITOS]: @@ -183,13 +188,13 @@
2023-01-14T20:18:20.266637+00:00 INFO [LIITOS]:  \begin{figure}
2023-01-14T20:18:20.266650+00:00 INFO [LIITOS]:  \centering
2023-01-14T20:18:20.266664+00:00 INFO [LIITOS]:  \includegraphics{images/red.png}
2023-01-14T20:18:20.266676+00:00 INFO [LIITOS]: -\caption{Caption Text Red}
2023-01-14T20:18:20.266688+00:00 INFO [LIITOS]: +\caption{Caption Text Red \label{fig:red}}
2023-01-14T20:18:20.266700+00:00 INFO [LIITOS]:  \end{figure}
2023-01-14T20:18:20.266713+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.266725+00:00 INFO [LIITOS]:  \begin{figure}
2023-01-14T20:18:20.266737+00:00 INFO [LIITOS]:  \centering
2023-01-14T20:18:20.266749+00:00 INFO [LIITOS]:  \includegraphics{images/lime.png}
2023-01-14T20:18:20.266761+00:00 INFO [LIITOS]: -\caption{Caption Text Dot Dot Lime}
2023-01-14T20:18:20.266774+00:00 INFO [LIITOS]: +\caption{Caption Text Dot Dot Lime \label{fig:lime}}
2023-01-14T20:18:20.266787+00:00 INFO [LIITOS]:  \end{figure}
2023-01-14T20:18:20.266799+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.266810+00:00 INFO [LIITOS]:  Yes, an SVG file:
2023-01-14T20:18:20.266825+00:00 INFO [LIITOS]: @@ -197,7 +202,7 @@
2023-01-14T20:18:20.266836+00:00 INFO [LIITOS]:  \begin{figure}
2023-01-14T20:18:20.266848+00:00 INFO [LIITOS]:  \centering
2023-01-14T20:18:20.266859+00:00 INFO [LIITOS]:  \includegraphics{diagrams/squares-and-edges.png}
2023-01-14T20:18:20.266871+00:00 INFO [LIITOS]: -\caption{Caption Text for SVG}
2023-01-14T20:18:20.266884+00:00 INFO [LIITOS]: +\caption{Caption Text for SVG \label{fig:squares-and-edges}}
2023-01-14T20:18:20.266897+00:00 INFO [LIITOS]:  \end{figure}
2023-01-14T20:18:20.266908+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.266920+00:00 INFO [LIITOS]:  And another one with application hinting suffices:
2023-01-14T20:18:20.266934+00:00 INFO [LIITOS]: @@ -205,7 +210,7 @@
2023-01-14T20:18:20.266947+00:00 INFO [LIITOS]:  \begin{figure}
2023-01-14T20:18:20.266959+00:00 INFO [LIITOS]:  \centering
2023-01-14T20:18:20.266971+00:00 INFO [LIITOS]:  \includegraphics{diagrams/nuts-and-bolts.png}
2023-01-14T20:18:20.266982+00:00 INFO [LIITOS]: -\caption{Caption Text for app specific SVG}
2023-01-14T20:18:20.266994+00:00 INFO [LIITOS]: +\caption{Caption Text for app specific SVG \label{fig:nuts-and-bolts}}
2023-01-14T20:18:20.267006+00:00 INFO [LIITOS]:  \end{figure}
2023-01-14T20:18:20.267019+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.267030+00:00 INFO [LIITOS]:  \textbf{Some bold text} normal text \emph{italic text} - even
2023-01-14T20:18:20.267046+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:20.267059+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:20.267071+00:00 INFO [LIITOS]: scale figures ...
2023-01-14T20:18:20.267432+00:00 INFO [LIITOS]: trigger a scale mod for the next figure environment at line #80|\scale=0.9
2023-01-14T20:18:20.267603+00:00 INFO [LIITOS]: - found the scale target start at line #84|\includegraphics{images/blue.png}
2023-01-14T20:18:20.269239+00:00 INFO [LIITOS]: diff of the (inject-scale-figures) filter result:
2023-01-14T20:18:20.269257+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:20.269425+00:00 INFO [LIITOS]: --- before
2023-01-14T20:18:20.269442+00:00 INFO [LIITOS]: +++ after
2023-01-14T20:18:20.269458+00:00 INFO [LIITOS]: @@ -77,11 +77,10 @@
2023-01-14T20:18:20.269472+00:00 INFO [LIITOS]:  \caption{Caption Text Blue \label{fig:blue}}
2023-01-14T20:18:20.269493+00:00 INFO [LIITOS]:  \end{figure}
2023-01-14T20:18:20.269507+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.269521+00:00 INFO [LIITOS]: -\scale=0.9
2023-01-14T20:18:20.269534+00:00 INFO [LIITOS]: -
2023-01-14T20:18:20.269548+00:00 INFO [LIITOS]: -\begin{figure}
2023-01-14T20:18:20.269561+00:00 INFO [LIITOS]: -\centering
2023-01-14T20:18:20.269574+00:00 INFO [LIITOS]: -\includegraphics{images/blue.png}
2023-01-14T20:18:20.269588+00:00 INFO [LIITOS]: +
2023-01-14T20:18:20.269601+00:00 INFO [LIITOS]: +\begin{figure}
2023-01-14T20:18:20.269614+00:00 INFO [LIITOS]: +\centering
2023-01-14T20:18:20.269627+00:00 INFO [LIITOS]: +\includegraphics[width=0.9\textwidth,height=0.9\textheight]{images/blue.png}
2023-01-14T20:18:20.269641+00:00 INFO [LIITOS]:  \caption{Caption Text Blue Repeated Image \label{fig:blue}}
2023-01-14T20:18:20.269655+00:00 INFO [LIITOS]:  \end{figure}
2023-01-14T20:18:20.269668+00:00 INFO [LIITOS]:
2023-01-14T20:18:20.269685+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:20.269699+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:20.269713+00:00 INFO [LIITOS]: apply user patches ...
2023-01-14T20:18:20.269933+00:00 INFO [LIITOS]: applying patches to 229 lines of text
2023-01-14T20:18:20.269949+00:00 INFO [LIITOS]:  - trying any (,height=\textheight]) --> (]) ...
2023-01-14T20:18:20.271948+00:00 INFO [LIITOS]: diff of the (user-patches) filter result:
2023-01-14T20:18:20.271979+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:20.272138+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:20.272157+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:20.272172+00:00 INFO [LIITOS]: cp -a driver.tex this.tex ...
2023-01-14T20:18:20.272921+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:20.272944+00:00 INFO [LIITOS]: 1/3) lualatex --shell-escape this.tex ...
2023-01-14T20:18:20.550427+00:00 INFO [LIITOS]: latex-to-pdf(1/3): This is LuaHBTeX, Version 1.15.0 (TeX Live 2022)
2023-01-14T20:18:20.550631+00:00 INFO [LIITOS]: latex-to-pdf(1/3):  system commands enabled.
2023-01-14T20:18:20.569311+00:00 INFO [LIITOS]: latex-to-pdf(1/3): (./this.tex
2023-01-14T20:18:20.569365+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX2e <2022-11-01> patch level 1
2023-01-14T20:18:20.704883+00:00 INFO [LIITOS]: latex-to-pdf(1/3):  L3 programming layer <2022-12-17> (./setup.tex
2023-01-14T20:18:20.705367+00:00 INFO [LIITOS]: latex-to-pdf(1/3): Document Class: scrartcl 2022/10/12 v3.38 KOMA-Script document class (article)
2023-01-14T20:18:21.120313+00:00 INFO [LIITOS]: latex-to-pdf(1/3): For additional information on amsmath, use the `?' option.
2023-01-14T20:18:21.647374+00:00 INFO [LIITOS]: latex-to-pdf(1/3): === Package selnolig, Version 0.302, Date 2015/10/26 ===
2023-01-14T20:18:21.665763+00:00 INFO [LIITOS]: latex-to-pdf(1/3): ex.sty)) (./metadata.tex)
2023-01-14T20:18:21.929201+00:00 INFO [LIITOS]: latex-to-pdf(1/3): (./this.aux (./bookmatter.aux) (./publisher.aux) (./document.aux
2023-01-14T20:18:21.929264+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX Warning: Label `fig:blue' multiply defined.
2023-01-14T20:18:21.929286+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX Warning: Label `fig:blue' multiply defined.
2023-01-14T20:18:21.929302+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX Warning: Label `fig:blue' multiply defined.
2023-01-14T20:18:21.929387+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX Warning: Label `fig:red' multiply defined.
2023-01-14T20:18:22.296708+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [Loading MPS to PDF converter (version 2006.09.02).]
2023-01-14T20:18:22.304473+00:00 INFO [LIITOS]: latex-to-pdf(1/3): *geometry* driver: auto-detecting
2023-01-14T20:18:22.304508+00:00 INFO [LIITOS]: latex-to-pdf(1/3): *geometry* detected driver: luatex
2023-01-14T20:18:22.326667+00:00 INFO [LIITOS]: latex-to-pdf(1/3): (./bookmatter.tex)
2023-01-14T20:18:22.373914+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [1{/usr/local/texlive/2022/texmf-var/fonts/map/pdftex/updmap/pdftex.map}</opt/l
2023-01-14T20:18:22.380932+00:00 INFO [LIITOS]: latex-to-pdf(1/3): ogo/liitos-logo.png>] (./publisher.tex
2023-01-14T20:18:22.380976+00:00 INFO [LIITOS]: latex-to-pdf(1/3): Overfull \hbox (0.5696pt too wide) in alignment at lines 8--22
2023-01-14T20:18:22.389385+00:00 INFO [LIITOS]: latex-to-pdf(1/3): warning  (pdf backend): ignoring duplicate destination with the name 'page.1'
2023-01-14T20:18:22.423912+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [1] (./this.toc)
2023-01-14T20:18:22.440466+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [2] (./this.lof)
2023-01-14T20:18:22.451687+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [3] (./this.lot)
2023-01-14T20:18:22.480977+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [4] (./document.tex
2023-01-14T20:18:22.498534+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [5]
2023-01-14T20:18:22.517529+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [6<./images/blue.png>]
2023-01-14T20:18:22.520061+00:00 INFO [LIITOS]: latex-to-pdf(1/3): Overfull \vbox (49.07889pt too high) has occurred while \output is active
2023-01-14T20:18:22.545825+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [7]
2023-01-14T20:18:22.556033+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [8<./images/yellow.png><./images/red.png><./images/lime.png>])
2023-01-14T20:18:22.569076+00:00 INFO [LIITOS]: latex-to-pdf(1/3): [9<./diagrams/squares-and-edges.png><./diagrams/nuts-and-bolts.png>]
2023-01-14T20:18:22.573154+00:00 INFO [LIITOS]: latex-to-pdf(1/3): (./this.aux (./bookmatter.aux) (./publisher.aux) (./document.aux))
2023-01-14T20:18:22.573187+00:00 INFO [LIITOS]: latex-to-pdf(1/3): LaTeX Warning: There were multiply-defined labels.
2023-01-14T20:18:22.573463+00:00 INFO [LIITOS]: latex-to-pdf(1/3):  761 words of node memory still in use:
2023-01-14T20:18:22.573482+00:00 INFO [LIITOS]: latex-to-pdf(1/3):    7 hlist, 2 vlist, 2 rule, 1 local_par, 4 glue, 4 kern, 1 penalty, 3 glyph, 1
2023-01-14T20:18:22.573498+00:00 INFO [LIITOS]: latex-to-pdf(1/3): 5 attribute, 91 glue_spec, 10 attribute_list, 3 write, 1 user_defined nodes
2023-01-14T20:18:22.573537+00:00 INFO [LIITOS]: latex-to-pdf(1/3):    avail lists: 1:4,2:1749,3:329,4:247,5:154,6:170,7:2788,8:32,9:1367,10:3,11:1
2023-01-14T20:18:22.573552+00:00 INFO [LIITOS]: latex-to-pdf(1/3): 15,12:1
2023-01-14T20:18:22.615229+00:00 INFO [LIITOS]: latex-to-pdf(1/3): </opt/fonts/ITCFranklinGothicStd-DemiIt.otf></opt/fonts/ITCFranklinGothicStd-Bo
2023-01-14T20:18:22.624092+00:00 INFO [LIITOS]: latex-to-pdf(1/3): okIt.otf></usr/local/texlive/2022/texmf-dist/fonts/opentype/adobe/sourcecodepro
2023-01-14T20:18:22.632976+00:00 INFO [LIITOS]: latex-to-pdf(1/3): /SourceCodePro-Bold.otf></usr/local/texlive/2022/texmf-dist/fonts/opentype/adob
2023-01-14T20:18:22.641678+00:00 INFO [LIITOS]: latex-to-pdf(1/3): e/sourcecodepro/SourceCodePro-Regular.otf></opt/fonts/ITCFranklinGothicStd-Demi
2023-01-14T20:18:22.662616+00:00 INFO [LIITOS]: latex-to-pdf(1/3): .otf></opt/fonts/ITCFranklinGothicStd-Book.otf>
2023-01-14T20:18:22.662679+00:00 INFO [LIITOS]: latex-to-pdf(1/3): Output written on this.pdf (10 pages, 38989 bytes).
2023-01-14T20:18:22.671561+00:00 INFO [LIITOS]: latex-to-pdf(1/3): Transcript written on this.log.
2023-01-14T20:18:22.720400+00:00 INFO [LIITOS]: latex-to-pdf process 1/3  (['lualatex', '--shell-escape', 'this.tex']) returned 0
2023-01-14T20:18:22.720494+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:22.720516+00:00 INFO [LIITOS]: 2/3) lualatex --shell-escape this.tex ...
2023-01-14T20:18:22.985005+00:00 INFO [LIITOS]: latex-to-pdf(2/3): This is LuaHBTeX, Version 1.15.0 (TeX Live 2022)
2023-01-14T20:18:22.985282+00:00 INFO [LIITOS]: latex-to-pdf(2/3):  system commands enabled.
2023-01-14T20:18:23.001368+00:00 INFO [LIITOS]: latex-to-pdf(2/3): (./this.tex
2023-01-14T20:18:23.001437+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX2e <2022-11-01> patch level 1
2023-01-14T20:18:23.123271+00:00 INFO [LIITOS]: latex-to-pdf(2/3):  L3 programming layer <2022-12-17> (./setup.tex
2023-01-14T20:18:23.123550+00:00 INFO [LIITOS]: latex-to-pdf(2/3): Document Class: scrartcl 2022/10/12 v3.38 KOMA-Script document class (article)
2023-01-14T20:18:23.523483+00:00 INFO [LIITOS]: latex-to-pdf(2/3): For additional information on amsmath, use the `?' option.
2023-01-14T20:18:24.023919+00:00 INFO [LIITOS]: latex-to-pdf(2/3): === Package selnolig, Version 0.302, Date 2015/10/26 ===
2023-01-14T20:18:24.040065+00:00 INFO [LIITOS]: latex-to-pdf(2/3): ex.sty)) (./metadata.tex)
2023-01-14T20:18:24.299119+00:00 INFO [LIITOS]: latex-to-pdf(2/3): (./this.aux (./bookmatter.aux) (./publisher.aux) (./document.aux
2023-01-14T20:18:24.299244+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX Warning: Label `fig:blue' multiply defined.
2023-01-14T20:18:24.299264+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX Warning: Label `fig:blue' multiply defined.
2023-01-14T20:18:24.299279+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX Warning: Label `fig:blue' multiply defined.
2023-01-14T20:18:24.299293+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX Warning: Label `fig:red' multiply defined.
2023-01-14T20:18:24.661373+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [Loading MPS to PDF converter (version 2006.09.02).]
2023-01-14T20:18:24.668479+00:00 INFO [LIITOS]: latex-to-pdf(2/3): *geometry* driver: auto-detecting
2023-01-14T20:18:24.668507+00:00 INFO [LIITOS]: latex-to-pdf(2/3): *geometry* detected driver: luatex
2023-01-14T20:18:24.689784+00:00 INFO [LIITOS]: latex-to-pdf(2/3): (./bookmatter.tex)
2023-01-14T20:18:24.735927+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [1{/usr/local/texlive/2022/texmf-var/fonts/map/pdftex/updmap/pdftex.map}</opt/l
2023-01-14T20:18:24.743082+00:00 INFO [LIITOS]: latex-to-pdf(2/3): ogo/liitos-logo.png>] (./publisher.tex
2023-01-14T20:18:24.743126+00:00 INFO [LIITOS]: latex-to-pdf(2/3): Overfull \hbox (0.5696pt too wide) in alignment at lines 8--22
2023-01-14T20:18:24.751757+00:00 INFO [LIITOS]: latex-to-pdf(2/3): warning  (pdf backend): ignoring duplicate destination with the name 'page.1'
2023-01-14T20:18:24.786750+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [1] (./this.toc)
2023-01-14T20:18:24.803135+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [2] (./this.lof)
2023-01-14T20:18:24.814409+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [3] (./this.lot)
2023-01-14T20:18:24.843266+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [4] (./document.tex
2023-01-14T20:18:24.861484+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [5]
2023-01-14T20:18:24.880990+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [6<./images/blue.png>]
2023-01-14T20:18:24.883616+00:00 INFO [LIITOS]: latex-to-pdf(2/3): Overfull \vbox (49.07889pt too high) has occurred while \output is active
2023-01-14T20:18:24.909444+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [7]
2023-01-14T20:18:24.919702+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [8<./images/yellow.png><./images/red.png><./images/lime.png>])
2023-01-14T20:18:24.932963+00:00 INFO [LIITOS]: latex-to-pdf(2/3): [9<./diagrams/squares-and-edges.png><./diagrams/nuts-and-bolts.png>]
2023-01-14T20:18:24.937159+00:00 INFO [LIITOS]: latex-to-pdf(2/3): (./this.aux (./bookmatter.aux) (./publisher.aux) (./document.aux))
2023-01-14T20:18:24.937207+00:00 INFO [LIITOS]: latex-to-pdf(2/3): LaTeX Warning: There were multiply-defined labels.
2023-01-14T20:18:24.937536+00:00 INFO [LIITOS]: latex-to-pdf(2/3):  761 words of node memory still in use:
2023-01-14T20:18:24.937558+00:00 INFO [LIITOS]: latex-to-pdf(2/3):    7 hlist, 2 vlist, 2 rule, 1 local_par, 4 glue, 4 kern, 1 penalty, 3 glyph, 1
2023-01-14T20:18:24.937577+00:00 INFO [LIITOS]: latex-to-pdf(2/3): 5 attribute, 91 glue_spec, 10 attribute_list, 3 write, 1 user_defined nodes
2023-01-14T20:18:24.937645+00:00 INFO [LIITOS]: latex-to-pdf(2/3):    avail lists: 1:4,2:1749,3:329,4:247,5:154,6:170,7:2788,8:32,9:1367,10:3,11:1
2023-01-14T20:18:24.937677+00:00 INFO [LIITOS]: latex-to-pdf(2/3): 15,12:1
2023-01-14T20:18:24.977604+00:00 INFO [LIITOS]: latex-to-pdf(2/3): </opt/fonts/ITCFranklinGothicStd-DemiIt.otf></opt/fonts/ITCFranklinGothicStd-Bo
2023-01-14T20:18:24.985765+00:00 INFO [LIITOS]: latex-to-pdf(2/3): okIt.otf></usr/local/texlive/2022/texmf-dist/fonts/opentype/adobe/sourcecodepro
2023-01-14T20:18:24.993943+00:00 INFO [LIITOS]: latex-to-pdf(2/3): /SourceCodePro-Bold.otf></usr/local/texlive/2022/texmf-dist/fonts/opentype/adob
2023-01-14T20:18:25.002207+00:00 INFO [LIITOS]: latex-to-pdf(2/3): e/sourcecodepro/SourceCodePro-Regular.otf></opt/fonts/ITCFranklinGothicStd-Demi
2023-01-14T20:18:25.022640+00:00 INFO [LIITOS]: latex-to-pdf(2/3): .otf></opt/fonts/ITCFranklinGothicStd-Book.otf>
2023-01-14T20:18:25.022705+00:00 INFO [LIITOS]: latex-to-pdf(2/3): Output written on this.pdf (10 pages, 38989 bytes).
2023-01-14T20:18:25.033040+00:00 INFO [LIITOS]: latex-to-pdf(2/3): Transcript written on this.log.
2023-01-14T20:18:25.079664+00:00 INFO [LIITOS]: latex-to-pdf process 2/3  (['lualatex', '--shell-escape', 'this.tex']) returned 0
2023-01-14T20:18:25.079740+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:25.079765+00:00 INFO [LIITOS]: 3/3) lualatex --shell-escape this.tex ...
2023-01-14T20:18:25.341849+00:00 INFO [LIITOS]: latex-to-pdf(3/3): This is LuaHBTeX, Version 1.15.0 (TeX Live 2022)
2023-01-14T20:18:25.342110+00:00 INFO [LIITOS]: latex-to-pdf(3/3):  system commands enabled.
2023-01-14T20:18:25.358092+00:00 INFO [LIITOS]: latex-to-pdf(3/3): (./this.tex
2023-01-14T20:18:25.358169+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX2e <2022-11-01> patch level 1
2023-01-14T20:18:25.481362+00:00 INFO [LIITOS]: latex-to-pdf(3/3):  L3 programming layer <2022-12-17> (./setup.tex
2023-01-14T20:18:25.481617+00:00 INFO [LIITOS]: latex-to-pdf(3/3): Document Class: scrartcl 2022/10/12 v3.38 KOMA-Script document class (article)
2023-01-14T20:18:25.883985+00:00 INFO [LIITOS]: latex-to-pdf(3/3): For additional information on amsmath, use the `?' option.
2023-01-14T20:18:26.387780+00:00 INFO [LIITOS]: latex-to-pdf(3/3): === Package selnolig, Version 0.302, Date 2015/10/26 ===
2023-01-14T20:18:26.404510+00:00 INFO [LIITOS]: latex-to-pdf(3/3): ex.sty)) (./metadata.tex)
2023-01-14T20:18:26.661984+00:00 INFO [LIITOS]: latex-to-pdf(3/3): (./this.aux (./bookmatter.aux) (./publisher.aux) (./document.aux
2023-01-14T20:18:26.662049+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX Warning: Label `fig:blue' multiply defined.
2023-01-14T20:18:26.662070+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX Warning: Label `fig:blue' multiply defined.
2023-01-14T20:18:26.662087+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX Warning: Label `fig:blue' multiply defined.
2023-01-14T20:18:26.662165+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX Warning: Label `fig:red' multiply defined.
2023-01-14T20:18:27.025538+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [Loading MPS to PDF converter (version 2006.09.02).]
2023-01-14T20:18:27.032916+00:00 INFO [LIITOS]: latex-to-pdf(3/3): *geometry* driver: auto-detecting
2023-01-14T20:18:27.032953+00:00 INFO [LIITOS]: latex-to-pdf(3/3): *geometry* detected driver: luatex
2023-01-14T20:18:27.054317+00:00 INFO [LIITOS]: latex-to-pdf(3/3): (./bookmatter.tex)
2023-01-14T20:18:27.099607+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [1{/usr/local/texlive/2022/texmf-var/fonts/map/pdftex/updmap/pdftex.map}</opt/l
2023-01-14T20:18:27.106751+00:00 INFO [LIITOS]: latex-to-pdf(3/3): ogo/liitos-logo.png>] (./publisher.tex
2023-01-14T20:18:27.106797+00:00 INFO [LIITOS]: latex-to-pdf(3/3): Overfull \hbox (0.5696pt too wide) in alignment at lines 8--22
2023-01-14T20:18:27.115260+00:00 INFO [LIITOS]: latex-to-pdf(3/3): warning  (pdf backend): ignoring duplicate destination with the name 'page.1'
2023-01-14T20:18:27.150095+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [1] (./this.toc)
2023-01-14T20:18:27.166949+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [2] (./this.lof)
2023-01-14T20:18:27.178437+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [3] (./this.lot)
2023-01-14T20:18:27.207966+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [4] (./document.tex
2023-01-14T20:18:27.226122+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [5]
2023-01-14T20:18:27.245564+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [6<./images/blue.png>]
2023-01-14T20:18:27.248136+00:00 INFO [LIITOS]: latex-to-pdf(3/3): Overfull \vbox (49.07889pt too high) has occurred while \output is active
2023-01-14T20:18:27.274123+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [7]
2023-01-14T20:18:27.284507+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [8<./images/yellow.png><./images/red.png><./images/lime.png>])
2023-01-14T20:18:27.298114+00:00 INFO [LIITOS]: latex-to-pdf(3/3): [9<./diagrams/squares-and-edges.png><./diagrams/nuts-and-bolts.png>]
2023-01-14T20:18:27.302263+00:00 INFO [LIITOS]: latex-to-pdf(3/3): (./this.aux (./bookmatter.aux) (./publisher.aux) (./document.aux))
2023-01-14T20:18:27.302289+00:00 INFO [LIITOS]: latex-to-pdf(3/3): LaTeX Warning: There were multiply-defined labels.
2023-01-14T20:18:27.302574+00:00 INFO [LIITOS]: latex-to-pdf(3/3):  761 words of node memory still in use:
2023-01-14T20:18:27.302593+00:00 INFO [LIITOS]: latex-to-pdf(3/3):    7 hlist, 2 vlist, 2 rule, 1 local_par, 4 glue, 4 kern, 1 penalty, 3 glyph, 1
2023-01-14T20:18:27.302607+00:00 INFO [LIITOS]: latex-to-pdf(3/3): 5 attribute, 91 glue_spec, 10 attribute_list, 3 write, 1 user_defined nodes
2023-01-14T20:18:27.302651+00:00 INFO [LIITOS]: latex-to-pdf(3/3):    avail lists: 1:4,2:1749,3:329,4:247,5:154,6:170,7:2788,8:32,9:1367,10:3,11:1
2023-01-14T20:18:27.302680+00:00 INFO [LIITOS]: latex-to-pdf(3/3): 15,12:1
2023-01-14T20:18:27.342674+00:00 INFO [LIITOS]: latex-to-pdf(3/3): </opt/fonts/ITCFranklinGothicStd-DemiIt.otf></opt/fonts/ITCFranklinGothicStd-Bo
2023-01-14T20:18:27.351319+00:00 INFO [LIITOS]: latex-to-pdf(3/3): okIt.otf></usr/local/texlive/2022/texmf-dist/fonts/opentype/adobe/sourcecodepro
2023-01-14T20:18:27.359631+00:00 INFO [LIITOS]: latex-to-pdf(3/3): /SourceCodePro-Bold.otf></usr/local/texlive/2022/texmf-dist/fonts/opentype/adob
2023-01-14T20:18:27.367755+00:00 INFO [LIITOS]: latex-to-pdf(3/3): e/sourcecodepro/SourceCodePro-Regular.otf></opt/fonts/ITCFranklinGothicStd-Demi
2023-01-14T20:18:27.387700+00:00 INFO [LIITOS]: latex-to-pdf(3/3): .otf></opt/fonts/ITCFranklinGothicStd-Book.otf>
2023-01-14T20:18:27.387748+00:00 INFO [LIITOS]: latex-to-pdf(3/3): Output written on this.pdf (10 pages, 38989 bytes).
2023-01-14T20:18:27.396369+00:00 INFO [LIITOS]: latex-to-pdf(3/3): Transcript written on this.log.
2023-01-14T20:18:27.443494+00:00 INFO [LIITOS]: latex-to-pdf process 3/3  (['lualatex', '--shell-escape', 'this.tex']) returned 0
2023-01-14T20:18:27.443584+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:27.443605+00:00 INFO [LIITOS]: Moving stuff around (result phase) ...
2023-01-14T20:18:27.453248+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:27.453296+00:00 INFO [LIITOS]: Deliverable taxonomy: ...
2023-01-14T20:18:27.536933+00:00 INFO [LIITOS]: - Writing render/pdf folder taxonomy to inventory.json ...
2023-01-14T20:18:27.538157+00:00 INFO [LIITOS]: - Ephemeral:
2023-01-14T20:18:27.538185+00:00 INFO [LIITOS]:   + name: index.pdf
2023-01-14T20:18:27.538203+00:00 INFO [LIITOS]:   + size: 38989 bytes
2023-01-14T20:18:27.538216+00:00 INFO [LIITOS]:   + date: 2023-01-14 20:18:27.453237 +00:00
2023-01-14T20:18:27.538229+00:00 INFO [LIITOS]: - Characteristic:
2023-01-14T20:18:27.538241+00:00 INFO [LIITOS]:   + Checksums:
2023-01-14T20:18:27.538254+00:00 INFO [LIITOS]:     sha512:ec9515f28732eed2cb81d9e4438fa97bb0c3888d8552fbab642fcfbbe269a881028f495e5943385bd13e55ca7cea6cc9ba73e1ffd22b8708e61f53da8f1f2ff5
2023-01-14T20:18:27.538267+00:00 INFO [LIITOS]:     sha256:ab98984be693c5a4749a07f4bc999a4a016e16077195d50ade2ef11d181ae524
2023-01-14T20:18:27.538279+00:00 INFO [LIITOS]:       sha1:180bc217a5a1c54ab03f8f602999bdbf29acab3b
2023-01-14T20:18:27.538291+00:00 INFO [LIITOS]:        md5:c13e312e4c00d800f3d5c191633ca860
2023-01-14T20:18:27.538304+00:00 INFO [LIITOS]:   + Fonts:
2023-01-14T20:18:27.556105+00:00 INFO [LIITOS]:     pdffonts: name                                 type              encoding         emb sub uni object ID
2023-01-14T20:18:27.556305+00:00 INFO [LIITOS]:     pdffonts: ------------------------------------ ----------------- ---------------- --- --- --- ---------
2023-01-14T20:18:27.556326+00:00 INFO [LIITOS]:     pdffonts: HOLKEB+ITCFranklinGothicStd-Book     CID Type 0C       Identity-H       yes yes yes      8  0
2023-01-14T20:18:27.556341+00:00 INFO [LIITOS]:     pdffonts: YBVCAA+ITCFranklinGothicStd-Demi     CID Type 0C       Identity-H       yes yes yes      9  0
2023-01-14T20:18:27.556356+00:00 INFO [LIITOS]:     pdffonts: OKMRSZ+SourceCodePro-Regular         CID Type 0C       Identity-H       yes yes yes     94  0
2023-01-14T20:18:27.556370+00:00 INFO [LIITOS]:     pdffonts: NASXML+SourceCodePro-Bold            CID Type 0C       Identity-H       yes yes yes     95  0
2023-01-14T20:18:27.556383+00:00 INFO [LIITOS]:     pdffonts: GVLGTU+ITCFranklinGothicStd-BookIt   CID Type 0C       Identity-H       yes yes yes    125  0
2023-01-14T20:18:27.556396+00:00 INFO [LIITOS]:     pdffonts: FZOXSG+ITCFranklinGothicStd-DemiIt   CID Type 0C       Identity-H       yes yes yes    126  0
2023-01-14T20:18:27.556447+00:00 INFO [LIITOS]: pdffonts process (['pdffonts', '../index.pdf']) returned 0
2023-01-14T20:18:27.556480+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:27.556496+00:00 INFO [LIITOS]: done.
2023-01-14T20:18:27.556510+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-14T20:18:27.556663+00:00 INFO [LIITOS]: End timestamp (2023-01-14 20:18:27.556598 UTC)
2023-01-14T20:18:27.556687+00:00 INFO [LIITOS]: Rendered prod_kind document for deep at ../../ in 9.466275 secs
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
- author: Another Author
  date: 01 DEC 2022
  issue: '01'
  summary: Initial Issue
- author: An Author
  date: PUBLICATIONDATE
  issue: '01'
  revision: '01'
  summary: Fixed some nit
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
in the example `deep` provide most known keys to demonstrate the features:

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
    revision: '01'
    header_date: 17 JAN 2023
    header_issue_revision_combined: null
    footer_frame_note: VERY CONSEQUENTIAL
    footer_page_number_prefix: Page
    change_log_issue_label: Iss.
    change_log_revision_label: Rev.
    change_log_date_label: Date
    change_log_author_label: Author
    change_log_description_label: Description
    approvals_adjustable_vertical_space: '0.5em'
    approvals_role_label: Approvals
    approvals_name_label: Name
    approvals_date_and_signature_label: Date and Signature
    proprietary_information: /opt/legal/proprietary_information.txt
    toc_level: 2
    list_of_figures: '%'  # empty string to enable lof
    list_of_tables: '%'  # empty string to enable lot
    font_path: /opt/fonts/
    font_suffix: .otf
    bold_font: ITCFranklinGothicStd-Demi  # Vollkorn-SemiBold
    italic_font: ITCFranklinGothicStd-BookIt  # Vollkorn-Italic
    bold_italic_font: ITCFranklinGothicStd-DemiIt  # Vollkorn-SemiBoldItalic
    main_font: ITCFranklinGothicStd-Book  # Vollkorn-Regular
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

The eject command when used to produce a `meta-base.yml` template provides all known keys:

```console
❯ liitos eject meta-base
---
document:
  common:
    title: null
    header_title: null
    sub_title: ' '
    header_type: Engineering Document
    header_id_show: true
    header_id: null
    header_id_label: 'Doc. ID:'
    issue: '01'
    revision: '00'
    header_issue_revision_combined_show: true
    header_issue_revision_combined: null
    header_issue_revision_combined_label: 'Issue, Revision:'
    header_date_enable_auto: true
    header_date_show: true
    header_date: null
    header_date_label: 'Date:'
    footer_frame_note: null
    footer_page_number_prefix: Page
    change_log_issue_label: Iss.
    change_log_revision_label: Rev.
    change_log_date_label: Date
    change_log_author_label: Author
    change_log_description_label: Description
    approvals_adjustable_vertical_space: '2.5em'
    approvals_role_label: Approvals
    approvals_name_label: Name
    approvals_date_and_signature_label: Date and Signature
    proprietary_information: /opt/legal/proprietary-information.txt
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

### Adding Options to Descriptions

The definition lists are mapped to description environments in LaTeX for PDF generation.

In case the description texts of the items shall share a common indent of say `6em`,
then one can inject the following command into the markdown preceding the definition list it shall apply to
2(taken from `example/deep/1.md`):

```markdown
## References

\option[style=multiline,leftmargin=6em]

\[CODE-A]
:    A book, a manuscript, and all that, 2021, City, Country, URL=<https://example.com/code-a>

\[CODE-C]
:    A Cook, a manuscript, and all that, 2022, City, Country, URL=<https://example.com/code-c>

\[CODE-BIT-LONG]
:    A bit, a manuscript, and all that, 2023, City, Country, URL=<https://example.com/code-bit-long>

```

This maps to the following LaTeX code:

```latex
\hypertarget{references}{%
\subsection{References}\label{references}}


\begin{description}[style=multiline,leftmargin=6em]
\tightlist
\item[{[}CODE-A{]}]
A book, a manuscript, and all that, 2021, City, Country,
URL=\url{https://example.com/code-a}
\item[{[}CODE-C{]}]
A Cook, a manuscript, and all that, 2022, City, Country,
URL=\url{https://example.com/code-c}
\item[{[}CODE-BIT-LONG{]}]
A bit, a manuscript, and all that, 2023, City, Country,
URL=\url{https://example.com/code-bit-long}
\end{description}
```

A typical indication in the log can be (again working on the `example/deep` document):

```console
# ... - - - 8< - - -  ...
2023-01-22T20:28:36.525269+00:00 INFO [LIITOS]: add options to descriptions (definition lists) ...
2023-01-22T20:28:36.525409+00:00 INFO [LIITOS]: trigger an option mod for the next description environment at line #169|\option[style=multiline,leftmargin=6em]
2023-01-22T20:28:36.525427+00:00 INFO [LIITOS]: - found the option target start at line #171|\begin{description}
2023-01-22T20:28:36.527933+00:00 INFO [LIITOS]: diff of the (inject-description-options) filter result:
2023-01-22T20:28:36.527953+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
2023-01-22T20:28:36.528136+00:00 INFO [LIITOS]: --- before
2023-01-22T20:28:36.528154+00:00 INFO [LIITOS]: +++ after
2023-01-22T20:28:36.528171+00:00 INFO [LIITOS]: @@ -166,9 +166,8 @@
2023-01-22T20:28:36.528186+00:00 INFO [LIITOS]:  \hypertarget{references}{%
2023-01-22T20:28:36.528201+00:00 INFO [LIITOS]:  \subsection{References}\label{references}}
2023-01-22T20:28:36.528216+00:00 INFO [LIITOS]:
2023-01-22T20:28:36.528230+00:00 INFO [LIITOS]: -\option[style=multiline,leftmargin=6em]
2023-01-22T20:28:36.528245+00:00 INFO [LIITOS]: -
2023-01-22T20:28:36.528259+00:00 INFO [LIITOS]: -\begin{description}
2023-01-22T20:28:36.528274+00:00 INFO [LIITOS]: +
2023-01-22T20:28:36.528289+00:00 INFO [LIITOS]: +\begin{description}[style=multiline,leftmargin=6em]
2023-01-22T20:28:36.528303+00:00 INFO [LIITOS]:  \tightlist
2023-01-22T20:28:36.528318+00:00 INFO [LIITOS]:  \item[{[}CODE-A{]}]
2023-01-22T20:28:36.528332+00:00 INFO [LIITOS]:  A book, a manuscript, and all that, 2021, City, Country,
2023-01-22T20:28:36.528350+00:00 INFO [LIITOS]: - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ... - - - 8< - - -  ...
```

Note: When reference texts are too log to fit a line some words may be hyphenated and (esp. when dashes found
inside such terms) broken across lines. To avoid that, you can break the line in the markdown source before that term
and append `\hfill \break` at the end of that line. Replacing say `LONG-TERM` with `\mbox{LONG-TERM}` also shields
against linebreaks cutting the term, but may cause "badness" (the term may well stick out the page to the right).
