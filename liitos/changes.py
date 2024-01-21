"""Weave the content of the changes data file into the output structure (for now LaTeX)."""
import os
import pathlib
from typing import Generator, Union, no_type_check

import liitos.gather as gat
import liitos.template_loader as template
import liitos.tools as too
from liitos import ENCODING, LOG_SEPARATOR, log

PathLike = Union[str, pathlib.Path]

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
CUT_MARKER_CHANGES_TOP = '% |-- changes - cut - marker - top -->'
CUT_MARKER_CHANGES_BOTTOM = '% <-- changes - cut - marker - bottom --|'
CUT_MARKER_NOTICES_TOP = '% |-- notices - cut - marker - top -->'
CUT_MARKER_NOTICES_BOTTOM = '% <-- notices - cut - marker - bottom --|'
TOKEN_ADJUSTED_PUSHDOWN = r'\AdustedPushdown'  # nosec B105
DEFAULT_ADJUSTED_PUSHDOWN_VALUE = 14

NL = '\n'


def get_layout(layout_path: PathLike, target_key: str, facet_key: str) -> dict[str, dict[str, dict[str, bool]]]:
    """Boolean layout decisions on bookmatter and publisher page conten.

    Deprecated as the known use cases evolved into a different direction ...
    """
    layout = {'layout': {'global': {'has_approvals': True, 'has_changes': True, 'has_notices': True}}}
    if layout_path:
        log.info(f'loading layout from {layout_path=} for changes and notices')
        return gat.load_layout(facet_key, target_key, layout_path)[0]  # type: ignore

    log.info('using default layout for approvals')
    return layout


def derive_model(model_path: PathLike) -> tuple[str, list[str]]:
    """Derive the model as channel type and column model from the given path."""
    channel = JSON_CHANNEL if str(model_path).endswith('.json') else YAML_CHANNEL
    columns_expected = COLUMNS_MINIMAL if channel == JSON_CHANNEL else COLUMNS_EXPECTED

    return channel, columns_expected


def columns_are_present(columns_present: list[str], columns_expected: list[str]) -> bool:
    """Ensure the needed columns are present."""
    return all(column in columns_expected for column in columns_present)


@no_type_check
def normalize(changes: object, channel: str, columns_expected: list[str]) -> list[dict[str, str]]:
    """Normalize the channel specific topology of the model into a logical model.

    On error an empty logical model is returned.
    """
    if channel == JSON_CHANNEL:
        for slot, change in enumerate(changes[0]['changes'], start=1):
            if not set(columns_expected).issubset(set(change)):
                log.error('unexpected column model!')
                log.error(f'-  expected: ({columns_expected})')
                log.error(f'-   minimal: ({COLUMNS_MINIMAL})')
                log.error(f'- but found: ({change}) for entry #{slot}')
                return []

    if channel == YAML_CHANNEL:
        for slot, change in enumerate(changes[0]['changes'], start=1):
            model = sorted(change.keys())
            if not set(COLUMNS_MINIMAL).issubset(set(model)):
                log.error('unexpected column model!')
                log.error(f'-  expected: ({columns_expected})')
                log.error(f'-   minimal: ({COLUMNS_MINIMAL})')
                log.error(f'- but found: ({model}) in slot {slot}')
                return []

    model = []
    if channel == JSON_CHANNEL:
        for change in changes[0]['changes']:
            issue, author, summary = change['issue'], change['author'], change['summary']
            revision = change.get('revision', DEFAULT_REVISION)
            model.append({'issue': issue, 'revision': revision, 'author': author, 'summary': summary})
        return model

    for change in changes[0]['changes']:
        author = change['author']
        issue = change['issue']
        revision = change.get('revision', DEFAULT_REVISION)
        summary = change['summary']
        model.append({'issue': issue, 'revision': revision, 'author': author, 'summary': summary})

    return model


def adjust_pushdown_gen(text_lines: list[str], pushdown: float) -> Generator[str, None, None]:
    """Update the pushdown line filtering the incoming lines."""
    for line in text_lines:
        if TOKEN_ADJUSTED_PUSHDOWN in line:
            line = line.replace(TOKEN_ADJUSTED_PUSHDOWN, f'{pushdown}em')
            log.info(f'set adjusted pushdown value {pushdown}em')
        yield line


def weave(
    doc_root: Union[str, pathlib.Path],
    structure_name: str,
    target_key: str,
    facet_key: str,
    options: dict[str, Union[bool, str]],
) -> int:
    """Later alligator."""
    log.info(LOG_SEPARATOR)
    log.info('entered changes weave function ...')
    structure, asset_map = gat.prelude(
        doc_root=doc_root, structure_name=structure_name, target_key=target_key, facet_key=facet_key, command='changes'
    )

    layout_path = asset_map[target_key][facet_key].get(gat.KEY_LAYOUT, '')
    layout = get_layout(layout_path, target_key=target_key, facet_key=facet_key)
    log.info(f'{layout=}')

    log.info(LOG_SEPARATOR)
    changes_path = asset_map[target_key][facet_key][gat.KEY_CHANGES]
    channel, columns_expected = derive_model(changes_path)
    log.info(f'detected changes channel ({channel}) weaving in from ({changes_path})')

    log.info(f'loading changes from {changes_path=}')
    changes = gat.load_changes(facet_key, target_key, changes_path)
    log.info(f'{changes=}')

    log.info(LOG_SEPARATOR)
    log.info('plausibility tests for changes ...')

    logical_model = normalize(changes, channel=channel, columns_expected=columns_expected)

    rows = [
        ROW_TEMPLATE.replace('issue', kv['issue'])
        .replace('revision', kv['revision'])
        .replace('author', kv['author'])
        .replace('summary', kv['summary'])
        for kv in logical_model
    ]

    pushdown = DEFAULT_ADJUSTED_PUSHDOWN_VALUE
    log.info(f'calculated adjusted pushdown to be {pushdown}em')

    publisher_template = template.load_resource(PUBLISHER_TEMPLATE, PUBLISHER_TEMPLATE_IS_EXTERNAL)
    lines = [line.rstrip() for line in publisher_template.split(NL)]

    if any(TOKEN_ADJUSTED_PUSHDOWN in line for line in lines):
        lines = list(adjust_pushdown_gen(lines, pushdown))
    else:
        log.error(f'token ({TOKEN_ADJUSTED_PUSHDOWN}) not found - template mismatch')

    if not layout['layout']['global']['has_changes']:
        log.info('removing changes from document layout')
        lines = list(too.remove_target_region_gen(lines, CUT_MARKER_CHANGES_TOP, CUT_MARKER_CHANGES_BOTTOM))

    if not layout['layout']['global']['has_notices']:
        log.info('removing notices from document layout')
        lines = list(too.remove_target_region_gen(lines, CUT_MARKER_NOTICES_TOP, CUT_MARKER_NOTICES_BOTTOM))

    log.info(LOG_SEPARATOR)
    log.info('weaving in the changes from {changes_path} ...')
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
