import os
import pathlib

import liitos.concat as concat

BASIC_FIXTURE_ROOT = pathlib.Path('test', 'fixtures', 'basic')
EXAMPLE_DEEP_DOC_ROOT = pathlib.Path('example', 'deep')


def test_adapt_image_images():
    collector = []
    caption = 'Cap...'
    img_path = 'x/images/abc.def'
    alt_text = '"Alt..."'
    text = f'![{caption}]({img_path} {alt_text})'
    assert concat.adapt_image(text, collector, 'x', root='y') == f'![{caption}](images/abc.def {alt_text})'
    assert collector == [f'{pathlib.Path().cwd()}/x/images/abc.def']


def test_adapt_image_diagrams():
    collector = []
    caption = 'Cap...'
    img_path = 'x/diagrams/abc.def'
    alt_text = '"Alt..."'
    text = f'![{caption}]({img_path} {alt_text})'
    assert concat.adapt_image(text, collector, 'x', root='y') == f'![{caption}](diagrams/abc.def {alt_text})'
    assert collector == [f'{pathlib.Path().cwd()}/x/diagrams/abc.def']


def test_adapt_image_other():
    collector = []
    # This may be not what anyone wants ...
    caption = 'Cap...'
    img_path = 'x/other/abc.def'
    alt_text = '"Alt..."'
    text = f'![{caption}]({img_path} {alt_text})'
    assert (
        concat.adapt_image(text, collector, 'x', root='y')
        == f'![{caption}]({pathlib.Path().cwd()}/x/other/abc.def {alt_text})'
    )
    assert collector == [f'{pathlib.Path().cwd()}/x/other/abc.def']


def test_adapt_image_dot_dot():
    collector = []
    # eg. example/deep/part/x.md has source ref to ../other/abc.def which is example/deep/other/abc.def
    caption = 'Cap...'
    img_path = '../other/abc.def'
    alt_text = '"Alt..."'
    text = f'![{caption}]({img_path} {alt_text})'
    assert (
        concat.adapt_image(text, collector, 'part/x.md', root='y')
        == f'![{caption}]({pathlib.Path().cwd()}/other/abc.def {alt_text})'
    )
    assert collector == [f'{pathlib.Path().cwd()}/other/abc.def']


def test_adapt_image_dot_dot_complete():
    """From example/deep/other/b.md."""
    collector = []
    caption = 'Caption Text Dot Dot Lime'
    img_path = '../images/lime.png'
    alt_text = '"Alt Text Dot Dot Lime"'
    text = f'![{caption}]({img_path} {alt_text})'
    assert concat.adapt_image(text, collector, 'other/b.md', root='y') == f'![{caption}](images/lime.png {alt_text})'
    assert collector == [f'{pathlib.Path().cwd()}/images/lime.png']


def test_parse_markdown_image():
    cases = {
        '! [Caption Text Red](images/red.png "Alt Text Red")': (
            '',
            '',
            '',
            '! [Caption Text Red](images/red.png "Alt Text Red")',
        ),
        ' ![Caption Text Red](images/red.png "Alt Text Red")': (
            '',
            '',
            '',
            ' ![Caption Text Red](images/red.png "Alt Text Red")',
        ),
        '![Caption Text Red] (images/red.png "Alt Text Red")': (
            '',
            '',
            '',
            '![Caption Text Red] (images/red.png "Alt Text Red")',
        ),
        '![ccc(sss "aaa") <!-- rest -->  ': (
            '',
            '',
            '',
            '![ccc(sss "aaa") <!-- rest -->  ',
        ),
        r'![cc\[c](sss "aaa") <!-- rest -->  ': (
            r'cc\[c',
            'sss',
            'aaa',
            ' <!-- rest -->  ',
        ),
        '![ccc](sss "aaa" <!-- rest -->  ': (
            '',
            '',
            '',
            '![ccc](sss "aaa" <!-- rest -->  ',
        ),
        '![ccc](sss)': (
            'ccc',
            'sss',
            '',
            '',
        ),
        '![cc(c](sss SSS "aaa") <!-- rest -->  ': (
            '',
            '',
            '',
            '![cc(c](sss SSS "aaa") <!-- rest -->  ',
        ),
        '![](sss "a(a)a")': (
            'INJECTED-CAP-TEXT-TO-MARK-MISSING-CAPTION-IN-OUTPUT',
            'sss',
            'a(a)a',
            '',
        ),
        '![captain](sss "a(a)a")': (
            'captain',
            'sss',
            'a(a)a',
            '',
        ),
        # This is not looking like anyone would want their alt text to be cut ...
        '![](sss "a(a)a" <!-- a remark you made -->': (
            'INJECTED-CAP-TEXT-TO-MARK-MISSING-CAPTION-IN-OUTPUT',
            'sss',
            'a(a',
            'a" <!-- a remark you made -->',
        ),
        # This is also not looking like anyone would want their alt text to be cut ...
        '![bla](sss "a(a)a"': (
            'bla',
            'sss',
            'a(a',
            'a"',
        ),
        '![Caption Text Red](images/red.png "Alt Text Red")': (
            'Caption Text Red',
            'images/red.png',
            'Alt Text Red',
            '',
        ),
        '![Caption Text Dot Dot Lime](../images/lime.png "Alt Text Dot Dot Lime")': (
            'Caption Text Dot Dot Lime',
            '../images/lime.png',
            'Alt Text Dot Dot Lime',
            '',
        ),
        '![Caption Text for SVG](/diagrams/squares-and-edges.svg) <!-- a comment -->  ': (
            'Caption Text for SVG',
            '/diagrams/squares-and-edges.svg',
            '',
            ' <!-- a comment -->  ',
        ),
        '![Caption Text for app specific SVG](diagrams/nuts-and-bolts.app.svg "Alt Text for app specific SVG")': (
            'Caption Text for app specific SVG',
            'diagrams/nuts-and-bolts.app.svg',
            'Alt Text for app specific SVG',
            '',
        ),
        r'![Caption \[Text] for app "specific SVG](diagrams/nuts-and-bolts.app.svg "Alt Text for ...")': (
            r'Caption \[Text] for app "specific SVG',
            'diagrams/nuts-and-bolts.app.svg',
            'Alt Text for ...',
            '',
        ),
        r'![Caption \[Text] for app "specific (SVG)](diagrams/nuts-and-bolts.app.svg "Alt Text ... SVG")': (
            r'Caption \[Text] for app "specific (SVG)',
            'diagrams/nuts-and-bolts.app.svg',
            'Alt Text ... SVG',
            '',
        ),
        '![](images/blue.png  "Alt Text Blue Same Repeated Image Caption Missing")': (
            'INJECTED-CAP-TEXT-TO-MARK-MISSING-CAPTION-IN-OUTPUT',
            'images/blue.png',
            'Alt Text Blue Same Repeated Image Caption Missing',
            '',
        ),
    }

    for text_line, expected in cases.items():
        assert concat.parse_markdown_image(text_line) == expected


def test_concatenate_base():
    parameters = {
        'doc_root': BASIC_FIXTURE_ROOT,
        'structure_name': 'structure.yml',
        'target_key': 'abc',
        'facet_key': 'mn',
        'options': {},
    }
    restore = os.getcwd()
    assert concat.concatenate(**parameters) == 0
    os.chdir(restore)


def test_concatenate_deep():
    parameters = {
        'doc_root': EXAMPLE_DEEP_DOC_ROOT,
        'structure_name': 'structure.yml',
        'target_key': 'prod_kind',
        'facet_key': 'deep',
        'options': {},
    }
    restore = os.getcwd()
    assert concat.concatenate(**parameters) == 0
    os.chdir(restore)
