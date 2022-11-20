#! /usr/bin/env python
"""Apply all pairs in patch module on document."""
import pathlib

from liitos import log

try:
    import patches  # type: ignore
except ImportError:
    log.warning('please provide a patches.py file on python path (or local folder) if you want patches to be applied.')

    class patches:  # type: ignore
        pairs: list[tuple[str, str]] = []

    log.info('provided dummy patches')

DOCUMENT = pathlib.Path('document.tex')
ENCODING = 'utf-8'


def apply() -> None:
    """Later alligator."""
    lines = []
    log.info(f'reading document ({DOCUMENT}) for patching')
    with open(DOCUMENT, 'rt', encoding=ENCODING) as handle:
        lines = [line.strip() for line in handle.readlines()]

    log.info(f'applying patches to {len(lines)} lines of text')
    for this, that in patches.pairs:
        log.info(f' - trying ({this}) --> ({that}) ...')
        for n, text in enumerate(lines):
            if this in text:
                print(f'- found match ({text})')
                lines[n] = text.replace(this, that)

    if lines[-1]:
        lines.append('')  # Add a guaranteed newline at the end of the file

    log.info(f'writing patched document ({DOCUMENT})')
    with open(DOCUMENT, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))
