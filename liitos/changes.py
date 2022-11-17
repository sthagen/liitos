"""Weave the content of the changes data file into the output structure (for now LaTeX)."""
import datetime as dti
import pathlib
import sys

import yaml

from liitos import log

CHANGES_PATH = pathlib.Path('changes.yml')
METADATATEX_PATH = pathlib.Path('metadata.tex')
PUB_DATE_GREP_TOKEN = r'\newcommand{\theMetaDate}{'
PUBLISHER_TEMPLATE_PATH = pathlib.Path('publisher.tex.in')
PUBLISHER_PATH = pathlib.Path('publisher.tex')
ENCODING = 'utf-8'
TOKEN = r'\theMetaIssCode & \theMetaRevCode & \theMetaDate & \theMetaAuthor & \theChangeLogEntryDesc \\'
ROW_TEMPLATE = r'issue & 00 & date & author & summary \\'
GLUE = '\n\\hline\n'
COLUMNS_EXPECTED = ['issue', 'author', 'date', 'summary']
FORMAT_DATE = '%d %b %Y'


def weave_changes():
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
            log.error(
                f'Did not find explicit publication date in meta data at ({METADATATEX_PATH})'
                f' thus keeping {publication_date}'
            )

    log.info(f'Validating date to be in format ({FORMAT_DATE}) that is DD MON YYYY')
    try:
        ref = dti.datetime.strptime(publication_date, FORMAT_DATE).date().strftime(FORMAT_DATE).upper()
        if ref == publication_date:
            log.info(f'- publication date ({publication_date}) is valid')
        else:
            log.error(f'ERROR: full cycle conversion of found date ({publication_date}) is not the date itself ({ref})')
            sys.exit(1)
    except Exception as err:
        log.error(f'ERROR: full cycle conversion of found date ({publication_date}) failed with: {err}')
        sys.exit(1)

    log.info(f'Reading changes data from ({CHANGES_PATH}) ...')
    with open(CHANGES_PATH, 'rt', encoding=ENCODING) as handle:
        changes = yaml.safe_load(handle)

    log.info('Plausibility tests for changes ...')
    for slot, change in enumerate(changes['changes'], start=1):
        if sorted(change) != sorted(COLUMNS_EXPECTED):
            log.error('Unexpected column model!')
            log.error(f'-  expected: ({COLUMNS_EXPECTED})')
            log.error(f'- but found: ({change}) for entry #{slot}')
            sys.exit(1)

    rows = []
    for change in changes['changes']:
        issue, author, date, summary = (
            change['issue'],
            change['author'],
            change['date'],
            change['summary'],
        )
        date_rep = publication_date if date == 'PUBLICATIONDATE' else date
        rows.append(
            ROW_TEMPLATE.replace('issue', issue)
            .replace('date', date_rep)
            .replace('author', author)
            .replace('summary', summary)
        )

    with open(PUBLISHER_TEMPLATE_PATH, 'rt', encoding=ENCODING) as handle:
        lines = [line.rstrip() for line in handle.readlines()]

    log.info('Weaving in the changes ...')
    for n, line in enumerate(lines):
        if line.strip() == TOKEN:
            lines[n] = GLUE.join(rows)
            break
    if lines[-1]:
        lines.append('\n')
    with open(PUBLISHER_PATH, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(lines))
