import liitos.figures as figures


def test_scale_empty():
    assert figures.scale([]) == []


def test_scale_trigger_but_incomplete():
    assert figures.scale([r'\scale=']) == []  # This is may be surprising: error yes, but silently steal?


def test_scale_trigger_plus():
    incoming = [r'\scale=', r'\includegraphics{']
    assert figures.scale(incoming) == [
        r'\includegraphics{'
    ]  # This is may be surprising: error yes, but silently steal?


def test_scale_trigger_complete():
    incoming = ['', r'\scale=90%', '']
    assert figures.scale(incoming) == ['', '']  # This is may be surprising: error yes, but silently steal?


def test_scale_trigger_decimal_complete():
    incoming = ['', r'\scale=0.9', '']
    assert figures.scale(incoming) == ['', '']  # This is may be surprising: error yes, but silently steal?


def test_scale_trigger_complete_plus():
    incoming = ['', r'\scale=90%', '', r'\includegraphics{']
    assert figures.scale(incoming) == ['', '', r'\includegraphics{']


def test_scale_copy_through():
    incoming = ['', 'x', 'y', 'z']
    assert figures.scale(incoming) == incoming


def test_scale_trigger_percent_complete_plus():
    incoming = ['', r'\scale=90\%', '', 'text', r'\includegraphics{', '', 'x']
    outgoing = ['', '', 'text', r'\includegraphics[width=0.9\textwidth,height=0.9\textheight]{', '', 'x']
    assert figures.scale(incoming) == outgoing


def test_scale_trigger_percent_tiny__complete_plus():
    incoming = ['', r'\scale=0.90000000000000000001\%', '', 'text', r'\includegraphics{', '', 'x']
    outgoing = ['', '', 'text', r'\includegraphics[width=0.01\textwidth,height=0.01\textheight]{', '', 'x']
    assert figures.scale(incoming) == outgoing


def test_scale_trigger_fraction_complete_plus():
    incoming = ['', r'\scale=0.90000000000000000001', '', 'text', r'\includegraphics{', '', 'x']
    outgoing = ['', '', 'text', r'\includegraphics[width=0.9\textwidth,height=0.9\textheight]{', '', 'x']
    assert figures.scale(incoming) == outgoing


def test_scale_trigger_percent_complete_plus_another():
    incoming = [
        '',
        r'\scale=90\%',
        '',
        'text',
        r'\includegraphics{',
        '',
        'x',
        '',
        r'\scale=92\%',
        '',
        'texte',
        r'\includegraphics{x',
        '',
        'x',
    ]
    outgoing = [
        '',
        '',
        'text',
        r'\includegraphics[width=0.9\textwidth,height=0.9\textheight]{',
        '',
        'x',
        '',
        '',
        'texte',
        r'\includegraphics[width=0.92\textwidth,height=0.92\textheight]{x',
        '',
        'x',
    ]
    assert figures.scale(incoming) == outgoing
