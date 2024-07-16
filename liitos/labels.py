from collections.abc import Iterable
from typing import Union

from liitos import log

NO_LABEL = 'no-label-found-ERROR'


def is_include_graphics(text: str) -> bool:
    """Only DRY."""
    ntoken = r'\pandocbounded'  # nosec B105
    pos_after = len(ntoken)
    if len(text) > len(ntoken) and text.startswith(ntoken) and text[pos_after] in ('[', '{'):
        return True
    token = r'\includegraphics'  # nosec B105
    pos_after = len(token)
    return len(text) > len(token) and text.startswith(token) and text[pos_after] in ('[', '{')


def extract_image_path(include_graphics_line: str) -> str:
    """We had a bug, so we isolate in a function."""
    if include_graphics_line and 'pandocbounded{' in include_graphics_line:
        return include_graphics_line.split('{', 2)[2].rstrip().rstrip('}')
    if include_graphics_line and '{' in include_graphics_line:
        return include_graphics_line.split('{', 1)[1].rstrip().rstrip('}')
    else:
        return 'IMAGE_PATH_NOT_FOUND'


def inject(incoming: Iterable[str], lookup: Union[dict[str, str], None] = None) -> list[str]:
    """Later alligator."""
    outgoing = []
    modus = 'copy'
    label = NO_LABEL
    figure: list[str] = []
    caption: list[str] = []
    precondition = r'\begin{figure}'
    precondition_met = False
    for slot, line in enumerate(incoming):
        if line.startswith(precondition) and not precondition_met:
            log.info(f'start of a figure environment at line #{slot + 1}')
            precondition_met = True
            outgoing.append(line)
            continue

        if modus == 'copy':
            if is_include_graphics(line) and not precondition_met:
                log.warning(f'graphics include outside of a figure environment at line #{slot + 1}')
                log.debug(f'line#{slot + 1}|{line.rstrip()}')
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
                captain = 'MISSING-CAPTION-IN-MARKDOWN'
                try:
                    token = extract_image_path(line)
                    log.debug(f'- looking up key ({token}) for captions ...')
                    if lookup is not None:
                        cand = lookup.get(token, None)
                        if cand is not None:
                            captain = cand
                            log.debug(f'  + found ({captain})')
                        else:
                            log.debug(f'  ? no match for key ({token})')
                    else:
                        log.debug('  + no lut?')
                except Exception as err:
                    log.error(
                        f'failed to extract file path token for caption lookup from {line.strip()} with err: {err}'
                    )
                outgoing.append(r'\begin{figure}' + '\n')
                outgoing.append(r'\centering' + '\n')
                outgoing.append(line)
                outgoing.append(r'\caption{' + captain + ' ' + adhoc_label + '}' + '\n')
                outgoing.append(r'\end{figure}' + '\n')
            elif is_include_graphics(line) and precondition_met:
                log.info(f'within a figure environment at line #{slot + 1}')
                log.info(line.rstrip())
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
                log.debug(f'- copying {slot + 1 :3d}|{line.rstrip()}')
                outgoing.append(line)
            continue

        if modus == 'figure':
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
                if caption_text == caption_text.rstrip():
                    caption_text += '\n'
                outgoing.append(caption_text)
                outgoing.append(line)
                modus = 'copy'
                label = NO_LABEL
                precondition_met = False
            else:
                log.debug(f'- figure continues at line #{slot + 1}')
                figure.append(line)
            continue

        if modus == 'caption':
            caption.append(line)
            if line.strip().endswith(r'}'):
                log.info(f'- caption read at line #{slot + 1}')
                modus = 'figure'
            continue

    return outgoing
