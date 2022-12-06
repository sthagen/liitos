import liitos.figures as figures


def test_scale_empty():
    assert figures.scale([]) == []


def test_scale_trigger_but_incomplete():
    assert figures.scale([r'\scale=']) == []  # This is may be surprising: error yes, but silently steal?


def test_scale_trigger_plus():
    incoming = [r'\scale=', r'\includegraphics{']
    assert figures.scale(incoming) == [r'\includegraphics{']  # This is may be surprising: error yes, but silently steal?


def test_scale_trigger_complete():
    incoming = ['', r'\scale=90%', '']
    assert figures.scale(incoming) == ['', '']  # This is may be surprising: error yes, but silently steal?


def test_scale_trigger_complete_plus():
    incoming = ['', r'\scale=90%', '', r'\includegraphics{']
    assert figures.scale(incoming) == ['', '', r'\includegraphics{']


def test_scale_copy_through():
    incoming = ['', 'x', 'y', 'z']
    assert figures.scale(incoming) == incoming


def test_scale_trigger_percent_complete_plus():
    incoming = ['', r'\scale=90\%', '', 'text', r'\includegraphics{', '', 'x']
    outgoing = ['', '', 'text', r'\includegraphics[width=0.9\textwidth,height=0.9\textheight]{','', 'x']
    assert figures.scale(incoming) == outgoing
