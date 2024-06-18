# Changes

2024.6.18
:    * Added new layout to the approvals table (WIP)
* Added upper case transformer to TOC (WIP)

2024.6.17
:    * Enabled list of x left indent
* Enabled set of stretch (mostly for text and tables)
* Enabled toc al dots

2024.2.13
:    * Enabled TOC indent reduction also for level 4 sections (<https://todo.sr.ht/~sthagen/liitos/59>)
* Enabled vertical afterskip compression also for level 3 and 4 headings (<https://todo.sr.ht/~sthagen/liitos/58>)

2024.2.12
:    * Adjusted indent and numwidth for the most used section levels in toc
* Reduced afterskip vertical separation from section title to start of text

2024.2.11
:    * Intermediate case changes on bookmark case for changes, blurb, and toc

2024.1.22
:    * Hotfix adding the placeholder resources to the published package

2024.1.21
:    * Activated the new per person orga field to approvals
* Enabled placeholder manager to replace missing JPG, PNG, SVG resource among others
* Fixed and extended command line interface

2024.1.20
:    * Removed extra bold typing of main title for title page

2024.1.19
:    * Enabled eastward approvals table(s)

2024.1.18
:    * Added feature flag and eastward spike

2024.1.17
:    * Changed page numbering to start on title page (breaking change)
* Refactored approvals module

2024.1.16
:    * Added context discovery (builder node id, source hash, and source hint) yielding coordinates in place and time
* Experimental change to centered and upper-cased fake section titles on publisher page (eject template to revert)
* Fixed the incoming markdown documents tree display
* Opinionated short-term change to header geometry
* Removed lower case smoothing from filter list parsing (Bugfix, as this blocked mixed case paths to filters)

2024.1.14
:    * Added bookmark title parameter to override the title slug for bookmarking

2023.11.21
:    * Implemented ensure the document title bookmark is in Title Case (<https://todo.sr.ht/~sthagen/liitos/54>)

2023.11.20
:    * Fixed remove newline commands from title for document attributes (<https://todo.sr.ht/~sthagen/liitos/53>)
* Implemented enable inject of document level title bookmark in PDF (<https://todo.sr.ht/~sthagen/liitos/49>)
* Implemented enable inject of section level changelog bookmark in PDF (<https://todo.sr.ht/~sthagen/liitos/50>)
* Implemented enable inject of section level proprietary information bookmark in PDF (<https://todo.sr.ht/~sthagen/liitos/51>)
* Implemented enable inject of section level table of contents bookmark in PDF (<https://todo.sr.ht/~sthagen/liitos/52>)

2023.11.11
:    * Fixed bug in label injector where figure parsing leaves out log points (<https://todo.sr.ht/~sthagen/liitos/48>)

2023.10.5
:    * Fixed inconsistent default for header date - now default is empty and not the current date as value

2023.10.4
:    * Changed some defaults to minimize noise in meta files

2023.10.3
:    * Added some vertical space tuning parameters

2023.6.25
:    * Enabled page x / y option in footers or any other outer footer value (<https://todo.sr.ht/~sthagen/liitos/46>)
* Fixed the impact of the upstream sans titles behavior change (<https://todo.sr.ht/~sthagen/liitos/44>)

2023.6.22
:    * Adapted example to show how to enable line break hints in title like data (<https://todo.sr.ht/~sthagen/liitos/34>) and how to achieve an empty subtitle
* Backported package to python 3.9 (<https://todo.sr.ht/~sthagen/liitos/43>)
* Fixed the filter argument parsing to allow no filter at all (<https://todo.sr.ht/~sthagen/liitos/42>)
* Fixed the log level for adjusted pushdown value set (<https://todo.sr.ht/~sthagen/liitos/41>)

2023.6.17
:    * Enabled control over showing approvals, changes, and notices (<https://todo.sr.ht/~sthagen/liitos/39>)
* Moved SBOM noise into folder and added SPDX SBOM (derived) in multiple file formats

2023.5.13
:    * Templates: ensure horizontal header lines for title page are of same length as in other header (<https://todo.sr.ht/~sthagen/liitos/30>)

2023.5.10
:    * Feature: Finished implementation of font size environment use for tables (<https://todo.sr.ht/~sthagen/liitos/11>)

2023.5.9
:    * Feature: Added tablefontsize parser function and corresponding tests
* Fix: Make the SVG asset patching more robust (<https://todo.sr.ht/~sthagen/liitos/28>)
* Feature: Widened the author column in the change log table

2023.4.25
:    * Fix: Mermaid captions not considered (<https://todo.sr.ht/~sthagen/liitos/27>)

2023.2.14
:    * Fix: Restore italics as emphasis instead of underline (<https://todo.sr.ht/~sthagen/liitos/26>)

2023.2.13
:    * Fix: Compare strings to strings for width manipulation (<https://todo.sr.ht/~sthagen/liitos/25>)

2023.2.12
:    * Feature: offer an injection feature like scale command for table column widths (<https://todo.sr.ht/~sthagen/liitos/9>)
* Fix: Table patching skipped due to failed refactoring (<https://todo.sr.ht/~sthagen/liitos/24>)

2023.2.8
:    * Fix: with pandoc 3+ the captions end up within the table (<https://todo.sr.ht/~sthagen/liitos/23>)

2023.2.7
:    * Fix: consider render value in logs (<https://todo.sr.ht/~sthagen/liitos/17>)
* Performance: do not report on environment for render false (<https://todo.sr.ht/~sthagen/liitos/21>)
* Performance: move report functionality to dedicated command (<https://todo.sr.ht/~sthagen/liitos/22>)

2023.2.6
:    * Feature: amended tool version reports with why and what for semantics (<https://todo.sr.ht/~sthagen/liitos/18>)

2023.2.5
:    * Robustness: modified external tool delegation harness to never exit the process per uncaught exception (<https://todo.sr.ht/~sthagen/liitos/16>)

2023.2.4
:    * Feature: Added from-format-spec and filter-cs-list parameters to extend the pandoc transformations
* Feature: Added enter log messages per function
* Fixed process render command to actually return the result codes to the parent process (some failures are now final!)
* Feature: Implemented minimal environment tool version reporting before rendering (<https://todo.sr.ht/~sthagen/liitos/14>)

2023.2.1
:    * Feature: Amended setup template to embrace more pandoc version transforms for strikeout (<https://todo.sr.ht/~sthagen/liitos/15>)

2023.1.31
:    * Feature: Added the header filtering and documented the use
* Feature: Enabled strike-out (a.k.a. strike-through) markup per the usual double tilde bracketing
* Refactoring: Replaced a print statement with a log call in patch module
* Refactoring: Wrapped all diff log loops in another newline split-level to ensure consistent prefixing

2023.1.29
:    * Feature: Added processing of columns command (no consideration when patching tables yet)
* Feature: Documented how to remove the bold style from description list terms in usage docs

2023.1.25
:    * Feature: Added experimental suppression of hyphenation
* Feature: Implemented an option command for opinionated table patching

2023.1.22
:    * Feature: Implemented an option command handling to style descriptions (definition lists) (<https://todo.sr.ht/~sthagen/liitos/8>)

2023.1.21
:    * Feature: Implemented an optional call string interface to pdf labeling (<https://todo.sr.ht/~sthagen/liitos/6>)

2023.1.17
:    * Feature: Added parameter to adjust the vertical placement of the approvals table (<https://todo.sr.ht/~sthagen/liitos/7>)
* Feature: Enhanced changes implementation to allow a revision key (<https://todo.sr.ht/~sthagen/liitos/10>)

2023.1.14
:    * Added total run duration to render command logging (<https://todo.sr.ht/~sthagen/liitos/4>)
* Fixed logging of locally changed repository files (<https://todo.sr.ht/~sthagen/liitos/5>)

2023.1.12
:    * Implemented use of selected fonts in all elements (<https://todo.sr.ht/~sthagen/liitos/3>)

2023.1.11
:    * Fixed templates packaging (<https://todo.sr.ht/~sthagen/liitos/2>)

2023.1.10
:    * Added initial implementation of PDF document structure to include numbering to implement (<https://todo.sr.ht/~sthagen/liitos/1>)

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
