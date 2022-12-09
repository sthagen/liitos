from collections.abc import Iterable

from liitos import log

NO_LABEL = 'no-label-found-ERROR'


def inject(incoming: Iterable[str]) -> list[str]:
    """Later alligator."""
    outgoing = []
    modus = 'copy'
    label = NO_LABEL
    figure: list[str] = []
    caption: list[str] = []
    precondition = r'\begin{figure}'
    precondition_met = False
    for slot, line in enumerate(incoming):
        if modus == 'copy':
            if line.startswith(precondition):
                log.info(f'start of a figure environment at line #{slot + 1}')
                precondition_met = True
                outgoing.append(line)
                continue
            if line.startswith(r'\includegraphics{') and not precondition_met:
                log.warning(f'graphics include outside of a figure environment at line #{slot + 1}')
                log.error(f'line#{slot + 1}|{line}')
                log.info('trying to fix temporarily ... watch for marker MISSING-CAPTION-IN-MARKDOWN')
                adhoc_label = 'FIX-AT-SOURCE'
                try:
                    lab = line.split('{', 1)[1]
                    lab = lab.rsplit('.', 1)[0]
                    lab = lab.rsplit('/', 1)[1]
                    adhoc_label = r'\label{fig:' + lab + '}'
                    log.info(adhoc_label)
                except Exception as err:
                    log.error(f'failed to extract generic label from {line.strip()} with err: {err}')
                outgoing.append('')  # TODO(sthagen) - why do we sometimes received joined strings?
                outgoing.append(r'\begin{figure}')
                outgoing.append(r'\centering')
                outgoing.append(line)
                outgoing.append(r'\caption{MISSING-CAPTION-IN-MARKDOWN ' + adhoc_label + '}')
                outgoing.append(r'\end{figure}')
            elif line.startswith(r'\includegraphics{') and precondition_met:
                log.info(f'within a figure environment at line #{slot + 1}')
                log.info(line)
                modus = 'figure'
                figure = [line]
                try:
                    lab = line.split('{', 1)[1]
                    lab = lab.rsplit('.', 1)[0]
                    lab = lab.rsplit('/', 1)[1]
                    label = r'\label{fig:' + lab + '}'
                    log.info(label)
                except Exception as err:
                    log.error(f'failed to extract generic label from {line.strip()} with err: {err}')
                caption = []
            else:
                outgoing.append(line)

        elif modus == 'figure':
            if line.startswith(r'\caption{'):
                log.info(f'- found the caption start at line #{slot + 1}')
                caption.append(line)
                if not line.strip().endswith('}'):
                    log.info(f'- multi line caption at line #{slot + 1}')
                    modus = 'caption'
            elif line.startswith(r'\end{figure}'):
                log.info(f'end of figure env detected at line #{slot + 1}')
                outgoing.extend(figure)
                caption_text = '\n'.join(caption)
                if r'\label{' not in caption_text:
                    caption_text = f"{caption_text.rstrip().rstrip('}')} {label}" + '}'
                # if caption == caption.strip():
                #    caption += '\n'
                outgoing.append(caption_text)
                outgoing.append(line)
                modus = 'copy'
                label = NO_LABEL
                precondition_met = False
            else:
                log.debug(f'- figure continues at line #{slot + 1}')
                figure.append(line)

        elif modus == 'caption':
            caption.append(line)
            if line.strip().endswith(r'}'):
                log.info(f'- caption read at line #{slot + 1}')
                modus = 'figure'

    return outgoing
