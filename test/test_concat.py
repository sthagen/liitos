import os
import pathlib

import liitos.concat as concat

BASIC_FIXTURE_ROOT = pathlib.Path('test', 'fixtures', 'basic')
EXAMPLE_DEEP_DOC_ROOT = pathlib.Path('example', 'deep')


def test_adapt_image_images():
    collector = []
    assert concat.adapt_image('](x/images/abc.def)', collector, 'x', root='y') == '](images/abc.def)'
    assert collector == [f'{pathlib.Path().cwd()}/x/images/abc.def']


def test_adapt_image_diagrams():
    collector = []
    assert concat.adapt_image('](x/diagrams/abc.def)', collector, 'x', root='y') == '](diagrams/abc.def)'
    assert collector == [f'{pathlib.Path().cwd()}/x/diagrams/abc.def']


def test_adapt_image_other():
    collector = []
    # This may be not what anyone wants ...
    assert (
        concat.adapt_image('](x/other/abc.def)', collector, 'x', root='y')
        == f']({pathlib.Path().cwd()}/x/other/abc.def)'
    )
    assert collector == [f'{pathlib.Path().cwd()}/x/other/abc.def']


def test_concatenate_base():
    parameters = {
        'doc_root': BASIC_FIXTURE_ROOT,
        'structure_name': 'structure.yml',
        'target_key': 'abc',
        'facet_key': 'mn',
        'options': {},
    }
    restore = os.getcwd()
    assert concat.concatenate(**parameters) == 0
    os.chdir(restore)


def test_concatenate_deep():
    parameters = {
        'doc_root': EXAMPLE_DEEP_DOC_ROOT,
        'structure_name': 'structure.yml',
        'target_key': 'prod_kind',
        'facet_key': 'deep',
        'options': {},
    }
    restore = os.getcwd()
    assert concat.concatenate(**parameters) == 0
    os.chdir(restore)
