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
