import hashlib
import os
import pathlib

import liitos.tools as too

BASIC_FIXTURE_ROOT = pathlib.Path('test', 'fixtures', 'basic')
EXAMPLE_DEEP_DOC_ROOT = pathlib.Path('example', 'deep')

EMPTY_SHA512 = (
    'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce'
    '47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e'
)
EMPTY_SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
EMPTY_SHA1 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
EMPTY_MD5 = 'd41d8cd98f00b204e9800998ecf8427e'

RESTORE = os.getcwd()


def setup():
    os.chdir(RESTORE)


def teardown():
    os.chdir(RESTORE)


def test_hash_file_default_on_empty():
    os.chdir(RESTORE)
    assert too.hash_file(BASIC_FIXTURE_ROOT / 'empty.md') == EMPTY_SHA512
    os.chdir(RESTORE)


def test_hash_file_explicit_sha512_on_empty():
    assert too.hash_file(BASIC_FIXTURE_ROOT / 'empty.md', hashlib.sha512) == EMPTY_SHA512


def test_hash_file_explicit_sha256_on_empty():
    assert too.hash_file(BASIC_FIXTURE_ROOT / 'empty.md', hashlib.sha256) == EMPTY_SHA256


def test_hash_file_explicit_sha1_on_empty():
    assert too.hash_file(BASIC_FIXTURE_ROOT / 'empty.md', hashlib.sha1) == EMPTY_SHA1


def test_hash_file_explicit_md5_on_empty():
    assert too.hash_file(BASIC_FIXTURE_ROOT / 'empty.md', hashlib.md5) == EMPTY_MD5


def test_report_taxonomy():
    assert too.report_taxonomy(BASIC_FIXTURE_ROOT / 'empty.md') is None


def test_unified_diff():
    ud = list(too.unified_diff(['foo'], ['bar']))
    assert ud == ['--- before', '+++ after', '@@ -1 +1 @@', '-foo', '+bar']


def test_remove_target_region_gen():
    from_cut = '2'
    thru_cut = '4'
    text_lines = ['1', from_cut, '3', thru_cut, '5']
    expected = ['1', '5']
    filtered = list(too.remove_target_region_gen(text_lines, from_cut, thru_cut))
    assert filtered == expected


def test_report_missing():
    assert too.report('not known') == 42


def test_report_git():
    assert too.report('git') == 0
