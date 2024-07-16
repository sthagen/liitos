import os
import pathlib

import liitos.render as render
from liitos import FILTER_CS_LIST

BASIC_FIXTURE_ROOT = pathlib.Path('test', 'fixtures', 'basic')
EXAMPLE_DEEP_DOC_ROOT = pathlib.Path('example', 'deep')

RESTORE = os.getcwd()


def setup():
    os.chdir(RESTORE)


def teardown():
    os.chdir(RESTORE)


def test_ren_der():
    parameters = {
        'doc_root': EXAMPLE_DEEP_DOC_ROOT,
        'structure_name': 'structure.yml',
        'target_key': 'prod_kind',
        'facet_key': 'deep',
        'options': {
            'filter_cs_list': FILTER_CS_LIST,
        },
    }
    os.chdir(RESTORE)
    assert render.der(**parameters) == 0
    os.chdir(RESTORE)
