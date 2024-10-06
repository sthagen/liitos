import os
import pathlib

import liitos.changes as changes
from liitos import EXTERNALS

EXAMPLE_DEEP_DOC_ROOT = pathlib.Path('example', 'deep')
EXAMPLE_LEGACY_DOC_ROOT = pathlib.Path('example', 'legacy')
LAYOUT_ALL_PATH = pathlib.Path('test/fixtures/layout/all.yml')


def test_changes_deep():
    parameters = {
        'doc_root': EXAMPLE_DEEP_DOC_ROOT,
        'structure_name': 'structure.yml',
        'target_key': 'prod_kind',
        'facet_key': 'deep',
        'options': {},
        'externals': EXTERNALS,
    }
    restore = os.getcwd()
    assert changes.weave(**parameters) == 0
    os.chdir(restore)


def test_changes_legacy():
    parameters = {
        'doc_root': EXAMPLE_LEGACY_DOC_ROOT,
        'structure_name': 'structure.yml',
        'target_key': 'prod_kind',
        'facet_key': 'legacy',
        'options': {},
        'externals': EXTERNALS,
    }
    restore = os.getcwd()
    assert changes.weave(**parameters) == 0
    os.chdir(restore)


def test_normalize_json_columns_mismatch():
    changes_in = [{'changes': ['columns', 'are', 'unexpected']}]
    channel = changes.JSON_CHANNEL
    columns_expected = changes.COLUMNS_EXPECTED
    assert changes.normalize(changes=changes_in, channel=channel, columns_expected=columns_expected) == []


def test_normalize_yaml_columns_mismatch():
    changes_in = [{'changes': [{'columns': 'are', 'not': 'expected'}]}]
    channel = changes.YAML_CHANNEL
    columns_expected = changes.COLUMNS_EXPECTED
    assert changes.normalize(changes=changes_in, channel=channel, columns_expected=columns_expected) == []


def test_get_layout_from_path():
    data = changes.get_layout(LAYOUT_ALL_PATH, 'target', 'facet')
    assert data == {'layout': {'global': {'has_approvals': True, 'has_changes': True, 'has_notices': True}}}
