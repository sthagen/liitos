import pathlib

import liitos.concat as concat


def test_adapt_image_images():
    collector = []
    assert concat.adapt_image('](x/images/abc.def)', collector, 'x', root='y') == '](images/abc.def)'
    assert collector == [f'{pathlib.Path().cwd()}/x/images/abc.def']


def test_adapt_image_diagrams():
    collector = []
    assert concat.adapt_image('](x/diagrams/abc.def)', collector, 'x', root='y') == '](diagrams/abc.def)'
    assert collector == [f'{pathlib.Path().cwd()}/x/diagrams/abc.def']


def test_adapt_image_other():
    collector = []
    # This may be not what anyone wants ...
    assert concat.adapt_image('](x/other/abc.def)', collector, 'x', root='y') == f']({pathlib.Path().cwd()}/x/other/abc.def)'
    assert collector == [f'{pathlib.Path().cwd()}/x/other/abc.def']
