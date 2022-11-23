"""Command line interface for splice (Finnish liitos) contributions."""
import argparse
import pathlib
import sys
from typing import List, Union

import typer

import liitos.approvals as sig
import liitos.captions as cap
import liitos.changes as chg
import liitos.figures as fig
import liitos.gather as gat
import liitos.labels as lab
import liitos.meta as met
import liitos.patch as pat
import liitos.tables as tab
from liitos import APP_ALIAS, APP_NAME, DEBUG, QUIET, VERBOSE, __version__ as APP_VERSION

app = typer.Typer(
    add_completion=False,
    context_settings={'help_option_names': ['-h', '--help']},
    no_args_is_help=True,
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


@app.command('verify')
def verify(  # noqa
    doc_root_pos: str = typer.Argument(''),
    doc_root: str = typer.Option(
        '',
        '-d',
        '--document-root',
        help='Root of the document tree to visit. Optional\n(default: positional tree root value)',
    ),
    structure: str = typer.Option(
        gat.DEFAULT_STRUCTURE_NAME,
        '-s',
        '--structure',
        help='structure mapping file (default: {gat.DEFAULT_STRUCTURE_NAME})',
    ),
    target: str = typer.Option(
        '',
        '-t',
        '--target',
        help='target document key',
    ),
    facet: str = typer.Option(
        '',
        '-f',
        '--facet',
        help='facet key of target document',
    ),
    verbose: bool = typer.Option(
        False,
        '-v',
        '--verbose',
        help='Verbose output (default is False)',
    ),
    strict: bool = typer.Option(
        False,
        '-s',
        '--strict',
        help='Ouput noisy warnings on console (default is False)',
    ),
) -> int:
    """
    Verify the structure definition against the file system.
    """
    doc = doc_root.strip()
    if not doc and doc_root_pos:
        doc = doc_root_pos
    if not doc:
        print('Document tree root required', file=sys.stderr)
        return sys.exit(2)

    doc_root_path = pathlib.Path(doc)
    if doc_root_path.exists():
        if not doc_root_path.is_dir():
            print(f'requested tree root at ({doc}) is not a folder', file=sys.stderr)
            return sys.exit(2)
    else:
        print(f'requested tree root at ({doc}) does not exist', file=sys.stderr)
        return sys.exit(2)

    options = {
        'quiet': QUIET and not verbose and not strict,
        'strict': strict,
        'verbose': verbose,
    }

    return sys.exit(
        gat.verify(doc_root=doc, structure_name=structure, target_key=target, facet_key=facet, options=options)
    )


@app.command('approvals')
def approvals(  # noqa
    doc_root_pos: str = typer.Argument(''),
    doc_root: str = typer.Option(
        '',
        '-d',
        '--document-root',
        help='Root of the document tree to visit. Optional\n(default: positional tree root value)',
    ),
    structure: str = typer.Option(
        gat.DEFAULT_STRUCTURE_NAME,
        '-s',
        '--structure',
        help='structure mapping file (default: {gat.DEFAULT_STRUCTURE_NAME})',
    ),
    target: str = typer.Option(
        '',
        '-t',
        '--target',
        help='target document key',
    ),
    facet: str = typer.Option(
        '',
        '-f',
        '--facet',
        help='facet key of target document',
    ),
    verbose: bool = typer.Option(
        False,
        '-v',
        '--verbose',
        help='Verbose output (default is False)',
    ),
    strict: bool = typer.Option(
        False,
        '-s',
        '--strict',
        help='Ouput noisy warnings on console (default is False)',
    ),
) -> int:
    """
    Weave in the approvals for facet of target within document root.
    """
    doc = doc_root.strip()
    if not doc and doc_root_pos:
        doc = doc_root_pos
    if not doc:
        print('Document tree root required', file=sys.stderr)
        return sys.exit(2)

    doc_root_path = pathlib.Path(doc)
    if doc_root_path.exists():
        if not doc_root_path.is_dir():
            print(f'requested tree root at ({doc}) is not a folder', file=sys.stderr)
            return sys.exit(2)
    else:
        print(f'requested tree root at ({doc}) does not exist', file=sys.stderr)
        return sys.exit(2)

    options = {
        'quiet': QUIET and not verbose and not strict,
        'strict': strict,
        'verbose': verbose,
    }

    return sys.exit(
        sig.weave(doc_root=doc, structure_name=structure, target_key=target, facet_key=facet, options=options)
    )


@app.command('version')
def app_version() -> None:
    """
    Display the application version and exit.
    """
    callback(True)
