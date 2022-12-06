import tempfile

import liitos.template_loader as template

META_PATCH_CONTENT = """\
---
document:
  import: meta.yml
  patch:
    header_id: P99999
    header_date: PUBLICATIONDATE
"""


def test_load_meta_patch():
    assert template.load_resource('templates/meta-patch.yml', False) == META_PATCH_CONTENT


def test_eject():
    with tempfile.TemporaryDirectory() as tmpdirname:
        assert template.eject([tmpdirname]) == 0
