import yaml

import liitos.eject as eject
from liitos.meta import MAGIC_OF_TODAY


def test_this_ok(capsys):
    assert eject.this('meta-patch-yaml') == 0
    out, err = capsys.readouterr()
    assert not err
    assert 'patch' in out
    interpret_as_yaml = yaml.safe_load(out)
    assert interpret_as_yaml['document']['patch']['header_date'] == MAGIC_OF_TODAY


def test_this_no_thing(caplog):
    assert eject.this('') == 2
    assert 'eject of template with no name requested' in caplog.text


def test_this_wrong_thing(caplog):
    assert eject.this('unknown-thing') == 2
    assert 'unknown-thing' in caplog.text


def test_this_ambiguous_thing(caplog):
    assert eject.this('meta-') == 2
    assert 'template (meta-) requested - matches (meta-base-yaml, meta-patch-yaml)' in caplog.text


def test_this_write_weird_thing(caplog):
    assert eject.this('meta-b', out='/dev/null') == 0
    assert 'requested writing (templates/meta.yml) to file (null)' in caplog.text


def test_this_write_out_thing(caplog):
    assert eject.this('meta-b', out='/tmp/meta.yml') == 0
