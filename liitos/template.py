"""Loader function for templates."""

import pathlib
import pkgutil
from typing import Union

from liitos import ENCODING, PathLike

RESOURCES = (
    'templates/approvals.yml',
    'templates/bookmatter.tex.in',
    'templates/changes.yml',
    'templates/driver.tex.in',
    'templates/layout.yml',
    'templates/meta.yml',
    'templates/meta-patch.yml',
    'templates/metadata.tex.in',
    'templates/mkdocs.yml.in',
    'templates/publisher.tex.in',
    'templates/setup.tex.in',
    'templates/vocabulary.yml',
)


def load_resource(resource: PathLike, is_complete_path: bool = False) -> str:
    """Load the template either from the package resources or an external path."""
    if is_complete_path:
        with open(resource, 'rt', encoding=ENCODING) as handle:
            return handle.read()
    else:
        return pkgutil.get_data(__package__, str(resource)).decode(encoding=ENCODING)  # type: ignore


def eject(argv: Union[list[str], None] = None) -> int:
    """Eject the templates into the folder given (default EJECTED) and create the folder if it does not exist."""
    argv = argv if argv else ['']
    into = argv[0]
    if not into.strip():
        into = 'EJECTED'
    into_path = pathlib.Path(into)
    (into_path / 'templates').mkdir(parents=True, exist_ok=True)
    for resource in RESOURCES:
        write_to = into_path / resource
        data = pkgutil.get_data(__package__, resource).decode(encoding=ENCODING)  # type: ignore
        with open(write_to, 'wt', encoding=ENCODING) as target:
            target.write(data)

    return 0
