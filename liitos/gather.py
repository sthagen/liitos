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
Verification = Tuple[bool, str]


def load_structure(path: PathLike = 'structure.yml') -> Structure:
    """Load the structure information and content links from the YAML file per convention."""
    with open(path, 'rt', encoding=ENCODING) as handle:
        return yaml.safe_load(handle)


def targets(structure: Structure) -> Targets:
    """Extract the targets from the given structure information item."""
    return set(target for target in structure)


def facets(structure: Structure) -> Facets:
    """Extract the facets per target from the given structure information item."""
    return {target: set(facet for facet_data in cnt for facet in facet_data) for target, cnt in structure.items()}


def assets(structure: Structure) -> Assets:
    """Map the assets to facets of targets."""
    return {target: {f: asset for fd in cnt for f, asset in fd.items()} for target, cnt in structure.items()}


def verify_target(name: str, targets: Targets) -> Verification:
    """Verify presence of target yielding predicate and message (in case of failure)."""
    return (True, '') if name in targets else (False, f'ERROR: target ({name}) not in {sorted(targets)}')


def verify_facet(name: str, target: str, facets: Facets) -> Verification:
    """Verify presence of facet for target yielding predicate and message (in case of failure)."""
    if name in facets[target]:
        return True, ''
    return False, f'ERROR: facet ({name}) of target ({target}) not in {sorted(facets[target])}'


def binder(facet: str, target: str, assets: Assets) -> Tuple[Binder, str]:
    """Yield the binder for facet of target from link in assets and message (in case of failure)."""
    try:
        path = pathlib.Path(assets[target][facet]['bind'])
    except KeyError:
        return [], f'ERROR: Binder link not found in assets for facet ({facet}) of target ({target})'
    try:
        with open(path, 'rt', encoding=ENCODING) as handle:
            return [line.strip() for line in handle.readlines() if line.strip()], ''
    except FileNotFoundError:
        return [], f'ERROR: Binder not found at ({path}) or invalid for facet ({facet}) of target ({target})'


def meta(facet: str, target: str, assets: Assets) -> Tuple[Meta, str]:
    """Yield the metadata for facet of target from link in assets and message (in case of failure)."""
    try:
        path = pathlib.Path(assets[target][facet]['meta'])
    except KeyError:
        return {}, f'ERROR: Metadata link not found in assets for facet ({facet}) of target ({target})'
    try:
        with open(path, 'rt', encoding=ENCODING) as handle:
            return yaml.safe_load(handle), ''
    except FileNotFoundError:
        return {}, f'ERROR: Metadata not found at ({path}) or invalid for facet ({facet}) of target ({target})'


def approvals(facet: str, target: str, assets: Assets) -> Tuple[Approvals, str]:
    """Yield the approvals for facet of target from link in assets and message (in case of failure)."""
    try:
        path = pathlib.Path(assets[target][facet]['approvals'])
    except KeyError:
        return {}, f'ERROR: Approvals link not found in assets for facet ({facet}) of target ({target})'
    try:
        with open(path, 'rt', encoding=ENCODING) as handle:
            return json.load(handle), ''
    except FileNotFoundError:
        return {}, f'ERROR: Approvals not found at ({path}) or invalid for facet ({facet}) of target ({target})'


def changes(facet: str, target: str, assets: Assets) -> Tuple[Changes, str]:
    """Yield the changes for facet of target from link in assets and message (in case of failure)."""
    try:
        path = pathlib.Path(assets[target][facet]['changes'])
    except KeyError:
        return {}, f'ERROR: Changes link not found in assets for facet ({facet}) of target ({target})'
    try:
        with open(path, 'rt', encoding=ENCODING) as handle:
            return json.load(handle), ''
    except FileNotFoundError:
        return {}, f'ERROR: Changes not found at ({path}) or invalid for facet ({facet}) of target ({target})'
