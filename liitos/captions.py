"""Move a caption below a table.

Implementer note: We use a three state machine with transitions COPY [-> TABLE [-> CAPTION -> TABLE] -> COPY].
"""

from collections.abc import Iterable
from enum import Enum
from typing import Union

from liitos import log

Caption = list[str]
Table = list[str]

Modus = Enum('Modus', 'COPY TABLE CAPTION')

TABLE_START_TRIGGER_STARTSWITH = r'\begin{longtable}'
CAPTION_START_TRIGGER_STARTSWITH = r'\caption{'
CAPTION_END_TRIGGER_ENDSWITH = r'}\tabularnewline'
TABLE_END_TRIGGER_STARTSWITH = r'\end{longtable}'


def filter_seek_table(line: str, slot: int, modus: Modus, outgoing: list[str], table: Table, caption: Caption) -> Modus:
    r"""Filter line, seek for a table, if found init table and caption, and return updated mnodus.

    Examples:

    >>> o = []
    >>> line = TABLE_START_TRIGGER_STARTSWITH  # r'\begin{longtable}'
    >>> t, c = [], []
    >>> m = filter_seek_table(line, 0, Modus.COPY, o, t, c)
    >>> assert not o
    >>> m.name
    'TABLE'
    >>> t
    ['\\begin{longtable}']
    >>> assert c == []
    """
    if line.startswith(TABLE_START_TRIGGER_STARTSWITH):
        log.info(f'start of a table environment at line #{slot + 1}')
        modus = Modus.TABLE
        table.append(line)
        caption.clear()
    else:
        outgoing.append(line)

    return modus


def filter_seek_caption(
    line: str, slot: int, modus: Modus, outgoing: list[str], table: Table, caption: Caption
) -> Modus:
    r"""Filter line in table, seek for a caption, and return updated mnodus.

    Examples:

    >>> o = []
    >>> line = CAPTION_START_TRIGGER_STARTSWITH  # r'\caption{'
    >>> t, c = [], []
    >>> m = filter_seek_caption(line, 0, Modus.TABLE, o, t, c)
    >>> assert not o
    >>> m.name
    'CAPTION'
    >>> t
    []
    >>> c
    ['\\caption{']

    >>> o = []
    >>> line = r'\caption{something maybe}\tabularnewline'
    >>> t, c = ['foo'], ['bar']
    >>> m = filter_seek_caption(line, 0, Modus.TABLE, o, t, c)
    >>> o
    []
    >>> m.name
    'TABLE'
    >>> t
    ['foo']
    >>> c
    ['bar', '\\caption{something maybe}\\tabularnewline']

    >>> o = []
    >>> line = r'\end{longtable}'
    >>> t, c = ['foo', r'\endlastfoot'], ['bar']
    >>> m = filter_seek_caption(line, 0, Modus.TABLE, o, t, c)
    >>> o
    ['foo', 'bar', '\\endlastfoot', '\\end{longtable}']
    >>> m.name
    'COPY'
    >>> assert t == []
    >>> assert c == []
    """
    if line.startswith(CAPTION_START_TRIGGER_STARTSWITH):
        log.info(f'- found the caption start at line #{slot + 1}')
        caption.append(line)
        if not line.strip().endswith(CAPTION_END_TRIGGER_ENDSWITH):
            log.info(f'- multi line caption at line #{slot + 1}')
            modus = Modus.CAPTION
    elif line.startswith(TABLE_END_TRIGGER_STARTSWITH):
        log.info(f'end of table env detected at line #{slot + 1}')
        while table:
            stmt = table.pop(0)
            if not stmt.startswith(r'\endlastfoot'):
                outgoing.append(stmt)
                continue
            else:
                while caption:
                    outgoing.append(caption.pop(0))
                outgoing.append(stmt)
        outgoing.append(line)
        modus = Modus.COPY
    else:
        log.debug('- table continues')
        table.append(line)

    return modus


def filter_collect_caption(
    line: str, slot: int, modus: Modus, outgoing: list[str], table: Table, caption: Caption
) -> Modus:
    r"""Filter line in caption until end marker, and return updated mnodus.

    Examples:

    >>> o = []
    >>> line = 'some caption text'
    >>> t, c = ['foo'], ['bar']
    >>> m = filter_collect_caption(line, 0, Modus.CAPTION, o, t, c)
    >>> assert not o
    >>> m.name
    'CAPTION'
    >>> assert t == ['foo']
    >>> assert c == ['bar', 'some caption text']

    >>> o = []
    >>> line = r'}\tabularnewline'
    >>> t, c = ['foo'], ['bar']
    >>> m = filter_collect_caption(line, 0, Modus.CAPTION, o, t, c)
    >>> assert not o
    >>> m.name
    'TABLE'
    >>> assert t == ['foo']
    >>> assert c == ['bar', r'}\tabularnewline']
    """
    caption.append(line)
    if line.strip().endswith(CAPTION_END_TRIGGER_ENDSWITH):
        log.info(f'- caption read at line #{slot + 1}')
        modus = Modus.TABLE

    return modus


def weave(incoming: Iterable[str], lookup: Union[dict[str, str], None] = None) -> list[str]:
    r"""Weave the table caption inside foot from (default) head of table.

    Examples:

    >>> incoming = ['']
    >>> o = weave(incoming)
    >>> o
    ['']

    >>> i = [
    ...     r'\begin{longtable}[]{@{}|l|c|r|@{}}',
    ...     r'\caption{The old tune\label{tab:tuna}}\tabularnewline',
    ...     r'\hline\noalign{}\rowcolor{light-gray}',
    ...     r'Foo & Bar & Baz \\',
    ...     r'\hline\noalign{}',
    ...     r'\endfirsthead',
    ...     r'\hline\noalign{}\rowcolor{light-gray}',
    ...     r'Foo & Bar & Baz \\',
    ...     r'\hline\noalign{}',
    ...     r'\endhead',
    ...     r'\hline\noalign{}',
    ...     r'\endlastfoot',
    ...     r'Quux & x & 42 \\ \hline',
    ...     r'xQuu & y & -1 \\ \hline',
    ...     r'uxQu & z & true \\',
    ...     r'\end{longtable}',
    ... ]
    >>> o = weave(i)
    >>> o
    ['\\begin{longtable}[]{@{}|l|c|r|@{}}', ... '\\caption{The old tune..., '\\endlastfoot', ...]
    """
    outgoing: list[str] = []
    modus = Modus.COPY
    table: Table = []
    caption: Caption = []
    for slot, line in enumerate(incoming):
        if modus == Modus.COPY:
            modus = filter_seek_table(line, slot, modus, outgoing, table, caption)
        elif modus == Modus.TABLE:
            modus = filter_seek_caption(line, slot, modus, outgoing, table, caption)
        else:  # modus == Modus.CAPTION:
            modus = filter_collect_caption(line, slot, modus, outgoing, table, caption)

    return outgoing
