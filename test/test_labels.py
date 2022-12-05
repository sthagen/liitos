import liitos.labels as labels


def test_inject_on_empty_ok():
    assert labels.inject([]) == []


def test_inject_no_match_passes_through_ok():
    pass_me_through = ['a', 'b', 'caption', 'figure', 'table', 'label']
    assert labels.inject(pass_me_through) == pass_me_through
