import pathlib

import liitos.gather as gather

TEST_PREFIX = pathlib.Path('test', 'fixtures', 'basic')


def test_load_structure():
    structure = gather.load_structure(TEST_PREFIX / 'structure.yml')
    assert 'abc' in structure
    assert {
        'mn': {'approvals': 'approvals.json', 'bind': 'bind-mn.txt', 'changes': 'changes.json', 'meta': 'meta-mn.md'}
    } in structure['abc']


def test_targets():
    structure = gather.load_structure(TEST_PREFIX / 'structure.yml')
    targets = gather.targets(structure)
    assert targets == set(['abc'])


def test_facets():
    structure = gather.load_structure(TEST_PREFIX / 'structure.yml')
    facets = gather.facets(structure)
    assert facets == {'abc': {'opq', 'mn'}}


def test_assets():
    structure = gather.load_structure(TEST_PREFIX / 'structure.yml')
    assets = gather.assets(structure)
    assert assets['abc']['mn'] == {
        'approvals': 'approvals.json',
        'bind': 'bind-mn.txt',
        'changes': 'changes.json',
        'meta': 'meta-mn.md',
    }


def test_changes():
    structure = gather.load_structure(TEST_PREFIX / 'structure.yml')
    assets = gather.assets(structure)
    assets['abc']['mn']['changes'] = str(TEST_PREFIX / 'changes.json')
    changes, message = gather.changes('mn', 'abc', assets)
    assert not message
    assert changes == {
        'columns': ['issue', 'author', 'date', 'summary'],
        'rows': [['01', 'One Author', '31.12.2024', 'Initial Issue']],
    }


def test_changes_key_missing():
    structure = gather.load_structure(TEST_PREFIX / 'structure.yml')
    assets = gather.assets(structure)
    del assets['abc']['mn']['changes']
    changes, message = gather.changes('mn', 'abc', assets)
    assert message
    assert not changes


def test_changes_link_missing():
    structure = gather.load_structure(TEST_PREFIX / 'structure.yml')
    assets = gather.assets(structure)
    assets['abc']['mn']['changes'] = str(TEST_PREFIX / 'missing-this-file-for-changes.json')
    changes, message = gather.changes('mn', 'abc', assets)
    assert message
    assert not changes


def test_approvals():
    structure = gather.load_structure(TEST_PREFIX / 'structure.yml')
    assets = gather.assets(structure)
    assets['abc']['mn']['approvals'] = str(TEST_PREFIX / 'approvals.json')
    approvals, message = gather.approvals('mn', 'abc', assets)
    assert not message
    assert approvals == {
        'columns': ['Approvals', 'Name'],
        'rows': [['Author', 'One Author'], ['Review', 'One Reviewer'], ['Approved', 'One Approver']],
    }


def test_approvals_key_missing():
    structure = gather.load_structure(TEST_PREFIX / 'structure.yml')
    assets = gather.assets(structure)
    del assets['abc']['mn']['approvals']
    approvals, message = gather.approvals('mn', 'abc', assets)
    assert message
    assert not approvals


def test_approvals_link_missing():
    structure = gather.load_structure(TEST_PREFIX / 'structure.yml')
    assets = gather.assets(structure)
    assets['abc']['mn']['approvals'] = str(TEST_PREFIX / 'missing-this-file-for-approvals.json')
    approvals, message = gather.approvals('mn', 'abc', assets)
    assert message
    assert not approvals
