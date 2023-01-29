"""Apply all pairs in patch module on document."""

_ = r"""
\columns=,10\%,30\%,50\%

\begin{longtable}[]{@{}
  >{\raggedright\arraybackslash}p{(\columnwidth - 6\tabcolsep) * \real{0.0735}}
  >{\raggedright\arraybackslash}p{(\columnwidth - 6\tabcolsep) * \real{0.1471}}
  >{\raggedright\arraybackslash}p{(\columnwidth - 6\tabcolsep) * \real{0.3824}}
  >{\raggedright\arraybackslash}p{(\columnwidth - 6\tabcolsep) * \real{0.3971}}@{}}
\caption{A caption for a patchable table
\label{table:patchable-table}}\tabularnewline
\toprule\noalign{}
\begin{minipage}[b]{\linewidth}\raggedright
Key
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
Summary
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
Parent Requirement
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
Means of Compliance (MOC)
\end{minipage} \\
\midrule\noalign{}
\endfirsthead
\toprule\noalign{}
\begin{minipage}[b]{\linewidth}\raggedright
Key
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
Summary
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
Parent Requirement
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
Means of Compliance (MOC)
\end{minipage} \\
\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
A-1 & Be good & I told you so! & Observation \\
A-2 & Be nice & I asked you to! & Trust \\
A-3 & Be good & I told you once! & Observation \\
A-4 & Be nice & I asked you once! & Trust \\
A-5 & Be good & I told you twice! & Observation \\
A-6 & Be nice & I asked you twice! & Trust \\
A-7 & Be good & I told you three times! & Observation \\
A-8 & Be nice & I asked you three times! & Trust \\
\end{longtable}
"""

# after captions patch:
__ = r"""
\columns=,10\%,30\%,50\%

\begin{longtable}[]{@{}
  >{\raggedright\arraybackslash}p{(\columnwidth - 6\tabcolsep) * \real{0.0735}}
  >{\raggedright\arraybackslash}p{(\columnwidth - 6\tabcolsep) * \real{0.1471}}
  >{\raggedright\arraybackslash}p{(\columnwidth - 6\tabcolsep) * \real{0.3824}}
  >{\raggedright\arraybackslash}p{(\columnwidth - 6\tabcolsep) * \real{0.3971}}@{}}
\toprule\noalign{}
\begin{minipage}[b]{\linewidth}\raggedright
Key
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
Summary
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
Parent Requirement
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
Means of Compliance (MOC)
\end{minipage} \\
\midrule\noalign{}
\endfirsthead
\toprule\noalign{}
\begin{minipage}[b]{\linewidth}\raggedright
Key
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
Summary
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
Parent Requirement
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
Means of Compliance (MOC)
\end{minipage} \\
\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
A-1 & Be good & I told you so! & Observation \\
A-2 & Be nice & I asked you to! & Trust \\
A-3 & Be good & I told you once! & Observation \\
A-4 & Be nice & I asked you once! & Trust \\
A-5 & Be good & I told you twice! & Observation \\
A-6 & Be nice & I asked you twice! & Trust \\
A-7 & Be good & I told you three times! & Observation \\
A-8 & Be nice & I asked you three times! & Trust \\
\rowcolor{white}
\caption{A caption for a patchable table
\label{table:patchable-table}}\tabularnewline
\end{longtable}
"""

from collections.abc import Iterable

from liitos import log

# Width lines for header:
FUT_LSPLIT_ONCE_FOR_PREFIX_VAL_COMMA_RIGHT = '}}'
FUT_LSPLIT_ONCE_FOR_PREFIX_COMMA_VAL = r'\real{'
# then concat PREFIX + r'\real{' + str(column_width_new) + '}}' + RIGHT

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


def parse_columns_command(slot: int, text_line: str) -> tuple[bool, str, list[float]]:
    """Parse the \\columns=,0.2,0.7 command."""
    if text_line.startswith(r'\columns='):
        log.info(f'trigger a columns mod for the next table environment at line #{slot + 1}|{text_line}')
        try:
            cols_csv = text_line.split('=', 1)[1].strip()  # r'\columns    =    , 20\%,70\%'  --> r', 20\%,70\%'
            cols = [v.strip() for v in cols_csv.split(COMMA)]
            widths = [float(v.replace(r'\%', '')) / 100 if r'\%' in v else (float(v) if v else 0) for v in cols]
            rest = 1 - sum(widths)
            widths = [v if v else rest for v in widths]
            log.info(f' -> parsed columns mod as | {" | ".join(str(round(v, 2)) for v in widths)} |')
            return True, '', widths
        except Exception as err:
            log.error(f'failed to parse columns values from {text_line.strip()} with err: {err}')
            return False, text_line, []
    else:
        return False, text_line, []


def patch(incoming: Iterable[str]) -> list[str]:
    """Later alligator. \\columns=,0.2,0.7 as mandatory trigger"""
    table_section, head, annotation = False, False, False
    table_ranges = []
    guess_slot = 0
    table_range = {}
    has_column = False
    widths: list[float] = []
    comment_outs = []
    for n, text in enumerate(incoming):

        if not table_section:
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
    punch_me = set(comment_outs)
    for n, line in enumerate(incoming):
        if n in punch_me:
            out.append(f'%CONSIDERED_{line}')
            continue

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
        if n < tb.get('bottom_rule', 0):
            out.append(line)
            if n in tb['end_data_row']:  # type: ignore
                out.append(NEW_RULE)
            continue
        if tb.get('bottom_rule', 0) <= n < tb['amend']:
            continue
        if n == tb['amend']:
            out.append(TAB_NEW_END.replace('ANNOTATION', line))
            next_slot += 1

    log.debug(' -----> ')
    log.debug('# - - - 8< - - -')
    log.debug(str('\n'.join(out)))
    log.debug('# - - - 8< - - -')

    return out
