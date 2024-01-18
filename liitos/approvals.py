"""Weave the content of the approvals data file into the output structure (for now LaTeX).

# Supported Table Layouts

# Layout `south` (the old default)

| Approvals  | Name         | Date and Signature |
|:-----------|:-------------|:-------------------|
| Author     | Au. Thor.    |                    |
| Reviewer   | Re. Viewer.  |                    |
| Approver   | Ap. Prover.  |                    |
| Authorizer | Au. Thorizer |                    |

# Layout `east` (the new default)

| Department          |    AB    |     AB     |     AB     |     AB.      |
|:--------------------|:--------:|:----------:|:----------:|:------------:|
| Approvals           |  Author  |  Reviewer  |  Approver  |  Authorizer  |
| Name                | Au. Thor | Re. Viewer | Ap. Prover | Au. Thorizer |
| Date <br> Signature |          |            |            |              |

requires more dynamic LaTeX generation:

```
\begin{longtable}[]{|
  >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|% <- fixed
  >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.1500}}|% at least
  >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.1500}}|% two but
% ... can be more columns for every role
}
\hline
\begin{minipage}[b]{\linewidth}\raggedright
\ \mbox{\textbf{\theDepartmentLabel}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{THE.DEP.SLOT}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{THE.DEP.SLOT}}
...
\end{minipage} \\[0.5ex]
\hline
\ \mbox{\textbf{\theApprovalsRoleLabel}} & \mbox{THE.ROLE.SLOT} & \mbox{THE.ROLE.SLOT} ... \\[0.5ex]
\hline
\ \mbox{\textbf{\theApprovalsNameLabel}} & \mbox{THE.NAME.SLOT} & \mbox{THE.NAME.SLOT} ... \\[0.5ex]
\hline
\ \mbox{\textbf{\theApprovalsDateAndSignatureLabel}} & \mbox{} & \mbox{} ... \\[0.5ex]
\hline

\end{longtable}
```

"""
import os
import pathlib
from typing import Union, no_type_check

import liitos.gather as gat
import liitos.template_loader as template
from liitos import ENCODING, KNOWN_APPROVALS_STRATEGIES, LOG_SEPARATOR, log

PathLike = Union[str, pathlib.Path]

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
APPROVALS_CUT_MARKER_TOP = '% |-- approvals - cut - marker - top -->'
APPROVALS_CUT_MARKER_BOTTOM = '% <-- approvals - cut - marker - bottom --|'

LAYOUT_SOUTH_CUT_MARKER_TOP = '% |-- layout south - cut - marker - top -->'
LAYOUT_SOUTH_CUT_MARKER_BOTTOM = '% <-- layout south - cut - marker - bottom --|'

NL = '\n'
YAGNI = r"""% |-- layout east - cut - marker - top -->
\begin{large}
\addtolength\aboverulesep{0.15ex}  % extra spacing above and below rules
\addtolength\belowrulesep{0.35ex}
\begin{longtable}[]{|
  >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|% <- fixed
  >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|% at least
  >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|% two but
  >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|% two but
% ... can be more columns for every role
}
\hline
\begin{minipage}[b]{\linewidth}\raggedright
\ \mbox{\textbf{\theApprovalsDepartmentLabel}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{\theApprovalsDepartmentValue}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{\theApprovalsDepartmentValue}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{\theApprovalsDepartmentValue}}
% ... can be more columns
\end{minipage} \\[0.5ex]
\hline
\ \mbox{\textbf{\theApprovalsRoleLabel}} & \mbox{THE.ROLE0.SLOT} & \mbox{THE.ROLE1.SLOT} & \mbox{THE.ROLE2.SLOT} \\[0.5ex]
\hline
\ \mbox{\textbf{\theApprovalsNameLabel}} & \mbox{THE.NAME0.SLOT} & \mbox{THE.NAME1.SLOT} & \mbox{THE.NAME2.SLOT} \\[0.5ex]
\hline
\ \mbox{\textbf{Date}} \mbox{\textbf{\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ }} \mbox{\textbf{\ Signature}} \mbox{\textbf{\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ }} & \mbox{} & \mbox{} & \mbox{} \\[0.5ex]
\hline

\end{longtable}
\end{large}
% <-- layout east - cut - marker - bottom --|
"""


def get_layout(layout_path: PathLike, target_key: str, facet_key: str) -> dict[str, dict[str, dict[str, bool]]]:
    """DRY."""
    layout = {'layout': {'global': {'has_approvals': True, 'has_changes': True, 'has_notices': True}}}
    if layout_path:
        log.info(f'loading layout from {layout_path=} for approvals')
        layout = gat.load_layout(facet_key, target_key, layout_path)[0]  # type: ignore
    else:
        log.info('using default layout for approvals')
    return layout


def derive_model(model_path: PathLike) -> tuple[str, list[str]]:
    """Derive the model as channel type and column model from the given path."""
    channel = JSON_CHANNEL if str(model_path).endswith('.json') else YAML_CHANNEL
    columns_expected = ['Approvals', 'Name'] if channel == JSON_CHANNEL else COLUMNS_EXPECTED

    return channel, columns_expected


@no_type_check
def normalize(signatures: object, channel: str, columns_expected: list[str]) -> list[dict[str, str]]:
    """Normalize the channel specific topology of the model into a logical model.

    On error an empty logical model is returned.
    """
    if channel == JSON_CHANNEL:
        if signatures[0]['columns'] != columns_expected:
            log.error('unexpected column model!')
            log.error(f'-  expected: ({columns_expected})')
            log.error(f'- but found: ({signatures[0]["columns"]})')
            return []

    if channel == YAML_CHANNEL:
        for slot, approval in enumerate(signatures[0]['approvals'], start=1):
            log.debug(f'{slot=}, {approval=}')
            if sorted(approval) != sorted(columns_expected):
                log.error('unexpected column model!')
                log.error(f'-  expected: ({columns_expected})')
                log.error(f'- but found: ({sorted(approval)}) in slot #{slot}')
                return []

    if channel == JSON_CHANNEL:
        return [{'role': role, 'name': name} for role, name in signatures[0]['rows']]

    return [{'role': approval['role'], 'name': approval['name']} for approval in signatures[0]['approvals']]


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
    hack = YAGNI
    log.info('logical model for approvals table is:')
    for slot, entry in enumerate(normalized):
        log.info(f'- {entry["role"]} <-- {entry["name"]}')
        hack = hack.replace(f'THE.ROLE{slot}.SLOT', entry['role']).replace(f'THE.NAME{slot}.SLOT', entry['name'])
    lines.extend(hack.split(NL))
    if lines[-1]:  # Need separating empty line?
        lines.append(NL)


@no_type_check
def remove_target_region_gen(text_lines: list[str], from_cut: str, thru_cut: str):
    """Return generator that yields only the lines beyond the cut mark region skipping lines in [from, thru]."""
    in_section = False
    for line in text_lines:
        if not in_section:
            if from_cut in line:
                in_section = True
                continue
        if in_section:
            if thru_cut in line:
                in_section = False
            continue
        yield line


def weave(
    doc_root: Union[str, pathlib.Path],
    structure_name: str,
    target_key: str,
    facet_key: str,
    options: dict[str, Union[bool, str]],
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

    bookmatter_template = template.load_resource(BOOKMATTER_TEMPLATE, BOOKMATTER_TEMPLATE_IS_EXTERNAL)
    lines = [line.rstrip() for line in bookmatter_template.split('\n')]

    if not layout['layout']['global']['has_approvals']:
        log.info('removing approvals from document layout')
        lines = list(remove_target_region_gen(lines, APPROVALS_CUT_MARKER_TOP, APPROVALS_CUT_MARKER_BOTTOM))

    log.info(LOG_SEPARATOR)
    log.info(f'weaving in the approvals from {signatures_path}...')
    approvals_strategy = options.get('approvals_strategy', KNOWN_APPROVALS_STRATEGIES[0])
    log.info(f'selected approvals layout strategy is ({approvals_strategy})')
    if approvals_strategy == 'south':
        inject_southwards(lines, rows, pushdown)
    else:  # default is east
        lines = list(remove_target_region_gen(lines, LAYOUT_SOUTH_CUT_MARKER_TOP, LAYOUT_SOUTH_CUT_MARKER_BOTTOM))
        inject_eastwards(lines, logical_model, pushdown)

    effective_path = pathlib.Path(layout_path).parent / BOOKMATTER_PATH
    log.info(f'Writing effective bookmatter file to ({effective_path})')
    with open(effective_path, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))
    log.info(LOG_SEPARATOR)

    return 0
