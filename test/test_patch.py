import liitos.patch as patch


def test_apply_empty_on_empty_ok():
    assert patch.apply([], []) == []


def test_apply_empty_on_some_ok():
    some = ['a', '', 'z']
    assert patch.apply([], some) == some


def test_apply_pair_on_some_ok():
    pair = [('a', 'b')]
    some = ['a', '', 'z']
    assert patch.apply(pair, some) == ['b', '', 'z']


def test_apply_pairs_on_some_ok():
    pairs = [('a', 'b'), ['a', 'b']]
    some = ['a', '', 'z']
    assert patch.apply(pairs, some) == ['b', '', 'z']


def test_apply_pairs_on_some_orderly_ok():
    pairs = [['a', 'b'], ['b', 'a']]
    some = ['a', '', 'z']
    assert patch.apply(pairs, some) == some  # type: ignore
