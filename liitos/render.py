"""Render the concat document to pdf."""

import json
import os
import pathlib
import re
import shutil
import time
from typing import Union, no_type_check

import yaml

import liitos.captions as cap
import liitos.concat as con
import liitos.description_lists as dsc
import liitos.figures as fig
import liitos.gather as gat
import liitos.labels as lab
import liitos.patch as pat
import liitos.tables as tab
import liitos.tools as too
from liitos import (
    CONTEXT,
    ENCODING,
    FROM_FORMAT_SPEC,
    LATEX_PAYLOAD_NAME,
    LOG_SEPARATOR,
    log,
    parse_csl,
)

DOC_BASE = pathlib.Path('..', '..')
STRUCTURE_PATH = DOC_BASE / 'structure.yml'
IMAGES_FOLDER = 'images/'
DIAGRAMS_FOLDER = 'diagrams/'
PATCH_SPEC_NAME = 'patch.yml'
INTER_PROCESS_SYNC_SECS = 0.1
INTER_PROCESS_SYNC_ATTEMPTS = 10
VENDORED_SVG_PAT = re.compile(r'^.+\]\([^.]+\.[^.]+\.svg\ .+$')


@no_type_check
def read_patches(folder_path: pathlib.Path, patches_path: pathlib.Path) -> tuple[list[tuple[str, str]], bool]:
    """Ja ja."""
    patches = []
    need_patching = False
    log.info(f'inspecting any patch spec file ({patches_path}) ...')
    if patches_path.is_file() and patches_path.stat().st_size:
        target_path = folder_path / PATCH_SPEC_NAME
        shutil.copy(patches_path, target_path)
        try:
            with open(patches_path, 'rt', encoding=ENCODING) as handle:
                patch_spec = yaml.safe_load(handle)
            need_patching = True
        except (OSError, UnicodeDecodeError) as err:
            log.error(f'failed to load patch spec from ({patches_path}) with ({err}) - patching will be skipped')
            need_patching = False
        if need_patching:
            try:
                patches = [(rep, lace) for rep, lace in patch_spec]
                patch_pair_count = len(patches)
                if not patch_pair_count:
                    need_patching = False
                    log.warning('- ignoring empty patch spec')
                else:
                    log.info(
                        f'- loaded {patch_pair_count} patch pair{"" if patch_pair_count == 1 else "s"}'
                        f' from patch spec file ({patches_path})'
                    )
            except ValueError as err:
                log.error(f'- failed to parse patch spec from ({patch_spec}) with ({err}) - patching will be skipped')
                need_patching = False
    else:
        if patches_path.is_file():
            log.warning(f'- ignoring empty patch spec file ({patches_path})')
        else:
            log.info(f'- no patch spec file ({patches_path}) detected')
    return patches, need_patching


@no_type_check
def der(
    doc_root: Union[str, pathlib.Path],
    structure_name: str,
    target_key: str,
    facet_key: str,
    options: dict[str, Union[bool, str]],
) -> int:
    """Later alligator."""
    log.info(LOG_SEPARATOR)
    log.info('entered render function ...')
    target_code = target_key
    facet_code = facet_key
    if not facet_code.strip() or not target_code.strip():
        log.error(f'render requires non-empty target ({target_code}) and facet ({facet_code}) codes')
        return 2
    log.info(f'parsed target ({target_code}) and facet ({facet_code}) from request')

    from_format_spec = options.get('from_format_spec', FROM_FORMAT_SPEC)
    filter_cs_list = parse_csl(options.get('filter_cs_list', ''))
    if filter_cs_list:
        log.info(f'parsed from-format-spec ({from_format_spec}) and filters ({", ".join(filter_cs_list)}) from request')
    else:
        log.info(f'parsed from-format-spec ({from_format_spec}) and no filters from request')

    structure, asset_map = gat.prelude(
        doc_root=doc_root, structure_name=structure_name, target_key=target_key, facet_key=facet_key, command='render'
    )
    log.info(f'prelude teleported processor into the document root at ({os.getcwd()}/)')

    rel_concat_folder_path = pathlib.Path('render/pdf/')
    rel_concat_folder_path.mkdir(parents=True, exist_ok=True)

    patches, need_patching = read_patches(rel_concat_folder_path, pathlib.Path(PATCH_SPEC_NAME))

    os.chdir(rel_concat_folder_path)
    log.info(f'render (this processor) teleported into the render/pdf location ({os.getcwd()}/)')

    log.info(LOG_SEPARATOR)
    log.info('Assessing the local version control status (compared to upstream) ...')
    too.ensure_separate_log_lines(too.vcs_probe)
    CONTEXT['builder_node_id'] = too.node_id()
    log.info('Context noted with:')
    log.info(f'- builder-node-id({CONTEXT.get("builder_node_id")})')
    log.info(f'- source-hash({CONTEXT.get("source_hash")})')
    log.info(f'- source-hint({CONTEXT.get("source_hint")})')

    ok, aspect_map = too.load_target(target_code, facet_code)
    if not ok or not aspect_map:
        return 0 if ok else 1

    do_render = aspect_map.get('render', None)
    if do_render is not None:
        log.info(f'found render instruction with value ({aspect_map["render"]})')

    if do_render is None or do_render:
        log.info('we will render ...')
    else:
        log.warning('we will not render ...')
        return 0xFADECAFE

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
                too.delegate(svg_to_png_command, 'svg-to-png')

    special_patching = []
    log.info(LOG_SEPARATOR)
    log.info('rewriting src attribute values of SVG to PNG sources ...')
    with open('document.md', 'rt', encoding=ENCODING) as handle:
        lines = [line.rstrip() for line in handle.readlines()]
    for slot, line in enumerate(lines):
        if line.startswith('![') and '](' in line:
            if VENDORED_SVG_PAT.match(line):
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
                            f'post-action[#{slot + 1}]: adding to queue for sync move: ({dia_path_old})'
                            f' -> ({dia_path_new})'
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
                    f'- resource ({old}) still not present at ({source_asset})'
                    f' as seen from ({os.getcwd()}) after {remaining_attempts} attempts'
                    f' and ({round(remaining_attempts * INTER_PROCESS_SYNC_SECS, 0) :.0f} seconds waiting)'
                )
            shutil.move(source_asset, target_asset)
    else:
        log.info('post-action queue (from reference renaming) is empty - nothing to move')
    log.info(LOG_SEPARATOR)

    # prototyping >>>
    fmt_spec = from_format_spec
    in_doc = 'document.md'
    out_doc = 'ast-no-filter.json'
    markdown_to_ast_command = [
        'pandoc',
        '--verbose',
        '-f',
        fmt_spec,
        '-t',
        'json',
        in_doc,
        '-o',
        out_doc,
    ]
    log.info(LOG_SEPARATOR)
    log.info(f'executing ({" ".join(markdown_to_ast_command)}) ...')
    if code := too.delegate(markdown_to_ast_command, 'markdown-to-ast'):
        return code

    log.info(LOG_SEPARATOR)

    mermaid_caption_map = too.mermaid_captions_from_json_ast(out_doc)
    log.info(LOG_SEPARATOR)
    # no KISS too.ensure_separate_log_lines(json.dumps, [mermaid_caption_map, 2])
    for line in json.dumps(mermaid_caption_map, indent=2).split('\n'):
        for fine in line.split('\n'):
            log.info(fine)
    log.info(LOG_SEPARATOR)

    # <<< prototyping

    fmt_spec = from_format_spec
    in_doc = 'document.md'
    out_doc = LATEX_PAYLOAD_NAME
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
    ]
    if filter_cs_list:
        filters = [added_prefix for expr in filter_cs_list for added_prefix in ('--filter', expr)]
        markdown_to_latex_command += filters
    log.info(LOG_SEPARATOR)
    log.info(f'executing ({" ".join(markdown_to_latex_command)}) ...')
    if code := too.delegate(markdown_to_latex_command, 'markdown-to-latex'):
        return code

    log.info(LOG_SEPARATOR)
    log.info(f'load text lines from intermediate {LATEX_PAYLOAD_NAME} file before internal transforms ...')
    with open(LATEX_PAYLOAD_NAME, 'rt', encoding=ENCODING) as handle:
        lines = [line.rstrip() for line in handle.readlines()]

    patch_counter = 1
    if options.get('table_caption_below', False):
        lines = too.execute_filter(
            cap.weave,
            head='move any captions below tables ...',
            backup=f'document-before-caps-patch-{patch_counter}.tex.txt',
            label='captions-below-tables',
            text_lines=lines,
            lookup=None,
        )
        patch_counter += 1
    else:
        log.info('NOT moving captions below tables!')

    lines = too.execute_filter(
        lab.inject,
        head='inject stem (derived from file name) labels ...',
        backup=f'document-before-inject-stem-label-patch-{patch_counter}.tex.txt',
        label='inject-stem-derived-labels',
        text_lines=lines,
        lookup=mermaid_caption_map,
    )
    patch_counter += 1

    lines = too.execute_filter(
        fig.scale,
        head='scale figures ...',
        backup=f'document-before-scale-figures-patch-{patch_counter}.tex.txt',
        label='inject-scale-figures',
        text_lines=lines,
        lookup=None,
    )
    patch_counter += 1

    lines = too.execute_filter(
        dsc.options,
        head='add options to descriptions (definition lists) ...',
        backup=f'document-before-description-options-patch-{patch_counter}.tex.txt',
        label='inject-description-options',
        text_lines=lines,
        lookup=None,
    )
    patch_counter += 1

    if options.get('patch_tables', False):
        lines = too.execute_filter(
            tab.patch,
            head='patching tables EXPERIMENTAL (table-shape) ...',
            backup=f'document-before-table-shape-patch-{patch_counter}.tex.txt',
            label='changed-table-shape',
            text_lines=lines,
            lookup=None,
        )
        patch_counter += 1
    else:
        log.info(LOG_SEPARATOR)
        log.info('not patching tables but commenting out (ignoring) any columns command (table-shape) ...')
        patched_lines = [f'%IGNORED_{v}' if v.startswith(r'\columns=') else v for v in lines]
        patched_lines = [f'%IGNORED_{v}' if v.startswith(r'\tablefontsize=') else v for v in patched_lines]
        log.info('diff of the (ignore-table-shape-if-not-patched) filter result:')
        too.log_unified_diff(lines, patched_lines)
        lines = patched_lines
        log.info(LOG_SEPARATOR)

    if need_patching:
        log.info(LOG_SEPARATOR)
        log.info('apply user patches ...')
        doc_before_user_patch = f'document-before-user-patch-{patch_counter}.tex.txt'
        patch_counter += 1
        with open(doc_before_user_patch, 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(lines))
        patched_lines = pat.apply(patches, lines)
        with open(LATEX_PAYLOAD_NAME, 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(patched_lines))
        log.info('diff of the (user-patches) filter result:')
        too.log_unified_diff(lines, patched_lines)
        lines = patched_lines
    else:
        log.info(LOG_SEPARATOR)
        log.info('skipping application of user patches ...')

    log.info(LOG_SEPARATOR)
    log.info(f'Internal text line buffer counts {len(lines)} lines')

    log.info(LOG_SEPARATOR)
    log.info('cp -a driver.tex this.tex ...')
    source_asset = 'driver.tex'
    target_asset = 'this.tex'
    shutil.copy(source_asset, target_asset)

    latex_to_pdf_command = ['lualatex', '--shell-escape', 'this.tex']
    log.info(LOG_SEPARATOR)
    log.info('1/3) lualatex --shell-escape this.tex ...')
    if code := too.delegate(latex_to_pdf_command, 'latex-to-pdf(1/3)'):
        return code

    log.info(LOG_SEPARATOR)
    log.info('2/3) lualatex --shell-escape this.tex ...')
    if code := too.delegate(latex_to_pdf_command, 'latex-to-pdf(2/3)'):
        return code

    log.info(LOG_SEPARATOR)
    log.info('3/3) lualatex --shell-escape this.tex ...')
    if code := too.delegate(latex_to_pdf_command, 'latex-to-pdf(3/3)'):
        return code

    if str(options.get('label', '')).strip():
        labeling_call = str(options['label']).strip().split()
        labeling_call.extend(
            [
                '--key-value-pairs',
                (
                    f'BuilderNodeID={CONTEXT["builder_node_id"]}'
                    f',SourceHash={CONTEXT.get("source_hash", "no-source-hash-given")}'
                    f',SourceHint={CONTEXT.get("source_hint", "no-source-hint-given")}'
                ),
            ]
        )
        log.info(LOG_SEPARATOR)
        log.info(f'Labeling the resulting pdf file per ({" ".join(labeling_call)})')
        too.delegate(labeling_call, 'label-pdf')
        log.info(LOG_SEPARATOR)

    log.info(LOG_SEPARATOR)
    log.info('Moving stuff around (result phase) ...')
    source_asset = 'this.pdf'
    target_asset = '../index.pdf'
    shutil.copy(source_asset, target_asset)

    log.info(LOG_SEPARATOR)
    log.info('Deliverable taxonomy: ...')
    too.report_taxonomy(pathlib.Path(target_asset))

    pdffonts_command = ['pdffonts', target_asset]
    too.delegate(pdffonts_command, 'assess-pdf-fonts')

    log.info(LOG_SEPARATOR)
    log.info('done.')
    log.info(LOG_SEPARATOR)

    return 0
