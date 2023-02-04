"""Weave the content of the changes data file into the output structure (for now LaTeX)."""
import os
import pathlib

import liitos.gather as gat
import liitos.template_loader as template
from liitos import ENCODING, LOG_SEPARATOR, log

PUBLISHER_TEMPLATE = os.getenv('LIITOS_PUBLISHER_TEMPLATE', '')
PUBLISHER_TEMPLATE_IS_EXTERNAL = bool(PUBLISHER_TEMPLATE)
if not PUBLISHER_TEMPLATE:
    PUBLISHER_TEMPLATE = 'templates/publisher.tex.in'

PUBLISHER_PATH = pathlib.Path('render/pdf/publisher.tex')
TOKEN = r'THE.ISSUE.CODE & THE.REVISION.CODE & THE.AUTHOR.NAME & THE.DESCRIPTION \\'  # nosec B105
DEFAULT_REVISION = '00'
ROW_TEMPLATE = r'issue & revision & author & summary \\'
GLUE = '\n\\hline\n'
JSON_CHANNEL = 'json'
YAML_CHANNEL = 'yaml'
COLUMNS_EXPECTED = sorted(['author', 'date', 'issue', 'revision', 'summary'])
COLUMNS_MINIMAL = sorted(['author', 'issue', 'summary'])


def weave(
    doc_root: str | pathlib.Path, structure_name: str, target_key: str, facet_key: str, options: dict[str, bool | str]
) -> int:
    """Later alligator."""
    log.info(LOG_SEPARATOR)
    log.info('entered changes weave function ...')
    structure, asset_map = gat.prelude(
        doc_root=doc_root, structure_name=structure_name, target_key=target_key, facet_key=facet_key, command='changes'
    )

    channel = YAML_CHANNEL
    columns_expected = COLUMNS_EXPECTED
    changes_path = asset_map[target_key][facet_key][gat.KEY_CHANGES]
    if str(changes_path).endswith('.json'):
        channel = JSON_CHANNEL

    log.info(f'detected changes channel ({channel}) weaving in from ({changes_path})')
    log.info(f'loading changes from {changes_path=}')
    changes = gat.load_changes(facet_key, target_key, changes_path)
    log.info(f'{changes=}')

    log.info(LOG_SEPARATOR)
    log.info('plausibility tests for changes ...')

    rows = []
    if channel == JSON_CHANNEL:
        for slot, change in enumerate(changes[0]['changes'], start=1):
            if not set(COLUMNS_MINIMAL).issubset(set(change)):
                log.error('unexpected column model!')
                log.error(f'-  expected: ({columns_expected})')
                log.error(f'-   minimal: ({COLUMNS_MINIMAL})')
                log.error(f'- but found: ({change}) for entry #{slot}')
                return 1

        for change in changes[0]['changes']:
            issue, author, summary = change['issue'], change['author'], change['summary']  # type: ignore
            revision = change.get('revision', DEFAULT_REVISION)  # type: ignore
            rows.append(
                ROW_TEMPLATE.replace('issue', issue)
                .replace('revision', revision)
                .replace('author', author)
                .replace('summary', summary)
            )
    else:
        for slot, change in enumerate(changes[0]['changes'], start=1):
            model = sorted(change.keys())  # type: ignore
            if not set(COLUMNS_MINIMAL).issubset(set(model)):
                log.error('unexpected column model!')
                log.error(f'-  expected: ({columns_expected})')
                log.error(f'-   minimal: ({COLUMNS_MINIMAL})')
                log.error(f'- but found: ({model}) in slot {slot}')
                return 1

        for change in changes[0]['changes']:
            author = change['author']  # type: ignore
            issue = change['issue']  # type: ignore
            revision = change.get('revision', DEFAULT_REVISION)  # type: ignore
            summary = change['summary']  # type: ignore
            rows.append(
                ROW_TEMPLATE.replace('issue', issue)
                .replace('revision', revision)
                .replace('author', author)
                .replace('summary', summary)
            )

    publisher_template = template.load_resource(PUBLISHER_TEMPLATE, PUBLISHER_TEMPLATE_IS_EXTERNAL)
    lines = [line.rstrip() for line in publisher_template.split('\n')]

    log.info(LOG_SEPARATOR)
    log.info('weaving in the changes ...')
    for n, line in enumerate(lines):
        if line.strip() == TOKEN:
            lines[n] = GLUE.join(rows)
            break
    if lines[-1]:
        lines.append('\n')
    with open(PUBLISHER_PATH, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))
    log.info(LOG_SEPARATOR)

    return 0
