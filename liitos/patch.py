"""Apply all pairs in patches to incoming."""
from collections.abc import Iterable

from liitos import log


def apply(patches: list[tuple[str, str]], incoming: Iterable[str]) -> list[str]:
    """Later alligator."""
    outgoing = [line for line in incoming]

    log.info(f'applying patches to {len(outgoing)} lines of text')
    for this, that in patches:
        log.info(f' - replacing any ({this}) with ({that}) ...')
        for n, text in enumerate(outgoing):
            if this in text:
                print(f'- found match ({text})')
                outgoing[n] = text.replace(this, that)

    return outgoing
