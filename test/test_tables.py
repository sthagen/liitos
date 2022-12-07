import liitos.tables as tables


def test_patch_empty():
    assert tables.patch([]) == []


def test_patch_tab_start():
    incoming = [
        '',
        tables.TAB_START_TOK,
        tables.TOP_RULE,
        tables.MID_RULE,
        tables.END_HEAD,
        tables.END_DATA_ROW,
        tables.BOT_RULE,
        tables.TAB_END_TOK,
    ]
    assert tables.patch(incoming) == incoming
