import liitos.captions as captions


def test_weave_on_empty_ok():
    assert captions.weave([]) == []


def test_weave_no_match_passes_through_ok():
    pass_me_through = ['a', 'b', 'caption', 'figure', 'table', 'label']
    assert captions.weave(pass_me_through) == pass_me_through
