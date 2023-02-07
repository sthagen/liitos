"""Command line interface for splice (Finnish liitos) contributions."""
import datetime as dti
import logging
import os
import pathlib
import sys

import typer

import liitos.approvals as sig
import liitos.changes as chg
import liitos.concat as cat
import liitos.eject as eje
import liitos.gather as gat
import liitos.meta as met
import liitos.render as ren
import liitos.tools as too
from liitos import (
    APP_NAME,
    APP_VERSION,
    FILTER_CS_LIST,
    FROM_FORMAT_SPEC,
    LOG_SEPARATOR,
    QUIET,
    TOOL_VERSION_COMMAND_MAP,
    TS_FORMAT_PAYLOADS,
    log,
)

app = typer.Typer(
    add_completion=False,
    context_settings={'help_option_names': ['-h', '--help']},
    no_args_is_help=True,
)

DocumentRoot = typer.Option(
    '',
    '-d',
    '--document-root',
    help='Root of the document tree to visit. Optional\n(default: positional tree root value)',
)
StructureName = typer.Option(
    gat.DEFAULT_STRUCTURE_NAME,
    '-s',
    '--structure',
    help='structure mapping file (default: {gat.DEFAULT_STRUCTURE_NAME})',
)
TargetName = typer.Option(
    '',
    '-t',
    '--target',
    help='target document key',
)
FacetName = typer.Option(
    '',
    '-f',
    '--facet',
    help='facet key of target document',
)
FromFormatSpec = typer.Option(
    FROM_FORMAT_SPEC,
    '-s',
    '--from-format-spec',
    help='from format specification handed over to pandoc',
)
FilterCSList = typer.Option(
    FILTER_CS_LIST,
    '-F',
    '--filters',
    help='comma separated list of filters handed over to pandoc (in order)',
)
Verbosity = typer.Option(
    False,
    '-v',
    '--verbose',
    help='Verbose output (default is False)',
)
Strictness = typer.Option(
    False,
    '-s',
    '--strict',
    help='Ouput noisy warnings on console (default is False)',
)
OutputPath = typer.Option(
    '',
    '-o',
    '--output-path',
    help='Path to output unambiguous content to - like when ejecting a template',
)
LabelCall = typer.Option(
    '',
    '-l',
    '--label',
    help='optional label call to execute',
)
PatchTables = typer.Option(
    False,
    '-p',
    '--patch-tables',
    help='Patch tables EXPERIMENTAL (default is False)',
)


@app.callback(invoke_without_command=True)
def callback(
    version: bool = typer.Option(
        False,
        '-V',
        '--version',
        help='Display the application version and exit',
        is_eager=True,
    )
) -> None:
    """
    Splice (Finnish liitos) contributions.
    """
    if version:
        typer.echo(f'{APP_NAME} version {APP_VERSION}')
        raise typer.Exit()


def _verify_call_vector(
    doc_root: str,
    doc_root_pos: str,
    verbose: bool,
    strict: bool,
    label: str = '',
    patch_tables: bool = False,
    from_format_spec: str = '',
    filter_cs_list: str = '',
) -> tuple[int, str, str, dict[str, bool | str]]:
    """DRY"""
    doc = doc_root.strip()
    if not doc and doc_root_pos:
        doc = doc_root_pos
    if not doc:
        print('Document tree root required', file=sys.stderr)
        return 2, 'Document tree root required', '', {}

    doc_root_path = pathlib.Path(doc)
    if doc_root_path.exists():
        if not doc_root_path.is_dir():
            print(f'requested tree root at ({doc}) is not a folder', file=sys.stderr)
            return 2, f'requested tree root at ({doc}) is not a folder', '', {}
    else:
        print(f'requested tree root at ({doc}) does not exist', file=sys.stderr)
        return 2, f'requested tree root at ({doc}) does not exist', '', {}

    options: dict[str, bool | str] = {
        'quiet': QUIET and not verbose and not strict,
        'strict': strict,
        'verbose': verbose,
        'label': label,
        'patch_tables': patch_tables,
        'from_format_spec': from_format_spec if from_format_spec else FROM_FORMAT_SPEC,
        'filter_cs_list': filter_cs_list if filter_cs_list else FILTER_CS_LIST,
    }
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    return 0, '', doc, options


@app.command('verify')
def verify(  # noqa
    doc_root_pos: str = typer.Argument(''),
    doc_root: str = DocumentRoot,
    structure: str = StructureName,
    target: str = TargetName,
    facet: str = FacetName,
    verbose: bool = Verbosity,
    strict: bool = Strictness,
) -> int:
    """
    Verify the structure definition against the file system.
    """
    code, message, doc, options = _verify_call_vector(doc_root, doc_root_pos, verbose, strict)
    if code:
        log.error(message)
        return code

    return sys.exit(
        gat.verify(doc_root=doc, structure_name=structure, target_key=target, facet_key=facet, options=options)
    )


@app.command('approvals')
def approvals(  # noqa
    doc_root_pos: str = typer.Argument(''),
    doc_root: str = DocumentRoot,
    structure: str = StructureName,
    target: str = TargetName,
    facet: str = FacetName,
    verbose: bool = Verbosity,
    strict: bool = Strictness,
) -> int:
    """
    Weave in the approvals for facet of target within document root.
    """
    code, message, doc, options = _verify_call_vector(doc_root, doc_root_pos, verbose, strict)
    if code:
        log.error(message)
        return 2

    return sys.exit(
        sig.weave(doc_root=doc, structure_name=structure, target_key=target, facet_key=facet, options=options)
    )


@app.command('changes')
def changes(  # noqa
    doc_root_pos: str = typer.Argument(''),
    doc_root: str = DocumentRoot,
    structure: str = StructureName,
    target: str = TargetName,
    facet: str = FacetName,
    verbose: bool = Verbosity,
    strict: bool = Strictness,
) -> int:
    """
    Weave in the changes for facet of target within document root.
    """
    code, message, doc, options = _verify_call_vector(doc_root, doc_root_pos, verbose, strict)
    if code:
        log.error(message)
        return 2

    return sys.exit(
        chg.weave(doc_root=doc, structure_name=structure, target_key=target, facet_key=facet, options=options)
    )


@app.command('concat')
def concat(  # noqa
    doc_root_pos: str = typer.Argument(''),
    doc_root: str = DocumentRoot,
    structure: str = StructureName,
    target: str = TargetName,
    facet: str = FacetName,
    verbose: bool = Verbosity,
    strict: bool = Strictness,
) -> int:
    """
    Concatenate the markdown tree for facet of target within render/pdf below document root.
    """
    code, message, doc, options = _verify_call_vector(doc_root, doc_root_pos, verbose, strict)
    if code:
        log.error(message)
        return 2

    return sys.exit(
        cat.concatenate(doc_root=doc, structure_name=structure, target_key=target, facet_key=facet, options=options)
    )


@app.command('render')
def render(  # noqa
    doc_root_pos: str = typer.Argument(''),
    doc_root: str = DocumentRoot,
    structure: str = StructureName,
    target: str = TargetName,
    facet: str = FacetName,
    label: str = LabelCall,
    verbose: bool = Verbosity,
    strict: bool = Strictness,
    patch_tables: bool = PatchTables,
    from_format_spec: str = FromFormatSpec,
    filter_cs_list: str = FilterCSList,
) -> int:
    """
    Render the markdown tree for facet of target within render/pdf below document root.
    """
    code, message, doc, options = _verify_call_vector(
        doc_root,
        doc_root_pos,
        verbose,
        strict,
        label=label,
        patch_tables=patch_tables,
        from_format_spec=from_format_spec,
        filter_cs_list=filter_cs_list,
    )
    if code:
        log.error(message)
        return sys.exit(code)

    start_time = dti.datetime.now(tz=dti.timezone.utc)
    start_ts = start_time.strftime(TS_FORMAT_PAYLOADS)
    log.info(f'Start timestamp ({start_ts})')
    code = cat.concatenate(doc_root=doc, structure_name=structure, target_key=target, facet_key=facet, options=options)
    if code:
        return sys.exit(code)

    idem = os.getcwd()
    doc = '../../'
    log.info(f'before met.weave(): {os.getcwd()} set doc ({doc})')
    code = met.weave(doc_root=doc, structure_name=structure, target_key=target, facet_key=facet, options=options)
    if code:
        return sys.exit(code)

    log.info(f'before sig.weave(): {os.getcwd()} set doc ({doc})')
    os.chdir(idem)
    log.info(f'relocated for sig.weave(): {os.getcwd()} with doc ({doc})')
    code = sig.weave(doc_root=doc, structure_name=structure, target_key=target, facet_key=facet, options=options)
    if code:
        return sys.exit(code)

    log.info(f'before chg.weave(): {os.getcwd()} set doc ({doc})')
    os.chdir(idem)
    log.info(f'relocated for chg.weave(): {os.getcwd()} with doc ({doc})')
    code = chg.weave(doc_root=doc, structure_name=structure, target_key=target, facet_key=facet, options=options)
    if code:
        return sys.exit(code)

    log.info(f'before chg.weave(): {os.getcwd()} set doc ({doc})')
    os.chdir(idem)
    log.info(f'relocated for chg.weave(): {os.getcwd()} with doc ({doc})')
    code = ren.der(doc_root=doc, structure_name=structure, target_key=target, facet_key=facet, options=options)

    end_time = dti.datetime.now(tz=dti.timezone.utc)
    end_ts = end_time.strftime(TS_FORMAT_PAYLOADS)
    duration_secs = (end_time - start_time).total_seconds()
    log.info(f'End timestamp ({end_ts})')
    acted = 'Rendered'
    if code == 0xFADECAFE:
        acted = 'Did not render'
        code = 0  # HACK A DID ACK
    log.info(f'{acted} {target} document for {facet} at {doc} in {duration_secs} secs')
    return sys.exit(code)


@app.command('report')
def report() -> int:
    """
    Report on the environment.
    """
    log.info(LOG_SEPARATOR)
    log.info('inspecting environment (tool version information):')
    for tool_key in TOOL_VERSION_COMMAND_MAP:
        too.report(tool_key)
    log.info(LOG_SEPARATOR)

    return sys.exit(0)


@app.command('eject')
def eject(  # noqa
    that: str = typer.Argument(''),
    out: str = OutputPath,
) -> int:
    """
    Eject a template. Enter unique part to retrieve, any unknown word to obtain the list of known templates.
    """
    return sys.exit(eje.this(thing=that, out=out))


@app.command('version')
def app_version() -> None:
    """
    Display the application version and exit.
    """
    callback(True)
