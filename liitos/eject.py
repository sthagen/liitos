"""Eject templates and configurations."""
import json
import os
import pathlib
import shutil
import sys

import yaml

import liitos.gather as gat
import liitos.template_loader as template
from liitos import ENCODING, log

THINGS = {
    'bookmatter-pdf': (BOOKMATTER_TEMPLATE := 'templates/bookmatter.tex.in'),
    'driver-pdf': (DRIVER_TEMPLATE := 'templates/driver.tex.in'),
    'metadata-pdf': (METADATA_TEMPLATE := 'templates/metadata.tex.in'),
    'publisher-pdf': (PUBLISHER_TEMPLATE := 'templates/publisher.tex.in'),
    'setup-pdf': (SETUP_TEMPLATE := 'templates/setup.tex.in'),
    'approvals-yaml': (APPROVALS_YAML := 'templates/approvals.yml'),
    'changes-yaml': (CHANGES_YAML := 'templates/changes.yml'),
    'meta-base-yaml': (META_YAML := 'templates/meta.yml'),
    'meta-patch-yaml': (META_PATCH_YAML := 'templates/meta-patch.yml'),
    'vocabulary-yaml': (VOCABULARY_YAML := 'templates/vocabulary.yml'),
}


def this(thing: str, out: str = '') -> int:
    """Later Alligator."""
    if not thing:
        log.error('eject of template with no name requested')
        log.info(f'templates known: ({", ".join(sorted(THINGS))})')
        return 2
    guesses = sorted(entry for entry in THINGS if entry.startswith(thing))
    if not guesses:
        log.error(f'eject of unknown template ({thing}) requested')
        log.info(f'templates known: ({", ".join(sorted(THINGS))})')
        return 2
    if len(guesses) > 1:
        log.error(f'eject of ambiguous template ({thing}) requested - matches ({", ".join(guesses)})')
        return 2
    content = template.load_resource(THINGS[guesses[0]], False)
    if not out:
        print(content)
        return 0

    out_path = pathlib.Path(out)
    out_name = out_path.name
    if not THINGS[guesses[0]].endswith(out_name):
        log.warning(f'requested writing ({THINGS[guesses[0]]}) to file ({out_name})')
    with open(out_path, 'wt', encoding=ENCODING) as handle:
        handle.write(content)
    return 0
