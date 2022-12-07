# Third Party Dependencies

<!--[[[fill sbom_sha256()]]]-->
The [SBOM in CycloneDX v1.4 JSON format](https://github.com/sthagen/pilli/blob/default/sbom.json) with SHA256 checksum ([c093e676 ...](https://raw.githubusercontent.com/sthagen/pilli/default/sbom.json.sha256 "sha256:c093e67608e498437b6bfeb993169d8081e7dd3f9afc57f24a8cb451c55c9126")).
<!--[[[end]]] (checksum: 069f8ca22141a5fe49886febe74e236e)-->
## Licenses 

JSON files with complete license info of: [direct dependencies](direct-dependency-licenses.json) | [all dependencies](all-dependency-licenses.json)

### Direct Dependencies

<!--[[[fill direct_dependencies_table()]]]-->
| Name                                             | Version                                                     | License                 | Author            | Description (from packaging data)                                                                                                         |
|:-------------------------------------------------|:------------------------------------------------------------|:------------------------|:------------------|:------------------------------------------------------------------------------------------------------------------------------------------|
| [PyYAML](https://pyyaml.org/)                    | [6.0](https://pypi.org/project/PyYAML/6.0/)                 | MIT License             | Kirill Simonov    | YAML parser and emitter for Python                                                                                                        |
| [treelib](https://github.com/caesar0301/treelib) | [1.6.1](https://pypi.org/project/treelib/1.6.1/)            | Apache Software License | Xiaming Chen      | A Python 2/3 implementation of tree structure.                                                                                            |
| [typer](https://github.com/tiangolo/typer)       | [0.7.0](https://pypi.org/project/typer/0.7.0/)              | MIT License             | Sebastián Ramírez | Typer, build great CLIs. Easy to code. Based on Python type hints.                                                                        |
| foran                                            | [2022.12.7](https://pypi.org/project/foran/2022.12.7/)      | MIT License             | UNKNOWN           | In front or behind (Danish: foran eller bagved)? Answering the question if a local repository status is in front of or behind its remote. |
| taksonomia                                       | [2022.9.21](https://pypi.org/project/taksonomia/2022.9.21/) | MIT License             | UNKNOWN           | Taxonomy (Finnish: taksonomia) of a folder tree, guided by conventions.                                                                   |
<!--[[[end]]] (checksum: 52ceb48160e72c813e233d9ee2b50ffa)-->

### Indirect Dependencies

<!--[[[fill indirect_dependencies_table()]]]-->
| Name                                          | Version                                        | License     | Author         | Description (from packaging data)         |
|:----------------------------------------------|:-----------------------------------------------|:------------|:---------------|:------------------------------------------|
| [click](https://palletsprojects.com/p/click/) | [8.1.3](https://pypi.org/project/click/8.1.3/) | BSD License | Armin Ronacher | Composable command line interface toolkit |
<!--[[[end]]] (checksum: dc3a866a7aa3332404bde3da87727cb9)-->

## Dependency Tree(s)

JSON file with the complete package dependency tree info of: [the full dependency tree](package-dependency-tree.json)

### Rendered SVG

Base graphviz file in dot format: [Trees of the direct dependencies](package-dependency-tree.dot.txt)

<img src="./package-dependency-tree.svg" alt="Trees of the direct dependencies" title="Trees of the direct dependencies"/>

### Console Representation

<!--[[[fill dependency_tree_console_text()]]]-->
````console
foran==2022.12.7
  - GitPython [required: >=3.1.29, installed: 3.1.29]
    - gitdb [required: >=4.0.1,<5, installed: 4.0.9]
      - smmap [required: >=3.0.1,<6, installed: 5.0.0]
  - typer [required: >=0.7.0, installed: 0.7.0]
    - click [required: >=7.1.1,<9.0.0, installed: 8.1.3]
taksonomia==2022.9.21
  - lxml [required: >=4.9.1, installed: 4.9.1]
  - orjson [required: >=3.8.0, installed: 3.8.3]
  - psutil [required: >=5.9.2, installed: 5.9.4]
  - py-cpuinfo [required: >=8.0.0, installed: 9.0.0]
  - PyYAML [required: >=6.0, installed: 6.0]
treelib==1.6.1
  - future [required: Any, installed: 0.18.2]
````
<!--[[[end]]] (checksum: e3619c290eee2e49ede02f899f6a67dc)-->
