"""Apply all pairs in patch module on document."""

import re
from collections.abc import Iterable, Iterator
from typing import Union, no_type_check

from liitos import log

# The "target pattern for a line base minimal regex parser"
_ = r"""
\columns=

\begin{longtable}[]{
... \real{fwidth_1}}
...
... \real{fwidth_n}}@{}}
\toprule\noalign{}
\begin{minipage}[
text_1
\end{minipage} & \begin{minipage}[
text_2
...
\end{minipage} & \begin{minipage}[
text_n
\end{minipage} \\
\midrule\noalign{}
\endfirsthead
\toprule\noalign{}
\begin{minipage}[
text_1
\end{minipage} & \begin{minipage}[
text_2
...
\end{minipage} & \begin{minipage}[
text_n
\end{minipage} \\
\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
cell_1_1 & cell_1_2 & ... & cell_1_n \\
cell_1_2 & cell_2_2 & ... & cell_2_n \\
...
row_1_m & row_2_m & ... & cell_n_m \\
\rowcolor{white}
\caption{cap_text_x
cap_text_y\tabularnewline
\end{longtable}
"""

TAB_START_TOK = r'\begin{longtable}[]{'  # '@{}'
TOP_RULE = r'\toprule()'
MID_RULE = r'\midrule()'
END_HEAD = r'\endhead'
END_DATA_ROW = r'\\'
BOT_RULE = r'\bottomrule()'
TAB_END_TOK = r'\end{longtable}'

TAB_NEW_START = r"""\begin{small}
\begin{longtable}[]{|
>{\raggedright\arraybackslash}p{(\columnwidth - 12\tabcolsep) * \real{0.1500}}|
>{\raggedright\arraybackslash}p{(\columnwidth - 12\tabcolsep) * \real{0.5500}}|
>{\raggedright\arraybackslash}p{(\columnwidth - 12\tabcolsep) * \real{0.1500}}|
>{\raggedright\arraybackslash}p{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|}
\hline"""

TAB_HACKED_HEAD = r"""\begin{minipage}[b]{\linewidth}\raggedright
\ \mbox{\textbf{Key}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{Summary}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{Parent}} \mbox{\textbf{Requirement}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{Means of}} \mbox{\textbf{Compliance (MOC)}}
\end{minipage} \\
\hline
\endfirsthead
\multicolumn{4}{@{}l}{\small \ldots continued}\\\hline
\hline
\begin{minipage}[b]{\linewidth}\raggedright
\ \mbox{\textbf{Key}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{Summary}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{Parent}} \mbox{\textbf{Requirement}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{Means of}} \mbox{\textbf{Compliance (MOC)}}
\end{minipage} \\
\endhead
\hline"""

NEW_RULE = r'\hline'

TAB_NEW_END = r"""\end{longtable}
\end{small}
\vspace*{-2em}
\begin{footnotesize}
ANNOTATION
\end{footnotesize}"""

COMMA = ','


class Table:
    """Some adhoc structure to encapsulate the source and target table."""

    SourceMapType = list[tuple[int, str]]
    ColumnsType = dict[str, dict[str, Union[float, int, str]]]

    # ---- begin of LBP skeleton / shape ---
    LBP_STARTSWITH_TAB_ENV_BEGIN = r'\begin{longtable}[]{'
    LBP_REAL_INNER_COLW_PAT = re.compile(r'^(?P<clspec>.+)\\real{(?P<cwval>[0-9.]+)}}\s*$')
    LBP_REAL_OUTER_COLW_PAT = re.compile(r'^(?P<clspec>.+)\\real{(?P<cwval>[0-9.]+)}}@{}}\s*$')
    # Width lines for header:
    FUT_LSPLIT_ONCE_FOR_PREFIX_VAL_COMMA_RIGHT = '}}'
    FUT_LSPLIT_ONCE_FOR_PREFIX_COMMA_VAL = r'\real{'
    # then concat PREFIX + r'\real{' + str(column_width_new) + '}}' + RIGHT

    LBP_TOP_RULE_CONTEXT_STARTSWITH = r'\toprule\noalign{}'
    LPB_START_COLUMN_LABEL_STARTSWITH = r'\begin{minipage}['
    LBP_SEP_COLUMN_LABEL_STARTSWITH = r'\end{minipage} & \begin{minipage}['
    LBP_STOP_COLUMN_LABEL_STARTSWITH = r'\end{minipage} \\'

    LBP_MID_RULE_CONTEXT_STARTSWITH = r'\midrule\noalign{}'

    LBP_END_FIRST_HEAD_STARTSWITH = r'\endfirsthead'

    # LBP_TOP_RULE_CONTEXT_STARTSWITH = r'\toprule\noalign{}'
    # LPB_START_COLUMN_LABEL_STARTSWITH = r'\begin{minipage}['
    # LBP_SEP_COLUMN_LABEL_STARTSWITH = r'\end{minipage} & \begin{minipage}['
    # LBP_STOP_COLUMN_LABEL_STARTSWITH = r'\end{minipage} \\'

    # LBP_MID_RULE_CONTEXT_STARTSWITH = r'\midrule\noalign{}'

    LBP_END_ALL_HEAD_STARTSWITH = r'\endhead'

    LBP_BOTTOM_RULE_CONTEXT_STARTSWITH = r'\bottomrule\noalign{}'

    LBP_END_LAST_FOOT_STARTSWITH = r'\endlastfoot'

    # ... data lines - we want inject of r'\hline' following every data line (not text line)
    # -> that is, inject after lines ending with r'\\'

    LBP_END_OF_DATA_STARTSWITH = r'\rowcolor{white}'
    LBP_START_CAP_STARTSWITH = r'\caption{'
    LBP_STOP_CAP_ENDSWITH = r'\tabularnewline'
    LBP_STARTSWITH_TAB_ENV_END = r'\end{longtable}'

    # ---- end of LBP skeleton / shape ---
    @no_type_check
    def __init__(self, anchor: int, start_line: str, text_lines: Iterator[str], widths: list[float], font_sz: str = ''):
        """Initialize the table from source text lines anchored at anchor.
        The implementation allows reuse of the iterator on caller site for extracting subsequent tables in one go.
        """
        self.src_map: Table.SourceMapType = [(anchor, start_line.rstrip())]
        self.data_row_ends: Table.SourceMapType = []
        self.columns: Table.ColumnsType = {}
        self.target_widths: list[float] = widths
        self.source_widths: list[float] = []
        self.font_size = font_sz
        log.info(f'Received {anchor=}, {start_line=}, target {widths=}, and {font_sz=}')
        local_number = 0
        consumed = False
        while not consumed:
            local_number += 1
            pos = local_number + anchor
            line = next(text_lines).rstrip()
            self.src_map.append((pos, line))
            if line.startswith(Table.LBP_STARTSWITH_TAB_ENV_END):
                consumed = True

        self.parse_columns()
        self.parse_data_rows()
        self.data_row_count = len(self.data_row_ends)
        self.cw_patches: dict[str, str] = {}
        self.create_width_patches()
        log.info(f'Parsed {len(self.target_widths)} x {self.data_row_count} table starting at anchor {anchor}')

    @no_type_check
    def create_width_patches(self):
        """If widths are meaningful and consistent create the patches with the zero-based line-numbers as keys."""
        if not self.source_widths:
            log.warning('Found no useful width information')
            return {}
        wrapper = r'\real{'
        postfix = '}}'
        finalize = '@{}}'
        ranks = list(self.columns)
        for rank in ranks:
            anchor_str = str(self.columns[rank]['col_spec_line'])
            prefix = self.columns[rank]['colspec_prefix']
            value = self.columns[rank]['width']
            # concat PREFIX + r'\real{' + str(column_width_new) + '}}'
            self.cw_patches[anchor_str] = prefix + wrapper + str(value) + postfix
            if rank == ranks[-1]:
                self.cw_patches[anchor_str] += finalize

    def width_patches(self) -> dict[str, str]:
        """Return the map of width patches with the zero-based line-numbers as keys."""
        return self.cw_patches

    def source_map(self) -> SourceMapType:
        """Return the source map data (a random accessible sequence of pairs) mapping abs line number to text line."""
        return self.src_map

    def column_data(self) -> ColumnsType:
        """Return the column data (an ordered dict of first labels, other labels, and widths) with abs line map."""
        return self.columns

    def column_source_widths(self) -> list[float]:
        """Return the incoming column widths."""
        return self.source_widths

    def column_target_widths(self) -> list[float]:
        """Return the outgoing column widths."""
        return self.target_widths

    @no_type_check
    def table_width(self) -> float:
        """Return the sum of all column widths."""
        return sum(self.columns[r].get('width', 0) for r in self.columns)

    def data_row_seps(self) -> SourceMapType:
        """Return the map to the data row ends for injecting separators."""
        return self.data_row_ends

    @no_type_check
    def transform_widths(self) -> None:
        """Apply the target transform to column widths."""
        self.source_widths = [self.columns[rank]['width'] for rank in self.columns]
        if not self.target_widths:
            log.info('No target widths given - maintaining source column widths')
            self.target_widths = self.source_widths
            return
        if len(self.target_widths) != len(self.source_widths):
            log.warning(
                f'Mismatching {len(self.target_widths)} target widths given - maintaining'
                f'the {len(self.source_widths)} source column widths'
            )
            self.target_widths = self.source_widths
            return
        log.info('Applying target widths given - adapting source column widths')
        for rank, target_width in zip(self.columns, self.target_widths):
            self.columns[rank]['width'] = target_width

    @no_type_check
    def parse_columns(self) -> None:
        """Parse the head to extract the columns."""
        self.parse_column_widths()
        self.parse_column_first_head()
        self.parse_column_other_head()
        self.transform_widths()

    def parse_column_widths(self) -> None:
        r"""Parse the column width declarations to initialize the columns data.

        \begin{longtable}[]{@{}%wun-based-line-9
          >{\raggedright\arraybackslash}p{(\columnwidth - 6\tabcolsep) * \real{0.1118}}
          >{\raggedright\arraybackslash}p{(\columnwidth - 6\tabcolsep) * \real{0.5776}}
          >{\raggedright\arraybackslash}p{(\columnwidth - 6\tabcolsep) * \real{0.1739}}
          >{\raggedright\arraybackslash}p{(\columnwidth - 6\tabcolsep) * \real{0.1366}}@{}}
        \toprule\noalign{}
        """
        rank = 0
        for anchor, text in self.src_map:
            if text.startswith(Table.LBP_STARTSWITH_TAB_ENV_BEGIN):
                continue
            if text.startswith(Table.LBP_TOP_RULE_CONTEXT_STARTSWITH):
                break
            m = Table.LBP_REAL_INNER_COLW_PAT.match(text)
            if m:
                self.columns[str(rank)] = {
                    'first_label': '',
                    'first_label_line': -1,
                    'continued_label': '',
                    'continued_label_line': -1,
                    'col_spec_line': anchor,
                    'colspec_prefix': m.groupdict()['clspec'],
                    'width': float(m.groupdict()['cwval']),
                }
                rank += 1
                continue
            m = Table.LBP_REAL_OUTER_COLW_PAT.match(text)
            if m:
                self.columns[str(rank)] = {
                    'first_label': '',
                    'first_label_line': -1,
                    'continued_label': '',
                    'continued_label_line': -1,
                    'col_spec_line': anchor,
                    'colspec_prefix': m.groupdict()['clspec'],
                    'width': float(m.groupdict()['cwval']),
                }
                rank += 1
                continue

    def parse_column_first_head(self) -> None:
        r"""Parse the head to extract the columns.

        \begin{minipage}[b]{\linewidth}\raggedright
        Parameter
        \end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
        Description
        \end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
        Name
        \end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
        Example
        \end{minipage} \\
        \midrule\noalign{}
        \endfirsthead
        """
        rank = 0
        first_head = False
        label_next = False
        for anchor, text in self.src_map:
            if text.startswith(Table.LBP_TOP_RULE_CONTEXT_STARTSWITH):
                first_head = True
                continue
            if not first_head:
                continue
            if text.startswith(Table.LBP_END_FIRST_HEAD_STARTSWITH):
                break
            if text.startswith(Table.LPB_START_COLUMN_LABEL_STARTSWITH):
                label_next = True
                continue
            if text.startswith(Table.LBP_SEP_COLUMN_LABEL_STARTSWITH):
                label_next = True
                continue
            if text.startswith(Table.LBP_STOP_COLUMN_LABEL_STARTSWITH):
                label_next = True
                continue
            if label_next:
                self.columns[str(rank)]['first_label'] = text.strip()
                self.columns[str(rank)]['first_label_line'] = anchor
                rank += 1
                if str(rank) in self.columns:
                    continue
                break

    def parse_column_other_head(self) -> None:
        r"""Parse the other heads to extract the column labelss.

        \endfirsthead
        \toprule\noalign{}
        \begin{minipage}[b]{\linewidth}\raggedright
        Parameter
        \end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
        Description
        \end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
        Name
        \end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
        Example
        \end{minipage} \\
        \midrule\noalign{}
        \endhead
        """
        rank = 0
        continued_head = False
        label_next = False
        for anchor, text in self.src_map:
            if text.startswith(Table.LBP_END_FIRST_HEAD_STARTSWITH):
                continued_head = True
                continue
            if not continued_head:
                continue
            if text.startswith(Table.LBP_END_ALL_HEAD_STARTSWITH):
                break
            if text.startswith(Table.LPB_START_COLUMN_LABEL_STARTSWITH):
                label_next = True
                continue
            if text.startswith(Table.LBP_SEP_COLUMN_LABEL_STARTSWITH):
                label_next = True
                continue
            if text.startswith(Table.LBP_STOP_COLUMN_LABEL_STARTSWITH):
                label_next = True
                continue
            if label_next:
                self.columns[str(rank)]['continued_label'] = text.strip()
                self.columns[str(rank)]['continued_label_line'] = anchor
                rank += 1
                if str(rank) in self.columns:
                    continue
                break

    def parse_data_rows(self) -> None:
        r"""Parse the data rows.

        \endlastfoot
        A2 & B2 & C2 & D2 \\
        \end{longtable}
        """
        data_section = False
        for anchor, text in self.src_map:
            if text.startswith(Table.LBP_END_LAST_FOOT_STARTSWITH):
                data_section = True
                continue
            if text.startswith(Table.LBP_STARTSWITH_TAB_ENV_END):
                break
            if data_section and r'\\' in text:
                self.data_row_ends.append((anchor, text))
                continue


def parse_table_font_size_command(slot: int, text_line: str) -> tuple[bool, str, str]:
    """Parse the \\tablefontsize=footnotesize command."""
    backslash = '\\'
    known_sizes = (
        'tiny',
        'scriptsize',
        'footnotesize',
        'small',
        'normalsize',
        'large',
        'Large',
        'LARGE',
        'huge',
        'Huge',
    )
    if text_line.startswith(r'\tablefontsize='):
        log.info(f'trigger a fontsize mod for the next table environment at line #{slot + 1}|{text_line}')
        try:
            font_size = text_line.split('=', 1)[1].strip()  # r'\tablefontsize=Huge'  --> 'Huge'
            if font_size.startswith(backslash):
                font_size = font_size.lstrip(backslash)
            if font_size not in known_sizes:
                log.error(f'failed to map given fontsize ({font_size}) into known sizes ({",".join(known_sizes)})')
                return False, text_line, ''
            log.info(f' -> parsed table fontsize mod as ({font_size})')
            return True, '', font_size
        except Exception as err:
            log.error(f'failed to parse table fontsize value from {text_line.strip()} with err: {err}')
            return False, text_line, ''
    else:
        return False, text_line, ''


def parse_columns_command(slot: int, text_line: str) -> tuple[bool, str, list[float]]:
    """Parse the \\columns=,0.2,0.7 command."""
    if text_line.startswith(r'\columns='):
        log.info(f'trigger a columns mod for the next table environment at line #{slot + 1}|{text_line}')
        try:
            cols_csv = text_line.split('=', 1)[1].strip()  # r'\columns    =    , 20\%,70\%'  --> r', 20\%,70\%'
            cols = [v.strip() for v in cols_csv.split(COMMA)]
            widths = [float(v.replace(r'\%', '')) / 100 if r'\%' in v else (float(v) if v else 0) for v in cols]
            rest = round(1 - sum(round(w, 5) for w in widths), 5)
            widths = [v if v else rest for v in widths]
            log.info(f' -> parsed columns mod as | {" | ".join(str(round(v, 2)) for v in widths)} |')
            return True, '', widths
        except Exception as err:
            log.error(f'failed to parse columns values from {text_line.strip()} with err: {err}')
            return False, text_line, []
    else:
        return False, text_line, []


@no_type_check
def patch(incoming: Iterable[str], lookup: Union[dict[str, str], None] = None) -> list[str]:
    """Later alligator. \\columns=,0.2,0.7 as mandatory trigger"""
    table_section, head, annotation = False, False, False
    table_ranges = []
    guess_slot = 0
    table_range = {}
    has_column = False
    has_font_size = False
    widths: list[float] = []
    font_size = ''
    comment_outs = []
    for n, text in enumerate(incoming):
        if not table_section:
            if not has_font_size:
                has_font_size, text_line, font_size = parse_table_font_size_command(n, text)
                if has_font_size:
                    comment_outs.append(n)
            if not has_font_size:
                continue

            if not has_column:
                has_column, text_line, widths = parse_columns_command(n, text)
                if has_column:
                    comment_outs.append(n)
            if not has_column:
                continue

            if not text.startswith(TAB_START_TOK):
                continue
            table_range['start'] = n
            table_section = True
            head = True
            table_range['end_data_row'] = []
            continue

        if text.startswith(TOP_RULE):
            table_range['top_rule'] = n
            continue

        if text.startswith(MID_RULE):
            table_range['mid_rule'] = n
            continue

        if text.startswith(END_HEAD):
            table_range['end_head'] = n
            head = False
            continue

        if not head and text.strip().endswith(END_DATA_ROW):
            table_range['end_data_row'].append(n)
            continue

        if text.startswith(BOT_RULE):
            table_range['bottom_rule'] = n
            continue

        if text.startswith(TAB_END_TOK):
            table_range['end'] = n
            annotation = True
            guess_slot = n + 2
            continue

        if annotation and n == guess_slot:
            table_range['amend'] = n
            table_ranges.append(table_range)
            table_range = {}
            annotation, table_section = False, False

    log.info(f'Detected {len(table_ranges)} tables (method from before version 2023.2.12):')
    for thing in table_ranges:
        log.info(f'- {thing}')

    tables_in, on_off_slots = [], []
    for table in table_ranges:
        from_here = table['start']
        thru_there = table['amend']
        log.info('Table:')
        log.info(f'-from {incoming[from_here]}')
        log.info(f'-thru {incoming[thru_there]}')
        on_off = (from_here, thru_there + 1)
        on_off_slots.append(on_off)
        tables_in.append((on_off, [line for line in incoming[on_off[0] : on_off[1]]]))

    log.debug('# - - - 8< - - -')
    if tables_in:
        log.debug(str('\n'.join(tables_in[0][1])))
    log.debug('# - - - 8< - - -')

    reader = iter(incoming)
    tables = []
    comment_outs = []
    n = 0
    widths = []
    font_size = ''
    for line in reader:
        log.debug(f'zero-based-line-no={n}, text=({line}) table-count={len(tables)}')
        if not line.startswith(Table.LBP_STARTSWITH_TAB_ENV_BEGIN):
            if line.startswith(r'\tablefontsize='):
                has_font_size, text_line, font_size = parse_table_font_size_command(n, line)
                log.info(f'    + {has_font_size=}, {text_line=}, {font_size=}')
                if has_font_size:
                    comment_outs.append(n)
                    log.info(f'FONT-SIZE at <<{n}>>')
            if line.startswith(r'\columns='):
                has_column, text_line, widths = parse_columns_command(n, line)
                log.info(f'    + {has_column=}, {text_line=}, {widths=}')
                if has_column:
                    comment_outs.append(n)
                    log.info(f'COLUMNS-WIDTH at <<{n}>>')
            n += 1
        else:
            table = Table(n, line, reader, widths, font_size)  # sharing the meal - instead of iter(lines_buffer[n:]))
            tables.append(table)
            n += len(tables[-1].source_map())
            log.debug(f'- incremented n to {n}')
            log.debug(f'! next n (zero offset) is {n}')
            widths = []
            font_size = ''

    log.info('---')
    for n, table in enumerate(tables, start=1):
        log.info(f'Table #{n} (total width = {table.table_width()}):')
        for rank, column in table.column_data().items():
            log.info(f'{rank} -> {column}')
        log.info(f'- source widths = {table.column_source_widths()}):')
        log.info(f'- target widths = {table.column_target_widths()}):')
        for numba, replacement in table.width_patches().items():
            log.info(f'{numba} -> {replacement}')
        for anchor, text in table.data_row_seps():
            log.info(f'{anchor} -> {text}')
        log.info(f'= (fontsize command = "{table.font_size}"):')
    log.info('---')
    log.info(f'Comment out the following {len(comment_outs)} lines (zero based numbers) - punch:')
    for number in comment_outs:
        log.info(f'- {number}')

    wideners = {}
    for table in tables:
        for numba, replacement in table.width_patches().items():
            wideners[numba] = replacement
    widen_me = set(wideners)
    log.debug('widen me has:')
    log.debug(list(widen_me))
    log.debug('--- global replacement width lines: ---')
    for numba, replacement in wideners.items():
        log.debug(f'{numba} => {replacement}')
    log.debug('---')

    sizers = {}
    for table in tables:
        if table.font_size:
            sizers[str(table.src_map[0][0])] = '\\begin{' + table.font_size + '}\n' + table.src_map[0][1]
            sizers[str(table.src_map[-1][0])] = table.src_map[-1][1] + '\n' + '\\end{' + table.font_size + '}'
    size_me = set(sizers)
    log.debug('size me has:')
    log.debug(list(size_me))
    log.debug('--- global replacement sizer lines: ---')
    for numba, replacement in sizers.items():
        log.debug(f'{numba} => {replacement}')
    log.debug('---')

    out = []
    # next_slot = 0
    punch_me = set(comment_outs)
    for n, line in enumerate(incoming):
        if n in punch_me:
            corrected = f'%CONSIDERED_{line}'
            out.append(corrected)
            log.info(f' (x) Punched out line {n} -> ({corrected})')
            continue
        if str(n) in widen_me:
            out.append(wideners[str(n)])
            log.info(f' (<) Incoming: ({line})')
            log.info(f' (>) Outgoing: ({wideners[str(n)]})')
            continue
        if str(n) in size_me:
            out.append(sizers[str(n)])
            log.info(f' (<) Incoming: ({line})')
            log.info(f' (>) Outgoing: ({sizers[str(n)]})')
            continue
        out.append(line)

        # if next_slot < len(on_off_slots):
        #     trigger_on, trigger_off = on_off_slots[next_slot]
        #     tb = table_ranges[next_slot]
        # else:
        #     trigger_on = None
        # if trigger_on is None:
        #     out.append(line)
        #     continue
        #
        # if n < trigger_on:
        #     out.append(line)
        #     continue
        # if n == trigger_on:
        #     out.append(TAB_NEW_START)
        #     out.append(TAB_HACKED_HEAD)
        #     continue
        # if n <= tb['end_head']:
        #     continue
        # if n < tb.get('bottom_rule', 0):
        #     out.append(line)
        #     if n in tb['end_data_row']:  # type: ignore
        #         out.append(NEW_RULE)
        #     continue
        # if tb.get('bottom_rule', 0) <= n < tb['amend']:
        #     continue
        # if n == tb['amend']:
        #     out.append(TAB_NEW_END.replace('ANNOTATION', line))
        #     next_slot += 1

    log.warning('Disabled naive table patching from before version 2023.2.12 for now')

    log.debug(' -----> ')
    log.debug('# - - - 8< - - -')
    log.debug(str('\n'.join(out)))
    log.debug('# - - - 8< - - -')

    return out
