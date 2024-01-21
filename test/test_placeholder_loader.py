import os
import pathlib
import tempfile

import liitos.placeholder_loader as placeholder
from liitos import ENCODING

ALIEN_PATH = pathlib.Path('test', 'fixtures', 'templates', 'alien')


def test_load_svg_placeholder():
    kind, data = placeholder.load_resource('placeholders/this-resource-is-missing.svg', False)
    assert kind == 'str'
    assert isinstance(data, str)


def test_load_alien():
    kind, data = placeholder.load_resource(ALIEN_PATH, True)
    assert kind == 'bytes'
    assert isinstance(data, bytes)
    assert int(data.decode(encoding=ENCODING).strip()) == 42


def test_eject():
    with tempfile.TemporaryDirectory() as tmpdirname:
        assert placeholder.eject([tmpdirname]) == 0


def test_eject_default():
    prior = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname)
        assert placeholder.eject() == 0
    os.chdir(prior)
