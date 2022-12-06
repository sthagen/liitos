import liitos.meta as meta


def test_weave_meta_part_proprietary_information_on_empty_ok():
    assert meta.weave_meta_part_proprietary_information({}, '') == ''
