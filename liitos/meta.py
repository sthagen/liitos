"""Weave the content of the meta file(s) of metadata.tex.in into the output metadata.tex."""
import os
import pathlib

import yaml

import liitos.gather as gat
import liitos.template_loader as template
from liitos import ENCODING, log

METADATA_TEMPLATE = os.getenv('LIITOS_METADATA_TEMPLATE', '')
METADATA_TEMPLATE_IS_EXTERNAL = bool(METADATA_TEMPLATE)
if not METADATA_TEMPLATE:
    METADATA_TEMPLATE = 'templates/metadata.tex.in'

METADATA_PATH = pathlib.Path('metadata.tex')
VALUE_SLOT = 'VALUE.SLOT'
DOC_BASE = pathlib.Path('..', '..')
STRUCTURE_PATH = DOC_BASE / 'structure.yml'


def process_meta(aspects: str) -> gat.Meta | int:
    """TODO."""
    meta_path = DOC_BASE / aspects[gat.KEY_META]
    if not meta_path.is_file() or not meta_path.stat().st_size:
        log.error(f'destructure failed to find non-empty meta file at {meta_path}')
        return 1
    if meta_path.suffix.lower() not in ('.yaml', '.yml'):
        log.error(f'meta file format per suffix ({meta_path.suffix}) not supported')
        return 1
    with open(meta_path, 'rt', encoding=ENCODING) as handle:
        metadata = yaml.safe_load(handle)
    if not metadata:
        log.error(f'empty metadata file? Please add metadata to ({meta_path})')
        return 1
    if 'import' in metadata['document']:
        base_meta_path = DOC_BASE / metadata['document']['import']
        if not base_meta_path.is_file() or not base_meta_path.stat().st_size:
            log.error(
                f'metadata declares import of base data from ({base_meta_path.name}) but failed to find non-empty base file at {base_meta_path}')
            return 1
        with open(base_meta_path, 'rt', encoding=ENCODING) as handle:
            base_data = yaml.safe_load(handle)
        for key, value in metadata['document']['patch'].items():
            base_data['document']['common'][key] = value
        metadata = base_data
    with open('metadata.yml', 'wt', encoding=ENCODING) as handle:
        yaml.dump(metadata, handle, default_flow_style=False)
    return metadata


def weave(
    doc_root: str | pathlib.Path, structure_name: str, target_key: str, facet_key: str, options: dict[str, bool]
) -> int:
    """Later alligator."""
    target_code = target_key
    facet_code = facet_key
    if not facet_code.strip() or not target_code.strip():
        log.error(f'meta requires non-empty target ({target_code}) and facet ({facet_code}) codes')
        return 2

    log.info(f'parsed target ({target_code}) and facet ({facet_code}) from request')

    structure, asset_map = gat.prelude(
        doc_root=doc_root, structure_name=structure_name, target_key=target_key, facet_key=facet_key, command='meta'
    )
    log.info(f'prelude teleported processor into the document root at ({os.getcwd()}/)')
    rel_concat_folder_path = pathlib.Path("render/pdf/")
    rel_concat_folder_path.mkdir(parents=True, exist_ok=True)
    os.chdir(rel_concat_folder_path)
    log.info(f'meta (this processor) teleported into the render/pdf location ({os.getcwd()}/)')

    if not STRUCTURE_PATH.is_file() or not STRUCTURE_PATH.stat().st_size:
        log.error(f'meta failed to find non-empty structure file at {STRUCTURE_PATH}')
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
        if sorted(aspect_map.keys()) != sorted(gat.KEYS_REQUIRED):
            log.warning(
                f'structure does not strictly provide the expected aspects {sorted(gat.KEYS_REQUIRED)}'
                f' for target ({target_code}) and facet ({facet_code})'
            )
            log.warning(f'- found the following aspects instead:                   {sorted(aspect_map.keys())} instead')

        metadata = process_meta(aspect_map)
        if isinstance(metadata, int):
            return 1

    metadata_template = template.load_resource(METADATA_TEMPLATE, METADATA_TEMPLATE_IS_EXTERNAL)
    lines = [line.rstrip() for line in metadata_template.split('\n')]

    log.info('weaving in the meta data ...')
    for n, line in enumerate(lines):
        if line.rstrip().endswith('%%_PATCH_%_HEADER_%_TITLE_%%'):
            lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['header_title'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_MAIN_%_TITLE_%%'):
            lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['title'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_SUB_%_TITLE_%%'):
            lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['sub_title'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_TYPE_%%'):
            lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['header_type'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_ID_%%'):
            lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['header_id'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_ISSUE_%%'):
            lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['issue'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_REVISION_%%'):
            lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['revision'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_DATE_%%'):
            lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['header_date'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_FRAME_%_NOTE_%%'):
            lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['footer_frame_note'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_FOOT_%_PAGE_%_COUNTER_%_LABEL_%%'):
            if metadata['document']['common']['footer_page_number_prefix']:
                lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['footer_page_number_prefix'])
            else:
                log.warning('footer_page_number_prefix value missing ... setting default')
                lines[n] = line.replace(VALUE_SLOT, 'Page')
            continue
        if line.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_ISSUE_%_LABEL_%%'):
            lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['change_log_issue_label'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_REVISION_%_LABEL_%%'):
            lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['change_log_revision_label'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_DATE_%_LABEL_%%'):
            lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['change_log_date_label'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_AUTHOR_%_LABEL_%%'):
            lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['change_log_author_label'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_DESCRIPTION_%_LABEL_%%'):
            lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['change_log_description_label'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%%'):
            if metadata['document']['common']['header_issue_revision_combined']:
                lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['header_issue_revision_combined'])
            else:
                log.warning('footer_page_number_prefix value missing ... setting default')
                lines[n] = line.replace(VALUE_SLOT, r'Iss \theMetaIssCode, Rev \theMetaRevCode')
            continue
        if line.rstrip().endswith('%%_PATCH_%_PROPRIETARY_%_INFORMATION_%_LABEL_%%'):
            if metadata['document']['common']['proprietary_information']:
                lines[n] = line.replace(VALUE_SLOT, metadata['document']['common']['proprietary_information'])
            else:
                log.warning('proprietary_information value missing ...')
            continue
    if lines[-1]:
        lines.append('\n')
    with open(METADATA_PATH, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))

    return 0
