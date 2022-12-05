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


def this(thing: str) -> int:
    """Later Alligator."""
    if thing not in THINGS:
        log.error(f'eject of unknown template ({thing}) requested')
        return 2
    content = template.load_resource(THINGS[thing], False)
    print(content)
    return 0
