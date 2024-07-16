import os
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

RESTORE = os.getcwd()


def setup():
    os.chdir(RESTORE)


def teardown():
    os.chdir(RESTORE)


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


def test_table():
    os.chdir(RESTORE)
    with open('test/fixtures/random/tables.tex', 'rt', encoding='utf-8') as handle:
        lines_buffer = [line.rstrip() for line in handle.readlines()]

    reader = iter(lines_buffer)
    some_tables = []
    comment_outs = []
    n = 0
    widths = []
    for line in reader:
        if not line.startswith(tables.Table.LBP_STARTSWITH_TAB_ENV_BEGIN):
            if line.startswith(r'\columns='):
                has_column, text_line, widths = tables.parse_columns_command(n, line)
                if has_column:
                    comment_outs.append(n)
            n += 1
        else:
            table = tables.Table(n, line, reader, widths)  # sharing the meal - instead of iter(lines_buffer[n:]))
            widths = []
            some_tables.append(table)
            n += len(some_tables[-1].source_map())

    assert comment_outs == [92]


def test_patch_some():
    with open('test/fixtures/random/tables.tex', 'rt', encoding='utf-8') as handle:
        lines_buffer = [line.rstrip() for line in handle.readlines()]
    out_lines = tables.patch(lines_buffer)
    assert out_lines[92] == r'%CONSIDERED_\columns=,10\%,30\%,50\%'


def test_parse_table_font_size_command_unknown():
    line = '\\tablefontsize=unknown'
    worked, out_line, font_size = tables.parse_table_font_size_command(0, line)
    assert worked is False
    assert out_line == line
    assert font_size == ''


def test_parse_table_font_size_command_no_command_at_start():
    line = ' \\tablefontsize=notatstart'
    worked, out_line, font_size = tables.parse_table_font_size_command(0, line)
    assert worked is False
    assert out_line == line
    assert font_size == ''


def test_parse_table_font_size_command_known_size():
    line = '\\tablefontsize=footnotesize'
    worked, out_line, font_size = tables.parse_table_font_size_command(0, line)
    assert worked is True
    assert out_line == ''
    assert font_size == 'footnotesize'


def test_parse_table_font_size_command_known_size_with_backslash():
    line = '\\tablefontsize=\\tiny'
    worked, out_line, font_size = tables.parse_table_font_size_command(0, line)
    assert worked is True
    assert out_line == ''
    assert font_size == 'tiny'


def test_parse_table_font_size_command_no_equal_sign():
    line = '\\tablefontsize\\tiny'
    worked, out_line, font_size = tables.parse_table_font_size_command(0, line)
    assert worked is False
    assert out_line == line
    assert font_size == ''


def test_parse_table_font_size_command_missing_value():
    line = '\\tablefontsize='
    worked, out_line, font_size = tables.parse_table_font_size_command(0, line)
    assert worked is False
    assert out_line == line
    assert font_size == ''
