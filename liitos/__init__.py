"""Splice (Finnish liitos) contributions."""
import datetime as dti
import logging
import os
import pathlib
import shellingham  # type: ignore
from typing import List, no_type_check

# [[[fill git_describe()]]]
__version__ = '2023.2.25+parent.c8047488'
# [[[end]]] (checksum: adc3cbad5b41dbdb8f884dc0c67a6b55)
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
FROM_FORMAT_SPEC = 'markdown'
LATEX_PAYLOAD_NAME = 'document.tex'
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
    'etiketti': {
        'command': 'etiketti --version',
        'banner': 'Label and document the pdf file (data protection and identity)',
    },
    'exiftool': {
        'command': 'exiftool -ver',
        'banner': 'Change and list EXIF attributes',
    },
    'foran': {
        'command': 'foran version',
        'banner': 'Inspect local git status (or detect that there is no repository)',
    },
    'git': {
        'command': 'git --version',
        'banner': 'Version control system (git)',
    },
    'liitos': {
        'command': 'liitos version',
        'banner': 'Process the markdown documentation to produce PDF',
    },
    'lualatex': {
        'command': 'lualatex --version',
        'banner': 'Process LaTeX to produce PDF',
    },
    'mermaid': {
        'command': 'npm view mermaid',
        'banner': 'Mermaid for rendering diagrams from textual representations',
    },
    'mermaid-filter': {
        'command': 'npm view mermaid-filter',
        'banner': 'Pandoc filter for mermaid diagrams (rasterized version for PDF)',
    },
    'navigaattori': {
        'command': 'navigaattori version',
        'banner': 'Discover publication structural information from tree',
    },
    'node': {
        'command': 'node --version',
        'banner': 'Node server for executing some tools',
    },
    'npm': {
        'command': 'npm --version',
        'banner': 'Node package manager for inspecting versions of some node based tools',
    },
    'pandoc': {
        'command': 'pandoc --version',
        'banner': 'Pandoc for transforming markdown to LaTeX',
    },
    'pdfinfo': {
        'command': 'pdfinfo -v',
        'banner': 'Show PDF file information',
    },
    'python': {
        'command': 'python -V',
        'banner': 'Python driving it all',
    },
    'shell': {
        'command': f'{SHELL[1]} --version',
        'banner': 'The shell under which this process executes',
    },
    'svgexport': {
        'command': 'npm view svgexport',
        'banner': 'Export SVG to PNG (rasterized version for inclusion in PDF)',
    },
    'taksonomia': {
        'command': 'taksonomia --version',
        'banner': 'Assess and document the inventory of folders and files',
    },
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
    'LATEX_PAYLOAD_NAME',
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
