import os
import pathlib
import tempfile

import liitos.template as tpl

ALIEN_PATH = pathlib.Path('test', 'fixtures', 'template', 'alien')
META_PATCH_CONTENT = """\
---
document:
  import: meta.yml
  patch:
    header_date: PUBLICATIONDATE
    header_id: P99999
"""


def test_load_meta_patch():
    assert tpl.load_resource('templates/meta-patch.yml', False) == META_PATCH_CONTENT


def test_load_alien():
    assert int(tpl.load_resource(ALIEN_PATH, True).strip()) == 42


def test_eject():
    with tempfile.TemporaryDirectory() as tmpdirname:
        assert tpl.eject([tmpdirname]) == 0


def test_eject_default():
    prior = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname)
        assert tpl.eject() == 0
    os.chdir(prior)
