# Changes

## 2022.12.8

* Fixed link to CycloneDX format SBOM (the cyclonedx python package still does not find the indirect dependencies)
* Fixed transformation of relative upwards image source links
* Implemented more robust (and chatty) markdown image text line parser

## 2022.12.7

* Added creation of inventory file as post action to the rendering
* Added diff outputs in unified format for filter steps when rendering
* Added foran (vcs) and taksonomia (taxonomy) services per dependencies
* Added vcs info to renderer
* Extended and enhanced the deep example
* Fixed specific app SVG renaming (dangling ref) and extended to any app (naive parser)

## 2022.12.6

* Boosted test coverage above 80%

## 2022.12.5

* Added eject command for templates
* Added user patching to render command
* Increased the test coverage - way to go
* Updated user documentation

## 2022.12.4

* Fixed broken console script

## 2022.12.3

* Added concat command with prototype level implementation (WIP) - works already with the example/deep prod_kind target and deep facet
* Added meta weave for partial meta data
* Added mixed processing of future simplified include strategy
* Added more timely and more precise basic validation of request versus structure
* Added template handling
* Extended changes and approvals implementation to deal with channel dependent topologies
* Migrated to treelib and streamlined intermediate logging
* Removed outdated prototype code

## 2022.11.3

* Made the liitos.templates package an explicit member (YAGNI)

## 2022.11.2

* Added meta data parsing to verifier
* Added verbosity flag

## 2022.10.18

* Added YAML format readers for approvals and changes

## 2022.9.18

* Added command line verification script
* Added documentation
* Added PyYAML dependency

## 2022.8.1

* Initial release on PyPI
