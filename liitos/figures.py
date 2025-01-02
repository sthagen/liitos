from collections.abc import Iterable
import math
from typing import Union

from liitos import log

NAN = float('nan')


def filter_seek_scale(line: str, slot: int, modus: str, rescale: float, outgoing: list[str]) -> tuple[str, float]:
    r"""Filter line, seek for a scale command, and return updated mnodus, rescale pair.

    Examples:

    >>> o = []
    >>> m, r = filter_seek_scale(r'\scale=', 0, 'copy', NAN, o)
    >>> assert not o
    >>> assert m == 'scale'
    >>> assert math.isnan(r)

    >>> o = []
    >>> m, r = filter_seek_scale('foo', 0, 'copy', NAN, o)
    >>> assert o == ['foo']
    >>> assert m == 'copy'
    >>> assert math.isnan(r)

    >>> o = []
    >>> m, r = filter_seek_scale(r'\scale=80\%', 0, 'copy', NAN, o)
    >>> assert not o
    >>> assert m == 'scale'
    >>> assert r == 0.8
    """
    if line.startswith(r'\scale='):
        log.info(f'trigger a scale mod for the next figure environment at line #{slot + 1}|{line}')
        modus = 'scale'
        scale = line  # only for reporting will not pass the filter
        try:
            sca = scale.split('=', 1)[1].strip()  # \scale    =    75\%  --> 75\%
            rescale = float(sca.replace(r'\%', '')) / 100 if r'\%' in sca else float(sca)
        except Exception as err:
            log.error(f'failed to parse scale value from {line.strip()} with err: {err}')
    else:
        outgoing.append(line)

    return modus, rescale


def filter_seek_figure(line: str, slot: int, modus: str, rescale: float, outgoing: list[str]) -> tuple[str, float]:
    r"""Filter line, seek for a figure, rescale if applicable, and return updated mnodus, rescale pair.

    Examples:

    >>> o = []
    >>> m, r = filter_seek_figure(r'\includegraphics{', 0, 'copy', NAN, o)
    >>> assert o == [r'\includegraphics{']
    >>> assert m == 'copy'
    >>> assert math.isnan(r)

    >>> o = []
    >>> m, r = filter_seek_figure('foo', 0, 'copy', 0.8, o)
    >>> assert o == ['foo']
    >>> assert m == 'copy'
    >>> assert r == 0.8

    >>> o = []
    >>> rescale = 0.8
    >>> m, r = filter_seek_figure(r'\pandocbounded{\includegraphics', 0, 'copy', rescale, o)
    >>> assert o[0].startswith(r'\pandocbounded{\includegraphics')
    >>> assert f'textwidth,height={rescale}' in o[0]
    >>> assert m == 'copy'
    >>> assert math.isnan(r)

    >>> o = []
    >>> m, r = filter_seek_figure(r'\pandocbounded{\includegraphics', 0, 'copy', NAN, o)
    >>> assert o[0].startswith(r'\pandocbounded{\includegraphics')
    >>> assert m == 'copy'
    >>> assert math.isnan(r)
    """
    if line.startswith(r'\includegraphics{'):
        if not math.isnan(rescale):
            log.info(f'- found the scale target start at line #{slot + 1}|{line}')
            target = line.replace(r'\includegraphics', '')
            option = f'[width={round(rescale, 2)}\\textwidth,height={round(rescale, 2)}' '\\textheight,keepaspectratio]'
            outgoing.append(f'\\includegraphics{option}{target}')
        else:
            outgoing.append(line)
        modus = 'copy'
        rescale = NAN
    elif r'\pandocbounded{\includegraphics' in line:
        if not math.isnan(rescale):
            log.info(f'- found the scale target start at line #{slot + 1}|{line}')
            target = line.replace(r'\pandocbounded{\includegraphics', '').replace('[keepaspectratio]', '')
            parts = target.split('}}')
            rest, inside = '', ''
            if len(parts) > 1:
                inside = parts[0] + '}'
                if len(parts) == 2:
                    rest = parts[1].lstrip('}')
            option = f'[width={round(rescale, 2)}\\textwidth,height={round(rescale, 2)}' '\\textheight,keepaspectratio]'
            outgoing.append(f'\\pandocbounded{{\\includegraphics{option}{inside}}}{rest}')
        else:
            outgoing.append(line)
        modus = 'copy'
        rescale = NAN
    else:
        outgoing.append(line)

    return modus, rescale


def scale(incoming: Iterable[str], lookup: Union[dict[str, str], None] = None) -> list[str]:
    r"""Scan for scale command and if, apply it to the includegraphics LaTeX command.

    Examples:

    >>> in_lines = [r'\scale=80\%', '', r'\includegraphics{', '', 'quux']
    >>> scaled = scale(in_lines)
    >>> scaled
    ['', '\\includegraphics[width=0.8\\textwidth,height=0.8\\textheight,keepaspectratio]{', '', 'quux']


    >>> in_lines = ['foo', '', r'\includegraphics{', '', 'quux']
    >>> scaled = scale(in_lines)
    >>> scaled
    ['foo', '', '\\includegraphics{', '', 'quux']
    """
    outgoing: list[str] = []
    modus = 'copy'
    rescale = NAN
    for slot, line in enumerate(incoming):
        line = line.rstrip('\n')
        if modus == 'copy':
            modus, rescale = filter_seek_scale(line, slot, modus, rescale, outgoing)
        else:  # if modus == 'scale':
            modus, rescale = filter_seek_figure(line, slot, modus, rescale, outgoing)

    return outgoing
