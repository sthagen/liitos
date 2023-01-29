# Changes

## 2023

### 2023.1.29

* Added processing of columns command (no consideration when patching tables yet)
* Documented how to remove the bold style from description list terms in usage docs

### 2023.1.25

* Added experimental suppression of hyphenation
* Implemented an option command for opinionated table patching

### 2023.1.22

* Implemented an option command handling to style descriptions (definition lists) (<https://todo.sr.ht/~sthagen/liitos/8>)

### 2023.1.21

* Implemented an optional call string interface to pdf labeling (<https://todo.sr.ht/~sthagen/liitos/6>)

### 2023.1.17

* Added parameter to adjust the vertical placement of the approvals table (<https://todo.sr.ht/~sthagen/liitos/7>)
* Enhanced changes implementation to allow a revision key (<https://todo.sr.ht/~sthagen/liitos/10>)

### 2023.1.14

* Added total run duration to render command logging (<https://todo.sr.ht/~sthagen/liitos/4>)
* Fixed logging of locally changed repository files (<https://todo.sr.ht/~sthagen/liitos/5>)

### 2023.1.12

* Implemented use of selected fonts in all elements (<https://todo.sr.ht/~sthagen/liitos/3>)

### 2023.1.11

* Fixed templates packaging (<https://todo.sr.ht/~sthagen/liitos/2>)

### 2023.1.10

* Added initial implementation of PDF document structure to include numbering to implement (<https://todo.sr.ht/~sthagen/liitos/1>)

## 2022

2022.12.14
:    * Fixed title token in vocabulary (currently used only in packages interfacing with liitos)

2022.12.13
:    * Added new example for showing no date in the header
* Added new example for showing no date in the header and moving iss-rev field into that slot
* Added meta data keys to show or hide the three sub header fields coined id, iss_rev, and date
* Added workaround meta data key to disable the semantics of the header date field

2022.12.12
:    * Added info to error log from image parse
* Fixed inventory (failed CPSR refactoring)

2022.12.11
:    * Enhanced the logging
* Refactored markdown image text line rewrites for transformed images (formats)

2022.12.10
:    * Fixed silent failing svg-to-png conversion target path rename per ABYL ten times and extended logging

2022.12.9
:    * Fixed failing image parse cases where multiple spaces between src and alt as well as for empty caps

2022.12.8
:    * Fixed link to CycloneDX format SBOM (the cyclonedx python package still does not find the indirect dependencies)
* Fixed transformation of relative upwards image source links
* Implemented more robust (and chatty) markdown image text line parser

2022.12.7
:    * Added creation of inventory file as post action to the rendering
* Added diff outputs in unified format for filter steps when rendering
* Added foran (vcs) and taksonomia (taxonomy) services per dependencies
* Added vcs info to renderer
* Extended and enhanced the deep example
* Fixed specific app SVG renaming (dangling ref) and extended to any app (naive parser)

2022.12.6
:    * Boosted test coverage above 80%

2022.12.5
:    * Added eject command for templates
* Added user patching to render command
* Increased the test coverage - way to go
* Updated user documentation

2022.12.4
:    * Fixed broken console script

2022.12.3
:    * Added concat command with prototype level implementation (WIP) - works already with the example/deep prod_kind target and deep facet
* Added meta weave for partial meta data
* Added mixed processing of future simplified include strategy
* Added more timely and more precise basic validation of request versus structure
* Added template handling
* Extended changes and approvals implementation to deal with channel dependent topologies
* Migrated to treelib and streamlined intermediate logging
* Removed outdated prototype code

2022.11.3
:    * Made the liitos.templates package an explicit member (YAGNI)

2022.11.2
:    * Added meta data parsing to verifier
* Added verbosity flag

2022.10.18
:    * Added YAML format readers for approvals and changes

2022.9.18
:    * Added command line verification script
* Added documentation
* Added PyYAML dependency

2022.8.1
:    * Initial release on PyPI
