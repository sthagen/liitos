"""Render the concat document to pdf."""
import datetime as dti
import hashlib
import os
import pathlib
import shutil
import subprocess  # nosec B404


import yaml

import liitos.captions as cap
import liitos.figures as fig
import liitos.gather as gat
import liitos.labels as lab
import liitos.patch as pat
from liitos import ENCODING, log

DOC_BASE = pathlib.Path('..', '..')
STRUCTURE_PATH = DOC_BASE / 'structure.yml'
IMAGES_FOLDER = 'images/'
DIAGRAMS_FOLDER = 'diagrams/'
PATCH_SPEC_NAME = 'patch.yml'
CHUNK_SIZE = 2 << 15
TS_FORMAT = '%Y-%m-%d %H:%M:%S.%f +00:00'

def hash_file(path: pathlib.Path, hasher = None) -> str:
    """Return the SHA512 hex digest of the data from file."""
    if hasher is None:
        hasher = hashlib.sha512
    hash = hasher()
    with open(path, 'rb') as handle:
        while chunk := handle.read(CHUNK_SIZE):
            hash.update(chunk)
    return hash.hexdigest()


def log_subprocess_output(pipe, prefix: str):
    for line in iter(pipe.readline, b''):  # b'\n'-separated lines
        cand = line.decode(encoding=ENCODING).rstrip()
        if cand.strip().strip('[])yex'):
            if any([
                'microtype' in cand,
                'xassoccnt' in cand,
                'texlive/2022/texmf-dist/tex/' in cand,
                cand == 'erns.sty)',
                cand == '(see the transcript file for additional information)',
                cand.startswith(r'Overfull \hbox ') and cand.endswith(r'pt too wide) has occurred while \output is active')
            ]):
                log.debug(f'{prefix}: %s', cand)
            else:
                log.info(f'{prefix}: %s', cand)


def der(
    doc_root: str | pathlib.Path, structure_name: str, target_key: str, facet_key: str, options: dict[str, bool]
) -> int:
    """Later alligator."""
    separator = '- ' * 80
    log.info(separator)
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

    rel_concat_folder_path = pathlib.Path('render/pdf/')
    rel_concat_folder_path.mkdir(parents=True, exist_ok=True)

    patches = []
    need_patching = False
    patch_spec_path = pathlib.Path(PATCH_SPEC_NAME)
    log.info(f'inspecting any patch spec file ({patch_spec_path}) ...')
    if patch_spec_path.is_file() and patch_spec_path.stat().st_size:
        target_path = rel_concat_folder_path / PATCH_SPEC_NAME
        shutil.copy(patch_spec_path, target_path)
        try:
            with open(patch_spec_path, 'rt', encoding=ENCODING) as handle:
                patch_spec = yaml.safe_load(handle)
            need_patching = True
        except (OSError, UnicodeDecodeError) as err:
            log.error(f'failed to load patch spec from ({patch_spec_path}) with ({err}) - patching will be skipped')
            need_patching = False
        if need_patching:
            try:
                patches = [(rep, lace) for rep, lace in patch_spec]
                patch_pair_count = len(patches)
                if not patch_pair_count:
                    need_patching = False
                    log.warning(f'- ignoring empty patch spec')
                else:
                    log.info(
                        f'- loaded {patch_pair_count} patch pair{"" if patch_pair_count == 1 else "s"}'
                        f' from patch spec file ({patch_spec_path})'
                    )
            except ValueError as err:
                log.error(f'- failed to parse patch spec from ({patch_spec}) with ({err}) - patching will be skipped')
                need_patching = False
    else:
        if patch_spec_path.is_file():
            log.warning(f'- ignoring empty patch spec file ({patch_spec_path})')
        else:
            log.info(f'- no patch spec file ({patch_spec_path}) detected')

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

        log.info(separator)
        log.info('transforming SVG assets to high resolution PNG bitmaps ...')
        for path_to_dir in (IMAGES_FOLDER, DIAGRAMS_FOLDER):
            for svg in pathlib.Path(path_to_dir).iterdir():
                if svg.is_file() and svg.suffix == '.svg':
                    png = str(svg).replace('.svg', '.png')
                    svg_to_png_command = ['svgexport', svg,  png, '100%']
                    process = subprocess.Popen(svg_to_png_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec B603
                    with process.stdout:
                        log_subprocess_output(process.stdout, 'svg-to-png')
                    return_code = process.wait()
                    if return_code < 0:
                        log.error(
                            f'svg-to-png process ({svg_to_png_command}) was terminated by signal {-return_code}')
                    else:
                        log.info(f'svg-to-png process ({svg_to_png_command}) returned {return_code}')

        log.info(separator)
        log.info('rewriting src attribute values of SVG to PNG sources ...')
        with open('document.md', 'rt', encoding=ENCODING) as handle:
            lines = [line.rstrip() for line in handle.readlines()]
        for slot, line in enumerate(lines):
            if '.drawio.svg' in line:
                fine = line.replace('.drawio.svg', '.png')
                log.info(f'transform[#{slot + 1}]: {line}')
                log.info(f'     into[#{slot + 1}]: {fine}')
                lines[slot] = fine
                continue
            if '.svg' in line:
                fine = line.replace('.svg', '.png')
                log.info(f'transform[#{slot + 1}]: {line}')
                log.info(f'     into[#{slot + 1}]: {fine}')
                lines[slot] = fine
                continue
        with open('document.md', 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines))

        fmt_spec = 'markdown+link_attributes'
        in_doc = 'document.md'
        out_doc = 'document.tex'
        markdown_to_latex_command = [
            'pandoc', '--verbose', '-f', fmt_spec, '-t', 'latex', in_doc, '-o', out_doc, '--filter', 'mermaid-filter'
        ]
        log.info(separator)
        log.info('pandoc -f markdown+link_attributes -t latex document.md -o document.tex --filter mermaid-filter ...')
        process = subprocess.Popen(markdown_to_latex_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec B603
        with process.stdout:
            log_subprocess_output(process.stdout, 'markdown-to-latex')
        return_code = process.wait()
        if return_code < 0:
            log.error(f'markdown-to-latex process ({markdown_to_latex_command}) was terminated by signal {-return_code}')
        else:
            log.info(f'markdown-to-latex process ({markdown_to_latex_command}) returned {return_code}')

        log.info(separator)
        log.info('move any captions below tables ...')
        with open('document.tex', 'rt', encoding=ENCODING) as handle:
            lines = [line.rstrip() for line in handle.readlines()]
        doc_before_caps_patch = 'document-before-caps-patch.tex.txt'
        with open(doc_before_caps_patch, 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines))
        lines_in_pipe = cap.weave(lines)
        with open('document.tex', 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines_in_pipe))

        log.info(separator)
        log.info('inject stem (derived from file name) labels ...')
        doc_before_label_patch = 'document-before-inject-stem-label-patch.tex.txt'
        with open(doc_before_label_patch, 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines_in_pipe))
        lines_in_pipe = lab.inject(lines_in_pipe)
        with open('document.tex', 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines_in_pipe))

        log.info(separator)
        log.info('scale figures ...')
        doc_before_figures_patch = 'document-before-scale-figures-patch.tex.txt'
        with open(doc_before_figures_patch, 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines_in_pipe))
        lines_in_pipe = fig.scale(lines_in_pipe)
        with open('document.tex', 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines_in_pipe))

        if need_patching:
            log.info(separator)
            log.info('apply user patches ...')
            doc_before_user_patch = 'document-before-user-patch.tex.txt'
            with open(doc_before_user_patch, 'wt', encoding=ENCODING) as handle:
                handle.write('\n'.join(lines_in_pipe))
            lines_in_pipe = pat.apply(patches, lines_in_pipe)
            with open('document.tex', 'wt', encoding=ENCODING) as handle:
                handle.write('\n'.join(lines_in_pipe))
        else:
            log.info(separator)
            log.info('skipping application of user patches ...')

        log.info(separator)
        log.info('cp -a driver.tex this.tex ...')
        source_asset = 'driver.tex'
        target_asset = 'this.tex'
        shutil.copy(source_asset, target_asset)

        latex_to_pdf_command = ['lualatex', '--shell-escape', 'this.tex']
        log.info(separator)
        log.info('1/3) lualatex --shell-escape this.tex ...')
        process = subprocess.Popen(latex_to_pdf_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec B603
        with process.stdout:
            log_subprocess_output(process.stdout, 'latex-to-pdf(1/3)')
        return_code = process.wait()
        if return_code < 0:
            log.error(f'latex-to-pdf process 1/3 ({latex_to_pdf_command}) was terminated by signal {-return_code}')
        else:
            log.info(f'latex-to-pdf process 1/3  ({latex_to_pdf_command}) returned {return_code}')

        log.info(separator)
        log.info('2/3) lualatex --shell-escape this.tex ...')
        process = subprocess.Popen(latex_to_pdf_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec B603
        with process.stdout:
            log_subprocess_output(process.stdout, 'latex-to-pdf(2/3)')
        return_code = process.wait()
        if return_code < 0:
            log.error(f'latex-to-pdf process 2/3 ({latex_to_pdf_command}) was terminated by signal {-return_code}')
        else:
            log.info(f'latex-to-pdf process 2/3  ({latex_to_pdf_command}) returned {return_code}')

        log.info(separator)
        log.info('3/3) lualatex --shell-escape this.tex ...')
        process = subprocess.Popen(latex_to_pdf_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec B603
        with process.stdout:
            log_subprocess_output(process.stdout, 'latex-to-pdf(3/3)')
        return_code = process.wait()
        if return_code < 0:
            log.error(f'latex-to-pdf process 3/3 ({latex_to_pdf_command}) was terminated by signal {-return_code}')
        else:
            log.info(f'latex-to-pdf process 3/3  ({latex_to_pdf_command}) returned {return_code}')

        log.info(separator)
        log.info('Moving stuff around (result phase) ...')
        source_asset = 'this.pdf'
        target_asset = '../index.pdf'
        shutil.copy(source_asset, target_asset)

        log.info(separator)
        log.info('Deliverable taxonomy: ...')
        target_path = pathlib.Path(target_asset)
        stat = target_path.stat()
        size_bytes = stat.st_size
        mod_time = dti.datetime.fromtimestamp(stat.st_ctime, tz=dti.timezone.utc).strftime(TS_FORMAT)
        sha612_hash = hash_file(target_path, hashlib.sha512)
        sha256_hash = hash_file(target_path, hashlib.sha256)
        sha1_hash = hash_file(target_path, hashlib.sha1)
        md5_hash = hash_file(target_path, hashlib.md5)
        log.info('- Ephemeral:')
        log.info(f'  + name: {target_path.name}')
        log.info(f'  + size: {size_bytes} bytes')
        log.info(f'  + date: {mod_time}')
        log.info('- Characteristic:')
        log.info('  + Checksums:')
        log.info(f'    sha512:{sha612_hash}')
        log.info(f'    sha256:{sha256_hash}')
        log.info(f'      sha1:{sha1_hash}')
        log.info(f'       md5:{md5_hash}')
        log.info('  + Fonts:')

        pdffonts_command = ['pdffonts', target_asset]
        process = subprocess.Popen(pdffonts_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec B603
        with process.stdout:
            log_subprocess_output(process.stdout, '    pdffonts')
        return_code = process.wait()
        if return_code < 0:
            log.error(f'pdffonts process ({pdffonts_command}) was terminated by signal {-return_code}')
        else:
            log.info(f'pdffonts process ({pdffonts_command}) returned {return_code}')


        log.info(separator)
        log.info('done.')
        log.info(separator)

    return 0
