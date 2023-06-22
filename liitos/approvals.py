"""Weave the content of the approvals data file into the output structure (for now LaTeX)."""
import os
import pathlib
from typing import Union

import liitos.gather as gat
import liitos.template_loader as template
from liitos import ENCODING, LOG_SEPARATOR, log

BOOKMATTER_TEMPLATE = os.getenv('LIITOS_BOOKMATTER_TEMPLATE', '')
BOOKMATTER_TEMPLATE_IS_EXTERNAL = bool(BOOKMATTER_TEMPLATE)
if not BOOKMATTER_TEMPLATE:
    BOOKMATTER_TEMPLATE = 'templates/bookmatter.tex.in'

BOOKMATTER_PATH = pathlib.Path('render/pdf/bookmatter.tex')
TOKEN_EXTRA_PUSHDOWN = r'\ExtraPushdown'  # nosec B105
EXTRA_OFFSET_EM = 24
TOKEN = r'\ \mbox{THE.ROLE.SLOT} & \mbox{THE.NAME.SLOT} & \mbox{} \\[0.5ex]'  # nosec B105
ROW_TEMPLATE = r'\ \mbox{role} & \mbox{name} & \mbox{} \\[0.5ex]'
GLUE = '\n\\hline\n'
FORMAT_DATE = '%d %b %Y'
JSON_CHANNEL = 'json'
YAML_CHANNEL = 'yaml'
COLUMNS_EXPECTED = ['name', 'role']
CUT_MARKER_TOP = '% |-- approvals - cut - marker - top -->'
CUT_MARKER_BOTTOM = '% <-- approvals - cut - marker - bottom --|'


def weave(
    doc_root: Union[str, pathlib.Path],
    structure_name: str,
    target_key: str,
    facet_key: str,
    options: dict[str, Union[bool, str]],
) -> int:
    """Later alligator."""
    log.info(LOG_SEPARATOR)
    log.info('entered signatures weave function ...')
    structure, asset_map = gat.prelude(
        doc_root=doc_root,
        structure_name=structure_name,
        target_key=target_key,
        facet_key=facet_key,
        command='approvals',
    )

    layout = {'layout': {'global': {'has_approvals': True, 'has_changes': True, 'has_notices': True}}}
    layout_path = asset_map[target_key][facet_key].get(gat.KEY_LAYOUT, '')
    if layout_path:
        log.info(f'loading layout from {layout_path=} for approvals')
        layout = gat.load_layout(facet_key, target_key, layout_path)[0]  # type: ignore
    else:
        log.info('using default layout for approvals')
    log.info(f'{layout=}')

    log.info(LOG_SEPARATOR)

    channel = YAML_CHANNEL
    columns_expected = COLUMNS_EXPECTED
    signatures_path = asset_map[target_key][facet_key][gat.KEY_APPROVALS]
    if str(signatures_path).endswith('.json'):
        channel = JSON_CHANNEL
        columns_expected = ['Approvals', 'Name']

    log.info(f'detected approvals channel ({channel}) weaving in from ({signatures_path})')
    log.info(f'loading signatures from {signatures_path=}')
    signatures = gat.load_approvals(facet_key, target_key, signatures_path)
    log.info(f'{signatures=}')

    log.info(LOG_SEPARATOR)
    log.info('plausibility tests for approvals ...')

    rows = []
    if channel == JSON_CHANNEL:
        if signatures[0]['columns'] != columns_expected:
            log.error('unexpected column model!')
            log.error(f'-  expected: ({columns_expected})')
            log.error(f'- but found: ({signatures[0]["columns"]})')
            return 1

        for role, name in signatures[0]['rows']:  # type: ignore
            rows.append(ROW_TEMPLATE.replace('role', role).replace('name', name))
    else:
        for slot, approval in enumerate(signatures[0]['approvals'], start=1):
            log.debug(f'{slot=}, {approval=}')
            if sorted(approval) != sorted(columns_expected):
                log.error('unexpected column model!')
                log.error(f'-  expected: ({columns_expected})')
                log.error(f'- but found: ({sorted(approval)}) in slot #{slot}')
                return 1

        for approval in signatures[0]['approvals']:
            role = approval['role']  # type: ignore
            name = approval['name']  # type: ignore
            rows.append(ROW_TEMPLATE.replace('role', role).replace('name', name))

    pushdown = EXTRA_OFFSET_EM - 2 * len(rows)
    log.info(f'calculated extra pushdown to be {pushdown}em')

    bookmatter_template = template.load_resource(BOOKMATTER_TEMPLATE, BOOKMATTER_TEMPLATE_IS_EXTERNAL)
    lines = [line.rstrip() for line in bookmatter_template.split('\n')]

    if not layout['layout']['global']['has_approvals']:
        log.info('removing approvals from document layout')
        in_section = False
        keep = []
        for line in lines:
            if not in_section:
                if CUT_MARKER_TOP in line:
                    in_section = True
                    continue
            if in_section:
                if CUT_MARKER_BOTTOM in line:
                    in_section = False
                continue
            keep.append(line)
        lines = keep

    log.info(LOG_SEPARATOR)
    log.info(f'weaving in the approvals from {signatures_path}...')
    for n, line in enumerate(lines):
        if TOKEN_EXTRA_PUSHDOWN in line:
            lines[n] = line.replace(TOKEN_EXTRA_PUSHDOWN, f'{pushdown}em')
            continue
        if line == TOKEN:
            lines[n] = GLUE.join(rows)
            break

    if lines[-1]:
        lines.append('\n')

    with open(BOOKMATTER_PATH, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))
    log.info(LOG_SEPARATOR)

    return 0
