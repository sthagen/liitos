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


def test_this_wrong_thing(caplog):
    assert eject.this('unknown-thing') == 2
    assert 'unknown-thing' in caplog.text


def test_this_ambiguous_thing(caplog):
    assert eject.this('meta-') == 2
    assert 'template (meta-) requested - matches (meta-base-yaml, meta-patch-yaml)' in caplog.text
