import hashlib
import os
import pathlib

import liitos.render as render

BASIC_FIXTURE_ROOT = pathlib.Path('test', 'fixtures', 'basic')
EXAMPLE_DEEP_DOC_ROOT = pathlib.Path('example', 'deep')

EMPTY_SHA512 = (
    'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce'
    '47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e'
)
EMPTY_SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
EMPTY_SHA1 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
EMPTY_MD5 = 'd41d8cd98f00b204e9800998ecf8427e'


def test_hash_file_default_on_empty():
    assert render.hash_file(BASIC_FIXTURE_ROOT / 'empty.md') == EMPTY_SHA512


def test_hash_file_explicit_sha512_on_empty():
    assert render.hash_file(BASIC_FIXTURE_ROOT / 'empty.md', hashlib.sha512) == EMPTY_SHA512


def test_hash_file_explicit_sha256_on_empty():
    assert render.hash_file(BASIC_FIXTURE_ROOT / 'empty.md', hashlib.sha256) == EMPTY_SHA256


def test_hash_file_explicit_sha1_on_empty():
    assert render.hash_file(BASIC_FIXTURE_ROOT / 'empty.md', hashlib.sha1) == EMPTY_SHA1


def test_hash_file_explicit_md5_on_empty():
    assert render.hash_file(BASIC_FIXTURE_ROOT / 'empty.md', hashlib.md5) == EMPTY_MD5


def test_report_taxonomy():
    assert render.report_taxonomy(BASIC_FIXTURE_ROOT / 'empty.md') is None


def test_unified_diff():
    ud = list(render.unified_diff(['foo'], ['bar']))
    assert ud == ['--- before', '+++ after', '@@ -1 +1 @@', '-foo', '+bar']


def test_ren_der():
    parameters = {
        'doc_root': EXAMPLE_DEEP_DOC_ROOT,
        'structure_name': 'structure.yml',
        'target_key': 'prod_kind',
        'facet_key': 'deep',
        'options': {},
    }
    restore = os.getcwd()
    assert render.der(**parameters) == 0
    os.chdir(restore)
