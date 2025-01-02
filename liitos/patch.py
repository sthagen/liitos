"""Apply all pairs in patches to incoming."""

from collections.abc import Iterable

from liitos import log


def apply(patches: list[tuple[str, str]], incoming: Iterable[str]) -> list[str]:
    """Apply all pairs in patches to incoming strings.

    Examples:

    >>> incoming = ['a', 'b', 'cb', 'd']
    >>> patches = [('b', 'x'), ('c', ''), ('y', 'foo')]
    >>> apply(patches, incoming)
    ['a', 'x', 'x', 'd']
    """
    outgoing = [line for line in incoming]

    log.info(f'applying patches to {len(outgoing)} lines of text')
    for this, that in patches:
        log.info(f' - trying any ({this}) --> ({that}) ...')
        for n, text in enumerate(outgoing):
            if this in text:
                log.info(f'   + found match ({text})')
                outgoing[n] = text.replace(this, that)

    return outgoing
