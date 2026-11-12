"""Inventory checked-in data representations without claiming ROM matching.

Raw ranges use each target's own baserom coordinate space. They are not asset
identifications and auxiliary offsets must never be merged into the main ROM.
"""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import subprocess


def union_bytes(ranges):
    total, end = 0, 0
    for start, stop in sorted(ranges):
        if start < 0 or stop < start:
            raise ValueError('invalid range')
        total += max(0, stop-max(start, end))
        end = max(end, stop)
    return total


def raw_ranges(text):
    result, symbol = [], None
    for number, line in enumerate(text.splitlines(), 1):
        label = re.match(r'\s*([A-Za-z_]\w*)::?', line)
        if label:
            symbol = label[1]
        if not re.search(r'\.incbin\s+"baserom\.gba"', line):
            continue
        match = re.search(r'\.incbin\s+"baserom\.gba"\s*,\s*(0x[\da-fA-F]+|\d+)\s*,\s*(0x[\da-fA-F]+|\d+)\s*(?:@.*)?$', line)
        if not match:
            raise ValueError(f'unsupported baserom range at line {number}: {line}')
        offset, size = (int(value, 0) for value in match.groups())
        result.append(dict(symbol=symbol, offset=offset, size=size, line=number))
    return result


def inventory(root):
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
    tracked = [name for name in tracked if name and (root/name).is_file()]
    formats = defaultdict(Counter)
    raw = defaultdict(list)
    typed_units, incbin_wrappers = [], []
    for name in tracked:
        path = root/name
        parts = Path(name).parts
        target = 'main'
        if parts[0] == 'multi_boot':
            owners = [parent for parent in path.parents if parent.is_relative_to(root/'multi_boot') and (parent/'Makefile').is_file()]
            if not owners:
                raise ValueError('auxiliary source has no owning Makefile: '+name)
            target = owners[0].relative_to(root).as_posix()
        if parts[0] in {'graphics','sound','multi_boot'}:
            formats[target][path.suffix.lower() or '<none>'] += 1
        if path.suffix == '.s':
            for entry in raw_ranges(path.read_text(errors='replace')):
                raw[target].append(dict(entry, source=name))
        if path.suffix == '.c':
            text = path.read_text(errors='replace')
            if name.startswith('src/data/'):
                typed_units.append(name)
            for match in re.finditer(r'\b([A-Za-z_]\w*)\s*(?:\[[^;=]*\])*\s*=\s*INCBIN_(\w+)\("([^"]+)"\)', text):
                incbin_wrappers.append(dict(source=name, symbol=match[1], macro_type=match[2], asset=match[3]))
    return dict(schema_version=1, rom_verified=False, scope='tracked_source_inventory', limitations=['No data completion percentage: raw ranges are opaque, typed declarations need binary and semantic verification.', 'Auxiliary baserom offsets belong to independent ROMs.', 'File extension counts describe source representation, not recovered bytes.'], formats={target:dict(counts) for target,counts in formats.items()}, data_translation_units=typed_units, incbin_wrappers=incbin_wrappers, raw={target:dict(directives=len(entries), union_bytes=union_bytes((x['offset'],x['offset']+x['size']) for x in entries), entries=entries) for target,entries in raw.items()})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('build/progress/data-inventory.json'))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = inventory(root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({target:{key:value for key,value in values.items() if key!='entries'} for target,values in result['raw'].items()}, indent=2))
