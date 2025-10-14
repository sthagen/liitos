# Changes

2025.10.14
:    Accepting a space or equal sign for scale and columns commands (#84 and #85)

2025.10.7
:    Fixed import with non-local image references

2025.9.21
:    Added asset teleportation race and incoherent math in caption detectors
- detect and avoid attenmpts to move a non-existing source to a target
- detect and warn about probably unwanted undescores and carets in captions (outside of math mode)
- increased test coverage

2025.8.31
:    Added media overwrite warnings and provide enhanced logs on error from buffer even in quiet mode
- added media overwrite warnings on concat collection and format conversion of visuals
- enforced long lines in lualatex logs to keep context (<https://todo.sr.ht/~sthagen/liitos/83>)
- enhanced logging to backtrack to a log buffer on error when in quiet mode

2025.8.30
:    Added force mode and faster skip for render-false else

2025.8.11
:    Lush Life edition - added phantom dependency and bumped some other dependencies

2025.8.9
:    Fixed the VCS probing function, extended the report query set, and suppressed a noisy error log corner case
- the vcs_probe function failed to detect repositories when executed in a branch with no commit yet
- amended the returned information in non-detect cases and promoted the log level to warning to increase visibility
- moved the noisy missing adjustment parameter log event from error to debug as it occurred when users di not use changes data at all
- some users have problems with the always brittle mermaid-filter, so they should use --filters ' ' (space enclosed by quotes) to not filter when no mermaid code blocks are in the source documents
- to further help such users (when they do have mermaid fenced blocks), the report function was amended with some checks
- a check for pandoc-filter javascript module has been added, as this is a dependency of the currently default mermaid-filter module
- another check has been added for puppeteer javascript module, because this is a dependency of the SVG to PNG filter we use
- platform information on machine, os, python version and user directories has also been added to the report function

2025.6.28
:    Adapted to pandoc 3.7.0.2, made quiet the new default, and removed JSON format support of approvals and changes
- fixed #81: The upstream pandoc version 3.7.0.2 mandates changes
- implemented #82: Remove chatter from info log level or provide a quiet mode
- implemented #80: Remove legacy JSON formats for changes and approvals

2025.1.5
:    Added tests, fixed corner cases, fixed small bugs, and corrected wording in log messages
- a work around a test failure since long time has been fixed for real
- adapted the render module to share responsibility for asset folder creation
- added doc_base argument to allow set of the effective doc base
- added doctest execution to all test runs
- added doctests
- added sad path fixtures
- added some default parameters for better testability
- added some guards and additional failure path logging around asset handling
- bumped license year
- changed the return codes in load to make the error reason explicit in tests and code examples
- enhanced meta module and added doctests 
- fixed failed CPSR-coding in meta module
- fixed test (removed bad work around)
- handled a corner case and removed tautology
- made the images and diagrams folder creation lazy
- migrated to enums for modus operandi in several modules
- refactored captions, description lists, figures, meta modules
- removed copy of meta loader function in concat and added import instead
- removed unreachable code
- removed unused code from concat module
- renamed function from *.process_meta to meta.load
- replaced a placeholder in a docstring
- replaced use of pkg_resources - untested
- reworded missing to not set in meta parser logs

2024.11.25
:    Fixed digital signature fields for south layout of approvals table (<https://todo.sr.ht/~sthagen/liitos/79>)

2024.11.24
:    Added PDF signature block insertion capability (<https://todo.sr.ht/~sthagen/liitos/78>)

2024.11.10
:    Enable dtable uglification and fixed mermaid derived figure environments
- Enabled shading the header cell background in uglified tables (<https://todo.sr.ht/~sthagen/liitos/75>)
- Enabled table uglification also for unscaled tables (<https://todo.sr.ht/~sthagen/liitos/74>)
- Fixed injection of blank lines in mermaid derived figure environments (<https://todo.sr.ht/~sthagen/liitos/56>)
- Restored uglification of tables as a meta option (<https://todo.sr.ht/~sthagen/liitos/73>)

2024.11.6
:    Eased debug of patch chains for authors and enabled choice of table caption placement
- Added a patch backup file counter to ease debug for authors (<https://todo.sr.ht/~sthagen/liitos/72>)
- Added an option to place table captions above or below the table foot (<https://todo.sr.ht/~sthagen/liitos/71>)

2024.10.29
:    Fixed inconsistent font weight for level 5 headings / subparagraphs (<https://todo.sr.ht/~sthagen/liitos/70>)

2024.10.23
:    Fixed the footer run-ins of text from body (<https://todo.sr.ht/~sthagen/liitos/69>)

2024.10.9
:    Changed and extended approvals strategies and fixed a regression in legacy channels
- Added approvals strategy parameter to configuration (feature)
- Changed default layouts and amended approvals and changes data processing (breaking changes)
- Fixed legacy channels to survive newer options (regression)

2024.10.8
:    Enabled a logo slot for first page only (<https://todo.sr.ht/~sthagen/liitos/65>)

2024.10.7
:    Fixed the runtime handling of templates feature and removed the eager logging on env read in init

2024.10.6
:    Implemented runtime handling of templates per configuration overwriting environment paths

2024.10.3
:    
- Enhanced support for use of ejected / customized layouts
- Provided detection of version semantics in changes data

2024.9.29
:    
- Enabled bold dotted lines for sections in table of contents (<https://todo.sr.ht/~sthagen/liitos/64>)
- Implemented normal font weight of level 3+ headings (<https://todo.sr.ht/~sthagen/liitos/63>)

2024.7.15
:    
- Enabled the labeling bridge in the absence of a git repo
- Fixed failing make test with a little hammer
- Reduced error level to info for a special case handled well

2024.7.14
:    
- Added regression test example for mermaid figures
- Fixed mermaid figure regression
- Migrated to all pandoc bounded figure patching

2024.7.9
:    Fixed the image distortion regression

2024.7.7
:    
- Added parsing and setup code for pandoc 3.2.1+
- Added some user wishes
- Introduced new anonymized cnages layout

2024.6.18
:    
- Added new layout to the approvals table (WIP)
- Added upper case transformer to TOC (WIP)
- Fixed bug in toc_all_dots implementation

2024.6.17
:    
- Enabled list of x left indent
- Enabled set of stretch (mostly for text and tables)
- Enabled toc al dots

2024.2.13
:    
- Enabled TOC indent reduction also for level 4 sections (<https://todo.sr.ht/~sthagen/liitos/59>)
- Enabled vertical after skip compression also for level 3 and 4 headings (<https://todo.sr.ht/~sthagen/liitos/58>)

2024.2.12
:    
- Adjusted indent and number width for the most used section levels in toc
- Reduced after skip vertical separation from section title to start of text

2024.2.11
:    Intermediate case changes on bookmark case for changes, blurb, and toc

2024.1.22
:    Hotfix adding the placeholder resources to the published package

2024.1.21
:    
- Activated the new per person orga field to approvals
- Enabled placeholder manager to replace missing JPG, PNG, SVG resource among others
- Fixed and extended command line interface

2024.1.20
:    Removed extra bold typing of main title for title page

2024.1.19
:    Enabled eastward approvals table(s)

2024.1.18
:    Added feature flag and eastward spike

2024.1.17
:    
- Changed page numbering to start on title page (breaking change)
- Refactored approvals module

2024.1.16
:    
- Added context discovery (builder node id, source hash, and source hint) yielding coordinates in place and time
- Experimental change to centered and upper-cased fake section titles on publisher page (eject template to revert)
- Fixed the incoming markdown documents tree display
- Opinionated short-term change to header geometry
- Removed lower case smoothing from filter list parsing (Bugfix, as this blocked mixed case paths to filters)

2024.1.14
:    Added bookmark title parameter to override the title slug for bookmarking

## 2023

2023.11.21
:    Implemented ensure the document title bookmark is in Title Case (<https://todo.sr.ht/~sthagen/liitos/54>)

2023.11.20
:    
- Fixed remove newline commands from title for document attributes (<https://todo.sr.ht/~sthagen/liitos/53>)
- Implemented enable inject of document level title bookmark in PDF (<https://todo.sr.ht/~sthagen/liitos/49>)
- Implemented enable inject of section level changelog bookmark in PDF (<https://todo.sr.ht/~sthagen/liitos/50>)
- Implemented enable inject of section level proprietary information bookmark in PDF (<https://todo.sr.ht/~sthagen/liitos/51>)
- Implemented enable inject of section level table of contents bookmark in PDF (<https://todo.sr.ht/~sthagen/liitos/52>)

2023.11.11
:    Fixed bug in label injector where figure parsing leaves out log points (<https://todo.sr.ht/~sthagen/liitos/48>)

2023.10.5
:    Fixed inconsistent default for header date - now default is empty and not the current date as value

2023.10.4
:    Changed some defaults to minimize noise in meta files

2023.10.3
:    Added some vertical space tuning parameters

2023.6.25
:    
- Enabled page x / y option in footers or any other outer footer value (<https://todo.sr.ht/~sthagen/liitos/46>)
- Fixed the impact of the upstream sans titles behavior change (<https://todo.sr.ht/~sthagen/liitos/44>)

2023.6.22
:    
- Adapted example to show how to enable line break hints in title like data (<https://todo.sr.ht/~sthagen/liitos/34>) and how to achieve an empty subtitle
- Backported package to python 3.9 (<https://todo.sr.ht/~sthagen/liitos/43>)
- Fixed the filter argument parsing to allow no filter at all (<https://todo.sr.ht/~sthagen/liitos/42>)
- Fixed the log level for adjusted pushdown value set (<https://todo.sr.ht/~sthagen/liitos/41>)

2023.6.17
:    
- Enabled control over showing approvals, changes, and notices (<https://todo.sr.ht/~sthagen/liitos/39>)
- Moved SBOM noise into folder and added SPDX SBOM (derived) in multiple file formats

2023.5.13
:    Templates: ensure horizontal header lines for title page are of same length as in other header (<https://todo.sr.ht/~sthagen/liitos/30>)

2023.5.10
:    Feature: Finished implementation of font size environment use for tables (<https://todo.sr.ht/~sthagen/liitos/11>)

2023.5.9
:    
- Feature: Added table fontsize parser function and corresponding tests
- Fix: Make the SVG asset patching more robust (<https://todo.sr.ht/~sthagen/liitos/28>)
- Feature: Widened the author column in the change log table

2023.4.25
:    Fix: Mermaid captions not considered (<https://todo.sr.ht/~sthagen/liitos/27>)

2023.2.14
:    Fix: Restore italics as emphasis instead of underline (<https://todo.sr.ht/~sthagen/liitos/26>)

2023.2.13
:    Fix: Compare strings to strings for width manipulation (<https://todo.sr.ht/~sthagen/liitos/25>)

2023.2.12
:    
- Feature: offer an injection feature like scale command for table column widths (<https://todo.sr.ht/~sthagen/liitos/9>)
- Fix: Table patching skipped due to failed refactoring (<https://todo.sr.ht/~sthagen/liitos/24>)

2023.2.8
:    Fix: with pandoc 3+ the captions end up within the table (<https://todo.sr.ht/~sthagen/liitos/23>)

2023.2.7
:    
- Fix: consider render value in logs (<https://todo.sr.ht/~sthagen/liitos/17>)
- Performance: do not report on environment for render false (<https://todo.sr.ht/~sthagen/liitos/21>)
- Performance: move report functionality to dedicated command (<https://todo.sr.ht/~sthagen/liitos/22>)

2023.2.6
:    Feature: amended tool version reports with why and what for semantics (<https://todo.sr.ht/~sthagen/liitos/18>)

2023.2.5
:    Robustness: modified external tool delegation harness to never exit the process per uncaught exception (<https://todo.sr.ht/~sthagen/liitos/16>)

2023.2.4
:    
- Feature: Added from-format-spec and filter-cs-list parameters to extend the pandoc transformations
- Feature: Added enter log messages per function
- Fixed process render command to actually return the result codes to the parent process (some failures are now final!)
- Feature: Implemented minimal environment tool version reporting before rendering (<https://todo.sr.ht/~sthagen/liitos/14>)

2023.2.1
:    Feature: Amended setup template to embrace more pandoc version transforms for strikeout (<https://todo.sr.ht/~sthagen/liitos/15>)

2023.1.31
:    
- Feature: Added the header filtering and documented the use
- Feature: Enabled strike-out (a.k.a. strike-through) markup per the usual double tilde bracketing
- Refactoring: Replaced a print statement with a log call in patch module
- Refactoring: Wrapped all diff log loops in another newline split-level to ensure consistent prefixing

2023.1.29
:    
- Feature: Added processing of columns command (no consideration when patching tables yet)
- Feature: Documented how to remove the bold style from description list terms in usage docs

2023.1.25
:    
- Feature: Added experimental suppression of hyphenation
- Feature: Implemented an option command for opinionated table patching

2023.1.22
:    Feature: Implemented an option command handling to style descriptions (definition lists) (<https://todo.sr.ht/~sthagen/liitos/8>)

2023.1.21
:    Feature: Implemented an optional call string interface to pdf labeling (<https://todo.sr.ht/~sthagen/liitos/6>)

2023.1.17
:    
- Feature: Added parameter to adjust the vertical placement of the approvals table (<https://todo.sr.ht/~sthagen/liitos/7>)
- Feature: Enhanced changes implementation to allow a revision key (<https://todo.sr.ht/~sthagen/liitos/10>)

2023.1.14
:    
- Added total run duration to render command logging (<https://todo.sr.ht/~sthagen/liitos/4>)
- Fixed logging of locally changed repository files (<https://todo.sr.ht/~sthagen/liitos/5>)

2023.1.12
:    Implemented use of selected fonts in all elements (<https://todo.sr.ht/~sthagen/liitos/3>)

2023.1.11
:    Fixed templates packaging (<https://todo.sr.ht/~sthagen/liitos/2>)

2023.1.10
:    Added initial implementation of PDF document structure to include numbering to implement (<https://todo.sr.ht/~sthagen/liitos/1>)

## 2022

2022.12.14
:    Fixed title token in vocabulary (currently used only in packages interfacing with liitos)

2022.12.13
:    Added examples and new meta keys to support users
- Added new example for showing no date in the header
- Added new example for showing no date in the header and moving iss-rev field into that slot
- Added meta data keys to show or hide the three sub header fields coined id, iss_rev, and date
- Added workaround meta data key to disable the semantics of the header date field

2022.12.12
:    Extended logging and fixed inventory bug
- Added info to error log from image parse
- Fixed inventory (failed CPSR refactoring)

2022.12.11
:    Enhanced logging and markdown image text transformation
- Enhanced the logging
- Refactored markdown image text line rewrites for transformed images (formats)

2022.12.10
:    Fixed silent failing svg-to-png conversion target path rename per ABYL ten times and extended logging

2022.12.9
:    Fixed failing image parse cases where multiple spaces between src and alt as well as for empty caps

2022.12.8
:    
- Fixed link to CycloneDX format SBOM (the cyclonedx python package still does not find the indirect dependencies)
- Fixed transformation of relative upwards image source links
- Implemented more robust (and chatty) markdown image text line parser

2022.12.7
:    
- Added creation of inventory file as post action to the rendering
- Added diff outputs in unified format for filter steps when rendering
- Added foran (vcs) and taksonomia (taxonomy) services per dependencies
- Added vcs info to renderer
- Extended and enhanced the deep example
- Fixed specific app SVG renaming (dangling ref) and extended to any app (naive parser)

2022.12.6
:    Boosted test coverage above 80%

2022.12.5
:    
- Added eject command for templates
- Added user patching to render command
- Increased the test coverage - way to go
- Updated user documentation

2022.12.4
:    Fixed broken console script

2022.12.3
:    
- Added concat command with prototype level implementation (WIP) - works already with the example/deep prod_kind target and deep facet
- Added meta weave for partial meta data
- Added mixed processing of future simplified include strategy
- Added more timely and more precise basic validation of request versus structure
- Added template handling
- Extended changes and approvals implementation to deal with channel dependent topologies
- Migrated to treelib and streamlined intermediate logging
- Removed outdated prototype code

2022.11.3
:    Made the liitos.templates package an explicit member (YAGNI)

2022.11.2
:    
- Added meta data parsing to verifier
- Added verbosity flag

2022.10.18
:    Added YAML format readers for approvals and changes

2022.9.18
:    
- Added command line verification script
- Added documentation
- Added PyYAML dependency

2022.8.1
:    Initial release on PyPI
