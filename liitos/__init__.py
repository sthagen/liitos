"""Splice (Finnish liitos) contributions."""

import datetime as dti
import logging
import os
import pathlib
import shellingham  # type: ignore
from typing import Union, no_type_check

# [[[fill git_describe()]]]
__version__ = '2024.11.6+parent.g82650d35'
# [[[end]]] (checksum: 83e1dc58fbbf7eb71f615e45238b623f)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)

APP_ALIAS = str(pathlib.Path(__file__).parent.name)
APP_ENV = APP_ALIAS.upper()
APP_NAME = locals()['__doc__']
DEBUG = bool(os.getenv(f'{APP_ENV}_DEBUG', ''))
VERBOSE = bool(os.getenv(f'{APP_ENV}_VERBOSE', ''))
QUIET = False
STRICT = bool(os.getenv(f'{APP_ENV}_STRICT', ''))
ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'
DEFAULT_CONFIG_NAME = f'.{APP_ALIAS}.json'

APP_VERSION = __version__
COMMA = ','
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

DEFAULT_STRUCTURE_NAME = 'structure.yml'
KEY_APPROVALS = 'approvals'
KEY_BIND = 'bind'
KEY_CHANGES = 'changes'
KEY_LAYOUT = 'layout'
KEY_META = 'meta'
KEYS_REQUIRED = (KEY_APPROVALS, KEY_BIND, KEY_CHANGES, KEY_META)

CONTEXT: dict[str, str] = {}
KNOWN_APPROVALS_STRATEGIES = ('south', 'east')
APPROVALS_STRATEGY = os.getenv('LIITOS_APPROVALS_STRATEGY', '').lower()

PathLike = Union[str, pathlib.Path]
PathLikeOrBool = Union[PathLike, bool]
ExternalsType = dict[str, dict[str, PathLikeOrBool]]

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

EXTERNALS: ExternalsType = {
    'bookmatter': {
        'id': 'templates/bookmatter.tex.in',
        'is_custom': False,
    },
    'driver': {
        'id': 'templates/driver.tex.in',
        'is_custom': False,
    },
    'publisher': {
        'id': 'templates/publisher.tex.in',
        'is_custom': False,
    },
    'metadata': {
        'id': 'templates/metadata.tex.in',
        'is_custom': False,
    },
    'setup': {
        'id': 'templates/setup.tex.in',
        'is_custom': False,
    },
}

BOOKMATTER_TEMPLATE = os.getenv('LIITOS_BOOKMATTER_TEMPLATE', '')
if BOOKMATTER_TEMPLATE:
    EXTERNALS['bookmatter'] = {'id': BOOKMATTER_TEMPLATE, 'is_custom': True}

DRIVER_TEMPLATE = os.getenv('LIITOS_DRIVER_TEMPLATE', '')
if DRIVER_TEMPLATE:
    EXTERNALS['driver'] = {'id': DRIVER_TEMPLATE, 'is_custom': True}

METADATA_TEMPLATE = os.getenv('LIITOS_METADATA_TEMPLATE', '')
if METADATA_TEMPLATE:
    EXTERNALS['metadata'] = {'id': METADATA_TEMPLATE, 'is_custom': True}

PUBLISHER_TEMPLATE = os.getenv('LIITOS_PUBLISHER_TEMPLATE', '')
if PUBLISHER_TEMPLATE:
    EXTERNALS['publisher'] = {'id': PUBLISHER_TEMPLATE, 'is_custom': True}

SETUP_TEMPLATE = os.getenv('LIITOS_SETUP_TEMPLATE', '')
if SETUP_TEMPLATE:
    EXTERNALS['setup'] = {'id': SETUP_TEMPLATE, 'is_custom': True}

TS_FORMAT_LOG = '%Y-%m-%dT%H:%M:%S'
TS_FORMAT_PAYLOADS = '%Y-%m-%d %H:%M:%S.%f UTC'

__all__: list[str] = [
    'APP_ALIAS',
    'APP_ENV',
    'APP_VERSION',
    'APPROVALS_STRATEGY',
    'DEFAULT_STRUCTURE_NAME',
    'ENCODING',
    'EXTERNALS',
    'ExternalsType',
    'CONTEXT',
    'FILTER_CS_LIST',
    'FROM_FORMAT_SPEC',
    'KEY_APPROVALS',
    'KEY_BIND',
    'KEY_CHANGES',
    'KEY_LAYOUT',
    'KEY_META',
    'KEYS_REQUIRED',
    'KNOWN_APPROVALS_STRATEGIES',
    'LATEX_PAYLOAD_NAME',
    'LOG_SEPARATOR',
    'PathLike',
    'TOOL_VERSION_COMMAND_MAP',
    'ToolKey',
    'TS_FORMAT_PAYLOADS',
    'log',
    'parse_csl',
]


def parse_csl(csl: str) -> list[str]:
    """DRY."""
    return [fmt.strip() for fmt in csl.split(COMMA) if fmt.strip()]


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
