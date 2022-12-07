import logging
import os
import pathlib

import pytest
from typer.testing import CliRunner

import liitos
import liitos.gather as gather
from liitos.cli import app, render

runner = CliRunner()

EXAMPLE_DEEP_PREFIX = pathlib.Path('example', 'deep')
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
OLE_WD = pathlib.Path.cwd()


def setup():
    print(pathlib.Path.cwd(), "before")
    global OLE_WD
    OLE_WD = pathlib.Path.cwd()
    print(pathlib.Path.cwd(), "during")


def teardown():
    os.chdir(OLE_WD)
    print(pathlib.Path.cwd(), "after")


def test_version_ok():
    result = runner.invoke(app, ['version'])
    assert result.exit_code == 0
    assert f'version {liitos.__version__}' in result.stdout


def test_verify():
    result = runner.invoke(app, ['verify', '-f', 'mn', '-t', 'abc'])
    assert result.exit_code == 0


def test_verify_doc_root_option():
    result = runner.invoke(app, ['verify', '-d', f'{TEST_PREFIX}', '-f', 'mn', '-t', 'abc'])
    assert result.exit_code == 0


def test_verify_pos():
    result = runner.invoke(app, ['verify', f'{TEST_PREFIX}', '-f', 'mn', '-t', 'abc'])
    assert result.exit_code == 0


def test_verify_pos_doc_root_not_present():
    result = runner.invoke(app, ['verify', f'{TEST_MAKE_MISSING}{TEST_PREFIX}', '-f', 'mn', '-t', 'abc'])
    assert result.exit_code == 0


def test_verify_pos_doc_root_no_folder():
    bad_location = f'{TEST_PREFIX}/{gather.DEFAULT_STRUCTURE_NAME}'
    result = runner.invoke(app, ['verify', bad_location, '-f', 'mn', '-t', 'abc'])
    assert result.exit_code == 0


def test_help():
    for options in ([], ['-h'], ['--help']):
        result = runner.invoke(app, options)
        assert result.exit_code == 0
        assert 'Verify the structure definition against the file system.' in result.stdout


def test_main():
    result = runner.invoke(app, ['verify', f'{TEST_PREFIX}', '-f', 'mn', '-t', 'abc'])
    assert result.exit_code == 0


def test_main_wrong_target():
    result = runner.invoke(app, ['verify', f'{TEST_PREFIX}', '-f', 'mn', '-t', 'no-target'])
    assert result.exit_code == 0


def test_main_wrong_facet():
    result = runner.invoke(app, ['verify', f'{TEST_PREFIX}', '-f', 'no-facet', '-t', 'abc'])
    assert result.exit_code == 0


def test_main_missing_asset():
    result = runner.invoke(app, ['verify', f'{TEST_PREFIX}', '-f', 'missing', '-t', 'abc'])
    assert result.exit_code == 0
    assert 'requested tree root at (test/fixtures/basic) does not exist' in result.stdout


def test_command_concat():
    result = runner.invoke(app, ['concat', f'{TEST_PREFIX}', '-f', 'mn', '-t', 'abc'])
    assert result.exit_code == 0


def test_command_render_base():
    result = runner.invoke(app, ['render', f'{TEST_PREFIX}', '-f', 'mn', '-t', 'abc'])
    assert result.exit_code == 0


def test_command_changes_base():
    result = runner.invoke(app, ['changes', f'{TEST_PREFIX}', '-f', 'mn', '-t', 'abc'])
    assert result.exit_code == 0


def test_command_approvals_base():
    result = runner.invoke(app, ['approvals', f'{TEST_PREFIX}', '-f', 'mn', '-t', 'abc'])
    assert result.exit_code == 0


def test_command_render_deep():
    result = runner.invoke(
        app, ['render', '-d', f'{EXAMPLE_DEEP_PREFIX}', '-f', 'deep', '-s', 'structure.yml', '-t', 'prod_kind', '-v']
    )
    assert result.exit_code == 0
