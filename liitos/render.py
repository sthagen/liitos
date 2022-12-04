"""
for f in images/*.svg; do svgexport "$f" "${f%%.*}.png" 100%; done
for f in diagrams/*.svg; do svgexport "$f" "${f%%.*}.png" 100%; done
temp_md="_patched.md"
sed "s/\.drawio\.svg/.png/g;" < document.md > "${temp_md}" && mv "${temp_md}" document.md
sed "s/\.svg/.png/g;" < document.md > "${temp_md}" && mv "${temp_md}" document.md
pandoc -f markdown+link_attributes -t latex document.md -o document.tex --filter mermaid-filter
cp -a driver.tex this.tex
lualatex --shell-escape this.tex
lualatex --shell-escape this.tex
lualatex --shell-escape this.tex
"""
import os
import pathlib
import subprocess


import yaml

import liitos.gather as gat
from liitos import ENCODING, log

DOC_BASE = pathlib.Path('..', '..')
STRUCTURE_PATH = DOC_BASE / 'structure.yml'

def der(
    doc_root: str | pathlib.Path, structure_name: str, target_key: str, facet_key: str, options: dict[str, bool]
) -> int:
    """Later alligator."""
    target_code = target_key
    facet_code = facet_key
    if not facet_code.strip() or not target_code.strip():
        log.error(f'render requires non-empty target ({target_code}) and facet ({facet_code}) codes')
        return 2

    log.info(f'parsed target ({target_code}) and facet ({facet_code}) from request')

    structure, asset_map = gat.prelude(
        doc_root=doc_root, structure_name=structure_name, target_key=target_key, facet_key=facet_key, command='render'
    )
    log.info(f'prelude teleported processor into the document root at ({os.getcwd()}/)')
    rel_concat_folder_path = pathlib.Path("render/pdf/")
    rel_concat_folder_path.mkdir(parents=True, exist_ok=True)
    os.chdir(rel_concat_folder_path)
    log.info(f'render (this processor) teleported into the render/pdf location ({os.getcwd()}/)')

    if not STRUCTURE_PATH.is_file() or not STRUCTURE_PATH.stat().st_size:
        log.error(f'render failed to find non-empty structure file at {STRUCTURE_PATH}')
        return 1

    with open(STRUCTURE_PATH, 'rt', encoding=ENCODING) as handle:
        structure = yaml.safe_load(handle)

    targets = sorted(structure.keys())

    if not targets:
        log.error(f'structure at ({STRUCTURE_PATH}) does not provide any targets')
        return 1

    if target_code not in targets:
        log.error(f'structure does not provide ({target_code})')
        return 1

    if len(targets) == 1:
        target = targets[0]
        facets = sorted(list(facet.keys())[0] for facet in structure[target])
        log.info(f'found single target ({target}) with facets ({facets})')

        if facet_code not in facets:
            log.error(f'structure does not provide facet ({facet_code}) for target ({target_code})')
            return 1

        aspect_map = {}
        for data in structure[target]:
            if facet_code in data:
                aspect_map = data[facet_code]
                break
        missing_keys = [key for key in gat.KEYS_REQUIRED if key not in aspect_map]
        if missing_keys:
            log.error(
                f'structure does not provide all expected aspects {sorted(gat.KEYS_REQUIRED)}'
                f' for target ({target_code}) and facet ({facet_code})'
            )
            log.error(f'- the found aspects: {sorted(aspect_map.keys())}')
            log.error(f'- missing aspects:   {sorted(missing_keys)}')
            return 1

        do_render = aspect_map.get('render', None)
        if do_render is not None:
            log.info(f'found render instruction with value ({aspect_map["render"]})')

        if do_render is None or do_render:
            log.info(f'we will render ...')
        else:
            log.warning(f'we will not render ...')
            return 0

        log.info('transforming SVG assets to high resolution PNG bitmaps ...')
        try:
            retcode = subprocess.call("ls -lrt", shell=True)
            if retcode < 0:
                log.error(f'svg-to-png process was terminated by signal {-retcode}')
            else:
                log.info(f'svg-to-png process returned {retcode}')
        except OSError as err:
            print(f'execution of svg-to-png process failed: {err}')

        log.info('rewriting src attribute values of SVG to PNG sources ...')
        log.info('pandoc -f markdown+link_attributes -t latex document.md -o document.tex --filter mermaid-filter ...')
        log.info('cp -a driver.tex this.tex ...')
        log.info('1/3) lualatex --shell-escape this.tex ...')
        log.info('2/3) lualatex --shell-escape this.tex ...')
        log.info('3/3) lualatex --shell-escape this.tex ...')
        log.info('Moving stuff around (result phase) ...')

    return 0
