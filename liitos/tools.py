import datetime as dti
import difflib
import hashlib
import json
import os
import pathlib
import platform
import re
import subprocess  # nosec B404
import uuid
from typing import Any, Callable, Generator, Union, no_type_check

import yaml

import foran.foran as api  # type: ignore
from foran.report import generate_report  # type: ignore
from taksonomia.taksonomia import Taxonomy  # type: ignore

from liitos import (
    CONTEXT,
    ENCODING,
    KEYS_REQUIRED,
    LATEX_PAYLOAD_NAME,
    TOOL_VERSION_COMMAND_MAP,
    ToolKey,
    log,
)

PathLike = Union[str, pathlib.Path]

SPACE = ' '

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

IS_BORING = re.compile(r'\(.*texmf-dist/tex.*\.')
HAS_WARNING = re.compile(r'[Ww]arning')
HAS_ERROR = re.compile(r'[Ee]rror')


def hash_file(path: PathLike, hasher: Union[Callable[..., Any], None] = None) -> str:
    """Return the SHA512 hex digest of the data from file.

    Examples:

    >>> import pathlib, tempfile
    >>> empty_sha512 = (
    ...     'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce'
    ...     '47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e'
    ... )
    >>> with tempfile.NamedTemporaryFile() as handle:
    ...     empty_hash = hash_file(handle.name)
    >>> assert empty_hash == empty_sha512
    """
    if hasher is None:
        hasher = hashlib.sha512
    the_hash = hasher()
    with open(path, 'rb') as handle:
        while chunk := handle.read(CHUNK_SIZE):
            the_hash.update(chunk)
    return the_hash.hexdigest()


@no_type_check
def vcs_probe():
    """Are we in front, on par, or behind with the upstream?"""
    CONTEXT['source_hash'] = 'info:plain:built-outside-of-version-control'
    CONTEXT['source_hint'] = 'info:plain:built-outside-of-version-control'
    try:
        repo = api.Repo('.', search_parent_directories=True)
        status = api.Status(repo)
        CONTEXT['source_hash'] = f'sha1:{status.commit}'

        try:
            repo_root_folder = repo.git.rev_parse(show_toplevel=True)
            path = pathlib.Path(repo_root_folder)
            anchor = path.parent.name
            here = path.name
            CONTEXT['source_hint'] = f'{anchor}/{here}'
            yield f'Root     ({repo_root_folder})'
        except Exception:  # noqa
            yield 'WARNING - ignored exception when assessing repo root folder location'
        for line in generate_report(status):
            yield line.rstrip()

    except Exception as err:  # noqa
        yield f'WARNING - we seem to not be within a git repository clone ({err})'


def node_id() -> str:
    """Generate the build node identifier.

    Examples:

    >>> nid = node_id()
    >>> assert len(nid) == 36
    >>> assert all(c == '-' for c in (nid[8], nid[13], nid[18], nid[23]))
    """
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, platform.node()))


def report_taxonomy(target_path: pathlib.Path) -> None:
    """Convenience function to report date, size, and checksums of the deliverable."""
    taxonomy = Taxonomy(target_path, excludes='', key_function='md5')
    for path in sorted(target_path.parent.rglob('*')):
        taxonomy.add_branch(path) if path.is_dir() else taxonomy.add_leaf(path)
    log.warning('- Writing render/pdf folder taxonomy to inventory.json ...')
    taxonomy.dump(sink='inventory', format_type='json', base64_encode=False)

    stat = target_path.stat()
    size_bytes = stat.st_size
    mod_time = dti.datetime.fromtimestamp(stat.st_ctime, tz=dti.timezone.utc).strftime(TS_FORMAT)
    sha612_hash = hash_file(target_path, hashlib.sha512)
    sha256_hash = hash_file(target_path, hashlib.sha256)
    sha1_hash = hash_file(target_path, hashlib.sha1)
    md5_hash = hash_file(target_path, hashlib.md5)
    log.warning('- Ephemeral:')
    log.warning(f'  + name: {target_path.name}')
    log.warning(f'  + size: {size_bytes} bytes')
    log.warning(f'  + date: {mod_time}')
    log.warning('- Characteristic:')
    log.warning('  + Checksums:')
    log.warning(f'    sha512:{sha612_hash}')
    log.warning(f'    sha256:{sha256_hash}')
    log.warning(f'      sha1:{sha1_hash}')
    log.warning(f'       md5:{md5_hash}')
    log.warning('  + Fonts:')


@no_type_check
def unified_diff(left: list[str], right: list[str], left_label: str = 'before', right_label: str = 'after'):
    """Derive the unified diff between left and right lists of strings as generator of strings.

    Examples:

    >>> lines = list(unified_diff(['a', 'b'], ['aa', 'b', 'd'], '-', '+'))
    >>> lines
    ['--- -', '+++ +', '@@ -1,2 +1,3 @@', '-a', '+aa', ' b', '+d']
    """
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
def ensure_separate_log_lines(sourcer: Callable, trampoline: Callable = log.info, *args: Union[list[object], None]):
    """Wrapping idiom breaking up any strings containing newlines."""
    trampoline(LOG_SEPARATOR)
    for line in sourcer(*args) if args else sourcer():
        for fine in line.split('\n'):
            trampoline(fine)
    trampoline(LOG_SEPARATOR)


@no_type_check
def log_subprocess_output(pipe, prefix: str) -> list[str]:
    log_buffer = []
    for line in iter(pipe.readline, b''):  # b'\n'-separated lines
        cand = line.decode(encoding=ENCODING).rstrip()
        msg = prefix + ': ' + cand
        log_buffer.append(msg)
        if HAS_ERROR.search(cand):
            log.error(msg)
            continue
        if HAS_WARNING.search(cand) and not (
            'latex' in prefix
            and any(
                (
                    '"calc" is loaded -- this is not' in cand,
                    'Package microtype Warning: Unable to apply patch' in cand,
                    'Unknown document division name (startatroot)' in cand,
                    'Unknown slot number of character' in cand,
                )
            )
        ):
            log.warning(msg)
            continue
        if IS_BORING.search(cand):
            log.debug(msg)
            continue
        log.info(msg)

    return log_buffer


@no_type_check
def delegate(command: list[str], marker: str, do_shell: bool = False, is_quiet: bool = False) -> int:
    """Execute command in subprocess and follow requests.

    Hints on LaTeX noise reduction per special variables:

    - max_print_line=1000
    - error_line=254
    - half_error_line=238

    So, in texmf.copf or in shell process, these reduce the amount of lines ...

    max_print_line=1000 error_line=254 half_error_line=238
    """
    try:
        if 'latex' in marker:
            env = dict(os.environ)
            env['max_print_line'] = '1000'
            env['error_line'] = '254'
            env['half_error_line'] = '238'
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=do_shell, env=env  # nosec B602
            )
        else:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=do_shell  # nosec B602
            )
        with process.stdout:
            log_buffer = log_subprocess_output(process.stdout, marker)
        code = process.wait()
        if code < 0:
            log.error(f'{marker} process ({command}) was terminated by signal {-code}; (cf. below for hints)')
        elif code > 0:
            log.error(f'{marker} process ({command}) returned {code}; (cf. below for hints)')
        else:
            log.info(f'{marker} process succeeded')
    except Exception as err:
        log.error(f'failed executing tool with error: {err}; (cf. below for hints)')
        code = 42

    if code != 0 and is_quiet:
        for msg in log_buffer:
            if 'latex' in marker:
                payload = msg.replace(f'{marker}:', '').strip()
                if not payload:
                    continue
                if '(microtype)' in payload:
                    continue
                if 'Package microtype Warning: Unknown slot number of character' in payload:
                    continue
                if IS_BORING.search(payload):
                    continue
                if any(
                    (
                        '"calc" is loaded -- this is not' in payload,
                        'Package microtype Warning: Unable to apply patch' in payload,
                        'Unknown document division name (startatroot)' in payload,
                        'Unknown slot number of character' in payload,
                    )
                ):
                    continue
                cleansed = payload.replace('[', '').replace(']', '').replace('|', '')
                if not cleansed.strip():
                    continue
                if not payload.replace(')', ''):
                    continue
            log.error(msg)

    if code == 0 and is_quiet and marker in ('label-pdf', '', 'assess-pdf-fonts'):
        for msg in log_buffer:
            log.warning(msg)

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
    lookup: Union[dict[str, str], None] = None,
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


@no_type_check
def load_target(
    target_code: str, facet_code: str, structure_path: PathLike = STRUCTURE_PATH
) -> tuple[bool, dict[str, str]]:
    """DRY."""
    if not structure_path.is_file() or not structure_path.stat().st_size:
        log.error(f'render failed to find non-empty structure file at {structure_path}')
        return False, {}

    with open(structure_path, 'rt', encoding=ENCODING) as handle:
        structure = yaml.safe_load(handle)

    targets = sorted(structure.keys())

    if not targets:
        log.error(f'structure at ({structure_path}) does not provide any targets')
        return False, {}

    if target_code not in targets:
        log.error(f'structure does not provide ({target_code})')
        return False, {}

    if len(targets) != 1:
        log.warning(f'unexpected count of targets ({len(targets)}) from ({targets})')
        return True, {}

    target = targets[0]
    facets = sorted(list(facet.keys())[0] for facet in structure[target])
    log.info(f'found single target ({target}) with facets ({facets})')

    if facet_code not in facets:
        log.error(f'structure does not provide facet ({facet_code}) for target ({target_code})')
        return False, {}

    aspect_map = {}
    for data in structure[target]:
        if facet_code in data:
            aspect_map = data[facet_code]
            break
    missing_keys = [key for key in KEYS_REQUIRED if key not in aspect_map]
    if missing_keys:
        log.error(
            f'structure does not provide all expected aspects {sorted(KEYS_REQUIRED)}'
            f' for target ({target_code}) and facet ({facet_code})'
        )
        log.error(f'- the found aspects: {sorted(aspect_map.keys())}')
        log.error(f'- missing aspects:   {sorted(missing_keys)}')
        return False, {}

    if sorted(aspect_map.keys()) != sorted(KEYS_REQUIRED):
        log.debug(
            f'structure does not strictly provide the expected aspects {sorted(KEYS_REQUIRED)}'
            f' for target ({target_code}) and facet ({facet_code})'
        )
        log.debug(f'- found the following aspects instead:                   {sorted(aspect_map.keys())} instead')

    return True, aspect_map


def incoherent_math_mode_in_caption(caption: str, phase_info: str = '') -> list[str]:
    """Heuristics to warn on underscores and carets oustide of math mode in captions."""
    findings: list[str] = []
    if phase_info and not phase_info[0] == SPACE:
        phase_info = SPACE + phase_info
    if caption and '_' in caption and not ('$' in caption and not caption.count('$') % 2):
        findings.append(f'Underscore (_) and no LaTeX math mode tokens in caption ({caption}){phase_info}')
    if caption and '^' in caption and not ('$' in caption and not caption.count('$') % 2):
        findings.append(f'Caret (^) and no LaTeX math mode tokens in caption ({caption}){phase_info}')
    return findings


@no_type_check
def mermaid_captions_from_json_ast(json_ast_path: Union[str, pathlib.Path]) -> dict[str, str]:
    """Separation of concerns."""
    doc = json.load(open(json_ast_path, 'rt', encoding=ENCODING))
    blocks = doc['blocks']
    mermaid_caption_map = {}
    for b in blocks:
        if b['t'] == 'CodeBlock' and b['c'][0]:
            try:
                is_mermaid = b['c'][0][1][0] == 'mermaid'
                atts = b['c'][0][2]
            except IndexError:
                continue

            if not is_mermaid:
                continue
            m_caption, m_filename, m_format, m_loc = '', '', '', ''
            for k, v in atts:
                if k == 'caption':
                    m_caption = v
                elif k == 'filename':
                    m_filename = v
                elif k == 'format':
                    m_format = v
                elif k == 'loc':
                    m_loc = v
                else:
                    pass
            token = f'{m_loc}/{m_filename}.{m_format}'  # noqa
            if token in mermaid_caption_map:
                log.warning('Duplicate token, same caption?')
                log.warning(f'-   prior: {token} -> {m_caption}')
                log.warning(f'- current: {token} -> {mermaid_caption_map[token]}')
            for msg in incoherent_math_mode_in_caption(m_caption, phase_info=f'for mermaid image ({token})'):
                log.warning(msg)
            mermaid_caption_map[token] = m_caption
    return mermaid_caption_map


def remove_target_region_gen(text_lines: list[str], from_cut: str, thru_cut: str) -> Generator[str, None, None]:
    """Return generator that yields only the lines beyond the cut mark region skipping lines in [from, thru].

    Examples:

    >>> lines = ['a', 'b', 'c', 'd']
    >>> filtered = list(remove_target_region_gen(lines, 'b', 'c'))
    >>> filtered
    ['a', 'd']
    """
    in_section = False
    for line in text_lines:
        if not in_section:
            if from_cut in line:
                in_section = True
                continue
        if in_section:
            if thru_cut in line:
                in_section = False
            continue
        yield line
