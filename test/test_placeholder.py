import os
import pathlib
import tempfile

import liitos.placeholder as placeholder
from liitos import ENCODING

ALIEN_PATH = pathlib.Path('test', 'fixtures', 'template', 'alien')
EXTERNAL_PATH = pathlib.Path('test', 'fixtures', 'placeholder', 'this-resource-is-missing.svg')


def test_load_svg_placeholder():
    kind, data = placeholder.load_resource('placeholders/this-resource-is-missing.svg', False)
    assert kind == 'str'
    assert isinstance(data, str)


def test_load_svg_placeholder_external():
    kind, data = placeholder.load_resource(EXTERNAL_PATH, True)
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


def test_dump_placeholder_text():
    base = 'foo'
    suffix = '.svg'
    target_name = f'{base}{suffix}'
    with tempfile.TemporaryDirectory() as tmpdirname:
        code, msg = placeholder.dump_placeholder(pathlib.Path(tmpdirname) / target_name)
    assert code == 0
    assert msg.startswith(f'wrote text mode placeholder matching suffix ({suffix}) derived from target(')
    assert msg.endswith(f'/{target_name})')


def test_dump_placeholder_binary():
    base = 'foo'
    suffix = '.png'
    target_name = f'{base}{suffix}'
    with tempfile.TemporaryDirectory() as tmpdirname:
        code, msg = placeholder.dump_placeholder(pathlib.Path(tmpdirname) / target_name)
    assert code == 0
    assert msg.startswith(f'wrote binary mode placeholder matching suffix ({suffix}) derived from target(')
    assert msg.endswith(f'/{target_name})')


def test_dump_placeholder_miss():
    base = 'foo'
    suffix = '.does-not-exist'
    target_name = f'{base}{suffix}'
    with tempfile.TemporaryDirectory() as tmpdirname:
        code, msg = placeholder.dump_placeholder(pathlib.Path(tmpdirname) / target_name)
    assert code == 1
    assert msg.startswith(f'no placeholder found matching suffix ({suffix}) derived from target(')
    assert msg.endswith(f'/{target_name})')
