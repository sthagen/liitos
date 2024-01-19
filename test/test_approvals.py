import os
import pathlib

import liitos.approvals as approvals

BASIC_FIXTURE_ROOT = pathlib.Path('test', 'fixtures', 'basic')
EXAMPLE_DEEP_DOC_ROOT = pathlib.Path('example', 'deep')
EXAMPLE_LEGACY_DOC_ROOT = pathlib.Path('example', 'legacy')


def test_approvals():
    parameters = {
        'doc_root': EXAMPLE_DEEP_DOC_ROOT,
        'structure_name': 'structure.yml',
        'target_key': 'prod_kind',
        'facet_key': 'deep',
        'options': {},
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
    }
    restore = os.getcwd()
    assert approvals.weave(**parameters) == 0
    os.chdir(restore)


def test_eastern_scaffold():

    normalized = [{'role': 'role', 'name': 'name'}]
    table = approvals.eastern_scaffold(normalized)
    assert table
    assert 'THE.ROLE0.SLOT' in table
    assert 'THE.NAME0.SLOT' in table


def test_remove_target_region_gen():
    from_cut = '2'
    thru_cut = '4'
    text_lines = ['1', from_cut, '3', thru_cut, '5']
    expected = ['1', '5']
    filtered = list(approvals.remove_target_region_gen(text_lines, from_cut, thru_cut))
    assert filtered == expected
