import pathlib

import pytest

import liitos.cli as cli
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
            gather.KEY_META: 'meta-mn.md',
        }
    }
}
TEST_MAKE_MISSING = 'missing-this-file-for-'


def test_parse_request(capsys):
    options = cli.parse_request(['-d', f'{TEST_PREFIX}', '-f', 'mn', '-t', 'abc'])
    assert options.doc_root_pos == ''  # type: ignore
    assert options.doc_root == f'{TEST_PREFIX}'  # type: ignore
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_parse_request_help(capsys):
    for options in (['-h'], ['--help']):
        with pytest.raises(SystemExit) as err:
            cli.parse_request(options)
        assert not err.value.code
        out, err = capsys.readouterr()
        assert 'Root of the document tree to visit.' in out
        assert not err


def test_parse_request_empty(capsys):
    code = cli.parse_request([])
    assert not code
    out, err = capsys.readouterr()
    assert 'Root of the document tree to visit.' in out
    assert not err
