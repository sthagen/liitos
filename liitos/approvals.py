"""Weave the content of the approvals data file into the output structure (for now LaTeX)."""
import datetime as dti
import pathlib
import sys

import yaml

from liitos import log

APPROVALS_PATH = pathlib.Path('approvals.yml')
METADATATEX_IN_PATH = pathlib.Path('metadata.tex.in')
METADATATEX_PATH = pathlib.Path('metadata.tex')
PUB_DATE_GREP_TOKEN = r'\newcommand{\theMetaDate}{'
BOOKMATTER_TEMPLATE_PATH = pathlib.Path('bookmatter.tex.in')
BOOKMATTER_PATH = pathlib.Path('bookmatter.tex')
ENCODING = 'utf-8'
TOKEN = r'\theMetaIssCode & \theMetaRevCode & \theMetaDate & \theChangeLogEntryDesc \\'
ROW_TEMPLATE = r'issue & 00 & date & summary \\'
GLUE = '\n\\hline\n'
COLUMNS_EXPECTED = ['role', 'name']
FORMAT_DATE = '%d %b %Y'


def weave() -> None:
    """Later alligator."""
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
            sys.exit(1)
    except Exception as err:
        log.info(f'ERROR: full cycle conversion of found date ({publication_date}) failed with: {err}')
        sys.exit(1)

    log.info(f'Reading changes data from ({APPROVALS_PATH}) ...')
    with open(APPROVALS_PATH, 'rt', encoding=ENCODING) as handle:
        approvals = yaml.safe_load(handle)

    log.info('Plausibility tests for changes ...')
    for slot, approval in enumerate(approvals['approvals'], start=1):
        if sorted(approval) != sorted(COLUMNS_EXPECTED):
            log.info('ERROR: Unexpected column model!')
            log.info(f'-  expected: ({COLUMNS_EXPECTED})')
            log.info(f'- but found: ({approval}) for entry #{slot}')
            sys.exit(1)

    rows = []
    for approval in approvals['approvals']:
        role = approval['role']
        author = approval['author']
        rows.append(ROW_TEMPLATE.replace('role', role).replace('author', author))

    with open(BOOKMATTER_TEMPLATE_PATH, 'rt', encoding=ENCODING) as handle:
        lines = [line.rstrip() for line in handle.readlines()]

    log.info('Weaving in the changes ...')
    for n, line in enumerate(lines):
        if line.strip() == TOKEN:
            lines[n] = GLUE.join(rows)
            break
    if lines[-1]:
        lines.append('\n')
    with open(BOOKMATTER_PATH, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))
