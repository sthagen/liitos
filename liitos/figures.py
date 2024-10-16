from collections.abc import Iterable
from typing import Union

from liitos import log

NO_RESCALE: Union[float, int] = 0


def scale(incoming: Iterable[str], lookup: Union[dict[str, str], None] = None) -> list[str]:
    """Later alligator."""
    outgoing = []
    modus = 'copy'
    rescale = NO_RESCALE
    for slot, line in enumerate(incoming):
        if modus == 'copy':
            if line.startswith(r'\scale='):
                log.info(f'trigger a scale mod for the next figure environment at line #{slot + 1}|{line}')
                modus = 'scale'
                scale = line  # only for reporting wil not pass the filter
                try:
                    sca = scale.split('=', 1)[1].strip()  # \scale    =    75\%  --> 75\%
                    rescale = float(sca.replace(r'\%', '')) / 100 if r'\%' in sca else float(sca)
                except Exception as err:
                    log.error(f'failed to parse scale value from {line.strip()} with err: {err}')
            else:
                outgoing.append(line)

        else:  # if modus == 'scale':
            if line.startswith(r'\includegraphics{'):
                if rescale != NO_RESCALE:
                    log.info(f'- found the scale target start at line #{slot + 1}|{line}')
                    target = line.replace(r'\includegraphics', '')
                    option = (
                        f'[width={round(rescale, 2)}\\textwidth,height={round(rescale, 2)}'
                        '\\textheight,keepaspectratio]'
                    )
                    outgoing.append(f'\\includegraphics{option}{target}')
                else:
                    outgoing.append(line)
                modus = 'copy'
                rescale = NO_RESCALE
            elif r'\pandocbounded{\includegraphics' in line:
                if rescale != NO_RESCALE:
                    log.info(f'- found the scale target start at line #{slot + 1}|{line}')
                    target = line.replace(r'\pandocbounded{\includegraphics', '').replace('[keepaspectratio]', '')
                    parts = target.split('}}')
                    rest = ''
                    if len(parts) >= 1:
                        inside = parts[0] + '}'
                        if len(parts) == 2:
                            rest = parts[1].lstrip('}')
                    option = (
                        f'[width={round(rescale, 2)}\\textwidth,height={round(rescale, 2)}'
                        '\\textheight,keepaspectratio]'
                    )
                    outgoing.append(f'\\pandocbounded{{\\includegraphics{option}{inside}}}{rest}')
                else:
                    outgoing.append(line)
                modus = 'copy'
                rescale = NO_RESCALE
            else:
                outgoing.append(line)

    return outgoing
