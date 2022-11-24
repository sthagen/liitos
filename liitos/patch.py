#! /usr/bin/env python
"""Apply all pairs in patch module on document."""
import pathlib

import yaml

from liitos import ENCODING, log

DOCUMENT = pathlib.Path('document.tex')


def apply() -> None:
    """Later alligator."""
    with open('patches.yml', 'rt', encoding=ENCODING) as handle:
        patches = yaml.safe_load(handle)

    log.info(f'reading document ({DOCUMENT}) for patching')
    with open(DOCUMENT, 'rt', encoding=ENCODING) as handle:
        lines = [line.strip() for line in handle.readlines()]

    log.info(f'applying patches to {len(lines)} lines of text')
    for this, that in patches['pairs']:
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
