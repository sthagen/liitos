import liitos.tables as tables

TABLE_THREE_COLS = r"""\
\begin{longtable}[]{@{}lcr@{}}
\caption{A caption for a table
\label{table:left-middle-right}}\tabularnewline
\toprule()
Left & Middle & Right \\
\midrule()
\endfirsthead
\toprule()
Left & Middle & Right \\
\midrule()
\endhead
L1 & M2 & R3 \\
L4 & M5 & R6 \\
L7 & M8 & R9 \\
L10 & M11 & R12 \\
L13 & M14 & R15 \\
\bottomrule()
\end{longtable}
"""


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


def test_patch_tab_three_cols():
    incoming = TABLE_THREE_COLS.split()
    assert tables.patch(incoming) == incoming
