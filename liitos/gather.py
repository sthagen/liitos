"""Gather the structure and discover the content."""
import argparse
import json
import logging
import os
import pathlib
from typing import Dict, List, Set, Tuple, Union

import yaml

from liitos import ENCODING, log

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
KEYS_REQUIRED = (KEY_APPROVALS, KEY_BIND, KEY_CHANGES, KEY_META)


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


def verify_target(name: str, target_set: Targets) -> Verification:
    """Verify presence of target yielding predicate and message (in case of failure)."""
    return (True, '') if name in target_set else (False, f'target ({name}) not in {sorted(target_set)}')


def verify_facet(name: str, target: str, facet_map: Facets) -> Verification:
    """Verify presence of facet for target yielding predicate and message (in case of failure)."""
    if name in facet_map[target]:
        return True, ''
    return False, f'facet ({name}) of target ({target}) not in {sorted(facet_map[target])}'


def error_context(
    payload: Payload, label: str, facet: str, target: str, path: PathLike, err: Union[FileNotFoundError, KeyError]
) -> Tuple[Payload, str]:
    """Provide harmonized context for the error situation as per parameters."""
    if isinstance(err, FileNotFoundError):
        return payload, f'{label} link not found at ({path}) or invalid for facet ({facet}) of target ({target})'
    if isinstance(err, KeyError):
        return [], f'{label} not found in assets for facet ({facet}) of target ({target})'
    if isinstance(err, ValueError):
        return [], f'{label} requires json or yaml format in assets for facet ({facet}) of target ({target})'
    raise NotImplementedError(f'error context not implemented for error ({err})')


def load_binder(facet: str, target: str, path: PathLike) -> Tuple[Binder, str]:
    """Yield the binder for facet of target from path and message (in case of failure)."""
    try:
        with open(path, 'rt', encoding=ENCODING) as handle:
            return [line.strip() for line in handle.readlines() if line.strip()], ''
    except FileNotFoundError as err:
        return error_context([], 'Binder', facet, target, path, err)  # type: ignore


def binder(facet: str, target: str, asset_struct: Assets) -> Tuple[Binder, str]:
    """Yield the binder for facet of target from link in assets and message (in case of failure)."""
    try:
        path = pathlib.Path(asset_struct[target][facet][KEY_BIND])
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


def meta(facet: str, target: str, asset_struct: Assets) -> Tuple[Meta, str]:
    """Yield the metadata for facet of target from link in assets and message (in case of failure)."""
    try:
        path = pathlib.Path(asset_struct[target][facet][KEY_META])
    except KeyError as err:
        return error_context({}, 'Metadata', facet, target, '', err)  # type: ignore
    return load_meta(facet, target, path)


def load_approvals(facet: str, target: str, path: PathLike) -> Tuple[Approvals, str]:
    """Yield the approvals for facet of target from path and message (in case of failure)."""
    if str(path).lower().endswith('json'):
        try:
            with open(path, 'rt', encoding=ENCODING) as handle:
                return json.load(handle), ''
        except FileNotFoundError as err:
            return error_context({}, 'Approvals', facet, target, path, err)  # type: ignore
    elif str(path).lower().endswith(('yaml', 'yml')):
        try:
            with open(path, 'rt', encoding=ENCODING) as handle:
                return yaml.safe_load(handle), ''
        except FileNotFoundError as err:
            return error_context({}, 'Approvals', facet, target, path, err)  # type: ignore

    return error_context({}, 'Approvals', facet, target, path, ValueError('json or yaml required'))  # type: ignore


def approvals(facet: str, target: str, asset_struct: Assets) -> Tuple[Approvals, str]:
    """Yield the approvals for facet of target from link in assets and message (in case of failure)."""
    try:
        path = pathlib.Path(asset_struct[target][facet][KEY_APPROVALS])
    except KeyError as err:
        return error_context({}, 'Approvals', facet, target, '', err)  # type: ignore
    return load_approvals(facet, target, path)


def load_changes(facet: str, target: str, path: PathLike) -> Tuple[Approvals, str]:
    """Yield the changes for facet of target from path and message (in case of failure)."""
    if str(path).lower().endswith('json'):
        try:
            with open(path, 'rt', encoding=ENCODING) as handle:
                return json.load(handle), ''
        except FileNotFoundError as err:
            return error_context({}, 'Changes', facet, target, path, err)  # type: ignore
    elif str(path).lower().endswith(('yaml', 'yml')):
        try:
            with open(path, 'rt', encoding=ENCODING) as handle:
                return yaml.safe_load(handle), ''
        except FileNotFoundError as err:
            return error_context({}, 'Changes', facet, target, path, err)  # type: ignore

    return error_context({}, 'Changes', facet, target, path, ValueError('json or yaml required'))  # type: ignore


def changes(facet: str, target: str, asset_struct: Assets) -> Tuple[Changes, str]:
    """Yield the changes for facet of target from link in assets and message (in case of failure)."""
    try:
        path = pathlib.Path(asset_struct[target][facet][KEY_CHANGES])
    except KeyError as err:
        return error_context({}, 'Changes', facet, target, '', err)  # type: ignore
    return load_changes(facet, target, path)


def verify_asset_keys(facet: str, target: str, asset_struct: Assets) -> Verification:
    """Verify presence of required keys for facet of target yielding predicate and message (in case of failure)."""
    if all(key in asset_struct[target][facet] for key in KEYS_REQUIRED):
        return True, ''
    return False, f'keys in {sorted(KEYS_REQUIRED)} for facet ({facet}) of target ({target}) are missing'


def verify_asset_links(facet: str, target: str, asset_struct: Assets) -> Verification:
    """Verify presence of asset links for facet of target yielding predicate and message (in case of failure)."""
    predicate, message = verify_asset_keys(facet, target, asset_struct)
    if not predicate:
        return predicate, message
    for key in KEYS_REQUIRED:
        link = pathlib.Path(asset_struct[target][facet][key])
        log.debug(f'  + verifying: {pathlib.Path.cwd() / link}')
        if not link.is_file() or not link.stat().st_size:
            return False, f'{key} asset link ({link}) for facet ({facet}) of target ({target}) is invalid'
    return True, ''


ASSET_KEY_ACTION = {
    KEY_APPROVALS: approvals,
    KEY_BIND: binder,
    KEY_CHANGES: changes,
    KEY_META: meta,
}


def verify_assets(facet: str, target: str, asset_struct: Assets) -> Verification:
    """Verify assets for facet of target yielding predicate and message (in case of failure)."""
    predicate, message = verify_asset_links(facet, target, asset_struct)
    if not predicate:
        return predicate, message
    for key, action in ASSET_KEY_ACTION.items():
        asset, message = action(facet, target, asset_struct)
        if not asset:
            return False, f'{key} asset for facet ({facet}) of target ({target}) is invalid'
    return True, ''


def prelude(
    doc_root: str | pathlib.Path, structure_name: str, target_key: str, facet_key: str, command: str
) -> tuple[Structure, Assets]:
    """DRY."""
    doc_root = pathlib.Path(doc_root)
    idem = os.getcwd()
    os.chdir(doc_root)
    job_description = (
        f'facet ({facet_key}) of target ({target_key}) with structure map ({structure_name})'
        f' in document root ({doc_root}) coming from ({idem})'
    )
    log.info(f'executing prelude of command ({command}) for {job_description}')
    structure = load_structure(structure_name)
    asset_map = assets(structure)
    return structure, asset_map


def verify(
    doc_root: str | pathlib.Path, structure_name: str, target_key: str, facet_key: str, options: dict[str, bool]
) -> int:
    """Drive the verification."""
    doc_root = pathlib.Path(doc_root)
    os.chdir(doc_root)
    facet = facet_key
    target = target_key
    structure_name = structure_name
    job_description = (
        f'facet ({facet}) for target ({target}) with structure map ({structure_name})' f' in document root ({doc_root})'
    )
    log.info(f'starting verification of {job_description}')
    structure = load_structure(structure_name)
    target_set = targets(structure)
    facet_map = facets(structure)
    asset_map = assets(structure)

    predicate, message = verify_target(target, target_set)
    if not predicate:
        log.error(f'failed verification with: {message}')
        return 1
    log.info(f'- target ({target}) OK')

    predicate, message = verify_facet(facet, target, facet_map)
    if not predicate:
        log.error(f'failed verification with: {message}')
        return 1
    log.info(f'- facet ({facet}) of target ({target}) OK')

    predicate, message = verify_assets(facet, target, asset_map)
    if not predicate:
        log.error(f'failed verification with: {message}')
        return 1
    log.info(f'- assets ({", ".join(sorted(KEYS_REQUIRED))}) for facet ({facet}) of target ({target}) OK')

    signatures_path = asset_map[target][facet][KEY_APPROVALS]
    log.info(f'loading signatures from {signatures_path=}')
    signatures = load_approvals(facet, target, signatures_path)
    log.info(f'{signatures=}')
    history_path = asset_map[target][facet][KEY_CHANGES]
    log.info(f'loading history from {history_path=}')
    history = load_changes(facet, target, history_path)
    log.info(f'{history=}')
    metadata_path = asset_map[target][facet][KEY_META]
    log.info(f'loading metadata from {metadata_path=}')
    info = load_meta(facet, target, metadata_path)
    log.info(f'{info=}')
    log.info('successful verification')
    return 0
