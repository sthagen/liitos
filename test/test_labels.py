import json
import liitos.labels as labels


def test_inject_on_empty_ok():
    assert labels.inject([]) == []


def test_inject_no_match_passes_through_ok():
    pass_me_through = ['a', 'b', 'caption', 'figure', 'table', 'label']
    assert labels.inject(pass_me_through) == pass_me_through


def test_inject_precondition():
    partial_matches = ['a', r'\begin{figure}', 'z']
    assert labels.inject(partial_matches) == partial_matches


def test_inject_not_precondition():
    partial_matches = ['a\n', r'\includegraphics{' + '\n', 'z\n']
    augmented_content = [
        'a\n',
        r'\begin{figure}' + '\n',
        r'\centering' + '\n',
        r'\includegraphics{' + '\n',
        r'\caption{MISSING-CAPTION-IN-MARKDOWN FIX-AT-SOURCE}' + '\n',
        r'\end{figure}' + '\n',
        'z\n',
    ]
    assert labels.inject(partial_matches) == augmented_content


def test_inject_precondition_and_include():
    correct_match = [
        'a\n',
        '\n',
        r'\begin{figure}' + '\n',
        r'\centering' + '\n',
        r'\includegraphics{images/blue.png}' + '\n',
        r'\caption{Caption Text Blue}' + '\n',
        r'\end{figure}' + '\n',
        '\n',
        'z\n',
    ]
    injected = [
        'a\n',
        '\n',
        r'\begin{figure}' + '\n',
        r'\centering' + '\n',
        r'\includegraphics{images/blue.png}' + '\n',
        r'\caption{Caption Text Blue \label{fig:blue}}' + '\n',
        r'\end{figure}' + '\n',
        '\n',
        'z\n',
    ]
    assert labels.inject(correct_match) == injected


def test_is_include_graphics():
    assert labels.is_include_graphics(r'\includegraphics[') is True
    assert labels.is_include_graphics(r'\includegraphics{') is True
    assert labels.is_include_graphics(r'\includegraphics[]') is True
    assert labels.is_include_graphics(r'\includegraphics{}\n') is True
    assert labels.is_include_graphics(r'\includegraphics') is False
    assert labels.is_include_graphics(r'\includegraphic[') is False
    assert labels.is_include_graphics('') is False


def test_extract_image_path():
    assert labels.extract_image_path(r'\includegraphics{a/b}') == 'a/b'
    assert labels.extract_image_path(r'\includegraphics[]{a/b}') == 'a/b'
    assert labels.extract_image_path(r'\includegraphics[]{}\n') == r'}\n'
    assert labels.extract_image_path('') == 'IMAGE_PATH_NOT_FOUND'


def test_inject_regression_bug48():
    lookup = json.load(open('test/fixtures/bugs/labels/lookup.json', 'rt', encoding='utf-8'))
    incoming = open('test/fixtures/bugs/labels/document-pre-labels.tex', 'rt', encoding='utf-8').readlines()
    reference = open('test/fixtures/bugs/labels/document-post-labels.tex', 'rt', encoding='utf-8').readlines()
    outgoing = labels.inject(incoming, lookup)
    assert outgoing == reference
