"""Splice (Finnish liitos) contributions."""
import datetime as dti
import logging
import os
import pathlib
import shellingham  # type: ignore
from typing import List, no_type_check

# [[[fill git_describe()]]]
__version__ = '2023.2.4+parent.a8f9966f'
# [[[end]]] (checksum: fc1e4d77954f04df2374dae00bbdd189)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)

APP_NAME = 'Splice (Finnish liitos) contributions.'
APP_ALIAS = 'liitos'
APP_ENV = 'LIITOS'
APP_VERSION = __version__
COMMA = ','
DEBUG = bool(os.getenv(f'{APP_ENV}_DEBUG', ''))
VERBOSE = bool(os.getenv(f'{APP_ENV}_VERBOSE', ''))
QUIET = False
STRICT = bool(os.getenv(f'{APP_ENV}_STRICT', ''))
ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'
DEFAULT_CONFIG_NAME = '.liitos.json'
DEFAULT_LF_ONLY = 'YES'
FILTER_CS_LIST = 'mermaid-filter'
FROM_FORMAT_SPEC = 'markdown+header_attributes+link_attributes+strikeout'
log = logging.getLogger()  # Module level logger is sufficient
LOG_FOLDER = pathlib.Path('logs')
LOG_FILE = f'{APP_ALIAS}.log'
LOG_PATH = pathlib.Path(LOG_FOLDER, LOG_FILE) if LOG_FOLDER.is_dir() else pathlib.Path(LOG_FILE)
LOG_LEVEL = logging.INFO
LOG_SEPARATOR = '- ' * 80

try:
    SHELL = shellingham.detect_shell()
except shellingham.ShellDetectionFailure:
    SHELL = ('', 'echo')

TOOL_VERSION_COMMAND_MAP = {
    'etiketti': 'etiketti --version',
    'exiftool': 'exiftool -ver',
    'foran': 'foran version',
    'git': 'git --version',
    'liitos': 'liitos version',
    'lualatex': 'lualatex --version',
    'mermaid': 'npm view mermaid',
    'mermaid-filter': 'npm view mermaid-filter',
    'navigaattori': 'navigaattori version',
    'node': 'node --version',
    'npm': 'npm --version',
    'pandoc': 'pandoc --version',
    'pdfinfo': 'pdfinfo -v',
    'python': 'python -V',
    'shell': f'{SHELL[1]} --version',
    'svgexport': 'npm view svgexport',
    'taksonomia': 'taksonomia --version',
}

ToolKey = str

TS_FORMAT_LOG = '%Y-%m-%dT%H:%M:%S'
TS_FORMAT_PAYLOADS = '%Y-%m-%d %H:%M:%S.%f UTC'

__all__: List[str] = [
    'APP_ALIAS',
    'APP_ENV',
    'APP_VERSION',
    'ENCODING',
    'FILTER_CS_LIST',
    'FROM_FORMAT_SPEC',
    'LOG_SEPARATOR',
    'TOOL_VERSION_COMMAND_MAP',
    'ToolKey',
    'TS_FORMAT_PAYLOADS',
    'log',
    'parse_csl',
]


def parse_csl(csl: str) -> List[str]:
    """DRY."""
    return [fmt.strip().lower() for fmt in csl.split(COMMA) if fmt.strip()]


@no_type_check
def formatTime_RFC3339(self, record, datefmt=None):  # noqa
    """HACK A DID ACK we could inject .astimezone() to localize ..."""
    return dti.datetime.fromtimestamp(record.created, dti.timezone.utc).isoformat()  # pragma: no cover


@no_type_check
def init_logger(name=None, level=None):
    """Initialize module level logger"""
    global log  # pylint: disable=global-statement

    log_format = {
        'format': '%(asctime)s %(levelname)s [%(name)s]: %(message)s',
        'datefmt': TS_FORMAT_LOG,
        # 'filename': LOG_PATH,
        'level': LOG_LEVEL if level is None else level,
    }
    logging.Formatter.formatTime = formatTime_RFC3339
    logging.basicConfig(**log_format)
    log = logging.getLogger(APP_ENV if name is None else name)
    log.propagate = True


init_logger(name=APP_ENV, level=logging.DEBUG if DEBUG else None)
