"""Given a target and facet, concatenate a tree of markdown files to a single file rewriting all image refs."""
import json
import os
import pathlib
import shutil
import sys
import treelib
from io import StringIO

import yaml

import liitos.gather as gat
from liitos import ENCODING, log

DOC_BASE = pathlib.Path('..', '..')
STRUCTURE_PATH = DOC_BASE / 'structure.yml'
APPROVALS_KEY = 'approvals'
BIND_KEY = 'bind'
CHANGES_KEY = 'changes'
META_KEY = 'meta'
ASPECT_KEYS = sorted((APPROVALS_KEY, BIND_KEY, CHANGES_KEY, META_KEY))

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


class RedirectedStdout:
    def __init__(self):
        self._stdout = None
        self._string_io = None

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._string_io = StringIO()
        return self

    def __exit__(self, type, value, traceback):
        sys.stdout = self._stdout

    def __str__(self):
        return self._string_io.getvalue()


def concatenate(
    doc_root: str | pathlib.Path, structure_name: str, target_key: str, facet_key: str, options: dict[str, bool]
) -> int:
    """Later alligator."""
    target_code = target_key
    facet_code = facet_key
    if not facet_code.strip() or not target_code.strip():
        log.error(f'concatenate requires non-empty target ({target_code}) and facet ({facet_code}) codes')
        return 2

    log.info(f'parsed target ({target_code}) and facet ({facet_code}) from request')

    structure, asset_map = gat.prelude(
        doc_root=doc_root, structure_name=structure_name, target_key=target_key, facet_key=facet_key, command='changes'
    )
    log.info(f'prelude teleported processor into the document root at ({os.getcwd()}/)')
    rel_concat_folder_path = pathlib.Path("render/pdf/")
    rel_concat_folder_path.mkdir(parents=True, exist_ok=True)
    os.chdir(rel_concat_folder_path)
    log.info(f'concatenate (this processor) teleported into the render/pdf location ({os.getcwd()}/)')

    if not STRUCTURE_PATH.is_file() or not STRUCTURE_PATH.stat().st_size:
        log.error(f'destructure failed to find non-empty structure file at {STRUCTURE_PATH}')
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
                f'Structure does not provide all expected aspects {sorted(gat.KEYS_REQUIRED)}'
                f' for target ({target_code}) and facet ({facet_code})'
            )
            log.error(f'- the found aspects: {sorted(aspect_map.keys())}')
            log.error(f'- missing aspects:   {sorted(missing_keys)}')
            return 1
        if sorted(aspect_map.keys()) != sorted(gat.KEYS_REQUIRED):
            log.warning(
                f'Structure does not strictly provide the expected aspects {sorted(gat.KEYS_REQUIRED)}'
                f' for target ({target_code}) and facet ({facet_code})'
            )
            log.warning(f'- found the following aspects instead:                   {sorted(aspect_map.keys())} instead')

        approvals_path = DOC_BASE / aspect_map[gat.KEY_APPROVALS]
        if not approvals_path.is_file() or not approvals_path.stat().st_size:
            log.error(f'destructure failed to find non-empty approvals file at {approvals_path}')
            return 1
        bind_path = DOC_BASE / aspect_map[gat.KEY_BIND]
        if not bind_path.is_file() or not bind_path.stat().st_size:
            log.error(f'destructure failed to find non-empty bind file at {bind_path}')
            return 1
        changes_path = DOC_BASE / aspect_map[gat.KEY_CHANGES]
        if not changes_path.is_file() or not changes_path.stat().st_size:
            log.error(f'destructure failed to find non-empty changes file at {changes_path}')
            return 1
        meta_path = DOC_BASE / aspect_map[gat.KEY_META]
        if not meta_path.is_file() or not meta_path.stat().st_size:
            log.error(f'destructure failed to find non-empty meta file at {meta_path}')
            return 1

        if approvals_path.suffix.lower() not in ('.json', '.yaml', '.yml'):
            log.error(f'approvals file format per suffix ({approvals_path.suffix}) not supported')
            return 1
        approvals_channel = 'yaml' if approvals_path.suffix.lower() in ('.yaml', '.yml') else 'json'

        if bind_path.suffix.lower() not in ('.txt',):
            log.error(f'bind file format per suffix ({bind_path.suffix}) not supported')
            return 1

        if changes_path.suffix.lower() not in ('.json', '.yaml', '.yml'):
            log.error(f'changes file format per suffix ({changes_path.suffix}) not supported')
            return 1
        changes_channel = 'yaml' if changes_path.suffix.lower() in ('.yaml', '.yml') else 'json'

        if meta_path.suffix.lower() not in ('.yaml', '.yml'):
            log.error(f'meta file format per suffix ({meta_path.suffix}) not supported')
            return 1

        with open(approvals_path, 'rt', encoding=ENCODING) as handle:
            approvals = yaml.safe_load(handle) if approvals_channel == 'yaml' else json.load(handle)
        with open(bind_path, 'rt', encoding=ENCODING) as handle:
            binder = [line.strip() for line in handle.readlines() if line.strip()]
        with open(changes_path, 'rt', encoding=ENCODING) as handle:
            changes = yaml.safe_load(handle) if changes_channel == 'yaml' else json.load(handle)
        with open(meta_path, 'rt', encoding=ENCODING) as handle:
            metadata = yaml.safe_load(handle)

        if not approvals:
            log.error(f'Empty approvals file? Please add approvals to ({approvals_path})')
            return 1
        if not binder:
            log.error(f'Empty bind file? Please add component paths to ({bind_path})')
            return 1
        if not changes:
            log.error(f'Empty changes file? Please add changes data to ({changes_path})')
            return 1
        if not approvals:
            log.error(f'Empty metadata file? Please add metadata to ({meta_path})')
            return 1

        if approvals_channel == 'yaml':
            with open('approvals.yml', 'wt', encoding=ENCODING) as handle:
                yaml.dump(approvals, handle, default_flow_style=False)
        else:
            with open('approvals.json', 'wt', encoding=ENCODING) as handle:
                json.dump(approvals, handle, indent=2)

        with open('bind.txt', 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(binder) + '\n')

        if changes_channel == 'yaml':
            with open('changes.yml', 'wt', encoding=ENCODING) as handle:
                yaml.dump(changes, handle, default_flow_style=False)
        else:
            with open('changes.json', 'wt', encoding=ENCODING) as handle:
                json.dump(changes, handle, indent=2)

        if 'import' in metadata['document']:
            base_meta_path = DOC_BASE / metadata['document']['import']
            if not base_meta_path.is_file() or not base_meta_path.stat().st_size:
                log.error(f'metadata declares import of base data from ({base_meta_path.name}) but failed to find non-empty base file at {base_meta_path}')
                return 1
            with open(base_meta_path, 'rt', encoding=ENCODING) as handle:
                base_data = yaml.safe_load(handle)
            for key, value in metadata['document']['patch'].items():
                base_data['document']['common'][key] = value
            metadata = base_data

        with open('metadata.yml', 'wt', encoding=ENCODING) as handle:
            yaml.dump(metadata, handle, default_flow_style=False)

        log.info('processing binder ...')
        root_path = str(pathlib.Path.cwd().resolve()).rstrip('/') + '/'
        documents = {}
        tree = treelib.Tree()
        root = '/'
        tree.create_node(root, root)
        insert_regions = {}
        img_collector = []
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
                    before, xtr = line.split('](', 1)
                    has_caption = True if ' ' in xtr else False
                    img, after = xtr.split(' ', 1) if has_caption else xtr.split(')', 1)
                    img_path = str((pathlib.Path(entry).parent / img).resolve()).replace(root_path, '')
                    img_collector.append(img_path)
                    img_hack = img_path
                    if '/images/' in img_path:
                        img_hack = 'images/' + img_path.split('/images/', 1)[1]
                    elif '/diagrams/' in img_path:
                        img_hack = 'diagrams/' + img_path.split('/diagrams/', 1)[1]
                    if img_hack != img_path:
                        log.debug(f'{img_hack} <--- OK? --- {img_path}')
                    line = f'{before}]({img_hack}{" " if has_caption else ")"}{after}'
                    documents[entry][slot] = line
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
                        before, xtr = line.split('](', 1)
                        has_caption = True if ' ' in xtr else False
                        img, after = xtr.split(' ', 1) if has_caption else xtr.split(')', 1)
                        img_path = str((pathlib.Path(include).parent / img).resolve()).replace(root_path, '')
                        img_collector.append(img_path)
                        line = f'{before}]({img}{" " if has_caption else ")"}{after}'
                        documents[include][slot] = line
                    log.debug(f'{slot :02d}|{line.rstrip()}')
                    if not in_region:
                        if line.startswith(READ_SLOT_FENCE_BEGIN):
                            in_region = True
                            begin = slot
                            continue
                        if line.startswith(INCLUDE_SLOT):
                            sub_include = line.split(INCLUDE_SLOT, 1)[1].rstrip('}').strip()
                            sub_include = str(pathlib.Path(include).parent / sub_include)
                            insert_regions[include].append(((slot, slot), sub_include))
                            tree.create_node(sub_include, sub_include, parent=include)
                            sub_include = ''
                            continue
                    if in_region:
                        if line.startswith(READ_SLOT_CONTEXT_BEGIN):
                            sub_include = line.replace(READ_SLOT_CONTEXT_BEGIN, '').split(')', 1)[0].strip("'").strip('"')
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
                            before, xtr = line.split('](', 1)
                            has_caption = True if ' ' in xtr else False
                            img, after = xtr.split(' ', 1) if has_caption else xtr.split(')', 1)
                            img_path = str((pathlib.Path(sub_include).parent / img).resolve()).replace(root_path, '')
                            img_collector.append(img_path)
                            line = f'{before}]({img}{" " if has_caption else ")"}{after}'
                            documents[sub_include][slot] = line
                        log.debug(f'{slot :02d}|{line.rstrip()}')
                        if not in_region:
                            if line.startswith(READ_SLOT_FENCE_BEGIN):
                                in_region = True
                                begin = slot
                                continue
                            if line.startswith(INCLUDE_SLOT):
                                sub_sub_include = line.split(INCLUDE_SLOT, 1)[1].rstrip('}').strip()
                                sub_sub_include = str(pathlib.Path(sub_include).parent / sub_sub_include)
                                insert_regions[sub_include].append(((slot, slot), sub_sub_include))
                                tree.create_node(sub_sub_include, sub_sub_include, parent=sub_include)
                                sub_sub_include = ''
                                continue
                        if in_region:
                            if line.startswith(READ_SLOT_CONTEXT_BEGIN):
                                sub_sub_include = line.replace(READ_SLOT_CONTEXT_BEGIN, '').split(')', 1)[0].strip("'").strip('"')
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
                                before, xtr = line.split('](', 1)
                                has_caption = True if ' ' in xtr else False
                                img, after = xtr.split(' ', 1) if has_caption else xtr.split(')', 1)
                                img_path = str((pathlib.Path(sub_sub_include).parent / img).resolve()).replace(root_path, '')
                                img_collector.append(img_path)
                                line = f'{before}]({img}{" " if has_caption else ")"}{after}'
                                documents[sub_sub_include][slot] = line
                            log.debug(f'{slot :02d}|{line.rstrip()}')
                            if not in_region:
                                if line.startswith(READ_SLOT_FENCE_BEGIN):
                                    in_region = True
                                    begin = slot
                                    continue
                                if line.startswith(INCLUDE_SLOT):
                                    sub_sub_sub_include = line.split(INCLUDE_SLOT, 1)[1].rstrip('}').strip()
                                    sub_sub_sub_include = str(pathlib.Path(sub_sub_include).parent / sub_sub_sub_include)
                                    insert_regions[sub_sub_include].append(((slot, slot), sub_sub_sub_include))
                                    tree.create_node(sub_sub_sub_include, sub_sub_sub_include, parent=sub_sub_include)
                                    sub_sub_sub_include = ''
                                    continue
                            if in_region:
                                if line.startswith(READ_SLOT_CONTEXT_BEGIN):
                                    sub_sub_sub_include = line.replace(READ_SLOT_CONTEXT_BEGIN, '').split(')', 1)[0].strip("'").strip('"')
                                    sub_sub_sub_include = str(pathlib.Path(sub_sub_include).parent / sub_sub_sub_include)
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
                                    before, xtr = line.split('](', 1)
                                    has_caption = True if ' ' in xtr else False
                                    img, after = xtr.split(' ', 1) if has_caption else xtr.split(')', 1)
                                    img_path = str((pathlib.Path(sub_sub_sub_include).parent / img).resolve()).replace(root_path, '')
                                    img_collector.append(img_path)
                                    line = f'{before}]({img}{" " if has_caption else ")"}{after}'
                                    documents[sub_sub_sub_include][slot] = line
                                log.debug(f'{slot :02d}|{line.rstrip()}')
                                if not in_region:
                                    if line.startswith(READ_SLOT_FENCE_BEGIN):
                                        in_region = True
                                        begin = slot
                                        continue
                                    if line.startswith(INCLUDE_SLOT):
                                        sub_sub_sub_sub_include = line.split(INCLUDE_SLOT, 1)[1].rstrip('}').strip()
                                        sub_sub_sub_sub_include = str(
                                            pathlib.Path(sub_sub_sub_include).parent / sub_sub_sub_sub_include
                                        )
                                        insert_regions[sub_sub_sub_sub_include].append(((slot, slot), sub_sub_sub_sub_include))
                                        tree.create_node(sub_sub_sub_sub_include, sub_sub_sub_sub_include, parent=sub_sub_sub_include)
                                        sub_sub_sub_sub_include = ''
                                        continue
                                if in_region:
                                    if line.startswith(READ_SLOT_CONTEXT_BEGIN):
                                        sub_sub_sub_sub_include = line.replace(READ_SLOT_CONTEXT_BEGIN, '').split(')', 1)[0].strip("'").strip('"')
                                        sub_sub_sub_sub_include = str(pathlib.Path(sub_sub_sub_include).parent / sub_sub_sub_sub_include)
                                    elif line.startswith(READ_SLOT_FENCE_END):
                                        end = slot
                                        insert_regions[sub_sub_sub_include].append(((begin, end), sub_sub_sub_include))
                                        tree.create_node(sub_sub_sub_sub_include, sub_sub_sub_sub_include, parent=sub_sub_sub_include)
                                        in_region = False
                                        begin, end = 0, 0
                                        sub_sub_sub_sub_include = ''

        top_down_paths = tree.paths_to_leaves()
        bottom_up_paths = [list(reversed(td_p)) for td_p in top_down_paths]
        log.info('resulting tree:')
        with RedirectedStdout() as out:
            tree.show()
            for row in str(out).rstrip('\n').split('\n'):
                log.info(row)

        log.info(f'provisioning chains for the {len(bottom_up_paths)} bottom up leaf paths:')
        for num, leaf_path in enumerate(bottom_up_paths):
            the_way_up = f'|-> {leaf_path[0]}' if len(leaf_path) == 1 else f'{" -> ".join(leaf_path)}'
            log.info(f'{num :2d}: {the_way_up}')

        concat = {}
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
        log.info(f'starting insertions bottom up for the {len(chains)} inclusion chains:')

        remaining = [[job for job in chain if job not in concat] for chain in chains]
        tackle = [those[0] for those in remaining if those]
        if tackle:
            log.info(f'  Insertion ongoing with parts ({", ".join(tuple(sorted(tackle)))}) remaining')
        for that in tackle:
            if that == '/':
                continue
            buf = []
            for slot, line in enumerate(documents[that]):
                special = False
                the_first = False
                the_include = ''
                for pair, include in insert_regions[that]:
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
                    buf.append(concat[the_include])
            concat[that] = '\n'.join(buf) + '\n'

        still = [[job for job in chain if job not in concat] for chain in remaining]
        tackle = set(those[0] for those in still if those)
        if tackle:
            log.info(f'  Insertion ongoing with parts ({", ".join(tuple(sorted(tackle)))}) remaining')
        for that in tackle:
            if that == '/':
                continue
            buf = []
            for slot, line in enumerate(documents[that]):
                special = False
                the_first = False
                the_include = ''
                for pair, include in insert_regions[that]:
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
                    buf.append(concat[the_include])
            concat[that] = '\n'.join(buf) + '\n'

        more = [[job for job in chain if job not in concat] for chain in still]
        tackle = set(those[0] for those in more if those)
        if tackle:
            log.info(f'  Insertion ongoing with parts ({", ".join(tuple(sorted(tackle)))}) remaining')
        for that in tackle:
            if that == '/':
                continue
            # PROTOBUG print(that, insert_regions[that])
            buf = []
            for slot, line in enumerate(documents[that]):
                special = False
                the_first = False
                the_include = ''
                for pair, include in insert_regions[that]:
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
                    buf.append(concat[the_include])
            concat[that] = '\n'.join(buf) + '\n'

        done = [[job for job in chain if job not in concat] for chain in more]
        tackle = set(those[0] for those in done if those)
        if tackle and len(tackle) >= 1 and tuple(tackle)[0] != '/':
            log.warning(f' Insertion incomplete with parts ({", ".join(tuple(sorted(tackle)))}) remaining')

        log.info('writing final concat markdown to document.md')
        with open('document.md', 'wt', encoding=ENCODING) as handle:
            handle.write('\n'.join(concat[bind] for bind in binder) + '\n')

        log.info('collecting assets (images and diagrams)')
        images = pathlib.Path("images/")
        images.mkdir(parents=True, exist_ok=True)
        diagrams = pathlib.Path("diagrams/")
        diagrams.mkdir(parents=True, exist_ok=True)
        for img_path in img_collector:
            if 'images/' in img_path:
                source_asset = DOC_BASE / img_path
                target_asset = images / pathlib.Path(img_path).name
                shutil.copy(source_asset, target_asset)
                continue
            if 'diagrams/' in img_path:
                source_asset = DOC_BASE / img_path
                target_asset = diagrams / pathlib.Path(img_path).name
                shutil.copy(source_asset, target_asset)

        log.info(f'concat result document (document.md) and artifacts are within folder ({os.getcwd()}/)')
        log.info('processing complete - SUCCESS')
        return 0

    log.error(f'structure data files with other than one target currently not supported - found targets ({targets})')
    return 1
