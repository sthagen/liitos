from collections.abc import Iterable

from liitos import log


def weave(incoming: Iterable[str]) -> list[str]:
    """Later alligator."""
    outgoing = []
    modus = 'copy'
    table, caption = '', ''
    for line in incoming:
        if modus == 'copy':
            if line.startswith(r'\begin{longtable}'):
                log.debug('within a table environment')
                modus = 'table'
                table = line
                caption = ''
            else:
                outgoing.append(line)

        elif modus == 'table':
            if line.startswith(r'\caption{'):
                log.debug('- found the caption start')
                caption = line
                if not caption.strip().endswith(r'}\tabularnewline'):
                    log.debug('- multi line caption')
                    modus = 'caption'
            elif line.startswith(r'\end{longtable}'):
                log.debug('end of table env detected')
                outgoing.append(table)
                outgoing.append(r'\rowcolor{white}')
                outgoing.append(caption)
                outgoing.append(line)
                modus = 'copy'
            else:
                log.debug('- table continues')
                table += line

        elif modus == 'caption':
            caption += line
            if line.strip().endswith(r'}\tabularnewline'):
                log.debug('- caption read')
                modus = 'table'

    return outgoing
