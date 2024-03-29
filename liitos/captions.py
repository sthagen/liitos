from collections.abc import Iterable
from typing import Union

from liitos import log


def weave(incoming: Iterable[str], lookup: Union[dict[str, str], None] = None) -> list[str]:
    """Later alligator."""
    outgoing = []
    modus = 'copy'
    table: list[str] = []
    caption: list[str] = []
    for slot, line in enumerate(incoming):
        if modus == 'copy':
            if line.startswith(r'\begin{longtable}'):
                log.info(f'start of a table environment at line #{slot + 1}')
                modus = 'table'
                table = [line]
                caption = []
            else:
                outgoing.append(line)

        elif modus == 'table':
            if line.startswith(r'\caption{'):
                log.info(f'- found the caption start at line #{slot + 1}')
                caption.append(line)
                if not line.strip().endswith(r'}\tabularnewline'):
                    log.info(f'- multi line caption at line #{slot + 1}')
                    modus = 'caption'
            elif line.startswith(r'\end{longtable}'):
                log.info(f'end of table env detected at line #{slot + 1}')
                for stmt in table:
                    if not stmt.startswith(r'\endlastfoot'):
                        outgoing.append(stmt)
                        continue
                    else:
                        outgoing.extend(caption)
                        outgoing.append(stmt)
                outgoing.append(line)
                modus = 'copy'
            else:
                log.debug('- table continues')
                table.append(line)

        elif modus == 'caption':
            caption.append(line)
            if line.strip().endswith(r'}\tabularnewline'):
                log.info(f'- caption read at line #{slot + 1}')
                modus = 'table'

    return outgoing
