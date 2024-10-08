"""Weave the content of the approvals data file into the output structure (for now LaTeX).

# Supported Table Layouts

# Layout `south` (the old default)

| Approvals  | Name         | Date and Signature |
|:-----------|:-------------|:-------------------|
| Author     | Au. Thor.    |                    |
| Reviewer   | Re. Viewer.  |                    |
| Approver   | Ap. Prover.  |                    |
| Authorizer | Au. Thorizer |                    |

Table: The table is simple to grow by appending rows.

The southern layout relies on the skeleton in the bookmatter.tex.in template.

# Layout `east` (the new default)

|     Department      |    AB    |     AB     |     AB     |     AB.      |
|:--------------------|:--------:|:----------:|:----------:|:------------:|
| Approvals           |  Author  |  Reviewer  |  Approver  |  Authorizer  |
| Name                | Au. Thor | Re. Viewer | Ap. Prover | Au. Thorizer |
| Date <br> Signature |          |            |            |              |

Table: This table can only grow towards the right margin and a limit of only 4 role bearers is reasonable

The eastern layout requires more dynamic LaTeX generation and thus generates the construct
from the data inside this module.

For more than 4 role bearers a second table should be placed below the first, to keep the cell content readable.
"""

import pathlib
from typing import Union, no_type_check

import liitos.gather as gat
import liitos.template as tpl
import liitos.tools as too
from liitos import ENCODING, ExternalsType, KNOWN_APPROVALS_STRATEGIES, LOG_SEPARATOR, PathLike, log

TOKEN_EXTRA_PUSHDOWN = r'\ExtraPushdown'  # nosec B105
EXTRA_OFFSET_EM = 24
TOKEN = r'\ \mbox{THE.ROLE.SLOT} & \mbox{THE.NAME.SLOT} & \mbox{} \\[0.5ex]'  # nosec B105
ROW_TEMPLATE = r'\ \mbox{role} & \mbox{name} & \mbox{} \\[0.5ex]'
GLUE = '\n\\hline\n'
FORMAT_DATE = '%d %b %Y'
JSON_CHANNEL = 'json'
YAML_CHANNEL = 'yaml'
COLUMNS_EXPECTED = ['name', 'role', 'orga']
APPROVALS_CUT_MARKER_TOP = '% |-- approvals - cut - marker - top -->'
APPROVALS_CUT_MARKER_BOTTOM = '% <-- approvals - cut - marker - bottom --|'

LAYOUT_SOUTH_CUT_MARKER_TOP = '% |-- layout south - cut - marker - top -->'
LAYOUT_SOUTH_CUT_MARKER_BOTTOM = '% <-- layout south - cut - marker - bottom --|'

EASTERN_TABLE_MAX_MEMBERS = 4
EASTERN_TOTAL_MAX_MEMBERS = EASTERN_TABLE_MAX_MEMBERS * 2

NL = '\n'
BASE_TABLE = r"""% |-- layout east - cut - marker - top -->
\begin{small}
\addtolength\aboverulesep{0.15ex}  % extra spacing above and below rules
\addtolength\belowrulesep{0.35ex}
\begin{longtable}[]{|
 >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|% <- fixed
$HEAD.BLOCK$}
\hline
\begin{minipage}[b]{\linewidth}\raggedright\ \centering \textbf{\theApprovalsDepartmentLabel}\end{minipage}%
$ORGA.BLOCK$ \\[0.5ex]
\hline
\ \mbox{\textbf{\theApprovalsRoleLabel}}%
$ROLE.BLOCK$
 \\[0.5ex]
\hline
\ \mbox{\textbf{\theApprovalsNameLabel}}%
$NAME.BLOCK$
 \\[0.5ex]
\hline
\ \mbox{\textbf{Date}} \mbox{\textbf{\ \ \ \ \ \ }} \mbox{\textbf{\ Signature}}%
$SIGN.BLOCK$
 \\[0.5ex]
\hline

\end{longtable}
\end{small}
% <-- layout east - cut - marker - bottom --|
"""

HEAD_CELL = r' >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|'
ORGA_CELL = r' & \begin{minipage}[b]{\linewidth}\centering\arraybackslash \textbf{THE.ORGA$RANK$.SLOT}\end{minipage}'
ROLE_CELL = r' & \centering\arraybackslash \textbf{THE.ROLE$RANK$.SLOT}'
NAME_CELL = r' & \centering\arraybackslash THE.NAME$RANK$.SLOT'
SIGN_CELL = r' & \mbox{}'


def eastern_scaffold(normalized: list[dict[str, str]]) -> str:
    """Inject the blocks derived from the approvals data to yield the fill-in scaffold."""
    bearers = len(normalized)
    table_max_members = EASTERN_TABLE_MAX_MEMBERS
    total_max_members = EASTERN_TOTAL_MAX_MEMBERS
    if bearers > total_max_members:
        raise NotImplementedError(
            f'Please use southwards layout for more than {total_max_members} role bearers;'
            f' found ({bearers}) entries in approvals data source.'
        )

    # First up to 4 entries got into upper table and final upt to 4 entries (if any) to lower table
    upper, lower = normalized[:table_max_members], normalized[table_max_members:]
    uppers, lowers = len(upper), len(lower)
    log.info(f'SPLIT {uppers}, {lowers}, {bearers}')
    log.info(f'UPPER: {list(range(uppers))}')
    head_block = (f'{HEAD_CELL}{NL}' * uppers).rstrip(NL)
    orga_block = NL.join(ORGA_CELL.replace('$RANK$', str(slot)) for slot in range(uppers))
    role_block = NL.join(ROLE_CELL.replace('$RANK$', str(slot)) for slot in range(uppers))
    name_block = NL.join(NAME_CELL.replace('$RANK$', str(slot)) for slot in range(uppers))
    sign_block = f'{SIGN_CELL}{NL}' * uppers
    upper_table = (
        BASE_TABLE.replace('$HEAD.BLOCK$', head_block)
        .replace('$ORGA.BLOCK$', orga_block)
        .replace('$ROLE.BLOCK$', role_block)
        .replace('$NAME.BLOCK$', name_block)
        .replace('$SIGN.BLOCK$', sign_block)
    )

    for thing in upper_table.split(NL):
        log.debug(thing)

    if not lowers:
        return upper_table

    log.info(f'LOWER: {list(range(uppers, bearers))}')
    head_block = (f'{HEAD_CELL}{NL}' * lowers).rstrip(NL)
    orga_block = NL.join(ORGA_CELL.replace('$RANK$', str(slot)) for slot in range(uppers, bearers))
    role_block = NL.join(ROLE_CELL.replace('$RANK$', str(slot)) for slot in range(uppers, bearers))
    name_block = NL.join(NAME_CELL.replace('$RANK$', str(slot)) for slot in range(uppers, bearers))
    sign_block = f'{SIGN_CELL}{NL}' * lowers

    lower_table = (
        BASE_TABLE.replace('$HEAD.BLOCK$', head_block)
        .replace('$ORGA.BLOCK$', orga_block)
        .replace('$ROLE.BLOCK$', role_block)
        .replace('$NAME.BLOCK$', name_block)
        .replace('$SIGN.BLOCK$', sign_block)
    )

    for thing in lower_table.split(NL):
        log.debug(thing)

    return f'{upper_table}{NL}{lower_table}'


def get_layout(layout_path: PathLike, target_key: str, facet_key: str) -> dict[str, dict[str, dict[str, bool]]]:
    """Boolean layout decisions on bookmatter and publisher page conten.

    Deprecated as the known use cases evolved into a different direction ...
    """
    layout = {'layout': {'global': {'has_approvals': True, 'has_changes': True, 'has_notices': True}}}
    if layout_path:
        log.info(f'loading layout from {layout_path=} for approvals')
        return gat.load_layout(facet_key, target_key, layout_path)[0]  # type: ignore

    log.info('using default layout for approvals')
    return layout


def derive_model(model_path: PathLike) -> tuple[str, list[str]]:
    """Derive the model as channel type and column model from the given path."""
    channel = JSON_CHANNEL if str(model_path).endswith('.json') else YAML_CHANNEL
    columns_expected = ['Approvals', 'Name'] if channel == JSON_CHANNEL else COLUMNS_EXPECTED

    return channel, columns_expected


def columns_are_present(columns_present: list[str], columns_expected: list[str]) -> bool:
    """Ensure the needed columns are present."""
    return all(column in columns_expected for column in columns_present)


@no_type_check
def normalize(signatures: object, channel: str, columns_expected: list[str]) -> list[dict[str, str]]:
    """Normalize the channel specific topology of the model into a logical model.

    On error an empty logical model is returned.
    """
    if channel == JSON_CHANNEL:
        if not columns_are_present(signatures[0]['columns'], columns_expected):
            log.error('unexpected column model!')
            log.error(f'-  expected: ({columns_expected})')
            log.error(f'- but found: ({signatures[0]["columns"]})')
            return []

    if channel == YAML_CHANNEL:
        for slot, approval in enumerate(signatures[0]['approvals'], start=1):
            log.debug(f'{slot=}, {approval=}')
            if not columns_are_present(approval, columns_expected):
                log.error('unexpected column model!')
                log.error(f'-  expected: ({columns_expected})')
                log.error(f'- but found: ({sorted(approval)}) in slot #{slot}')
                return []

    default_orga = r'\theApprovalsDepartmentValue'

    if channel == JSON_CHANNEL:
        return [
            {
                'orga': default_orga,
                'role': role,
                'name': name,
                'orga_x_name': f'{default_orga} / {name}',
            }
            for role, name in signatures[0]['rows']
        ]

    return [
        {
            'orga': approval.get('orga', ''),
            'role': approval['role'],
            'name': approval['name'],
            'orga_x_name': f"{approval.get('orga', default_orga)} / {approval['name']}",
        }
        for approval in signatures[0]['approvals']
    ]


def inject_southwards(lines: list[str], rows: list[str], pushdown: float) -> None:
    """Deploy approvals data per southern layout strategy per updating the lines list in place."""
    for n, line in enumerate(lines):
        if TOKEN_EXTRA_PUSHDOWN in line:
            lines[n] = line.replace(TOKEN_EXTRA_PUSHDOWN, f'{pushdown}em')
            continue
        if line == TOKEN:
            lines[n] = GLUE.join(rows)
            break
    if lines[-1]:  # Need separating empty line?
        lines.append(NL)


def inject_eastwards(lines: list[str], normalized: list[dict[str, str]], pushdown: float) -> None:
    """Deploy approvals data per eastern layout strategy per updating the lines list in place."""
    for n, line in enumerate(lines):
        if TOKEN_EXTRA_PUSHDOWN in line:
            lines[n] = line.replace(TOKEN_EXTRA_PUSHDOWN, f'{pushdown}em')
            break
    hack = eastern_scaffold(normalized)
    log.info('logical model for approvals table is:')
    for slot, entry in enumerate(normalized):
        orga = entry['orga'] if entry['orga'] else r'\theApprovalsDepartmentValue'
        log.info(f'- {entry["role"]} <-- {entry["name"]} (from {orga})')
        hack = (
            hack.replace(f'THE.ORGA{slot}.SLOT', orga)
            .replace(f'THE.ROLE{slot}.SLOT', entry['role'])
            .replace(f'THE.NAME{slot}.SLOT', entry['name'])
        )
    lines.extend(hack.split(NL))
    if lines[-1]:  # pragma: no cover
        lines.append(NL)


def weave(
    doc_root: Union[str, pathlib.Path],
    structure_name: str,
    target_key: str,
    facet_key: str,
    options: dict[str, Union[bool, str]],
    externals: ExternalsType,
) -> int:
    """Map the approvals data to a table on the titlepage."""
    log.info(LOG_SEPARATOR)
    log.info('entered signatures weave function ...')
    structure, asset_map = gat.prelude(
        doc_root=doc_root,
        structure_name=structure_name,
        target_key=target_key,
        facet_key=facet_key,
        command='approvals',
    )

    layout_path = asset_map[target_key][facet_key].get(gat.KEY_LAYOUT, '')
    layout = get_layout(layout_path, target_key=target_key, facet_key=facet_key)
    log.info(f'{layout=}')

    log.info(LOG_SEPARATOR)
    signatures_path = asset_map[target_key][facet_key][gat.KEY_APPROVALS]
    channel, columns_expected = derive_model(signatures_path)
    log.info(f'detected approvals channel ({channel}) weaving in from ({signatures_path})')

    log.info(f'loading signatures from {signatures_path=}')
    signatures = gat.load_approvals(facet_key, target_key, signatures_path)
    log.info(f'{signatures=}')

    log.info(LOG_SEPARATOR)
    log.info('plausibility tests for approvals ...')

    logical_model = normalize(signatures, channel=channel, columns_expected=columns_expected)

    rows = [ROW_TEMPLATE.replace('role', kv['role']).replace('name', kv['name']) for kv in logical_model]

    pushdown = EXTRA_OFFSET_EM - 2 * len(rows)
    log.info(f'calculated extra pushdown to be {pushdown}em')

    bookmatter_template_is_custom = bool(externals['bookmatter']['is_custom'])
    bookmatter_template = str(externals['bookmatter']['id'])
    bookmatter_path = pathlib.Path('render/pdf/bookmatter.tex')

    bookmatter_template = tpl.load_resource(bookmatter_template, bookmatter_template_is_custom)
    lines = [line.rstrip() for line in bookmatter_template.split('\n')]

    if not layout['layout']['global']['has_approvals']:
        log.info('removing approvals from document layout')
        lines = list(too.remove_target_region_gen(lines, APPROVALS_CUT_MARKER_TOP, APPROVALS_CUT_MARKER_BOTTOM))

    log.info(LOG_SEPARATOR)
    log.info(f'weaving in the approvals from {signatures_path}...')
    approvals_strategy = options.get('approvals_strategy', KNOWN_APPROVALS_STRATEGIES[0])
    log.info(f'selected approvals layout strategy is ({approvals_strategy})')
    if approvals_strategy == 'south':
        rows_patch = [
            ROW_TEMPLATE.replace('role', kv['role']).replace('name', kv['orga_x_name']) for kv in logical_model
        ]
        inject_southwards(lines, rows_patch, pushdown)
    else:  # default is east
        lines = list(too.remove_target_region_gen(lines, LAYOUT_SOUTH_CUT_MARKER_TOP, LAYOUT_SOUTH_CUT_MARKER_BOTTOM))
        inject_eastwards(lines, logical_model, pushdown)

    effective_path = pathlib.Path(layout_path).parent / bookmatter_path
    log.info(f'Writing effective bookmatter file to ({effective_path})')
    with open(effective_path, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))
    log.info(LOG_SEPARATOR)

    return 0
