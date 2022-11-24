"""Weave the content of the changes data file into the output structure (for now LaTeX)."""
import os
import pathlib

import liitos.gather as gat
from liitos import ENCODING, log

CHANGES_PATH = pathlib.Path('changes.yml')
PUBLISHER_TEMPLATE_PATH = pathlib.Path('publisher.tex.in')
PUBLISHER_PATH = pathlib.Path('publisher.tex')
TOKEN = r'\theMetaIssCode & \theMetaRevCode & \theMetaAuthor & \theChangeLogEntryDesc \\'
ROW_TEMPLATE = r'issue & 00 & author & summary \\'
GLUE = '\n\\hline\n'
COLUMNS_EXPECTED = ['issue', 'author', 'date', 'summary']
FORMAT_DATE = '%d %b %Y'


def weave(
    doc_root: str | pathlib.Path, structure_name: str, target_key: str, facet_key: str, options: dict[str, bool]
) -> int:
    """Later alligator."""
    structure, asset_map = gat.prelude(
        doc_root=doc_root, structure_name=structure_name, target_key=target_key, facet_key=facet_key, command='changes'
    )

    changes_path = asset_map[target_key][facet_key][gat.KEY_CHANGES]
    log.info(f'Loading changes from {changes_path=}')
    changes = gat.load_changes(facet_key, target_key, changes_path)
    log.info(f'{changes=}')

    log.info('Plausibility tests for changes ...')
    for slot, change in enumerate(changes[0]['changes'], start=1):
        if sorted(change) != sorted(COLUMNS_EXPECTED):
            log.error('Unexpected column model!')
            log.error(f'-  expected: ({COLUMNS_EXPECTED})')
            log.error(f'- but found: ({change}) for entry #{slot}')
            return 1

    rows = []
    for change in changes[0]['changes']:
        issue, author, summary = change['issue'], change['author'], change['summary']  # type: ignore
        rows.append(ROW_TEMPLATE.replace('issue', issue).replace('author', author).replace('summary', summary))

    with open(PUBLISHER_TEMPLATE_PATH, 'rt', encoding=ENCODING) as handle:
        lines = [line.rstrip() for line in handle.readlines()]

    log.info('Weaving in the changes ...')
    for n, line in enumerate(lines):
        if line.strip() == TOKEN:
            lines[n] = GLUE.join(rows)
            break
    if lines[-1]:
        lines.append('\n')
    with open(PUBLISHER_PATH, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))

    return 0
