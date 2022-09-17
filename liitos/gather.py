"""Gather the structure and discover the content."""
import json
import pathlib
from typing import Dict, List, Set, Tuple, Union

import yaml

from liitos import ENCODING

PathLike = Union[str, pathlib.Path]

Approvals = Dict[str, Union[List[str], List[List[str]]]]
Assets = Dict[str, Dict[str, Dict[str, str]]]
Binder = List[str]
Changes = Dict[str, Union[List[str], List[List[str]]]]
Meta = Dict[str, str]
Structure = Dict[str, List[Dict[str, str]]]
Targets = Set[str]
Facets = Dict[str, Targets]
Payload = Union[Approvals, Binder, Changes, Meta]
Verification = Tuple[bool, str]

DEFAULT_STRUCTURE_NAME = 'structure.yml'
KEY_APPROVALS = 'approvals'
KEY_BIND = 'bind'
KEY_CHANGES = 'changes'
KEY_META = 'meta'


def load_structure(path: PathLike = DEFAULT_STRUCTURE_NAME) -> Structure:
    """Load the structure information and content links from the YAML file per convention."""
    with open(path, 'rt', encoding=ENCODING) as handle:
        return yaml.safe_load(handle)  # type: ignore


def targets(structure: Structure) -> Targets:
    """Extract the targets from the given structure information item."""
    return set(target for target in structure)


def facets(structure: Structure) -> Facets:
    """Extract the facets per target from the given structure information item."""
    return {target: set(facet for facet_data in cnt for facet in facet_data) for target, cnt in structure.items()}


def assets(structure: Structure) -> Assets:
    """Map the assets to facets of targets."""
    return {t: {f: asset for fd in cnt for f, asset in fd.items()} for t, cnt in structure.items()}  # type: ignore


def verify_target(name: str, targets: Targets) -> Verification:
    """Verify presence of target yielding predicate and message (in case of failure)."""
    return (True, '') if name in targets else (False, f'ERROR: target ({name}) not in {sorted(targets)}')


def verify_facet(name: str, target: str, facets: Facets) -> Verification:
    """Verify presence of facet for target yielding predicate and message (in case of failure)."""
    if name in facets[target]:
        return True, ''
    return False, f'ERROR: facet ({name}) of target ({target}) not in {sorted(facets[target])}'


def error_context(
    payload: Payload, label: str, facet: str, target: str, path: PathLike, err: Union[FileNotFoundError, KeyError]
) -> Tuple[Payload, str]:
    """Provide harmonized context for the error situation as per parameters."""
    if isinstance(err, FileNotFoundError):
        return payload, f'ERROR: {label} link not found at ({path}) or invalid for facet ({facet}) of target ({target})'
    if isinstance(err, KeyError):
        return [], f'ERROR: {label} not found in assets for facet ({facet}) of target ({target})'
    raise NotImplementedError(f'error context not implemented for error ({err})')


def load_binder(facet: str, target: str, path: PathLike) -> Tuple[Binder, str]:
    """Yield the binder for facet of target from path and message (in case of failure)."""
    try:
        with open(path, 'rt', encoding=ENCODING) as handle:
            return [line.strip() for line in handle.readlines() if line.strip()], ''
    except FileNotFoundError as err:
        return error_context([], 'Binder', facet, target, path, err)  # type: ignore


def binder(facet: str, target: str, assets: Assets) -> Tuple[Binder, str]:
    """Yield the binder for facet of target from link in assets and message (in case of failure)."""
    try:
        path = pathlib.Path(assets[target][facet][KEY_BIND])
    except KeyError as err:
        return error_context([], 'Binder', facet, target, '', err)  # type: ignore
    return load_binder(facet, target, path)


def load_meta(facet: str, target: str, path: PathLike) -> Tuple[Meta, str]:
    """Yield the metadata for facet of target from path and message (in case of failure)."""
    try:
        with open(path, 'rt', encoding=ENCODING) as handle:
            return yaml.safe_load(handle), ''
    except FileNotFoundError as err:
        return error_context({}, 'Metadata', facet, target, path, err)  # type: ignore


def meta(facet: str, target: str, assets: Assets) -> Tuple[Meta, str]:
    """Yield the metadata for facet of target from link in assets and message (in case of failure)."""
    try:
        path = pathlib.Path(assets[target][facet][KEY_META])
    except KeyError as err:
        return error_context({}, 'Metadata', facet, target, '', err)  # type: ignore
    return load_meta(facet, target, path)


def load_approvals(facet: str, target: str, path: PathLike) -> Tuple[Approvals, str]:
    """Yield the approvals for facet of target from path and message (in case of failure)."""
    try:
        with open(path, 'rt', encoding=ENCODING) as handle:
            return json.load(handle), ''
    except FileNotFoundError as err:
        return error_context({}, 'Approvals', facet, target, path, err)  # type: ignore


def approvals(facet: str, target: str, assets: Assets) -> Tuple[Approvals, str]:
    """Yield the approvals for facet of target from link in assets and message (in case of failure)."""
    try:
        path = pathlib.Path(assets[target][facet][KEY_APPROVALS])
    except KeyError as err:
        return error_context({}, 'Approvals', facet, target, '', err)  # type: ignore
    return load_approvals(facet, target, path)


def load_changes(facet: str, target: str, path: PathLike) -> Tuple[Approvals, str]:
    """Yield the changes for facet of target from path and message (in case of failure)."""
    try:
        with open(path, 'rt', encoding=ENCODING) as handle:
            return json.load(handle), ''
    except FileNotFoundError as err:
        return error_context({}, 'Changes', facet, target, path, err)  # type: ignore


def changes(facet: str, target: str, assets: Assets) -> Tuple[Changes, str]:
    """Yield the changes for facet of target from link in assets and message (in case of failure)."""
    try:
        path = pathlib.Path(assets[target][facet][KEY_CHANGES])
    except KeyError as err:
        return error_context({}, 'Changes', facet, target, '', err)  # type: ignore
    return load_changes(facet, target, path)
