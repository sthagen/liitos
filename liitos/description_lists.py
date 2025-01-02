"""Apply any option command to subsequent description environment.

Implementation Note: The empty string marker is used to indicate absence of option command.
"""

from collections.abc import Iterable
from enum import Enum
from typing import Union

from liitos import log

Modus = Enum('Modus', 'COPY OPTION')
NO_OPTION: str = ''


def filter_seek_option(line: str, slot: int, modus: Modus, opt: str, outgoing: list[str]) -> tuple[Modus, str]:
    r"""Filter line, seek for an option command, and return updated mnodus, opt pair.

    Examples:

    >>> filtered = []
    >>> m, opt = filter_seek_option(r'\option[]', 0, Modus.COPY, NO_OPTION, filtered)
    >>> assert not filtered
    >>> assert m == Modus.OPTION
    >>> assert opt == '[]'

    >>> filtered = []
    >>> m, opt = filter_seek_option('foo', 0, Modus.COPY, NO_OPTION, filtered)
    >>> assert filtered == ['foo']
    >>> assert m == Modus.COPY
    >>> assert opt == NO_OPTION

    >>> filtered = []
    >>> m, opt = filter_seek_option(r'\option[foo=bar]', 0, Modus.COPY, NO_OPTION, filtered)
    >>> assert not filtered
    >>> assert m == Modus.OPTION
    >>> assert opt == '[foo=bar]'
    """
    if line.startswith(r'\option['):
        log.info(f'trigger an option mod for the next description environment at line #{slot + 1}|{line}')
        # \option[style=multiline,leftmargin=6em]  --> [style=multiline,leftmargin=6em]
        opt = line.split(r'\option', 1)[1].strip()
        modus = Modus.OPTION
        log.info(f' -> parsed option as ({opt})')
        # return True, f'%CONSIDERED_{line}', opt
    else:
        outgoing.append(line)

    return modus, opt


def filter_seek_description(line: str, slot: int, modus: Modus, opt: str, outgoing: list[str]) -> tuple[Modus, str]:
    r"""Filter line, seek for a description, add options if applicable, and return updated mnodus, option pair.

    Examples:

    >>> filtered = []
    >>> m, opt = filter_seek_description('quux', 0, Modus.OPTION, '[foo=bar]', filtered)
    >>> assert filtered == ['quux']
    >>> assert m == Modus.OPTION
    >>> assert opt == '[foo=bar]'

    >>> filtered = []
    >>> m, opt = filter_seek_description(r'\begin{description}', 0, Modus.OPTION, NO_OPTION, filtered)
    >>> assert filtered == [r'\begin{description}']
    >>> assert m == Modus.COPY
    >>> assert opt == NO_OPTION

    >>> filtered = []
    >>> m, opt = filter_seek_description(r'\begin{description}', 0, Modus.OPTION, '[foo=bar]', filtered)
    >>> assert filtered == [r'\begin{description}[foo=bar]']
    >>> assert m == Modus.COPY
    >>> assert opt == NO_OPTION
    """
    if line.startswith(r'\begin{description}'):
        if opt != NO_OPTION:
            log.info(f'- found the option target start at line #{slot + 1}|{line}')
            outgoing.append(f'\\begin{{description}}{opt}')
        else:
            outgoing.append(line)
        modus = Modus.COPY
        opt = NO_OPTION
    else:
        outgoing.append(line)

    return modus, opt


def options(incoming: Iterable[str], lookup: Union[dict[str, str], None] = None) -> list[str]:
    r"""Later alligator. \option[style=multiline,leftmargin=6em]

    Examples:

    >>> in_opts = '[style=multiline,leftmargin=6em]'
    >>> opt_line = f'\\option{in_opts}'
    >>> beg_desc = '\\begin{description}'
    >>> lines_in = ['a', '', opt_line, '', beg_desc, 'whatever']
    >>> lines_in
    ['a', '', '\\option[style=multiline,leftmargin=6em]', '', '\\begin{description}', 'whatever']
    >>> processed = options(lines_in)
    >>> processed
    ['a', '', '', '\\begin{description}[style=multiline,leftmargin=6em]', 'whatever']
    """
    outgoing: list[str] = []
    modus = Modus.COPY
    opt = NO_OPTION
    for slot, line in enumerate(incoming):
        if modus == Modus.COPY:
            modus, opt = filter_seek_option(line, slot, modus, opt, outgoing)
        else:  # if modus == Modus.OPTION:
            modus, opt = filter_seek_description(line, slot, modus, opt, outgoing)

    return outgoing
