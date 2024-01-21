"""Loader function for placeholders (mostly images)."""
import pathlib
import pkgutil
from typing import Union

from liitos import ENCODING, log

RESOURCES = (
    'placeholders/this-resource-is-missing.jpg',
    'placeholders/this-resource-is-missing.pdf',
    'placeholders/this-resource-is-missing.png',
    'placeholders/this-resource-is-missing.svg',
    'placeholders/this-resource-is-missing.tiff',
    'placeholders/this-resource-is-missing.webp',
)

READING_OPTIONS: dict[str, dict[str, Union[list[str], dict[str, str], None]]] = {
    '.jpg': {'args': ['rb'], 'kwargs': None},
    '.pdf': {'args': ['rb'], 'kwargs': None},
    '.png': {'args': ['rb'], 'kwargs': None},
    '.svg': {'args': ['rt'], 'kwargs': {'encoding': ENCODING}},
    '.tiff': {'args': ['rb'], 'kwargs': None},
    '.webp': {'args': ['rb'], 'kwargs': None},
}

WRITING_OPTIONS: dict[str, dict[str, Union[list[str], dict[str, str], None]]] = {
    '.jpg': {'args': ['wb'], 'kwargs': None},
    '.pdf': {'args': ['wb'], 'kwargs': None},
    '.png': {'args': ['wb'], 'kwargs': None},
    '.svg': {'args': ['wt'], 'kwargs': {'encoding': ENCODING}},
    '.tiff': {'args': ['wb'], 'kwargs': None},
    '.webp': {'args': ['wb'], 'kwargs': None},
}


def load_resource(resource: str, is_complete_path: bool = False) -> tuple[str, Union[bytes, str]]:
    """Load the template either from the package resources or an external path."""
    from_path = pathlib.Path(resource)
    suffix = from_path.suffix
    if is_complete_path:
        if suffix and suffix in READING_OPTIONS:
            args = READING_OPTIONS[suffix].get('args')
            kwargs = READING_OPTIONS[suffix].get('kwargs')
            if READING_OPTIONS[suffix].get('kwargs'):
                with open(from_path, *args, **kwargs) as handle:  # type: ignore
                    return 'str', handle.read()
            with open(from_path, *args) as handle:  # type: ignore
                return 'bytes', handle.read()
        with open(from_path, 'rb') as handle:  # type: ignore
            return 'bytes', handle.read()

    if suffix and suffix in READING_OPTIONS:
        args = READING_OPTIONS[suffix].get('args')
        kwargs = READING_OPTIONS[suffix].get('kwargs')
        if READING_OPTIONS[suffix].get('kwargs'):
            return 'str', pkgutil.get_data(__package__, resource).decode(**kwargs)  # type: ignore
        return 'bytes', pkgutil.get_data(__package__, resource)  # type: ignore

    return 'bytes', pkgutil.get_data(__package__, resource)  # type: ignore


def eject(argv: Union[list[str], None] = None) -> int:
    """Eject the templates into the folder given (default MISSING) and create the folder if it does not exist."""
    argv = argv if argv else ['']
    into = argv[0]
    if not into.strip():
        into = 'MISSING'
    into_path = pathlib.Path(into)
    (into_path / 'placeholders').mkdir(parents=True, exist_ok=True)
    for resource in RESOURCES:
        write_to = into_path / resource
        suffix = write_to.suffix
        log.info(f'{resource} -> {write_to}')
        if suffix and suffix in WRITING_OPTIONS:
            args = WRITING_OPTIONS[suffix].get('args')
            kwargs = WRITING_OPTIONS[suffix].get('kwargs')
            if WRITING_OPTIONS[suffix].get('kwargs'):
                log.info(f'text({resource}) per ({args=}) and ({kwargs=})')
                data = pkgutil.get_data(__package__, resource).decode(**kwargs)  # type: ignore
                with open(write_to, *args, **kwargs) as target:  # type: ignore
                    target.write(data)
                continue
            log.info(f'binary({resource}) per ({args=})')
            data = pkgutil.get_data(__package__, resource)
            with open(write_to, *args) as target:  # type: ignore
                target.write(data)  # type: ignore
            continue
        log.warning(f'suffix ({suffix}) empty or not in ({", ".join(WRITING_OPTIONS.keys())})')

    return 0
