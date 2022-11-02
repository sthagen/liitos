import copy
import os
import pathlib

import liitos.gather as gather

TEST_PREFIX = pathlib.Path('test', 'fixtures', 'basic')
DEFAULT_STRUCTURE_PATH = TEST_PREFIX / gather.DEFAULT_STRUCTURE_NAME
TEST_TARGET = 'abc'
TEST_FACET = 'mn'
TEST_STRUCTURE = {
    TEST_TARGET: {
        TEST_FACET: {
            gather.KEY_APPROVALS: 'approvals.json',
            gather.KEY_BIND: 'bind-mn.txt',
            gather.KEY_CHANGES: 'changes.json',
            gather.KEY_META: 'meta-mn.yml',
        }
    }
}
TEST_MAKE_MISSING = 'missing-this-file-for-'


def test_load_structure():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    assert TEST_TARGET in structure
    assert TEST_STRUCTURE[TEST_TARGET] in structure[TEST_TARGET]


def test_targets():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    targets = gather.targets(structure)
    assert targets == set([TEST_TARGET])


def test_facets():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    facets = gather.facets(structure)
    assert facets == {TEST_TARGET: {'missing', 'opq', TEST_FACET}}


def test_assets():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    assets = gather.assets(structure)
    assert assets[TEST_TARGET][TEST_FACET] == TEST_STRUCTURE[TEST_TARGET][TEST_FACET]


def test_changes():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    assets = gather.assets(structure)
    assets[TEST_TARGET][TEST_FACET][gather.KEY_CHANGES] = str(TEST_PREFIX / 'changes.json')
    changes, message = gather.changes(TEST_FACET, TEST_TARGET, assets)
    assert not message
    assert changes == {
        'columns': ['issue', 'author', 'date', 'summary'],
        'rows': [['01', 'One Author', '31.12.2024', 'Initial Issue']],
    }


def test_changes_key_missing():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    assets = gather.assets(structure)
    del assets[TEST_TARGET][TEST_FACET][gather.KEY_CHANGES]
    changes, message = gather.changes(TEST_FACET, TEST_TARGET, assets)
    assert message
    assert not changes


def test_changes_link_missing():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    assets = gather.assets(structure)
    assets[TEST_TARGET][TEST_FACET][gather.KEY_CHANGES] = str(TEST_PREFIX / f'{TEST_MAKE_MISSING}changes.json')
    changes, message = gather.changes(TEST_FACET, TEST_TARGET, assets)
    assert message
    assert not changes


def test_approvals():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    assets = gather.assets(structure)
    assets[TEST_TARGET][TEST_FACET][gather.KEY_APPROVALS] = str(TEST_PREFIX / 'approvals.json')
    approvals, message = gather.approvals(TEST_FACET, TEST_TARGET, assets)
    assert not message
    assert approvals == {
        'columns': ['Approvals', 'Name'],
        'rows': [['Author', 'One Author'], ['Review', 'One Reviewer'], ['Approved', 'One Approver']],
    }


def test_approvals_key_missing():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    assets = gather.assets(structure)
    del assets[TEST_TARGET][TEST_FACET][gather.KEY_APPROVALS]
    approvals, message = gather.approvals(TEST_FACET, TEST_TARGET, assets)
    assert message
    assert not approvals


def test_approvals_link_missing():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    assets = gather.assets(structure)
    assets[TEST_TARGET][TEST_FACET][gather.KEY_APPROVALS] = str(TEST_PREFIX / f'{TEST_MAKE_MISSING}approvals.json')
    approvals, message = gather.approvals(TEST_FACET, TEST_TARGET, assets)
    assert message
    assert not approvals


def test_meta_key_missing():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    assets = gather.assets(structure)
    del assets[TEST_TARGET][TEST_FACET][gather.KEY_META]
    meta, message = gather.meta(TEST_FACET, TEST_TARGET, assets)
    assert message
    assert not meta


def test_meta_link_missing():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    assets = gather.assets(structure)
    assets[TEST_TARGET][TEST_FACET][gather.KEY_META] = str(TEST_PREFIX / f'{TEST_MAKE_MISSING}meta.json')
    meta, message = gather.meta(TEST_FACET, TEST_TARGET, assets)
    assert message
    assert not meta


def test_binder_key_missing():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    assets = gather.assets(structure)
    del assets[TEST_TARGET][TEST_FACET][gather.KEY_BIND]
    binder, message = gather.binder(TEST_FACET, TEST_TARGET, assets)
    assert message
    assert not binder


def test_binder_link_missing():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    assets = gather.assets(structure)
    assets[TEST_TARGET][TEST_FACET][gather.KEY_BIND] = str(TEST_PREFIX / f'{TEST_MAKE_MISSING}bind-mn.txt')
    binder, message = gather.binder(TEST_FACET, TEST_TARGET, assets)
    assert message
    assert not binder


def test_binder():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    assets = gather.assets(structure)
    assets[TEST_TARGET][TEST_FACET][gather.KEY_BIND] = str(TEST_PREFIX / f'bind-{TEST_FACET}.txt')
    binder, message = gather.binder(TEST_FACET, TEST_TARGET, assets)
    assert not message
    assert binder == ['head.md', 'body.md']


def test_meta():
    structure = gather.load_structure(DEFAULT_STRUCTURE_PATH)
    assets = gather.assets(structure)
    assets[TEST_TARGET][TEST_FACET][gather.KEY_META] = str(TEST_PREFIX / f'meta-{TEST_FACET}.md')
    meta, message = gather.meta(TEST_FACET, TEST_TARGET, assets)
    assert not message
    assert meta == {'setting': 'value'}


def test_verify_target():
    targets = set([TEST_TARGET])
    predicate, message = gather.verify_target(TEST_TARGET, targets)
    assert not message
    assert predicate


def test_verify_target_not():
    targets = set([TEST_TARGET])
    predicate, message = gather.verify_target(f'{TEST_MAKE_MISSING}{TEST_TARGET}', targets)
    assert message == f'target ({TEST_MAKE_MISSING}{TEST_TARGET}) not in {sorted(targets)}'
    assert not predicate


def test_verify_facet():
    facets = {TEST_TARGET: set([TEST_FACET])}
    predicate, message = gather.verify_facet(TEST_FACET, TEST_TARGET, facets)
    assert not message
    assert predicate


def test_verify_facet_not():
    facets = {TEST_TARGET: set([TEST_FACET])}
    predicate, message = gather.verify_facet(f'{TEST_MAKE_MISSING}{TEST_FACET}', TEST_TARGET, facets)
    expected = (
        f'facet ({TEST_MAKE_MISSING}{TEST_FACET})' f' of target ({TEST_TARGET}) not in {sorted(facets[TEST_TARGET])}'
    )
    assert message == expected
    assert not predicate


def test_verify_asset_keys():
    assets = copy.deepcopy(TEST_STRUCTURE)
    predicate, message = gather.verify_asset_keys(TEST_FACET, TEST_TARGET, assets)
    assert not message
    assert predicate


def test_verify_asset_keys_not():
    assets = copy.deepcopy(TEST_STRUCTURE)
    del assets[TEST_TARGET][TEST_FACET][gather.KEY_BIND]
    predicate, message = gather.verify_asset_keys(TEST_FACET, TEST_TARGET, assets)
    expected = (
        f'keys in {sorted(gather.KEYS_REQUIRED)}' f' for facet ({TEST_FACET}) of target ({TEST_TARGET}) are missing'
    )
    assert message == expected
    assert not predicate


def test_verify_asset_links():
    assets = copy.deepcopy(TEST_STRUCTURE)
    ole_place = pathlib.Path.cwd()
    os.chdir(TEST_PREFIX)
    predicate, message = gather.verify_asset_links(TEST_FACET, TEST_TARGET, assets)
    os.chdir(ole_place)
    assert not message
    assert predicate


def test_verify_asset_links_no_key():
    assets = copy.deepcopy(TEST_STRUCTURE)
    del assets[TEST_TARGET][TEST_FACET][gather.KEY_BIND]
    ole_place = pathlib.Path.cwd()
    os.chdir(TEST_PREFIX)
    predicate, message = gather.verify_asset_links(TEST_FACET, TEST_TARGET, assets)
    os.chdir(ole_place)
    expected = (
        f'keys in {sorted(gather.KEYS_REQUIRED)}' f' for facet ({TEST_FACET}) of target ({TEST_TARGET}) are missing'
    )
    assert message == expected
    assert not predicate


def test_verify_asset_links_no_link():
    assets = copy.deepcopy(TEST_STRUCTURE)
    bad_link_value = f'{TEST_MAKE_MISSING}bind-{TEST_FACET}.txt'
    assets[TEST_TARGET][TEST_FACET][gather.KEY_BIND] = bad_link_value
    ole_place = pathlib.Path.cwd()
    os.chdir(TEST_PREFIX)
    predicate, message = gather.verify_asset_links(TEST_FACET, TEST_TARGET, assets)
    os.chdir(ole_place)
    expected = f'bind asset link ({bad_link_value})' f' for facet ({TEST_FACET}) of target ({TEST_TARGET}) is invalid'
    assert message == expected
    assert not predicate


def test_verify_assets():
    assets = copy.deepcopy(TEST_STRUCTURE)
    ole_place = pathlib.Path.cwd()
    os.chdir(TEST_PREFIX)
    predicate, message = gather.verify_assets(TEST_FACET, TEST_TARGET, assets)
    os.chdir(ole_place)
    assert not message
    assert predicate


def test_verify_assets_no_key():
    assets = copy.deepcopy(TEST_STRUCTURE)
    del assets[TEST_TARGET][TEST_FACET][gather.KEY_BIND]
    ole_place = pathlib.Path.cwd()
    os.chdir(TEST_PREFIX)
    predicate, message = gather.verify_assets(TEST_FACET, TEST_TARGET, assets)
    os.chdir(ole_place)
    expected = (
        f'keys in {sorted(gather.KEYS_REQUIRED)}' f' for facet ({TEST_FACET}) of target ({TEST_TARGET}) are missing'
    )
    assert message == expected
    assert not predicate


def test_verify_assets_no_link():
    assets = copy.deepcopy(TEST_STRUCTURE)
    bad_link_value = f'{TEST_MAKE_MISSING}bind-{TEST_FACET}.txt'
    assets[TEST_TARGET][TEST_FACET][gather.KEY_BIND] = bad_link_value
    ole_place = pathlib.Path.cwd()
    os.chdir(TEST_PREFIX)
    predicate, message = gather.verify_assets(TEST_FACET, TEST_TARGET, assets)
    os.chdir(ole_place)
    expected = f'bind asset link ({bad_link_value}) for facet ({TEST_FACET}) of target ({TEST_TARGET}) is invalid'
    assert message == expected
    assert not predicate


def test_verify_assets_empty_changes():
    assets = copy.deepcopy(TEST_STRUCTURE)
    link_value_to_bad_content = 'no-changes.json'
    assets[TEST_TARGET][TEST_FACET][gather.KEY_CHANGES] = link_value_to_bad_content
    ole_place = pathlib.Path.cwd()
    os.chdir(TEST_PREFIX)
    predicate, message = gather.verify_assets(TEST_FACET, TEST_TARGET, assets)
    os.chdir(ole_place)
    expected = f'changes asset for facet ({TEST_FACET}) of target ({TEST_TARGET}) is invalid'
    assert message == expected
    assert not predicate
