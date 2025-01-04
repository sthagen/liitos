"""Apply any scale command to subsequent figure environment.

Implementation Note: The not a number (NAN) marker is used to indicate absence of scale command.
"""

from collections.abc import Iterable
from enum import Enum
import math
from typing import Union

from liitos import log

Modus = Enum('Modus', 'COPY SCALE')
NAN = float('nan')

SCALE_START_TRIGGER_STARTSWITH = r'\scale='
BARE_GRAPHICS_START_STARTSWITH = r'\includegraphics{'
WRAPPED_GRAPHICS_START_IN = r'\pandocbounded{\includegraphics'


def filter_seek_scale(line: str, slot: int, modus: Modus, rescale: float, outgoing: list[str]) -> tuple[Modus, float]:
    r"""Filter line, seek for a scale command, and return updated mnodus, rescale pair.

    Examples:

    >>> o = []
    >>> line = SCALE_START_TRIGGER_STARTSWITH  # r'\scale='
    >>> m, r = filter_seek_scale(line, 0, Modus.COPY, NAN, o)
    >>> assert not o
    >>> assert m == Modus.SCALE
    >>> assert math.isnan(r)

    >>> o = []
    >>> m, r = filter_seek_scale('foo', 0, Modus.COPY, NAN, o)
    >>> assert o == ['foo']
    >>> assert m == Modus.COPY
    >>> assert math.isnan(r)

    >>> o = []
    >>> m, r = filter_seek_scale(r'\scale=80\%', 0, Modus.COPY, NAN, o)
    >>> assert not o
    >>> assert m == Modus.SCALE
    >>> assert r == 0.8
    """
    if line.startswith(SCALE_START_TRIGGER_STARTSWITH):
        log.info(f'trigger a scale mod for the next figure environment at line #{slot + 1}|{line}')
        modus = Modus.SCALE
        scale = line  # only for reporting will not pass the filter
        try:
            sca = scale.split('=', 1)[1].strip()  # \scale    =    75\%  --> 75\%
            rescale = float(sca.replace(r'\%', '')) / 100 if r'\%' in sca else float(sca)
        except Exception as err:
            log.error(f'failed to parse scale value from {line.strip()} with err: {err}')
    else:
        outgoing.append(line)

    return modus, rescale


def filter_seek_figure(line: str, slot: int, modus: Modus, rescale: float, outgoing: list[str]) -> tuple[Modus, float]:
    r"""Filter line, seek for a figure, rescale if applicable, and return updated mnodus, rescale pair.

    Examples:

    >>> o = []
    >>> m, r = filter_seek_figure(r'\includegraphics{', 0, Modus.COPY, NAN, o)
    >>> assert o == [r'\includegraphics{']
    >>> assert m == Modus.COPY
    >>> assert math.isnan(r)

    >>> o = []
    >>> m, r = filter_seek_figure('foo', 0, Modus.COPY, 0.8, o)
    >>> assert o == ['foo']
    >>> assert m == Modus.COPY
    >>> assert r == 0.8

    >>> o = []
    >>> rescale = 0.8
    >>> m, r = filter_seek_figure(r'\pandocbounded{\includegraphics', 0, Modus.COPY, rescale, o)
    >>> assert o[0].startswith(r'\pandocbounded{\includegraphics')
    >>> assert f'textwidth,height={rescale}' in o[0]
    >>> assert m == Modus.COPY
    >>> assert math.isnan(r)

    >>> o = []
    >>> m, r = filter_seek_figure(r'\pandocbounded{\includegraphics', 0, Modus.COPY, NAN, o)
    >>> assert o[0].startswith(r'\pandocbounded{\includegraphics')
    >>> assert m == Modus.COPY
    >>> assert math.isnan(r)
    """
    if line.startswith(BARE_GRAPHICS_START_STARTSWITH):
        if not math.isnan(rescale):
            log.info(f'- found the scale target start at line #{slot + 1}|{line}')
            target = line.replace(BARE_GRAPHICS_START_STARTSWITH, '{')
            option = f'[width={round(rescale, 2)}\\textwidth,height={round(rescale, 2)}' '\\textheight,keepaspectratio]'
            outgoing.append(f'\\includegraphics{option}{target}')
        else:
            outgoing.append(line)
        modus = Modus.COPY
        rescale = NAN
    elif WRAPPED_GRAPHICS_START_IN in line:
        if not math.isnan(rescale):
            log.info(f'- found the scale target start at line #{slot + 1}|{line}')
            target = line.replace(WRAPPED_GRAPHICS_START_IN, '').replace('[keepaspectratio]', '')
            parts = target.split('}}')
            rest, inside = ('', '') if len(parts) < 2 else (parts[1].lstrip('}'), parts[0] + '}')
            option = f'[width={round(rescale, 2)}\\textwidth,height={round(rescale, 2)}' '\\textheight,keepaspectratio]'
            outgoing.append(f'{WRAPPED_GRAPHICS_START_IN}{option}{inside}}}{rest}')
        else:
            outgoing.append(line)
        modus = Modus.COPY
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
    modus = Modus.COPY
    rescale = NAN
    for slot, line in enumerate(incoming):
        line = line.rstrip('\n')
        if modus == Modus.COPY:
            modus, rescale = filter_seek_scale(line, slot, modus, rescale, outgoing)
        else:  # if modus == Modus.SCALE:
            modus, rescale = filter_seek_figure(line, slot, modus, rescale, outgoing)

    return outgoing
