"""Given a target and facet, concatenate a tree of markdown files to a single file rewriting all image refs."""
import json
import os
import pathlib
import re
import shutil
import sys
from io import StringIO
from typing import no_type_check

import treelib  # type: ignore
import yaml

import liitos.gather as gat
from liitos import ENCODING, log

ALT_INJECTOR_HACK = 'INJECTED-ALT-TEXT-TO-TRIGGER-FIGURE-ENVIRONMENT-AROUND-IMAGE-IN-PANDOC'
CAP_INJECTOR_HACK = 'INJECTED-CAP-TEXT-TO-MARK-MISSING-CAPTION-IN-OUTPUT'
DOC_BASE = pathlib.Path('..', '..')
STRUCTURE_PATH = DOC_BASE / 'structure.yml'
SLASH = '/'
IMAGES_FOLDER = 'images/'
DIAGRAMS_FOLDER = 'diagrams/'

"""
```{.python .cb.run}
with open('sub/as.md') as fp:
    print(fp.read())
```
"""
READ_SLOT_FENCE_BEGIN = '```{.python .cb.run}'
READ_SLOT_CONTEXT_BEGIN = 'with open('
READ_SLOT_FENCE_END = '```'

r"""
\include{markdown_file_path}
"""
INCLUDE_SLOT = '\\include{'

"""
![Alt Text Red](images/red.png "Caption Text Red")
![Alt Text Dot Dot Lime](../images/lime.png "Caption Text Dot Dot Lime")
![Alt Text Blue](images/blue.png "Caption Text Blue")
![Alt Text Sting Red](other/images/red.png "Caption Text Sting Red")
"""
IMG_LINE_STARTSWITH = '!['
MD_IMG_PATTERN = re.compile(r"^!\[(?P<cap>[^(]*)\]\((?P<src>[^ ]+)\ *\"?(?P<alt>[^\"]*)\"?\)(?P<rest>.*)?$")
MD_IMG_PATTERN_RIGHT_SPLIT = re.compile(r"^(?P<src>[^ ]+)\ *\"?(?P<alt>[^\"]*)\"?\)(?P<rest>.*)?$")


@no_type_check
class RedirectedStdout:
    @no_type_check
    def __init__(self):
        self._stdout = None
        self._string_io = None

    @no_type_check
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._string_io = StringIO()
        return self

    @no_type_check
    def __exit__(self, type, value, traceback):
        sys.stdout = self._stdout

    @no_type_check
    def __str__(self):
        return self._string_io.getvalue()


@no_type_check
def process_approvals(aspects: str) -> gat.Approvals | int:
    """TODO."""
    approvals_path = DOC_BASE / aspects[gat.KEY_APPROVALS]
    if not approvals_path.is_file() or not approvals_path.stat().st_size:
        log.error(f'destructure failed to find non-empty approvals file at {approvals_path}')
        return 1
    if approvals_path.suffix.lower() not in ('.json', '.yaml', '.yml'):
        log.error(f'approvals file format per suffix ({approvals_path.suffix}) not supported')
        return 1
    approvals_channel = 'yaml' if approvals_path.suffix.lower() in ('.yaml', '.yml') else 'json'
    with open(approvals_path, 'rt', encoding=ENCODING) as handle:
        approvals = yaml.safe_load(handle) if approvals_channel == 'yaml' else json.load(handle)
    if not approvals:
        log.error(f'empty approvals file? Please add approvals to ({approvals_path})')
        return 1
    if approvals_channel == 'yaml':
        with open('approvals.yml', 'wt', encoding=ENCODING) as handle:
            yaml.dump(approvals, handle, default_flow_style=False)
    else:
        with open('approvals.json', 'wt', encoding=ENCODING) as handle:
            json.dump(approvals, handle, indent=2)
    return approvals


@no_type_check
def process_binder(aspects: str) -> gat.Binder | int:
    """TODO."""
    bind_path = DOC_BASE / aspects[gat.KEY_BIND]
    if not bind_path.is_file() or not bind_path.stat().st_size:
        log.error(f'destructure failed to find non-empty bind file at {bind_path}')
        return 1
    if bind_path.suffix.lower() not in ('.txt',):
        log.error(f'bind file format per suffix ({bind_path.suffix}) not supported')
        return 1
    with open(bind_path, 'rt', encoding=ENCODING) as handle:
        binder = [line.strip() for line in handle.readlines() if line.strip()]
    if not binder:
        log.error(f'empty bind file? Please add component paths to ({bind_path})')
        return 1
    with open('bind.txt', 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(binder) + '\n')
    return binder


@no_type_check
def process_changes(aspects: str) -> gat.Changes | int:
    """TODO."""
    changes_path = DOC_BASE / aspects[gat.KEY_CHANGES]
    if not changes_path.is_file() or not changes_path.stat().st_size:
        log.error(f'destructure failed to find non-empty changes file at {changes_path}')
        return 1
    if changes_path.suffix.lower() not in ('.json', '.yaml', '.yml'):
        log.error(f'changes file format per suffix ({changes_path.suffix}) not supported')
        return 1
    changes_channel = 'yaml' if changes_path.suffix.lower() in ('.yaml', '.yml') else 'json'
    with open(changes_path, 'rt', encoding=ENCODING) as handle:
        changes = yaml.safe_load(handle) if changes_channel == 'yaml' else json.load(handle)
    if not changes:
        log.error(f'empty changes file? Please add changes data to ({changes_path})')
        return 1
    if changes_channel == 'yaml':
        with open('changes.yml', 'wt', encoding=ENCODING) as handle:
            yaml.dump(changes, handle, default_flow_style=False)
    else:
        with open('changes.json', 'wt', encoding=ENCODING) as handle:
            json.dump(changes, handle, indent=2)
    return changes


@no_type_check
def process_meta(aspects: str) -> gat.Meta | int:
    """TODO."""
    meta_path = DOC_BASE / aspects[gat.KEY_META]
    if not meta_path.is_file() or not meta_path.stat().st_size:
        log.error(f'destructure failed to find non-empty meta file at {meta_path}')
        return 1
    if meta_path.suffix.lower() not in ('.yaml', '.yml'):
        log.error(f'meta file format per suffix ({meta_path.suffix}) not supported')
        return 1
    with open(meta_path, 'rt', encoding=ENCODING) as handle:
        metadata = yaml.safe_load(handle)
    if not metadata:
        log.error(f'empty metadata file? Please add metadata to ({meta_path})')
        return 1
    if 'import' in metadata['document']:
        base_meta_path = DOC_BASE / metadata['document']['import']
        if not base_meta_path.is_file() or not base_meta_path.stat().st_size:
            log.error(
                f'metadata declares import of base data from ({base_meta_path.name}) but failed to find non-empty base file at {base_meta_path}'
            )
            return 1
        with open(base_meta_path, 'rt', encoding=ENCODING) as handle:
            base_data = yaml.safe_load(handle)
        for key, value in metadata['document']['patch'].items():
            base_data['document']['common'][key] = value
        metadata = base_data
    with open('metadata.yml', 'wt', encoding=ENCODING) as handle:
        yaml.dump(metadata, handle, default_flow_style=False)
    return metadata


@no_type_check
def parse_markdown_image(text_line: str) -> tuple[str, str, str, str]:
    """Parse a markdown image line within our conventions into caption, src, alt, and optional rest."""
    invalid_marker = ('', '', '', text_line)

    exclam = '!'
    osb = '['
    if not text_line or not text_line.startswith(f'{exclam}{osb}'):
        log.error(f'- INVALID-MD-IMG_LINE::START <<{text_line.rstrip()}>>')
        return invalid_marker

    csb = ']'
    osb_cnt = text_line.count(osb)
    csb_cnt = text_line.count(csb)
    if osb_cnt + csb_cnt < 2:
        log.error(f'- INVALID-MD-IMG_LINE::SB-TOK-CNT-LOW <<{text_line.rstrip()}>>')
        return invalid_marker
    if osb_cnt != csb_cnt:
        log.warning(f'- INCOMPLETE-MD-IMG_LINE::SB-TOK-CNT-UNBALANCED <<{text_line.rstrip()}>>')

    orb = '('
    cap_src_boundary = f'{csb}{orb}'
    if cap_src_boundary not in text_line:
        log.error(f'- INVALID-MD-IMG_LINE::CAP-SRC-BOUNDARY <<{text_line.rstrip()}>>')
        return invalid_marker

    crb = ')'
    orb_cnt = text_line.count(orb)
    crb_cnt = text_line.count(crb)
    if orb_cnt + crb_cnt < 2:
        log.error(f'- INVALID-MD-IMG_LINE::RB-TOK-CNT-LOW <<{text_line.rstrip()}>>')
        return invalid_marker
    if orb_cnt != crb_cnt:
        log.warning(f'- INCOMPLETE-MD-IMG_LINE::RB-TOK-CNT-UNBALANCED <<{text_line.rstrip()}>>')

    quo = '"'
    quo_cnt = text_line.count(quo)
    if quo_cnt < 2:
        log.warning(f'- INCOMPLETE-MD-IMG_LINE::QU-TOK-CNT-LOW <<{text_line.rstrip()}>>')
    if quo_cnt % 2:
        log.warning(f'- INCOMPLETE-MD-IMG_LINE::QU-TOK-CNT-UNBALANCED <<{text_line.rstrip()}>>')

    sp = ' '
    sp_cnt = text_line.count(sp)
    if not sp_cnt:
        log.warning(f'- INCOMPLETE-MD-IMG_LINE::SP-TOK-CNT-LOW <<{text_line.rstrip()}>>')

    dot = '.'
    sla = '/'
    abs_path_indicator = f'{csb}{orb}{sla}'
    may_have_abs_path = abs_path_indicator in text_line
    if may_have_abs_path:
        log.info(f'- SUSPICIOUS-MD-IMG_LINE::MAY-HAVE-ABS-PATH <<{text_line.rstrip()}>>')
    naive_upwards_path_indicator = f'{csb}{orb}{dot}{dot}{sla}'
    may_have_upwards_path = naive_upwards_path_indicator in text_line
    if may_have_upwards_path:
        log.info(f'- SUSPICIOUS-MD-IMG_LINE::MAY-HAVE-UPWARDS-PATH <<{text_line.rstrip()}>>')

    log.info('- parsing the markdown image text line ...')
    if orb_cnt + crb_cnt > 2 or orb_cnt != crb_cnt:
        # The regex is not safe for orb inside caption
        left, right = text_line.split(cap_src_boundary, 1)
        match_right = MD_IMG_PATTERN_RIGHT_SPLIT.match(right)
        if not match_right:
            log.error(f'- INVALID-MD-IMG_LINE::RE-MATCH-RIGHT-SPLIT-FAILED <<{text_line.rstrip()}>>')
            return invalid_marker

        parts = match_right.groupdict()
        cap = left[2:]
        if not cap:
            log.warning(f'- INCOMPLETE-MD-IMG_LINE::CAP-MISS-INJECTED <<{text_line.rstrip()}>>')
            cap = CAP_INJECTOR_HACK

        src = parts['src']
        alt = parts['alt']
        rest = parts['rest']
        if orb in alt or crb in alt:
            log.warning(f'- MAYBE-MD-IMG_LINE::ALT-TRUNCATED-PARTIAL-MATCH <<{text_line.rstrip()}>>')
            log.warning(f"  + parsed as ({cap=}, {src=}, {alt=}, {rest=}")

        return cap, src, alt, rest

    match = MD_IMG_PATTERN.match(text_line)
    if not match:
        log.error(f'- INVALID-MD-IMG_LINE::RE-MATCH-FAILED <<{text_line.rstrip()}>>')
        return invalid_marker

    parts = match.groupdict()
    cap = parts['cap']
    if not cap:
        log.warning(f'- INCOMPLETE-MD-IMG_LINE::CAP-MISS-INJECTED <<{text_line.rstrip()}>>')
        cap = CAP_INJECTOR_HACK

    src = parts['src']
    alt = parts['alt']
    rest = parts['rest']
    if orb in alt or crb in alt:
        log.warning(f'- MAYBE-MD-IMG_LINE::ALT-TRUNCATED-FULL-MATCH <<{text_line.rstrip()}>>')
        log.warning(f"  + parsed as ({cap=}, {src=}, {alt=}, {rest=}")

    return cap, src, alt, rest


@no_type_check
def adapt_image(text_line: str, collector: list[str], upstream: str, root: str) -> str:
    """YES."""
    cap, src, alt, rest = parse_markdown_image(text_line)
    if not src:
        log.error(f'parse of markdown image text line failed - empty src, and rest is <<{rest.rstrip()}>>')
        return text_line

    img_path = str((pathlib.Path(upstream).parent / src).resolve()).replace(root, '')
    collector.append(img_path)
    img_hack = img_path
    if f'/{IMAGES_FOLDER}' in img_path:
        img_hack = IMAGES_FOLDER + img_path.split(f'/{IMAGES_FOLDER}', 1)[1]
    elif f'/{DIAGRAMS_FOLDER}' in img_path:
        img_hack = DIAGRAMS_FOLDER + img_path.split(f'/{DIAGRAMS_FOLDER}', 1)[1]

    if img_hack != img_path:
        log.info(f'{img_hack} <--- OK? --- {img_path}')

    alt_text = f'"{alt}"' if alt else f'"{ALT_INJECTOR_HACK}"'
    belte_og_seler = f'![{cap}]({img_hack} {alt_text}){rest}'
    log.info(f'==> belte-og-seler: ->>{belte_og_seler}<<-')
    return belte_og_seler


@no_type_check
def harvest_include(
    text_line: str, slot: int, regions: dict[str, list[tuple[tuple[int, int], str]]], tree: treelib.Tree, parent: str
) -> None:
    """TODO."""
    include_local = text_line.split(INCLUDE_SLOT, 1)[1].rstrip('}').strip()
    include = str(pathlib.Path(parent).parent / include_local)
    regions[parent].append(((slot, slot), include))
    tree.create_node(include, include, parent=parent)


@no_type_check
def rollup(
    jobs: list[list[str]],
    docs: dict[str, list[str]],
    regions: dict[str, list[tuple[tuple[int, int], str]]],
    flat: dict[str, str],
) -> list[list[str]]:
    """TODO."""
    tackle = [those[0] for those in jobs if those and those[0] != SLASH]
    if tackle:
        log.info(f'  Insertion ongoing with parts ({", ".join(tuple(sorted(tackle)))}) remaining')
    else:
        return [[]]
    for that in tackle:
        buf = []
        for slot, line in enumerate(docs[that]):
            special = False
            the_first = False
            the_include = ''
            for pair, include in regions[that]:
                low, high = pair
                if low <= slot <= high:
                    special = True
                if low == slot:
                    the_first = True
                    the_include = include
            if not special:
                buf.append(line)
                continue
            if the_first:
                buf.append(flat[the_include])
        flat[that] = '\n'.join(buf) + '\n'

    return [[job for job in chain if job not in flat] for chain in jobs]


@no_type_check
def collect_assets(collector: list[str]) -> None:
    """TODO"""
    images = pathlib.Path(IMAGES_FOLDER)
    images.mkdir(parents=True, exist_ok=True)
    diagrams = pathlib.Path(DIAGRAMS_FOLDER)
    diagrams.mkdir(parents=True, exist_ok=True)
    for img_path in collector:
        if IMAGES_FOLDER in img_path:
            source_asset = DOC_BASE / img_path
            target_asset = images / pathlib.Path(img_path).name
            shutil.copy(source_asset, target_asset)
            continue
        if DIAGRAMS_FOLDER in img_path:
            source_asset = DOC_BASE / img_path
            target_asset = diagrams / pathlib.Path(img_path).name
            shutil.copy(source_asset, target_asset)


@no_type_check
def concatenate(
    doc_root: str | pathlib.Path, structure_name: str, target_key: str, facet_key: str, options: dict[str, bool]
) -> int:
    """Later alligator."""
    separator = '- ' * 80
    log.info(separator)
    target_code = target_key
    facet_code = facet_key
    if not facet_code.strip() or not target_code.strip():
        log.error(f'concatenate requires non-empty target ({target_code}) and facet ({facet_code}) codes')
        return 2

    log.info(f'parsed target ({target_code}) and facet ({facet_code}) from request')

    structure, asset_map = gat.prelude(
        doc_root=doc_root, structure_name=structure_name, target_key=target_key, facet_key=facet_key, command='concat'
    )
    log.info(f'prelude teleported processor into the document root at ({os.getcwd()}/)')
    rel_concat_folder_path = pathlib.Path("render/pdf/")
    rel_concat_folder_path.mkdir(parents=True, exist_ok=True)
    os.chdir(rel_concat_folder_path)
    log.info(f'concatenate (this processor) teleported into the render/pdf location ({os.getcwd()}/)')

    if not STRUCTURE_PATH.is_file() or not STRUCTURE_PATH.stat().st_size:
        log.error(f'concat failed to find non-empty structure file at {STRUCTURE_PATH}')
        return 1

    with open(STRUCTURE_PATH, 'rt', encoding=ENCODING) as handle:
        structure = yaml.safe_load(handle)

    targets = sorted(structure.keys())

    if not targets:
        log.error(f'structure at ({STRUCTURE_PATH}) does not provide any targets')
        return 1

    if target_code not in targets:
        log.error(f'structure does not provide ({target_code})')
        return 1

    if len(targets) == 1:
        target = targets[0]
        facets = sorted(list(facet.keys())[0] for facet in structure[target])
        log.info(f'found single target ({target}) with facets ({facets})')

        if facet_code not in facets:
            log.error(f'structure does not provide facet ({facet_code}) for target ({target_code})')
            return 1

        aspect_map = {}
        for data in structure[target]:
            if facet_code in data:
                aspect_map = data[facet_code]
                break
        missing_keys = [key for key in gat.KEYS_REQUIRED if key not in aspect_map]
        if missing_keys:
            log.error(
                f'structure does not provide all expected aspects {sorted(gat.KEYS_REQUIRED)}'
                f' for target ({target_code}) and facet ({facet_code})'
            )
            log.error(f'- the found aspects: {sorted(aspect_map.keys())}')
            log.error(f'- missing aspects:   {sorted(missing_keys)}')
            return 1
        if sorted(aspect_map.keys()) != sorted(gat.KEYS_REQUIRED):
            log.warning(
                f'structure does not strictly provide the expected aspects {sorted(gat.KEYS_REQUIRED)}'
                f' for target ({target_code}) and facet ({facet_code})'
            )
            log.warning(f'- found the following aspects instead:                   {sorted(aspect_map.keys())} instead')

        approvals = process_approvals(aspect_map)
        if isinstance(approvals, int):
            return 1
        binder = process_binder(aspect_map)
        if isinstance(binder, int):
            return 1
        changes = process_changes(aspect_map)
        if isinstance(changes, int):
            return 1
        metadata = process_meta(aspect_map)
        if isinstance(metadata, int):
            return 1

        root = SLASH
        root_path = str(pathlib.Path.cwd().resolve()).rstrip(SLASH) + SLASH
        tree = treelib.Tree()
        tree.create_node(root, root)
        documents = {}
        insert_regions = {}
        img_collector = []
        log.info(separator)
        log.info('processing binder ...')
        for entry in binder:
            path = DOC_BASE / entry
            log.debug(f'- {entry} as {path}')
            with open(path, 'rt', encoding=ENCODING) as handle:
                documents[entry] = [line.rstrip() for line in handle.readlines()]
            insert_regions[entry] = []
            in_region = False
            begin, end = 0, 0
            include = ''
            tree.create_node(entry, entry, parent=root)
            for slot, line in enumerate(documents[entry]):
                if line.startswith(IMG_LINE_STARTSWITH):
                    documents[entry][slot] = adapt_image(line, img_collector, entry, root_path)
                log.debug(f'{slot :02d}|{line.rstrip()}')
                if not in_region:
                    if line.startswith(READ_SLOT_FENCE_BEGIN):
                        in_region = True
                        begin = slot
                        continue
                    if line.startswith(INCLUDE_SLOT):
                        include = line.split(INCLUDE_SLOT, 1)[1].rstrip('}').strip()
                        insert_regions[entry].append(((slot, slot), include))
                        tree.create_node(include, include, parent=entry)
                        include = ''
                        continue
                if in_region:
                    if line.startswith(READ_SLOT_CONTEXT_BEGIN):
                        include = line.replace(READ_SLOT_CONTEXT_BEGIN, '').split(')', 1)[0].strip("'").strip('"')
                    elif line.startswith(READ_SLOT_FENCE_END):
                        end = slot
                        insert_regions[entry].append(((begin, end), include))
                        tree.create_node(include, include, parent=entry)
                        in_region = False
                        begin, end = 0, 0
                        include = ''

            for coords, include in insert_regions[entry]:  # include is anchored on DOC_BASE
                ref_path = DOC_BASE / include
                with open(ref_path, 'rt', encoding=ENCODING) as handle:
                    documents[include] = [line.rstrip() for line in handle.readlines()]
                insert_regions[include] = []
                in_region = False
                begin, end = 0, 0
                sub_include = ''
                for slot, line in enumerate(documents[include]):
                    if line.startswith(IMG_LINE_STARTSWITH):
                        documents[include][slot] = adapt_image(line, img_collector, include, root_path)
                    log.debug(f'{slot :02d}|{line.rstrip()}')
                    if not in_region:
                        if line.startswith(READ_SLOT_FENCE_BEGIN):
                            in_region = True
                            begin = slot
                            continue
                        if line.startswith(INCLUDE_SLOT):
                            harvest_include(line, slot, insert_regions, tree, include)
                            continue
                    if in_region:
                        if line.startswith(READ_SLOT_CONTEXT_BEGIN):
                            sub_include = (
                                line.replace(READ_SLOT_CONTEXT_BEGIN, '').split(')', 1)[0].strip("'").strip('"')
                            )
                            sub_include = str(pathlib.Path(include).parent / sub_include)
                        elif line.startswith(READ_SLOT_FENCE_END):
                            end = slot
                            insert_regions[include].append(((begin, end), sub_include))
                            tree.create_node(sub_include, sub_include, parent=include)
                            in_region = False
                            begin, end = 0, 0
                            sub_include = ''

                for coords, sub_include in insert_regions[include]:
                    ref_path = DOC_BASE / sub_include
                    with open(ref_path, 'rt', encoding=ENCODING) as handle:
                        documents[sub_include] = [line.rstrip() for line in handle.readlines()]
                    insert_regions[sub_include] = []
                    in_region = False
                    begin, end = 0, 0
                    sub_sub_include = ''
                    for slot, line in enumerate(documents[sub_include]):
                        if line.startswith(IMG_LINE_STARTSWITH):
                            documents[sub_include][slot] = adapt_image(line, img_collector, sub_include, root_path)
                        log.debug(f'{slot :02d}|{line.rstrip()}')
                        if not in_region:
                            if line.startswith(READ_SLOT_FENCE_BEGIN):
                                in_region = True
                                begin = slot
                                continue
                            if line.startswith(INCLUDE_SLOT):
                                harvest_include(line, slot, insert_regions, tree, sub_include)
                                continue
                        if in_region:
                            if line.startswith(READ_SLOT_CONTEXT_BEGIN):
                                sub_sub_include = (
                                    line.replace(READ_SLOT_CONTEXT_BEGIN, '').split(')', 1)[0].strip("'").strip('"')
                                )
                                sub_sub_include = str(pathlib.Path(sub_include).parent / sub_sub_include)
                            elif line.startswith(READ_SLOT_FENCE_END):
                                end = slot
                                insert_regions[sub_include].append(((begin, end), sub_sub_include))
                                tree.create_node(sub_sub_include, sub_sub_include, parent=sub_include)
                                in_region = False
                                begin, end = 0, 0
                                sub_sub_include = ''

                    for coords, sub_sub_include in insert_regions[sub_include]:
                        ref_path = DOC_BASE / sub_sub_include
                        with open(ref_path, 'rt', encoding=ENCODING) as handle:
                            documents[sub_sub_include] = [line.rstrip() for line in handle.readlines()]
                        insert_regions[sub_sub_include] = []
                        in_region = False
                        begin, end = 0, 0
                        sub_sub_sub_include = ''
                        for slot, line in enumerate(documents[sub_sub_include]):
                            if line.startswith(IMG_LINE_STARTSWITH):
                                documents[sub_sub_include][slot] = adapt_image(
                                    line, img_collector, sub_sub_include, root_path
                                )
                            log.debug(f'{slot :02d}|{line.rstrip()}')
                            if not in_region:
                                if line.startswith(READ_SLOT_FENCE_BEGIN):
                                    in_region = True
                                    begin = slot
                                    continue
                                if line.startswith(INCLUDE_SLOT):
                                    harvest_include(line, slot, insert_regions, tree, sub_sub_include)
                                    continue
                            if in_region:
                                if line.startswith(READ_SLOT_CONTEXT_BEGIN):
                                    sub_sub_sub_include = (
                                        line.replace(READ_SLOT_CONTEXT_BEGIN, '').split(')', 1)[0].strip("'").strip('"')
                                    )
                                    sub_sub_sub_include = str(
                                        pathlib.Path(sub_sub_include).parent / sub_sub_sub_include
                                    )
                                elif line.startswith(READ_SLOT_FENCE_END):
                                    end = slot
                                    insert_regions[sub_sub_include].append(((begin, end), sub_sub_sub_include))
                                    tree.create_node(sub_sub_sub_include, sub_sub_sub_include, parent=sub_sub_include)
                                    in_region = False
                                    begin, end = 0, 0
                                    sub_sub_sub_include = ''

                        for coords, sub_sub_sub_include in insert_regions[sub_include]:
                            ref_path = DOC_BASE / sub_sub_sub_include
                            with open(ref_path, 'rt', encoding=ENCODING) as handle:
                                documents[sub_sub_sub_include] = [line.rstrip() for line in handle.readlines()]
                            insert_regions[sub_sub_sub_include] = []
                            in_region = False
                            begin, end = 0, 0
                            sub_sub_sub_sub_include = ''
                            for slot, line in enumerate(documents[sub_sub_sub_include]):
                                if line.startswith(IMG_LINE_STARTSWITH):
                                    documents[sub_sub_sub_include][slot] = adapt_image(
                                        line, img_collector, sub_sub_sub_include, root_path
                                    )
                                log.debug(f'{slot :02d}|{line.rstrip()}')
                                if not in_region:
                                    if line.startswith(READ_SLOT_FENCE_BEGIN):
                                        in_region = True
                                        begin = slot
                                        continue
                                    if line.startswith(INCLUDE_SLOT):
                                        harvest_include(line, slot, insert_regions, tree, sub_sub_sub_include)
                                        continue
                                if in_region:
                                    if line.startswith(READ_SLOT_CONTEXT_BEGIN):
                                        sub_sub_sub_sub_include = (
                                            line.replace(READ_SLOT_CONTEXT_BEGIN, '')
                                            .split(')', 1)[0]
                                            .strip("'")
                                            .strip('"')
                                        )
                                        sub_sub_sub_sub_include = str(
                                            pathlib.Path(sub_sub_sub_include).parent / sub_sub_sub_sub_include
                                        )
                                    elif line.startswith(READ_SLOT_FENCE_END):
                                        end = slot
                                        insert_regions[sub_sub_sub_include].append(((begin, end), sub_sub_sub_include))
                                        tree.create_node(
                                            sub_sub_sub_sub_include, sub_sub_sub_sub_include, parent=sub_sub_sub_include
                                        )
                                        in_region = False
                                        begin, end = 0, 0
                                        sub_sub_sub_sub_include = ''

        top_down_paths = tree.paths_to_leaves()
        bottom_up_paths = [list(reversed(td_p)) for td_p in top_down_paths]
        log.info(separator)
        log.info('resulting tree:')
        with RedirectedStdout() as out:
            tree.show()
            for row in str(out).rstrip('\n').split('\n'):
                log.info(row)

        log.info(separator)
        log.info(f'provisioning chains for the {len(bottom_up_paths)} bottom up leaf paths:')
        for num, leaf_path in enumerate(bottom_up_paths):
            the_way_up = f'|-> {leaf_path[0]}' if len(leaf_path) == 1 else f'{" -> ".join(leaf_path)}'
            log.info(f'{num :2d}: {the_way_up}')

        concat = {}
        log.info(separator)
        log.info(f'dependencies for the {len(insert_regions)} document parts:')
        for key, regions in insert_regions.items():
            num_in = len(regions)
            dashes = "-" * num_in
            incl_disp = f'( {num_in} include{"" if num_in == 1 else "s"} )'
            indicator = '(no includes)' if not regions else f'<{dashes + incl_disp + dashes}'
            log.info(f'- part {key} {indicator}')
            for region in regions:
                between = f'between lines {region[0][0] :3d} and {region[0][1] :3d}'
                insert = f'include fragment {region[1]}'
                log.info(f'  + {between} {insert}')
            if not regions:  # No includes
                concat[key] = '\n'.join(documents[key]) + '\n'
                log.info(f'  * did concat {key} document for insertion')

        chains = [leaf_path for leaf_path in bottom_up_paths]
        log.info(separator)
        log.info(f'starting insertions bottom up for the {len(chains)} inclusion chains:')
        todo = [[job for job in chain if job not in concat] for chain in chains]
        while todo != [[]]:
            todo = rollup(todo, documents, insert_regions, concat)

        log.info(separator)
        log.info('writing final concat markdown to document.md')
        with open('document.md', 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(concat[bind] for bind in binder) + '\n')

        log.info(separator)
        log.info('collecting assets (images and diagrams)')
        collect_assets(img_collector)
        log.info(separator)
        log.info(f'concat result document (document.md) and artifacts are within folder ({os.getcwd()}/)')
        log.info(separator)
        log.info('processing complete - SUCCESS')
        log.info(separator)
        return 0

    log.error(f'structure data files with other than one target currently not supported - found targets ({targets})')
    return 1
