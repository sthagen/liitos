import datetime as dti
import difflib
import hashlib
import pathlib
import subprocess  # nosec B404
from typing import Any, Callable, no_type_check

import foran.foran as api  # type: ignore
from foran.report import generate_report  # type: ignore
from taksonomia.taksonomia import Taxonomy  # type: ignore

from liitos import ENCODING, LATEX_PAYLOAD_NAME, TOOL_VERSION_COMMAND_MAP, ToolKey, log

DOC_BASE = pathlib.Path('..', '..')
STRUCTURE_PATH = DOC_BASE / 'structure.yml'
IMAGES_FOLDER = 'images/'
DIAGRAMS_FOLDER = 'diagrams/'
PATCH_SPEC_NAME = 'patch.yml'
CHUNK_SIZE = 2 << 15
TS_FORMAT = '%Y-%m-%d %H:%M:%S.%f +00:00'
LOG_SEPARATOR = '- ' * 80
INTER_PROCESS_SYNC_SECS = 0.1
INTER_PROCESS_SYNC_ATTEMPTS = 10


def hash_file(path: pathlib.Path, hasher: Callable[..., Any] | None = None) -> str:
    """Return the SHA512 hex digest of the data from file."""
    if hasher is None:
        hasher = hashlib.sha512
    the_hash = hasher()
    with open(path, 'rb') as handle:
        while chunk := handle.read(CHUNK_SIZE):
            the_hash.update(chunk)
    return the_hash.hexdigest()


@no_type_check
def log_subprocess_output(pipe, prefix: str):
    for line in iter(pipe.readline, b''):  # b'\n'-separated lines
        cand = line.decode(encoding=ENCODING).rstrip()
        if cand.strip().strip('[])yex'):
            if any(
                [
                    'microtype' in cand,
                    'xassoccnt' in cand,
                    'texlive/2022/texmf-dist/tex/' in cand,
                    cand == 'erns.sty)',
                    cand == '(see the transcript file for additional information)',
                    cand.startswith(r'Overfull \hbox ')
                    and cand.endswith(r'pt too wide) has occurred while \output is active'),
                ]
            ):
                log.debug(f'{prefix}: %s', cand)
            else:
                log.info(f'{prefix}: %s', cand)


@no_type_check
def vcs_probe():
    """Are we in front, on par, or behind with the upstream?"""
    try:
        repo = api.Repo('.', search_parent_directories=True)
        status = api.Status(repo)
        api.local_commits(repo, status)
        api.local_staged(repo, status)
        api.local_files(repo, status)
        try:
            repo_root_folder = repo.git.rev_parse(show_toplevel=True)
            yield f'Root     ({repo_root_folder})'
        except Exception:
            yield 'WARNING - ignored exception when assessing repo root folder location'
        for line in generate_report(status):
            yield line.rstrip()
    except Exception:
        yield 'WARNING - we seem to not be within a git repository clone'


def report_taxonomy(target_path: pathlib.Path) -> None:
    """Convenience function to report date, size, and checksums of the deliverable."""
    taxonomy = Taxonomy(target_path, excludes='', key_function='md5')
    for path in sorted(target_path.parent.rglob('*')):
        taxonomy.add_branch(path) if path.is_dir() else taxonomy.add_leaf(path)
    log.info('- Writing render/pdf folder taxonomy to inventory.json ...')
    taxonomy.dump(sink='inventory', format_type='json', base64_encode=False)

    stat = target_path.stat()
    size_bytes = stat.st_size
    mod_time = dti.datetime.fromtimestamp(stat.st_ctime, tz=dti.timezone.utc).strftime(TS_FORMAT)
    sha612_hash = hash_file(target_path, hashlib.sha512)
    sha256_hash = hash_file(target_path, hashlib.sha256)
    sha1_hash = hash_file(target_path, hashlib.sha1)
    md5_hash = hash_file(target_path, hashlib.md5)
    log.info('- Ephemeral:')
    log.info(f'  + name: {target_path.name}')
    log.info(f'  + size: {size_bytes} bytes')
    log.info(f'  + date: {mod_time}')
    log.info('- Characteristic:')
    log.info('  + Checksums:')
    log.info(f'    sha512:{sha612_hash}')
    log.info(f'    sha256:{sha256_hash}')
    log.info(f'      sha1:{sha1_hash}')
    log.info(f'       md5:{md5_hash}')
    log.info('  + Fonts:')


@no_type_check
def unified_diff(left: list[str], right: list[str], left_label: str = 'before', right_label: str = 'after'):
    """Derive the unified diff between left and right lists of strings as generator of strings."""
    for line in difflib.unified_diff(left, right, fromfile=left_label, tofile=right_label):
        yield line.rstrip()


@no_type_check
def log_unified_diff(left: list[str], right: list[str], left_label: str = 'before', right_label: str = 'after'):
    """Do the log bridging of the diff."""
    log.info(LOG_SEPARATOR)
    for line in unified_diff(left, right, left_label, right_label):
        for fine in line.split('\n'):
            log.info(fine)
    log.info(LOG_SEPARATOR)


@no_type_check
def ensure_separate_log_lines(sourcer: Callable, *args: list[object] | None):
    """Wrapping idiom breaking up any strings containing newlines."""
    log.info(LOG_SEPARATOR)
    for line in sourcer(*args) if args else sourcer():
        for fine in line.split('\n'):
            log.info(fine)
    log.info(LOG_SEPARATOR)


@no_type_check
def delegate(command: list[str], marker: str, do_shell: bool = False) -> int:
    """Execute command in subprocess and follow requests."""
    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=do_shell  # nosec B602
        )
        with process.stdout:
            log_subprocess_output(process.stdout, marker)
        code = process.wait()
        if code < 0:
            log.error(f'{marker} process ({command}) was terminated by signal {-code}')
        elif code > 0:
            log.error(f'{marker} process ({command}) returned {code}')
        else:
            log.info(f'{marker} process succeeded')
    except Exception as err:
        log.error(f'failed executing tool with error: {err}')
        code = 42

    return code


@no_type_check
def report(on: ToolKey) -> int:
    """Execute the tool specific version command."""
    tool_context = TOOL_VERSION_COMMAND_MAP.get(on, {})
    tool_version_call_text = str(tool_context.get('command', '')).strip()
    tool_version_call = tool_version_call_text.split()
    tool_reason_banner = str(tool_context.get('banner', 'No reason for the tool known')).strip()
    if not tool_version_call:
        log.warning(f'cowardly avoiding undefined call for tool key ({on})')
        log.info(f'- known tool keys are: ({", ".join(sorted(TOOL_VERSION_COMMAND_MAP))})')
        return 42

    log.info(LOG_SEPARATOR)
    log.info(f'requesting tool version information from environment per ({tool_version_call})')
    log.info(f'- {tool_reason_banner}')
    code = delegate(tool_version_call, f'tool-version-of-{on}')
    log.info(LOG_SEPARATOR)

    return code


@no_type_check
def execute_filter(
    the_filter: Callable,
    head: str,
    backup: str,
    label: str,
    text_lines: list[str],
    lookup: dict[str, str] | None = None,
) -> list[str]:
    """Chain filter calls by storing in and out lies in files and return the resulting lines."""
    log.info(LOG_SEPARATOR)
    log.info(head)
    doc_before_caps_patch = backup
    with open(doc_before_caps_patch, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(text_lines))
    patched_lines = the_filter(text_lines, lookup=lookup)
    with open(LATEX_PAYLOAD_NAME, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(patched_lines))
    log.info(f'diff of the ({label}) filter result:')
    log_unified_diff(text_lines, patched_lines)

    return patched_lines
