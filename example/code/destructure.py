#! /usr/bin/env python
# destructure the structure YAML file for target and facet
import json
import pathlib
import shutil
import sys

import yaml

ENCODING = 'utf-8'
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

"""
![Alt Text Red](images/red.png "Caption Text Red")
![Alt Text Dot Dot Lime](../images/lime.png "Caption Text Dot Dot Lime")
![Alt Text Blue](images/blue.png "Caption Text Blue")
![Alt Text Sting Red](other/images/red.png "Caption Text Sting Red")
"""
IMG_LINE_STARTSWITH = '!['

if len(sys.argv[1:]) != 2:
    print(f'destructure expected target and facet arguments but received {sys.argv[1:]}', file=sys.stderr)
    sys.exit(2)

target_code, facet_code = sys.argv[1:3]
print(f'Parsed target ({target_code}) and facet ({facet_code}) from request')

if not STRUCTURE_PATH.is_file() or not STRUCTURE_PATH.stat().st_size:
    print(f'destructure failed to find non-empty structure file at {STRUCTURE_PATH}', file=sys.stderr)
    sys.exit(1)

with open(STRUCTURE_PATH, 'rt', encoding=ENCODING) as handle:
    structure = yaml.safe_load(handle)

# PROTOBUG print(json.dumps(structure, indent=2))
targets = sorted(structure.keys())
if len(targets) == 1:
    target = targets[0]
    facets = sorted(list(facet.keys())[0] for facet in structure[target])
    print(f'Found single target ({target}) with facets ({facets})')

    if facet_code not in facets:
        print(f'Structure does not provide facet ({facet_code}) for target ({target_code})', file=sys.stderr)
        sys.exit(1)

    aspect_map = {}
    for data in structure[target]:
        if facet_code in data:
            aspect_map = data[facet_code]
            break
    if sorted(aspect_map.keys()) != ASPECT_KEYS:
        print(f'Structure does not provide the expected aspects ({ASPECT_KEYS}) for target ({target_code}) and facet ({facet_code})', file=sys.stderr)
        print(f'- found the following aspects instead:          ({sorted(aspect_map.keys())}) instead', file=sys.stderr)
        sys.exit(1)

    # PROTOBUG print(json.dumps(aspect_map, indent=2))
    approvals_path = DOC_BASE / aspect_map[APPROVALS_KEY]
    if not approvals_path.is_file() or not approvals_path.stat().st_size:
        print(f'destructure failed to find non-empty approvals file at {approvals_path}', file=sys.stderr)
        sys.exit(1)
    bind_path = DOC_BASE / aspect_map[BIND_KEY]
    if not bind_path.is_file() or not bind_path.stat().st_size:
        print(f'destructure failed to find non-empty bind file at {bind_path}', file=sys.stderr)
        sys.exit(1)
    changes_path = DOC_BASE / aspect_map[CHANGES_KEY]
    if not changes_path.is_file() or not changes_path.stat().st_size:
        print(f'destructure failed to find non-empty changes file at {changes_path}', file=sys.stderr)
        sys.exit(1)
    meta_path = DOC_BASE / aspect_map[META_KEY]
    if not meta_path.is_file() or not meta_path.stat().st_size:
        print(f'destructure failed to find non-empty meta file at {meta_path}', file=sys.stderr)
        sys.exit(1)

    if approvals_path.suffix.lower() not in ('.json', '.yaml', '.yml'):
        print(f'approvals file format per suffix ({approvals_path.suffix}) not supported', file=sys.stderr)
        sys.exit(1)
    approvals_channel = 'yaml' if approvals_path.suffix.lower() in ('.yaml', '.yml') else 'json'

    if bind_path.suffix.lower() not in ('.txt',):
        print(f'bind file format per suffix ({bind_path.suffix}) not supported', file=sys.stderr)
        sys.exit(1)

    if changes_path.suffix.lower() not in ('.json', '.yaml', '.yml'):
        print(f'changes file format per suffix ({changes_path.suffix}) not supported', file=sys.stderr)
        sys.exit(1)
    changes_channel = 'yaml' if changes_path.suffix.lower() in ('.yaml', '.yml') else 'json'

    if meta_path.suffix.lower() not in ('.yaml', '.yml'):
        print(f'meta file format per suffix ({meta_path.suffix}) not supported', file=sys.stderr)
        sys.exit(1)

    with open(approvals_path, 'rt', encoding=ENCODING) as handle:
        approvals = yaml.safe_load(handle) if approvals_channel == 'yaml' else json.load(handle)
    # PROTOBUG print(json.dumps(approvals, indent=2))
    with open(bind_path, 'rt', encoding=ENCODING) as handle:
        binder = [line.strip() for line in handle.readlines() if line.strip()]
    # PROTOBUG print(json.dumps(binder, indent=2))
    with open(changes_path, 'rt', encoding=ENCODING) as handle:
        changes = yaml.safe_load(handle) if changes_channel == 'yaml' else json.load(handle)
    # PROTOBUG print(json.dumps(changes, indent=2))
    with open(meta_path, 'rt', encoding=ENCODING) as handle:
        metadata = yaml.safe_load(handle)
    # PROTOBUG print(json.dumps(metadata, indent=2))

    if not approvals:
        print(f'Empty approvals file? Please add approvals to ({approvals_path})', file=sys.stderr)
        sys.exit(1)
    if not binder:
        print(f'Empty bind file? Please add component paths to ({bind_path})', file=sys.stderr)
        sys.exit(1)
    if not changes:
        print(f'Empty changes file? Please add changes data to ({changes_path})', file=sys.stderr)
        sys.exit(1)
    if not approvals:
        print(f'Empty metadata file? Please add metadata to ({meta_path})', file=sys.stderr)
        sys.exit(1)

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

    # PROTOBUG print(json.dumps(metadata, indent=2))
    if 'import' in metadata['document']:
        base_meta_path = DOC_BASE / metadata['document']['import']
        if not base_meta_path.is_file() or not base_meta_path.stat().st_size:
            print(f'metadata declares import of base data from ({base_meta_path.name}) but failed to find non-empty base file at {base_meta_path}', file=sys.stderr)
            sys.exit(1)
        with open(base_meta_path, 'rt', encoding=ENCODING) as handle:
            base_data = yaml.safe_load(handle)
        # PROTOBUG print(json.dumps(base_data, indent=2))
        for key, value in metadata['document']['patch'].items():
            base_data['document']['common'][key] = value
        metadata = base_data

    with open('metadata.yml', 'wt', encoding=ENCODING) as handle:
        yaml.dump(metadata, handle, default_flow_style=False)

    print('Processing binder ...')
    print('-' * 79)
    root_path = str(pathlib.Path.cwd().resolve()).rstrip('/') + '/'
    documents = {}
    refs = {}
    insert_regions = {}
    img_collector = []
    for entry in binder:
        path = DOC_BASE / entry
        print(f'- {entry} as {path}')
        with open(path, 'rt', encoding=ENCODING) as handle:
            documents[entry] = [line.rstrip() for line in handle.readlines()]
        insert_regions[entry] = []
        in_region = False
        begin, end = 0, 0
        include = ''
        refs[entry] = {}
        for slot, line in enumerate(documents[entry]):
            if line.startswith(IMG_LINE_STARTSWITH):
                before, xtr = line.split('](', 1)
                has_caption = True if ' ' in xtr else False
                img, after = xtr.split(' ', 1) if has_caption else xtr.split(')', 1)
                img_path = str((pathlib.Path(entry).parent / img).resolve()).replace(root_path, '')
                img_collector.append(img_path)
                line = f'{before}]({img}{" " if has_caption else ")"}{after}'
                documents[entry][slot] = line
            print(f'{slot :02d}|{line.rstrip()}')
            if not in_region:
                if line.startswith(READ_SLOT_FENCE_BEGIN):
                    in_region = True
                    begin = slot
                    continue
            if in_region:
                if line.startswith(READ_SLOT_CONTEXT_BEGIN):
                    # PROTOBUG print(f'<<<<< ({line})')
                    include = line.replace(READ_SLOT_CONTEXT_BEGIN, '').split(')', 1)[0].strip("'").strip('"')
                elif line.startswith(READ_SLOT_FENCE_END):
                    end = slot
                    # PROTOBUG print(f'>>>>> {entry} -> {include}')
                    insert_regions[entry].append(((begin, end), include))
                    refs[entry][include] = {}
                    in_region = False
                    begin, end = 0, 0
                    include = ''

        for coords, include in insert_regions[entry]:  # include is anchored on DOC_BASE
            ref_path = DOC_BASE / include
            print(f'  + {include} as {ref_path}')
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
                print(f'{slot :02d}|{line.rstrip()}')
                if not in_region:
                    if line.startswith(READ_SLOT_FENCE_BEGIN):
                        in_region = True
                        begin = slot
                        continue
                if in_region:
                    if line.startswith(READ_SLOT_CONTEXT_BEGIN):
                        # PROTOBUG print(f'<<<<< ({line})')
                        sub_include = line.replace(READ_SLOT_CONTEXT_BEGIN, '').split(')', 1)[0].strip("'").strip('"')
                        sub_include = str(pathlib.Path(include).parent / sub_include)
                    elif line.startswith(READ_SLOT_FENCE_END):
                        end = slot
                        # PROTOBUG print(f'>>>>> {entry} -> {include} -> {sub_include}')
                        insert_regions[include].append(((begin, end), sub_include))
                        refs[entry][include] = {}
                        in_region = False
                        begin, end = 0, 0
                        sub_include = ''

            for coords, sub_include in insert_regions[include]:
                ref_path = DOC_BASE / sub_include
                print(f'    * {sub_include} as {ref_path}')
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
                    print(f'{slot :02d}|{line.rstrip()}')
                    if not in_region:
                        if line.startswith(READ_SLOT_FENCE_BEGIN):
                            in_region = True
                            begin = slot
                            continue
                    if in_region:
                        if line.startswith(READ_SLOT_CONTEXT_BEGIN):
                            # PROTOBUG print(f'<<<<< ({line})')
                            sub_sub_include = line.replace(READ_SLOT_CONTEXT_BEGIN, '').split(')', 1)[0].strip("'").strip('"')
                            sub_sub_include = str(pathlib.Path(sub_include).parent / sub_sub_include)
                        elif line.startswith(READ_SLOT_FENCE_END):
                            end = slot
                            # PROTOBUG print(f'>>>>> {entry} -> {include} -> {sub_include}')
                            insert_regions[sub_include].append(((begin, end), sub_sub_include))
                            refs[entry][include][sub_include] = {}
                            in_region = False
                            begin, end = 0, 0
                            sub_sub_include = ''

                for coords, sub_sub_include in insert_regions[sub_include]:
                    ref_path = DOC_BASE / sub_sub_include
                    print(f'    * {sub_sub_include} as {ref_path}')
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
                        print(f'{slot :02d}|{line.rstrip()}')
                        if not in_region:
                            if line.startswith(READ_SLOT_FENCE_BEGIN):
                                in_region = True
                                begin = slot
                                continue
                        if in_region:
                            if line.startswith(READ_SLOT_CONTEXT_BEGIN):
                                # PROTOBUG print(f'<<<<< ({line})')
                                sub_sub_sub_include = line.replace(READ_SLOT_CONTEXT_BEGIN, '').split(')', 1)[0].strip("'").strip('"')
                                sub_sub_sub_include = str(pathlib.Path(sub_include).parent / sub_sub_sub_include)
                            elif line.startswith(READ_SLOT_FENCE_END):
                                end = slot
                                # PROTOBUG print(f'>>>>> {entry} -> {include} -> {sub_include}')
                                insert_regions[sub_sub_include].append(((begin, end), sub_sub_sub_include))
                                refs[entry][include][sub_include][sub_sub_include] = {}
                                in_region = False
                                begin, end = 0, 0
                                sub_sub_sub_include = ''
    print('-' * 79)
    print('insert_regions')
    print('- ' * 39)
    print(json.dumps(insert_regions, indent=2))
    print('refs')
    print('- ' * 39)
    print(json.dumps(refs, indent=2))
    print('documents')
    print('- ' * 39)
    print(json.dumps(documents, indent=2))
    print('img_collector')
    print('- ' * 39)
    print(json.dumps(img_collector, indent=2))
    print('documents.keys()')
    print('- ' * 39)
    print(json.dumps(list(documents.keys()), indent=2))
    print('- ' * 39)

    """
    concat = []
    for bind in binder:
    for key, regions in insert_regions.items():
        print(f'{key} -------')
        for line in lines:
            print(line)
    """
    print('OK or so')
    sys.exit(0)

print(f'structure data files with other than one target currently not supported - found targets ({targets})', file=sys.stderr)
sys.exit(1)
