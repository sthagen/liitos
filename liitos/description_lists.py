from collections.abc import Iterable

from liitos import log

NO_OPTION: str = ''


def options(incoming: Iterable[str]) -> list[str]:
    """Later alligator. \option[style=multiline,leftmargin=6em]"""
    outgoing = []
    modus = 'copy'
    opt = NO_OPTION
    for slot, line in enumerate(incoming):
        if modus == 'copy':
            if line.startswith(r'\option['):
                log.info(f'trigger an option mod for the next description environment at line #{slot + 1}|{line}')
                modus = 'scale'
                option_save = line  # only for reporting will not pass the filter
                try:
                    # \option[style=multiline,leftmargin=6em]  --> [style=multiline,leftmargin=6em]
                    opt = option_save.split(r'\option', 1)[1].strip()
                except Exception as err:
                    log.error(f'failed to parse option value from {line.strip()} with err: {err}')
            else:
                outgoing.append(line)

        else:  # if modus == 'scale':
            if line.startswith(r'\begin{description}'):
                if opt != NO_OPTION:
                    log.info(f'- found the option target start at line #{slot + 1}|{line}')
                    outgoing.append(f'\\begin{{description}}{opt}')
                else:
                    outgoing.append(line)
                modus = 'copy'
                opt = NO_OPTION
            else:
                outgoing.append(line)

    return outgoing
