from collections.abc import Iterable

from liitos import log

NO_LABEL = 'no-label-found-ERROR'


def inject(incoming: Iterable[str]) -> list[str]:
    """Later alligator."""
    outgoing = []
    modus = 'copy'
    label = NO_LABEL
    figure, caption = '', ''
    for line in incoming:
        if modus == 'copy':
            if line.startswith(r'\includegraphics{'):
                log.debug('within a figure environment')
                modus = 'figure'
                figure = line
                try:
                    lab = line.split('{', 1)[1]
                    lab = lab.rsplit('.', 1)[0]
                    lab = lab.rsplit('/', 1)[1]
                    label = r'\label{fig:' + lab + '}'
                except Exception as err:
                    log.error(f'failed to extract generic label from {line.strip()} with err: {err}')
                caption = ''
            else:
                outgoing.append(line)

        elif modus == 'figure':
            if line.startswith(r'\caption{'):
                log.debug('- found the caption start')
                caption = line
                if not caption.strip().endswith('}'):
                    log.debug('- multi line caption')
                    modus = 'caption'
            elif line.startswith(r'\end{figure}'):
                log.debug('end of figure env detected')
                outgoing.append(figure)
                if r'\label{' not in caption:
                    caption = f"{caption.rstrip().rstrip('}')} {label}" + '}'
                if caption == caption.strip():
                    caption += '\n'
                outgoing.append(caption)
                outgoing.append(line)
                modus = 'copy'
                label = NO_LABEL
            else:
                log.debug('- figure continues')
                figure += line

        elif modus == 'caption':
            caption += line
            if line.strip().endswith(r'}'):
                log.debug('- caption read')
                modus = 'figure'

    return outgoing
