"""Apply all pairs in patch module on document."""
from collections.abc import Iterable

from liitos import ENCODING, log

TAB_START_TOK = r'\begin{longtable}[]{@{}'
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


def patch(incoming: Iterable[str]) -> list[str]:
    """Later alligator."""
    table_section, head, annotation = False, False, False
    table_ranges = []
    guess_slot = 0
    table_range = {}
    for n, text in enumerate(incoming):

        if not table_section:
            if not text.startswith(TAB_START_TOK):
                continue
            table_range['start'] = n
            table_section = True
            head = True
            table_range['end_data_row'] = []  # type: ignore
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
            table_range['end_data_row'].append(n)  # type: ignore
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

    log.debug(str(table_ranges))

    tables_in, on_off_slots = [], []
    for table in table_ranges:
        from_here = table['start']
        thru_there = table['amend']
        log.info('Table:')
        log.info(f'-from {incoming[from_here]}')  # type: ignore
        log.info(f'-thru {incoming[thru_there]}')  # type: ignore
        on_off = (from_here, thru_there + 1)
        on_off_slots.append(on_off)
        tables_in.append((on_off, [line for line in incoming[on_off[0] : on_off[1]]]))  # type: ignore

    log.debug('# - - - 8< - - -')
    if tables_in:
        log.debug(str('\n'.join(tables_in[0][1])))
    log.debug('# - - - 8< - - -')

    out = []
    next_slot = 0
    for n, line in enumerate(incoming):
        if next_slot < len(on_off_slots):
            trigger_on, trigger_off = on_off_slots[next_slot]
            tb = table_ranges[next_slot]
        else:
            trigger_on = None
        if trigger_on is None:
            out.append(line)
            continue

        if n < trigger_on:
            out.append(line)
            continue
        if n == trigger_on:
            out.append(TAB_NEW_START)
            out.append(TAB_HACKED_HEAD)
            continue
        if n <= tb['end_head']:
            continue
        if n < tb['bottom_rule']:
            out.append(line)
            if n in tb['end_data_row']:  # type: ignore
                out.append(NEW_RULE)
            continue
        if tb['bottom_rule'] <= n < tb['amend']:
            continue
        if n == tb['amend']:
            out.append(TAB_NEW_END.replace('ANNOTATION', line))
            next_slot += 1

    log.debug(' -----> ')
    log.debug('# - - - 8< - - -')
    log.debug(str('\n'.join(out)))
    log.debug('# - - - 8< - - -')

    return out
