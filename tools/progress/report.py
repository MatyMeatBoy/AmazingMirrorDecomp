#!/usr/bin/env python3
"""Measure compiled main-object text without claiming a linked ROM comparison."""
import argparse
import json
from pathlib import Path
import re
import render

ORIGINAL_ASM = {'crt0', 'libagbsyscall', 'multi_sio_asm', 'm4a_asm'}


def named(name):
    return not re.match(r'^(?:sub_|func_|FUN_|nullsub_|_?0?8[0-9a-fA-F]{6})', name) and not name.startswith('<')


def _stats(cells):
    size = sum(c['size'] for c in cells)
    funcs = [c for c in cells if c['function']]
    c_bytes = sum(c['size'] for c in cells if c['kind'] == 'c')
    return {'bytes': size, 'c_bytes': c_bytes, 'c_percent': round(100*c_bytes/size, 4) if size else 0,
            'pending_asm_bytes': sum(c['size'] for c in cells if c['kind'] == 'asm'),
            'original_asm_bytes': sum(c['size'] for c in cells if c['kind'] == 'original_asm'),
            'unattributed_bytes': sum(c['size'] for c in cells if c['kind'] == 'unknown'),
            'functions': len(funcs), 'c_functions': sum(c['kind'] == 'c' for c in funcs),
            'named_functions': sum(c['named'] for c in funcs)}


def data_summary(census):
    return {'identified_bytes': None, 'total_bytes': None, 'status': 'source census; recovery not measured',
            'source_formats': census['formats'], 'data_translation_units': len(census['data_translation_units']),
            'incbin_wrappers': len(census['incbin_wrappers']),
            'raw_by_target': {target: {'directives': values['directives'], 'union_bytes': values['union_bytes']}
                              for target, values in census['raw'].items()}}


def summarize(manifest):
    if manifest.get('schema_version') != 1 or manifest.get('scope') != 'main_object_text' or manifest.get('rom_verified') is not False:
        raise ValueError('Expected an unverified main-object-text manifest')
    modules = []; sources = set(); excluded_header_bytes = 0
    for source in manifest['sources']:
        path = source['source']
        if not isinstance(path, str) or not re.fullmatch(r'(?:src|asm)/(?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_.-]+\.(?:c|s)', path) or any(p in ('.', '..') for p in path.split('/')):
            raise ValueError('Invalid source path')
        if path in sources:
            raise ValueError('Duplicate source entry')
        sources.add(path)
        all_sections = {}
        for section in source['sections']:
            name, size = section['name'], section['size']
            if not isinstance(name, str) or not re.fullmatch(r'\.[A-Za-z0-9_.-]+', name) or name in all_sections:
                raise ValueError('Invalid or duplicate section name')
            if type(size) is not int or size < 0:
                raise ValueError('Invalid section size')
            all_sections[name] = size
        for symbol in source['symbols']:
            if not isinstance(symbol['section'], str) or symbol['section'] not in all_sections:
                raise ValueError('Symbol references unknown section')
            if type(symbol['offset']) is not int or type(symbol['size']) is not int or symbol['offset'] < 0 or symbol['size'] < 0 or symbol['offset'] + symbol['size'] > all_sections[symbol['section']]:
                raise ValueError('Invalid symbol extent')
            if not isinstance(symbol.get('aliases', []), list):
                raise ValueError('Invalid aliases')
            names = [symbol['name'], *symbol.get('aliases', [])]
            if not all(isinstance(n, str) and n and not any(ord(c) < 32 for c in n) for n in names):
                raise ValueError('Invalid symbol name')
        sections = {name: size for name, size in all_sections.items() if name == '.text' or name.startswith('.text.')}
        cells = []
        for section, size in sections.items():
            aliases = {}
            for symbol in source['symbols']:
                if symbol['section'] != section or symbol['size'] == 0:
                    continue
                start = symbol['offset']; end = start + symbol['size']
                if start < 0 or end > size or end <= start or symbol['kind'] not in ('c', 'asm', 'unknown'):
                    raise ValueError('Invalid symbol span or attribution')
                if start in aliases:
                    other = aliases[start]
                    if other['size'] != symbol['size'] or other['kind'] != symbol['kind']:
                        raise ValueError('Conflicting aliases')
                    other['aliases'] = sorted(set(other['aliases'] + [symbol['name']] + symbol.get('aliases', [])))
                else:
                    aliases[start] = dict(symbol, aliases=sorted(set([symbol['name']] + symbol.get('aliases', []))))
            cursor = 0
            ranges = []
            for start, symbol in sorted(aliases.items()):
                if start < cursor:
                    raise ValueError('Overlapping symbol spans')
                if start > cursor:
                    ranges.append((cursor, start, 'unknown', ['<unattributed>']))
                ranges.append((start, start+symbol['size'], symbol['kind'], symbol['aliases']))
                cursor = start+symbol['size']
            if cursor < size:
                ranges.append((cursor, size, 'unknown', ['<unattributed>']))
            for start, end, kind, names in ranges:
                pieces = [(start, end)]
                if path == 'asm/crt0.s' and section == '.text':
                    removed = max(0, min(end, 192)-max(start, 4))
                    excluded_header_bytes += removed
                    pieces = [(a,b) for a,b in ((start,min(end,4)), (max(start,192),end)) if b>a] if removed else pieces
                if Path(path).stem in ORIGINAL_ASM and path.startswith('asm/') and kind == 'asm':
                    kind = 'original_asm'
                for index, (a,b) in enumerate(pieces):
                    cells.append({'name': next((n for n in names if named(n)), names[0]), 'aliases': sorted(names),
                                  'section': section, 'offset': a, 'size': b-a, 'kind': kind,
                                  'named': any(named(n) for n in names),
                                  'function': kind != 'unknown' and index == 0})
        modules.append({'source': path, 'cells': cells, **_stats(cells)})
    totals = _stats([cell for m in modules for cell in m['cells']])
    return {'schema_version': 1, 'game': 'Kirby & The Amazing Mirror', 'region': 'USA (B8KE)',
            'scope': 'main_object_text', 'rom_match_verified': False,
            'measurement': 'Unlinked main-object .text source inventory; not a whole-game matching percentage.',
            'excluded': ['Compiler archives', 'Auxiliary multiboot programs', 'Non-text sections', 'Cartridge header'],
            'excluded_header_bytes': excluded_header_bytes, 'totals': totals, 'modules': modules,
            'baseline_commit': manifest.get('baseline_commit'), 'source_fingerprint': manifest.get('input_sha256'),
            'data': {'identified_bytes': None, 'total_bytes': None, 'status': 'not measured'}}


def markdown(report):
    s = report['totals']
    return '\n'.join(['# AmazingMirrorDecomp progress', '',
        f"Compiled C coverage in measured main-object text: **{s['c_percent']:.3f}%** ({s['c_bytes']:,} / {s['bytes']:,} bytes).", '',
        '**ROM match: not verified.** This is an unlinked source inventory, not the complete-game matching percentage.', '',
        f"C functions: {s['c_functions']:,} / {s['functions']:,}. Existing names: {s['named_functions']:,} / {s['functions']:,}; names are not independently validated semantics.", '',
        f"Pending assembly: {s['pending_asm_bytes']:,} bytes. Intentionally retained assembly: {s['original_asm_bytes']:,} bytes. Unattributed padding/text: {s['unattributed_bytes']:,} bytes.", '',
        f"Excluded cartridge header: {report['excluded_header_bytes']} bytes. Compiler archives, auxiliary multiboot programs and non-text sections are outside this denominator. Function extents may include literal pools and alignment.", '',
        'Data-format recovery is not measured. Existing source assets and preserved bytes receive no automatic identification credit.', '',
        'The authoritative matching gate remains the original dependency-aware make compare with six successful checksums. No owned Kirby ROM was available for this report.', ''])


def write(report, out):
    out.mkdir(parents=True, exist_ok=True)
    outputs = {'progress.json': json.dumps(report, indent=2)+'\n', 'progress.md': markdown(report),
               'treemap.svg': render.treemap(report), 'names_treemap.svg': render.treemap(report, names=True),
               'data.svg': render.data_svg(report.get('data')),
               'badge_decompiled.svg': render.badge_svg('main object C', f"{report['totals']['c_percent']:.2f}%", render.GREEN),
               'badge_rom.svg': render.badge_svg('ROM match', 'NOT VERIFIED', render.GREY),
               'badge_names.svg': render.badge_svg('existing names', f"{report['totals']['named_functions']}/{report['totals']['functions']}", render.GREEN),
               'badge_data.svg': render.badge_svg('data recovery', 'NOT MEASURED', render.GREY)}
    for name, content in outputs.items():
        (out/name).write_text(content, encoding='utf-8', newline='\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--metadata-dir', type=Path, default=Path('build/metadata'))
    parser.add_argument('--out', type=Path, default=Path('docs/progress'))
    args = parser.parse_args()
    from metadata_build import validate_manifest
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((args.metadata_dir/'manifest.json').read_text())
    validate_manifest(manifest, root)
    report = summarize(manifest)
    from data_inventory import inventory
    report['data'] = data_summary(inventory(root))
    write(report, args.out)
    print(json.dumps(report['totals'], indent=2))


if __name__ == '__main__':
    main()
