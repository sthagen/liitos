"""Apply any option command to subsequent description environment.

Implementation Note: The empty string marker is used to indicate absence of option command.
"""

from collections.abc import Iterable
from enum import Enum
from typing import Union

from liitos import log

Modus = Enum('Modus', [('COPY', 1), ('OPTION', 2)])
NO_OPTION: str = ''


def parse_option_command(slot: int, text_line: str) -> tuple[bool, str, str]:
    r"""Parse the \option[style=multiline,leftmargin=6em].

    Examples:

    >>> in_opts = '[style=multiline,leftmargin=6em]'
    >>> line = rf'\option{in_opts}'
    >>> ok, processed, out_opts = parse_option_command(42, line)
    >>> assert ok
    >>> assert processed.startswith('%CONSIDERED_')
    >>> assert out_opts == in_opts

    >>> line = 'foo'
    >>> ok, processed, out_opts = parse_option_command(-1, line)
    >>> assert not ok
    >>> assert processed == line
    >>> assert out_opts == ''
    """
    if text_line.startswith(r'\option['):
        log.info(f'trigger an option mod for the next description environment at line #{slot + 1}|{text_line}')
        # \option[style=multiline,leftmargin=6em]  --> [style=multiline,leftmargin=6em]
        opt = text_line.split(r'\option', 1)[1].strip()
        log.info(f' -> parsed option as ({opt})')
        return True, f'%CONSIDERED_{text_line}', opt
    else:
        return False, text_line, ''


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
    outgoing = []
    modus = Modus.COPY
    opt = NO_OPTION
    for slot, line in enumerate(incoming):
        if modus == Modus.COPY:
            has_opt, text_line, opt = parse_option_command(slot, line)
            if has_opt:
                modus = Modus.OPTION
            else:
                outgoing.append(text_line)
            continue

        # if modus == 'option':
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

    return outgoing
