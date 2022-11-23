"""Weave the content of the approvals data file into the output structure (for now LaTeX)."""
import datetime as dti
import logging
import os
import pathlib

import yaml

import liitos.gather as gat
from liitos import log

APPROVALS_PATH = pathlib.Path('approvals.yml')
METADATATEX_IN_PATH = pathlib.Path('metadata.tex.in')
METADATATEX_PATH = pathlib.Path('metadata.tex')
PUB_DATE_GREP_TOKEN = r'\newcommand{\theMetaDate}{'
BOOKMATTER_TEMPLATE_PATH = pathlib.Path('bookmatter.tex.in')
BOOKMATTER_PATH = pathlib.Path('bookmatter.tex')
ENCODING = 'utf-8'
TOKEN = r'\ \mbox{THEROLE} & \mbox{THENAME} & \mbox{} \\[0.5ex]'
ROW_TEMPLATE = r'role & name & \mbox{} \\'
GLUE = '\n\\hline\n'
COLUMNS_EXPECTED = ['role', 'name']
FORMAT_DATE = '%d %b %Y'


def weave(
    doc_root: str | pathlib.Path, structure_name: str, target_key: str, facet_key: str, options: dict[str:bool]
) -> int:
    """Later alligator."""
    doc_root = pathlib.Path(doc_root)
    verbose = options['verbose']
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    os.chdir(doc_root)
    facet = facet_key
    target = target_key
    structure_name = structure_name
    job_description = (
        f'facet ({facet}) for target ({target}) with structure map ({structure_name})' f' in document root ({doc_root})'
    )
    log.info(f'Starting verification of {job_description}')
    structure = gat.load_structure(structure_name)
    asset_map = gat.assets(structure)

    signatures_path = asset_map[target][facet][gat.KEY_APPROVALS]
    log.info(f'Loading signatures from {signatures_path=}')
    signatures = gat.load_approvals(facet, target, signatures_path)
    log.info(f'{signatures=}')

    today = dti.datetime.today()
    publication_date = today.strftime(FORMAT_DATE).upper()
    log.info(f'Setting default publication date to today ({publication_date}) ...')
    log.info(f'Trying to read explicit publication date from meta data at ({METADATATEX_PATH}) ...')
    with open(METADATATEX_PATH, 'rt', encoding=ENCODING) as handle:
        for line in handle.readlines():
            if line.strip().startswith(PUB_DATE_GREP_TOKEN):
                pub_date_read = line.split(PUB_DATE_GREP_TOKEN, 1)[1].split('}', 1)[0].strip().upper()
                if pub_date_read == 'PUBLICATIONDATE':
                    log.info(f'- explicit publication date found as ({pub_date_read})')
                    log.info(f'  + keeping default {publication_date}')
                else:
                    publication_date = pub_date_read
                    log.info(f'- found explicit publication date override as ({publication_date})')
                break
        else:
            log.info(
                f'Did not find explicit publication date in meta data at ({METADATATEX_PATH})'
                f' thus keeping {publication_date}'
            )

    log.info(f'Validating date to be in format ({FORMAT_DATE}) that is DD MON YYYY')
    try:
        ref = dti.datetime.strptime(publication_date, FORMAT_DATE).date().strftime(FORMAT_DATE).upper()
        if ref == publication_date:
            log.info(f'- publication date ({publication_date}) is valid')
        else:
            log.info(f'ERROR: full cycle conversion of found date ({publication_date}) is not the date itself ({ref})')
            return 1
    except Exception as err:
        log.info(f'ERROR: full cycle conversion of found date ({publication_date}) failed with: {err}')
        return 1

    log.info('Plausibility tests for approvals ...')
    for slot, approval in enumerate(signatures[0]['approvals'], start=1):
        log.debug(f'{slot=}, {approval=}')
        if sorted(approval) != sorted(COLUMNS_EXPECTED):
            log.info('ERROR: Unexpected column model!')
            log.info(f'-  expected: ({COLUMNS_EXPECTED})')
            log.info(f'- but found: ({approval}) for entry #{slot}')
            return 1

    rows = []
    for approval in signatures[0]['approvals']:
        role = approval['role']  # type: ignore
        name = approval['name']  # type: ignore
        rows.append(ROW_TEMPLATE.replace('role', role).replace('name', name))

    with open(BOOKMATTER_TEMPLATE_PATH, 'rt', encoding=ENCODING) as handle:
        lines = [line.rstrip() for line in handle.readlines()]

    log.info('Weaving in the approvals ...')
    for n, line in enumerate(lines):
        if line.strip() == TOKEN:
            lines[n] = GLUE.join(rows)
            break
    if lines[-1]:
        lines.append('\n')
    with open(BOOKMATTER_PATH, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))
    return 0
