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
    partial_matches = ['a', r'\includegraphics{', 'z']
    augmented_content = [
        'a',
        '',
        r'\begin{figure}',
        r'\centering',
        r'\includegraphics{',
        r'\caption{MISSING-CAPTION-IN-MARKDOWN FIX-AT-SOURCE}',
        r'\end{figure}',
        'z',
    ]
    assert labels.inject(partial_matches) == augmented_content


def test_inject_precondition_and_include():
    correct_match = [
        'a',
        '',
        r'\begin{figure}',
        r'\centering',
        r'\includegraphics{images/blue.png}',
        r'\caption{Caption Text Blue}',
        r'\end{figure}',
        '',
        'z',
    ]
    injected = [
        'a',
        '',
        r'\begin{figure}',
        r'\centering',
        r'\includegraphics{images/blue.png}',
        r'\caption{Caption Text Blue \label{fig:blue}}',
        r'\end{figure}',
        '',
        'z',
    ]
    assert labels.inject(correct_match) == injected
