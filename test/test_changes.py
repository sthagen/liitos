import os
import pathlib

import liitos.changes as changes

EXAMPLE_DEEP_DOC_ROOT = pathlib.Path('example', 'deep')
EXAMPLE_LEGACY_DOC_ROOT = pathlib.Path('example', 'legacy')


def test_changes_deep():
    parameters = {
        'doc_root': EXAMPLE_DEEP_DOC_ROOT,
        'structure_name': 'structure.yml',
        'target_key': 'prod_kind',
        'facet_key': 'deep',
        'options': {},
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
    }
    restore = os.getcwd()
    assert changes.weave(**parameters) == 0
    os.chdir(restore)
