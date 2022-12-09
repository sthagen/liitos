"""Render the concat document to pdf."""
import datetime as dti
import difflib
import hashlib
import os
import pathlib
import shutil
import subprocess  # nosec B404
import time
from typing import Any, Callable, no_type_check

import foran.foran as api  # type: ignore
import yaml
from foran.report import generate_report  # type: ignore
from taksonomia.taksonomia import Taxonomy  # type: ignore

import liitos.captions as cap
import liitos.concat as con
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
LOG_SEPARATOR = '- ' * 80
INTER_PROCESS_SYNC_SECS = 0.1
INTER_PROCESS_SYNC_ATTEMPTS = 10


def hash_file(path: pathlib.Path, hasher: Callable[..., Any] | None = None) -> str:
    """Return the SHA512 hex digest of the data from file."""
    if hasher is None:
        hasher = hashlib.sha512
    hash = hasher()
    with open(path, 'rb') as handle:
        while chunk := handle.read(CHUNK_SIZE):
            hash.update(chunk)
    return hash.hexdigest()


@no_type_check
def log_subprocess_output(pipe, prefix: str):
    for line in iter(pipe.readline, b''):  # b'\n'-separated lines
        cand = line.decode(encoding=ENCODING).rstrip()
        if cand.strip().strip('[])yex'):
            if any(
                [
                    'microtype' in cand,
                    'xassoccnt' in cand,
                    'texlive/2022/texmf-dist/tex/' in cand,
                    cand == 'erns.sty)',
                    cand == '(see the transcript file for additional information)',
                    cand.startswith(r'Overfull \hbox ')
                    and cand.endswith(r'pt too wide) has occurred while \output is active'),
                ]
            ):
                log.debug(f'{prefix}: %s', cand)
            else:
                log.info(f'{prefix}: %s', cand)


@no_type_check
def vcs_probe():
    """Are we in front, on par, or behind with the upstream?"""
    try:
        repo = api.Repo('.', search_parent_directories=True)
        status = api.Status(repo)
        api.local_commits(repo, status)
        api.local_staged(repo, status)
        api.local_files(repo, status)
        try:
            repo_root_folder = repo.git.rev_parse(show_toplevel=True)
            yield f'Root     ({repo_root_folder})'
        except Exception:
            yield 'WARNING - ignored exception when assessing repo root folder location'
        for line in generate_report(status):
            yield line.rstrip()
    except Exception:
        yield 'WARNING - we seem to not be within a git repository clone'


def report_taxonomy(target_path: pathlib.Path) -> None:
    """Convenience function to report date, size, and checksums of the deliverable."""
    taxonomy = Taxonomy(target_path, excludes='', key_function='md5')
    for path in sorted(target_path.parent.rglob('*')):
        taxonomy.add_branch(path) if path.is_dir() else taxonomy.add_leaf(path)
    log.info('- Writing render/pdf folder taxonomy to inventory.json ...')
    taxonomy.dump(sink='inventory', format_type='json', base64_encode=False)

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


@no_type_check
def unified_diff(left: list[str], right: list[str], left_label: str = 'before', right_label: str = 'after'):
    """Derive the unified diff between left and right lists of strings as generator of strings."""
    for line in difflib.unified_diff(left, right, fromfile=left_label, tofile=right_label):
        yield line.rstrip()


@no_type_check
def der(
    doc_root: str | pathlib.Path, structure_name: str, target_key: str, facet_key: str, options: dict[str, bool]
) -> int:
    """Later alligator."""
    log.info(LOG_SEPARATOR)
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

    log.info(LOG_SEPARATOR)
    log.info('Assessing the local version control status (compared to upstream) ...')
    log.info(LOG_SEPARATOR)
    for line in vcs_probe():
        log.info(line)
    log.info(LOG_SEPARATOR)

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

        log.info(LOG_SEPARATOR)
        log.info('transforming SVG assets to high resolution PNG bitmaps ...')
        for path_to_dir in (IMAGES_FOLDER, DIAGRAMS_FOLDER):
            the_folder = pathlib.Path(path_to_dir)
            if not the_folder.is_dir():
                log.error(
                    f'svg-to-png directory ({the_folder}) in ({pathlib.Path().cwd()}) does not exist or is no directory'
                )
                continue
            for svg in pathlib.Path(path_to_dir).iterdir():
                if svg.is_file() and svg.suffix == '.svg':
                    png = str(svg).replace('.svg', '.png')
                    svg_to_png_command = ['svgexport', svg, png, '100%']
                    process = subprocess.Popen(  # nosec B603
                        svg_to_png_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
                    )
                    with process.stdout:
                        log_subprocess_output(process.stdout, 'svg-to-png')
                    return_code = process.wait()
                    if return_code < 0:
                        log.error(f'svg-to-png process ({svg_to_png_command}) was terminated by signal {-return_code}')
                    elif return_code == 0:
                        log.info(f'svg-to-png process ({svg_to_png_command}) returned {return_code}')
                    else:
                        log.error(f'svg-to-png process ({svg_to_png_command}) returned {return_code}')

        special_patching = []
        log.info(LOG_SEPARATOR)
        log.info('rewriting src attribute values of SVG to PNG sources ...')
        with open('document.md', 'rt', encoding=ENCODING) as handle:
            lines = [line.rstrip() for line in handle.readlines()]
        for slot, line in enumerate(lines):
            if '.svg' in line and line.count('.') >= 2:
                caption, src, alt, rest = con.parse_markdown_image(line)
                stem, app_indicator, format_suffix = src.rsplit('.', 2)
                log.info(f'- removing application indicator ({app_indicator}) from src ...')
                if format_suffix != 'svg':
                    log.warning(f'  + format_suffix (.{format_suffix}) unexpected in <<{line.rstrip()}>> ...')
                fine = f'![{caption}]({stem}.png "{alt}"){rest}'
                log.info(f'  transform[#{slot + 1}]: {line}')
                log.info(f'       into[#{slot + 1}]: {fine}')
                lines[slot] = fine
                dia_path_old = src.replace('.svg', '.png')
                dia_path_new = f'{stem}.png'
                dia_fine_rstrip = dia_path_new.rstrip()
                if dia_path_old and dia_path_new:
                    special_patching.append((dia_path_old, dia_path_new))
                    log.info(
                        f'post-action[#{slot + 1}]: adding to queue for sync move: ({dia_path_old}) -> ({dia_path_new})'
                    )
                else:
                    log.warning(f'- old: {src.rstrip()}')
                    log.warning(f'- new: {dia_fine_rstrip}')
                continue
            if '.svg' in line:
                fine = line.replace('.svg', '.png')
                log.info(f'  transform[#{slot + 1}]: {line}')
                log.info(f'       into[#{slot + 1}]: {fine}')
                lines[slot] = fine
                continue
        with open('document.md', 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines))

        log.info(LOG_SEPARATOR)
        log.info('ensure diagram files can be found when patched ...')
        if special_patching:
            for old, mew in special_patching:
                source_asset = pathlib.Path(old)
                target_asset = pathlib.Path(mew)
                log.info(f'- moving: ({source_asset}) -> ({target_asset})')
                present = False
                remaining_attempts = INTER_PROCESS_SYNC_ATTEMPTS
                while remaining_attempts > 0 and not present:
                    try:
                        present = source_asset.is_file()
                    except Exception as ex:
                        log.error(f'    * probing for resource ({old}) failed with ({ex}) ... continuing')
                    log.info(
                        f'  + resource ({old}) is{" " if present else " NOT "}present at ({source_asset})'
                        f' - attempt {11 - remaining_attempts} of {INTER_PROCESS_SYNC_ATTEMPTS} ...'
                    )
                    if present:
                        break
                    time.sleep(INTER_PROCESS_SYNC_SECS)
                    remaining_attempts -= 1
                if not source_asset.is_file():
                    log.warning(
                        f'- resource ({old}) still not present at ({source_asset}) after {remaining_attempts} attempts'
                        f' and ({round(remaining_attempts * INTER_PROCESS_SYNC_SECS, 0) :.0f} seconds waiting)'
                    )
                shutil.move(source_asset, target_asset)
        else:
            log.info('post-action queue (from reference renaming) is empty - nothing to move')
        log.info(LOG_SEPARATOR)

        fmt_spec = 'markdown+link_attributes'
        in_doc = 'document.md'
        out_doc = 'document.tex'
        markdown_to_latex_command = [
            'pandoc',
            '--verbose',
            '-f',
            fmt_spec,
            '-t',
            'latex',
            in_doc,
            '-o',
            out_doc,
            '--filter',
            'mermaid-filter',
        ]
        log.info(LOG_SEPARATOR)
        log.info('pandoc -f markdown+link_attributes -t latex document.md -o document.tex --filter mermaid-filter ...')
        process = subprocess.Popen(  # nosec B603
            markdown_to_latex_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        with process.stdout:
            log_subprocess_output(process.stdout, 'markdown-to-latex')
        return_code = process.wait()
        if return_code < 0:
            log.error(
                f'markdown-to-latex process ({markdown_to_latex_command}) was terminated by signal {-return_code}'
            )
        else:
            log.info(f'markdown-to-latex process ({markdown_to_latex_command}) returned {return_code}')

        log.info(LOG_SEPARATOR)
        log.info('move any captions below tables ...')
        with open('document.tex', 'rt', encoding=ENCODING) as handle:
            lines = [line.rstrip() for line in handle.readlines()]
        doc_before_caps_patch = 'document-before-caps-patch.tex.txt'
        with open(doc_before_caps_patch, 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines))
        lines_caps_patch = cap.weave(lines)
        with open('document.tex', 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines_caps_patch))
        log.info(f'diff of the (captions-below-tables) filter result:')
        log.info(LOG_SEPARATOR)
        for line in unified_diff(lines, lines_caps_patch):
            log.info(line)
        log.info(LOG_SEPARATOR)

        log.info(LOG_SEPARATOR)
        log.info('inject stem (derived from file name) labels ...')
        doc_before_label_patch = 'document-before-inject-stem-label-patch.tex.txt'
        with open(doc_before_label_patch, 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines_caps_patch))
        lines_inject_stem_label = lab.inject(lines_caps_patch)
        with open('document.tex', 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines_inject_stem_label))
        log.info(f'diff of the (inject-stem-derived-labels) filter result:')
        log.info(LOG_SEPARATOR)
        for line in unified_diff(lines_caps_patch, lines_inject_stem_label):
            log.info(line)
        log.info(LOG_SEPARATOR)

        log.info(LOG_SEPARATOR)
        log.info('scale figures ...')
        doc_before_figures_patch = 'document-before-scale-figures-patch.tex.txt'
        with open(doc_before_figures_patch, 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines_inject_stem_label))
        lines_scale_figures = fig.scale(lines_inject_stem_label)
        with open('document.tex', 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines_scale_figures))
        log.info(f'diff of the (inject-scale-figures) filter result:')
        log.info(LOG_SEPARATOR)
        for line in unified_diff(lines_inject_stem_label, lines_scale_figures):
            log.info(line)
        log.info(LOG_SEPARATOR)

        if need_patching:
            log.info(LOG_SEPARATOR)
            log.info('apply user patches ...')
            doc_before_user_patch = 'document-before-user-patch.tex.txt'
            with open(doc_before_user_patch, 'wt', encoding=ENCODING) as handle:
                handle.write('\n'.join(lines_scale_figures))
            lines_user_patches = pat.apply(patches, lines_scale_figures)
            with open('document.tex', 'wt', encoding=ENCODING) as handle:
                handle.write('\n'.join(lines_user_patches))
            log.info(f'diff of the (user-patches) filter result:')
            log.info(LOG_SEPARATOR)
            for line in unified_diff(lines_scale_figures, lines_user_patches):
                log.info(line)
            log.info(LOG_SEPARATOR)
        else:
            log.info(LOG_SEPARATOR)
            log.info('skipping application of user patches ...')

        log.info(LOG_SEPARATOR)
        log.info('cp -a driver.tex this.tex ...')
        source_asset = 'driver.tex'
        target_asset = 'this.tex'
        shutil.copy(source_asset, target_asset)

        latex_to_pdf_command = ['lualatex', '--shell-escape', 'this.tex']
        log.info(LOG_SEPARATOR)
        log.info('1/3) lualatex --shell-escape this.tex ...')
        process = subprocess.Popen(latex_to_pdf_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec B603
        with process.stdout:
            log_subprocess_output(process.stdout, 'latex-to-pdf(1/3)')
        return_code = process.wait()
        if return_code < 0:
            log.error(f'latex-to-pdf process 1/3 ({latex_to_pdf_command}) was terminated by signal {-return_code}')
        else:
            log.info(f'latex-to-pdf process 1/3  ({latex_to_pdf_command}) returned {return_code}')

        log.info(LOG_SEPARATOR)
        log.info('2/3) lualatex --shell-escape this.tex ...')
        process = subprocess.Popen(latex_to_pdf_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec B603
        with process.stdout:
            log_subprocess_output(process.stdout, 'latex-to-pdf(2/3)')
        return_code = process.wait()
        if return_code < 0:
            log.error(f'latex-to-pdf process 2/3 ({latex_to_pdf_command}) was terminated by signal {-return_code}')
        else:
            log.info(f'latex-to-pdf process 2/3  ({latex_to_pdf_command}) returned {return_code}')

        log.info(LOG_SEPARATOR)
        log.info('3/3) lualatex --shell-escape this.tex ...')
        process = subprocess.Popen(latex_to_pdf_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec B603
        with process.stdout:
            log_subprocess_output(process.stdout, 'latex-to-pdf(3/3)')
        return_code = process.wait()
        if return_code < 0:
            log.error(f'latex-to-pdf process 3/3 ({latex_to_pdf_command}) was terminated by signal {-return_code}')
        else:
            log.info(f'latex-to-pdf process 3/3  ({latex_to_pdf_command}) returned {return_code}')

        log.info(LOG_SEPARATOR)
        log.info('Moving stuff around (result phase) ...')
        source_asset = 'this.pdf'
        target_asset = '../index.pdf'
        shutil.copy(source_asset, target_asset)

        log.info(LOG_SEPARATOR)
        log.info('Deliverable taxonomy: ...')
        report_taxonomy(pathlib.Path(target_asset))

        pdffonts_command = ['pdffonts', target_asset]
        process = subprocess.Popen(pdffonts_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec B603
        with process.stdout:
            log_subprocess_output(process.stdout, '    pdffonts')
        return_code = process.wait()
        if return_code < 0:
            log.error(f'pdffonts process ({pdffonts_command}) was terminated by signal {-return_code}')
        else:
            log.info(f'pdffonts process ({pdffonts_command}) returned {return_code}')

        log.info(LOG_SEPARATOR)
        log.info('done.')
        log.info(LOG_SEPARATOR)

    return 0
