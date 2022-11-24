"""Weave the content of the approvals data file into the output structure (for now LaTeX)."""
import os
import pathlib

import liitos.gather as gat
from liitos import ENCODING, log

APPROVALS_PATH = pathlib.Path('approvals.yml')
BOOKMATTER_TEMPLATE_PATH = pathlib.Path('bookmatter.tex.in')
BOOKMATTER_PATH = pathlib.Path('bookmatter.tex')
TOKEN = r'\ \mbox{THEROLE} & \mbox{THENAME} & \mbox{} \\[0.5ex]'
ROW_TEMPLATE = r'role & name & \mbox{} \\'
GLUE = '\n\\hline\n'
COLUMNS_EXPECTED = ['role', 'name']
FORMAT_DATE = '%d %b %Y'


def weave(
    doc_root: str | pathlib.Path, structure_name: str, target_key: str, facet_key: str, options: dict[str, bool]
) -> int:
    """Later alligator."""
    structure, asset_map = gat.prelude(
        doc_root=doc_root,
        structure_name=structure_name,
        target_key=target_key,
        facet_key=facet_key,
        command='approvals',
    )

    signatures_path = asset_map[target_key][facet_key][gat.KEY_APPROVALS]
    log.info(f'Loading signatures from {signatures_path=}')
    signatures = gat.load_approvals(facet_key, target_key, signatures_path)
    log.info(f'{signatures=}')

    log.info('Plausibility tests for approvals ...')
    for slot, approval in enumerate(signatures[0]['approvals'], start=1):
        log.debug(f'{slot=}, {approval=}')
        if sorted(approval) != sorted(COLUMNS_EXPECTED):
            log.info('ERROR: Unexpected column model!')
            log.info(f'-  expected: ({COLUMNS_EXPECTED})')
            log.info(f'- but found: ({approval}) for entry #{slot}')
            return 1

    rows = []
    for approval in signatures[0]['approvals']:
        role = approval['role']  # type: ignore
        name = approval['name']  # type: ignore
        rows.append(ROW_TEMPLATE.replace('role', role).replace('name', name))

    with open(BOOKMATTER_TEMPLATE_PATH, 'rt', encoding=ENCODING) as handle:
        lines = [line.rstrip() for line in handle.readlines()]

    log.info('Weaving in the approvals ...')
    for n, line in enumerate(lines):
        if line.strip() == TOKEN:
            lines[n] = GLUE.join(rows)
            break
    if lines[-1]:
        lines.append('\n')
    with open(BOOKMATTER_PATH, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))
    return 0
