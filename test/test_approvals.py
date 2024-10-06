import os
import pathlib

import liitos.approvals as approvals
from liitos import EXTERNALS

BASIC_FIXTURE_ROOT = pathlib.Path('test', 'fixtures', 'basic')
EXAMPLE_DEEP_DOC_ROOT = pathlib.Path('example', 'deep')
EXAMPLE_LEGACY_DOC_ROOT = pathlib.Path('example', 'legacy')
LAYOUT_ALL_PATH = pathlib.Path('test/fixtures/layout/all.yml')


def test_approvals():
    parameters = {
        'doc_root': EXAMPLE_DEEP_DOC_ROOT,
        'structure_name': 'structure.yml',
        'target_key': 'prod_kind',
        'facet_key': 'deep',
        'options': {},
        'externals': EXTERNALS,
    }
    restore = os.getcwd()
    assert approvals.weave(**parameters) == 0
    os.chdir(restore)


def test_approvals_legacy():
    parameters = {
        'doc_root': EXAMPLE_LEGACY_DOC_ROOT,
        'structure_name': 'structure.yml',
        'target_key': 'prod_kind',
        'facet_key': 'legacy',
        'options': {},
        'externals': EXTERNALS,
    }
    restore = os.getcwd()
    assert approvals.weave(**parameters) == 0
    os.chdir(restore)


def test_normalize_json_columns_mismatch():
    signatures = [{'columns': ['columns', 'are', 'unexpected']}]
    channel = approvals.JSON_CHANNEL
    columns_expected = approvals.COLUMNS_EXPECTED
    assert approvals.normalize(signatures=signatures, channel=channel, columns_expected=columns_expected) == []


def test_normalize_yaml_columns_mismatch():
    signatures = [{'approvals': [{'columns': 'are', 'not': 'expected'}]}]
    channel = approvals.YAML_CHANNEL
    columns_expected = approvals.COLUMNS_EXPECTED
    assert approvals.normalize(signatures=signatures, channel=channel, columns_expected=columns_expected) == []


def test_eastern_scaffold():
    normalized = [{'role': 'role', 'name': 'name'}]
    table = approvals.eastern_scaffold(normalized)
    assert table
    assert 'THE.ORGA0.SLOT' in table
    assert 'THE.ROLE0.SLOT' in table
    assert 'THE.NAME0.SLOT' in table


def test_inject_eastwards():
    lines = ['a']
    expected = [
        'a',
        '% |-- layout east - cut - marker - top -->',
        r'\begin{small}',
        r'\addtolength\aboverulesep{0.15ex}  % extra spacing above and below rules',
        r'\addtolength\belowrulesep{0.35ex}',
        r'\begin{longtable}[]{|',
        r' >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|% <- fixed',
        r'}',
        r'\hline',
        r'\begin{minipage}[b]{\linewidth}\raggedright\ \centering \textbf{\theApprovalsDepartmentLabel}\end{minipage}%',
        r' \\[0.5ex]',
        r'\hline',
        r'\ \mbox{\textbf{\theApprovalsRoleLabel}}%',
        '',
        r' \\[0.5ex]',
        r'\hline',
        r'\ \mbox{\textbf{\theApprovalsNameLabel}}%',
        '',
        r' \\[0.5ex]',
        r'\hline',
        r'\ \mbox{\textbf{Date}} \mbox{\textbf{\ \ \ \ \ \ }} \mbox{\textbf{\ Signature}}%',
        r'',
        r' \\[0.5ex]',
        r'\hline',
        '',
        r'\end{longtable}',
        r'\end{small}',
        '% <-- layout east - cut - marker - bottom --|',
        '',
    ]
    approvals.inject_eastwards(lines, normalized=[], pushdown=42.0)
    assert lines == expected


def test_inject_eastwards_many():
    lines = ['a']
    normalized = [
        {'orga': f'orga{n}', 'role': f'rolen{n}', 'name': f'name{n}'}
        for n in range(1, approvals.EASTERN_TABLE_MAX_MEMBERS + 2)
    ]
    expected = [
        'a',
        '% |-- layout east - cut - marker - top -->',
        r'\begin{small}',
        r'\addtolength\aboverulesep{0.15ex}  % extra spacing above and below rules',
        r'\addtolength\belowrulesep{0.35ex}',
        r'\begin{longtable}[]{|',
        r' >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|% <- fixed',
        r' >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|',
        r' >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|',
        r' >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|',
        r' >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|}',
        r'\hline',
        r'\begin{minipage}[b]{\linewidth}\raggedright\ '
        r'\centering \textbf{\theApprovalsDepartmentLabel}\end{minipage}%',
        r' & \begin{minipage}[b]{\linewidth}\centering\arraybackslash \textbf{orga1}\end{minipage}',
        r' & \begin{minipage}[b]{\linewidth}\centering\arraybackslash \textbf{orga2}\end{minipage}',
        r' & \begin{minipage}[b]{\linewidth}\centering\arraybackslash \textbf{orga3}\end{minipage}',
        r' & \begin{minipage}[b]{\linewidth}\centering\arraybackslash \textbf{orga4}\end{minipage} \\[0.5ex]',
        r'\hline',
        r'\ \mbox{\textbf{\theApprovalsRoleLabel}}%',
        r' & \centering\arraybackslash \textbf{rolen1}',
        r' & \centering\arraybackslash \textbf{rolen2}',
        r' & \centering\arraybackslash \textbf{rolen3}',
        r' & \centering\arraybackslash \textbf{rolen4}',
        r' \\[0.5ex]',
        r'\hline',
        r'\ \mbox{\textbf{\theApprovalsNameLabel}}%',
        r' & \centering\arraybackslash name1',
        r' & \centering\arraybackslash name2',
        r' & \centering\arraybackslash name3',
        r' & \centering\arraybackslash name4',
        r' \\[0.5ex]',
        r'\hline',
        r'\ \mbox{\textbf{Date}} \mbox{\textbf{\ \ \ \ \ \ }} \mbox{\textbf{\ Signature}}%',
        r' & \mbox{}',
        r' & \mbox{}',
        r' & \mbox{}',
        r' & \mbox{}',
        '',
        r' \\[0.5ex]',
        r'\hline',
        '',
        r'\end{longtable}',
        r'\end{small}',
        '% <-- layout east - cut - marker - bottom --|',
        '',
        '% |-- layout east - cut - marker - top -->',
        r'\begin{small}',
        r'\addtolength\aboverulesep{0.15ex}  % extra spacing above and below rules',
        r'\addtolength\belowrulesep{0.35ex}',
        r'\begin{longtable}[]{|',
        r' >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|% <- fixed',
        r' >{\raggedright\arraybackslash}m{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|}',
        r'\hline',
        r'\begin{minipage}[b]{\linewidth}\raggedright\ '
        r'\centering \textbf{\theApprovalsDepartmentLabel}\end{minipage}%',
        r' & \begin{minipage}[b]{\linewidth}\centering\arraybackslash \textbf{orga5}\end{minipage} \\[0.5ex]',
        r'\hline',
        r'\ \mbox{\textbf{\theApprovalsRoleLabel}}%',
        r' & \centering\arraybackslash \textbf{rolen5}',
        r' \\[0.5ex]',
        r'\hline',
        r'\ \mbox{\textbf{\theApprovalsNameLabel}}%',
        r' & \centering\arraybackslash name5',
        r' \\[0.5ex]',
        r'\hline',
        r'\ \mbox{\textbf{Date}} \mbox{\textbf{\ \ \ \ \ \ }} \mbox{\textbf{\ Signature}}%',
        r' & \mbox{}',
        '',
        r' \\[0.5ex]',
        r'\hline',
        '',
        r'\end{longtable}',
        r'\end{small}',
        '% <-- layout east - cut - marker - bottom --|',
        '',
    ]
    approvals.inject_eastwards(lines, normalized=normalized, pushdown=3.14156)
    assert lines == expected


def test_inject_southwards():
    lines = ['a']
    approvals.inject_southwards(lines, rows=[], pushdown=42.0)
    assert lines == ['a', '\n']


def test_get_layout_from_path():
    data = approvals.get_layout(LAYOUT_ALL_PATH, 'target', 'facet')
    assert data == {'layout': {'global': {'has_approvals': True, 'has_changes': True, 'has_notices': True}}}
