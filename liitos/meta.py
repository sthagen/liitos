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
    common = metadata['document']['common']
    for n, line in enumerate(lines):
        if line.rstrip().endswith('%%_PATCH_%_HEADER_%_TITLE_%%'):
            if common.get('header_title'):
                lines[n] = line.replace(VALUE_SLOT, common['header_title'])
            else:
                log.warning('header_title value missing ... setting default (the title value)')
                lines[n] = line.replace(VALUE_SLOT, common['title'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_MAIN_%_TITLE_%%'):
            lines[n] = line.replace(VALUE_SLOT, common['title'])
            continue
        if line.rstrip().endswith('%%_PATCH_%_SUB_%_TITLE_%%'):
            if common.get('sub_title'):
                lines[n] = line.replace(VALUE_SLOT, common['sub_title'])
            else:
                log.warning('sub_title value missing ... setting default (single space)')
                lines[n] = line.replace(VALUE_SLOT, ' ')
            continue
        if line.rstrip().endswith('%%_PATCH_%_TYPE_%%'):
            if common.get('header_type'):
                lines[n] = line.replace(VALUE_SLOT, common['header_type'])
            else:
                log.warning('header_type value missing ... setting default (Engineering Document)')
                lines[n] = line.replace(VALUE_SLOT, 'Engineering Document')
            continue
        if line.rstrip().endswith('%%_PATCH_%_ID_%%'):
            if common.get('header_id'):
                lines[n] = line.replace(VALUE_SLOT, common['header_id'])
            else:
                log.warning('header_id value missing ... setting default (P99999)')
                lines[n] = line.replace(VALUE_SLOT, 'P99999')
            continue
        if line.rstrip().endswith('%%_PATCH_%_ISSUE_%%'):
            if common.get('issue'):
                lines[n] = line.replace(VALUE_SLOT, common['issue'])
            else:
                log.warning('issue value missing ... setting default (01)')
                lines[n] = line.replace(VALUE_SLOT, '01')
            continue
        if line.rstrip().endswith('%%_PATCH_%_REVISION_%%'):
            if common.get('revision'):
                lines[n] = line.replace(VALUE_SLOT, common['revision'])
            else:
                log.warning('revision value missing ... setting default (00)')
                lines[n] = line.replace(VALUE_SLOT, '00')
            continue
        if line.rstrip().endswith('%%_PATCH_%_DATE_%%'):
            if common.get('header_date'):
                lines[n] = line.replace(VALUE_SLOT, common['header_date'])
            else:
                log.warning('header_date value missing ... setting default (DD MON YYYY)')
                lines[n] = line.replace(VALUE_SLOT, 'DD MON YYYY')
            continue
        if line.rstrip().endswith('%%_PATCH_%_FRAME_%_NOTE_%%'):
            if common.get('footer_frame_note'):
                lines[n] = line.replace(VALUE_SLOT, common['footer_frame_note'])
            else:
                log.warning('footer_frame_note value missing ... setting default (VERY CONSEQUENTIAL)')
                lines[n] = line.replace(VALUE_SLOT, 'VERY CONSEQUENTIAL')
            continue
        if line.rstrip().endswith('%%_PATCH_%_FOOT_%_PAGE_%_COUNTER_%_LABEL_%%'):
            if common.get('footer_page_number_prefix'):
                lines[n] = line.replace(VALUE_SLOT, common['footer_page_number_prefix'])
            else:
                log.warning('footer_page_number_prefix value missing ... setting default (Page)')
                lines[n] = line.replace(VALUE_SLOT, 'Page')
            continue
        if line.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_ISSUE_%_LABEL_%%'):
            if common.get('change_log_issue_label'):
                lines[n] = line.replace(VALUE_SLOT, common['change_log_issue_label'])
            else:
                log.warning('change_log_issue_label value missing ... setting default (Iss.)')
                lines[n] = line.replace(VALUE_SLOT, 'Iss.')
            continue
        if line.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_REVISION_%_LABEL_%%'):
            if common.get('change_log_revision_label'):
                lines[n] = line.replace(VALUE_SLOT, common['change_log_revision_label'])
            else:
                log.warning('change_log_revision_label value missing ... setting default (Rev.)')
                lines[n] = line.replace(VALUE_SLOT, 'Rev.')
            continue
        if line.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_DATE_%_LABEL_%%'):
            if common.get('change_log_date_label'):
                lines[n] = line.replace(VALUE_SLOT, common['change_log_date_label'])
            else:
                log.warning('change_log_date_label value missing ... setting default (Date)')
                lines[n] = line.replace(VALUE_SLOT, 'Date')
            continue
        if line.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_AUTHOR_%_LABEL_%%'):
            if common.get('change_log_author_label'):
                lines[n] = line.replace(VALUE_SLOT, common['change_log_author_label'])
            else:
                log.warning('change_log_author_label value missing ... setting default (Author)')
                lines[n] = line.replace(VALUE_SLOT, 'Author')
            continue
        if line.rstrip().endswith('%%_PATCH_%_CHANGELOG_%_DESCRIPTION_%_LABEL_%%'):
            if common.get('change_log_description_label'):
                lines[n] = line.replace(VALUE_SLOT, common['change_log_description_label'])
            else:
                log.warning('change_log_description_label value missing ... setting default (Description)')
                lines[n] = line.replace(VALUE_SLOT, 'Description')
            continue
        if line.rstrip().endswith('%%_PATCH_%_ISSUE_%_REVISION_%_COMBINED_%%'):
            if common.get('header_issue_revision_combined'):
                lines[n] = line.replace(VALUE_SLOT, common['header_issue_revision_combined'])
            else:
                log.warning('footer_page_number_prefix value missing ... setting default (Iss \\theMetaIssCode, Rev \\theMetaRevCode)')
                lines[n] = line.replace(VALUE_SLOT, r'Iss \theMetaIssCode, Rev \theMetaRevCode')
            continue
        if line.rstrip().endswith('%%_PATCH_%_PROPRIETARY_%_INFORMATION_%_LABEL_%%'):
            if common.get('proprietary_information'):
                lines[n] = line.replace(VALUE_SLOT, common['proprietary_information'])
            else:
                log.warning('proprietary_information value missing ... setting default (Proprietary Information MISSING)')
                lines[n] = line.replace(VALUE_SLOT, 'Proprietary Information MISSING')
            continue
    if lines[-1]:
        lines.append('\n')
    with open(METADATA_PATH, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))

    return 0
