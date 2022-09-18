import logging
import os
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
    options = cli.parse_request(['-f', 'mn', '-t', 'abc'])
    assert options.doc_root_pos == ''  # type: ignore
    assert options.doc_root == str(pathlib.Path.cwd())  # type: ignore
    out, err = capsys.readouterr()
    assert not out
    assert not err

def test_parse_request_doc_root_option(capsys):
    options = cli.parse_request(['-d', f'{TEST_PREFIX}', '-f', 'mn', '-t', 'abc'])
    assert options.doc_root_pos == ''  # type: ignore
    assert options.doc_root == f'{TEST_PREFIX}'  # type: ignore
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_parse_request_pos(capsys):
    options = cli.parse_request([f'{TEST_PREFIX}', '-f', 'mn', '-t', 'abc'])
    assert options.doc_root_pos == f'{TEST_PREFIX}'  # type: ignore
    assert options.doc_root == options.doc_root_pos  # type: ignore
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_parse_request_pos_doc_root_not_present(capsys):
    with pytest.raises(SystemExit) as err:
        cli.parse_request([f'{TEST_MAKE_MISSING}{TEST_PREFIX}', '-f', 'mn', '-t', 'abc'])
    assert err.value.code == 2
    out, err = capsys.readouterr()
    assert not out
    assert f'liitos: error: requested tree root at ({TEST_MAKE_MISSING}{TEST_PREFIX}) does not exist' in err


def test_parse_request_pos_doc_root_no_folder(capsys):
    with pytest.raises(SystemExit) as err:
        cli.parse_request([f'{TEST_PREFIX}/{gather.DEFAULT_STRUCTURE_NAME}', '-f', 'mn', '-t', 'abc'])
    assert err.value.code == 2
    out, err = capsys.readouterr()
    assert not out
    assert f'liitos: error: requested tree root at ({TEST_PREFIX}/{gather.DEFAULT_STRUCTURE_NAME}) is not a folder' in err


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


def test_main_empty(capsys):
    code = cli.main([])
    assert not code
    out, err = capsys.readouterr()
    assert 'Root of the document tree to visit.' in out
    assert not err


def test_main(capsys, caplog):
    ole_wd = pathlib.Path.cwd()
    with caplog.at_level(logging.INFO):
        code = cli.main([f'{TEST_PREFIX}', '-f', 'mn', '-t', 'abc'])
    os.chdir(ole_wd)
    assert not code
    assert 'Successful verification' in caplog.text
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_main_wrong_target(capsys, caplog):
    ole_wd = pathlib.Path.cwd()
    with caplog.at_level(logging.ERROR):
        code = cli.main([f'{TEST_PREFIX}', '-f', 'mn', '-t', 'no-target'])
    os.chdir(ole_wd)
    assert code == 1
    assert 'target (no-target) not in' in caplog.text
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_main_wrong_facet(capsys, caplog):
    ole_wd = pathlib.Path.cwd()
    with caplog.at_level(logging.ERROR):
        code = cli.main([f'{TEST_PREFIX}', '-f', 'no-facet', '-t', 'abc'])
    os.chdir(ole_wd)
    assert code == 1
    assert 'facet (no-facet) of target (abc) not in' in caplog.text
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_main_missing_asset(capsys, caplog):
    ole_wd = pathlib.Path.cwd()
    with caplog.at_level(logging.ERROR):
        code = cli.main([f'{TEST_PREFIX}', '-f', 'opq', '-t', 'abc'])
    os.chdir(ole_wd)
    assert code == 1
    assert 'Failed verification with' in caplog.text and 'for facet (opq) of target (abc) is invalid' in caplog.text
    out, err = capsys.readouterr()
    assert not out
    assert not err
