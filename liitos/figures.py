from collections.abc import Iterable

from liitos import log

NO_RESCALE: float | int = 0


def inject(incoming: Iterable[str]) -> list[str]:
    """Later alligator."""
    outgoing = []
    modus = 'copy'
    rescale = NO_RESCALE
    for line in incoming:
        if modus == 'copy':
            if line.startswith(r'\scale='):
                log.debug('trigger a scale mod for the next figure environment')
                modus = 'scale'
                scale = line  # only for reporting wil not pass the filter
                try:
                    sca = scale.split('=', 1)[1].strip()  # \scale    =    75\%  --> 75\%
                    rescale = float(sca.replace(r'\%', '')) / 100 if r'\%' in sca else float(sca)
                except Exception as err:
                    log.error(f'failed to parse scale value from {line.strip()} with err: {err}')
            else:
                outgoing.append(line)

        elif modus == 'scale':
            if line.startswith(r'\includegraphics{'):
                if rescale != NO_RESCALE:
                    log.debug('- found the scale target start')
                    target = line.replace(r'\includegraphics', '')
                    option = f'[width={round(rescale, 2)}\\textwidth,height={round(rescale, 2)}\\textheight]'
                    outgoing.append(f'\\includegraphics{option}{target}')
                else:
                    outgoing.append(line)
                modus = 'copy'
                rescale = NO_RESCALE
            else:
                outgoing.append(line)

    return outgoing
