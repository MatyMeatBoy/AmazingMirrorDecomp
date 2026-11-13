#!/usr/bin/env python3
"""Render source-current evidence of an owner-local European ROM rebuild."""
import argparse
import hashlib
from html import escape
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import render

ROOT = Path(__file__).resolve().parents[2]
SHA1 = '6f478a455383a2a12378f292581dfd7300300700'
ROM_SIZE = 0x1000000
CODE_END = 0x15C714
COMPILER_COMMIT = '59b966ed1b8f371856dcf99f1546c2fe89c678ca'
CFLAGS = '-mthumb-interwork -Wimplicit -Wparentheses -Werror -O2 -fhex-asm -f2003-patch -ffix-debug-line -g'
RECIPES = {'tools/progress/eu_match.py', 'tools/progress/eu_build.py', 'tools/progress/metadata_build.py'}


def hash_value(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def safe_path(value):
    if not isinstance(value, str) or '\\' in value or ':' in value:
        return False
    p = PurePosixPath(value)
    return bool(p.parts) and not p.is_absolute() and '..' not in p.parts and p.as_posix() == value


def source_data_spans(receipt):
    if 'source_data_spans' in receipt:
        return receipt['source_data_spans']
    spans = []
    for module in receipt.get('modules', []):
        for section in module['sections']:
            name = section['name']
            if name not in ('.rodata','.data') and not name.startswith(('.rodata.','.data.')):
                continue
            start = section['address']-0x08000000
            spans.append({'source':module['source'],'section':name,'start':start,
                          'end':start+section['size'],'bytes':section['size'],
                          'sha256':section['sha256'],'object_sha256':module['object_sha256']})
    return spans


def assess(receipt, root):
    if not isinstance(receipt, dict):
        raise ValueError('Receipt must be an object')
    root = Path(root).resolve(); issues = []; stale = []
    expected = {'schema_version': 1, 'analysis_only': False, 'rom_match_verified': True,
                'full_rom_byte_compare': True, 'expected_sha1': SHA1, 'rebuilt_sha1': SHA1,
                'eu_sha1': SHA1, 'rom_size': ROM_SIZE, 'code_end': CODE_END}
    for key, value in expected.items():
        if type(receipt.get(key)) is not type(value) or receipt.get(key) != value:
            issues.append(f'Invalid or missing {key}')
    compiler = receipt.get('compiler', {})
    if not isinstance(compiler, dict) or compiler.get('commit') != COMPILER_COMMIT or not hash_value(compiler.get('sha256')):
        issues.append('Pinned compiler evidence missing')
    binaries = receipt.get('compiler_binary_sha256', {})
    if not isinstance(binaries, dict) or not {'agbcc','old_agbcc'}.issubset({n.removesuffix('.exe') for n in binaries}) or not all(hash_value(v) for v in binaries.values()):
        issues.append('Compiler binary hashes missing')
    recipe = receipt.get('compiler_recipe', {})
    if not isinstance(recipe, dict) or recipe.get('default_cflags') != CFLAGS:
        issues.append('Original compiler flags not established')
    for key in ('source_manifest_sha256', 'matcher_sha256', 'builder_sha256'):
        if not hash_value(receipt.get(key)):
            issues.append(f'Invalid or missing {key}')
    inputs = receipt.get('inputs_sha256', {}); modes = receipt.get('source_hash_modes', {})
    if not isinstance(inputs, dict) or not inputs:
        issues.append('Source fingerprints missing'); inputs = {}
    if not isinstance(modes, dict):
        issues.append('Fingerprint modes missing'); modes = {}
    if not RECIPES.issubset(inputs):
        issues.append('Required recipe fingerprints missing')
    from eu_build import provenance
    try:
        current_inputs, current_modes = provenance(root)
        if inputs != current_inputs or modes != current_modes:
            issues.append('Complete source inventory or fingerprints changed')
    except (OSError, ValueError, subprocess.SubprocessError):
        issues.append('Current source inventory unavailable')
    for name, wanted in inputs.items():
        if not safe_path(name) or not hash_value(wanted) or modes.get(name) not in ('lf','raw'):
            stale.append(str(name)); continue
        p = (root/name).resolve()
        if not p.is_relative_to(root) or not p.is_file():
            stale.append(name); continue
        b = p.read_bytes()
        if modes[name] == 'lf':
            b = b.replace(b'\r\n', b'\n')
        if hashlib.sha256(b).hexdigest() != wanted:
            stale.append(name)
    if stale:
        issues.append('Source inputs changed or missing')
    spans = receipt.get('c_spans', [])
    if not isinstance(spans, list):
        raise ValueError('C spans must be a list')
    checked = []; previous = 0
    for span in sorted(spans, key=lambda s:s['start']):
        start, end = span['start'], span['end']; source = span['source']
        if type(start) is not int or type(end) is not int or type(span.get('bytes')) is not int or start < previous or start < 0 or end <= start or end > CODE_END or max(start,4) < min(end,192) or span.get('bytes') != end-start:
            raise ValueError('Invalid, overlapping or header-containing C span')
        if not safe_path(source) or not source.startswith('src/') or not source.endswith('.c'):
            raise ValueError('C spans require repository C source paths')
        if source not in inputs:
            issues.append('C source fingerprint missing: '+source)
        for key in ('object_sha256','linked_span_sha256'):
            if not hash_value(span.get(key)):
                issues.append(f'{key} missing: {source}')
        name = span.get('name')
        if not isinstance(name, str) or not name or any(ord(c)<32 for c in name):
            raise ValueError('Invalid function name')
        checked.append({'source': source, 'name': name, 'start': start, 'end': end, 'bytes': end-start,
                        'object_sha256': span.get('object_sha256'), 'linked_span_sha256': span.get('linked_span_sha256')})
        previous = end
    if receipt.get('credited_c_bytes') != sum(s['bytes'] for s in checked):
        issues.append('Credited byte total inconsistent')
    data_spans = source_data_spans(receipt)
    data_ranges = []
    for span in data_spans:
        a,b = span['start'],span['end']; source = span['source']; section = span['section']
        if type(a) is not int or type(b) is not int or type(span['bytes']) is not int or not CODE_END <= a < b <= ROM_SIZE or span['bytes'] != b-a:
            raise ValueError('Invalid initialized ROM data extent')
        if not isinstance(section,str) or (section not in ('.rodata','.data') and not section.startswith(('.rodata.','.data.'))):
            raise ValueError('Only initialized non-text sections earn data evidence')
        if not safe_path(source) or not source.startswith('src/') or not source.endswith('.c'):
            raise ValueError('Verified local data requires a repository C owner')
        if source not in inputs or not hash_value(span.get('sha256')) or not hash_value(span.get('object_sha256')):
            issues.append('Local data evidence incomplete')
        data_ranges.append((a,b))
    from data_inventory import union_bytes
    data_bytes = union_bytes(data_ranges)
    verified = not issues
    credited = sum(s['bytes'] for s in checked) if verified else 0
    checked = checked if verified else []
    named = [s for s in checked if not re.match(r'^(?:sub_|func_|FUN_|nullsub_|_?0?8[0-9a-fA-F]{6})', s['name'])]
    return {'schema_version': 1, 'game': 'Kirby & The Amazing Mirror', 'region': 'EU', 'game_code': 'B8KP',
            'expected_sha1': SHA1, 'rom_match_verified': verified,
            'verification_scope': 'Owned local full-ROM rebuild receipt; CI validates current source evidence and does not obtain the ROM.',
            'code_end_offset': CODE_END, 'code_bytes': CODE_END-188, 'excluded_header_bytes': 188,
            'credited_c_bytes': credited, 'c_percent': round(100*credited/(CODE_END-188), 5),
            'pending_code_bytes': CODE_END-188-credited, 'c_spans': checked,
            'verified_c_function_spans': len(checked), 'existing_names_in_c_spans': len(named), 'total_functions': None,
            'languages': ['English','French','German','Spanish','Italian'], 'preferred_language': 'Spanish (original selectable option)',
            'preserved_asset_region_bytes': ROM_SIZE-CODE_END, 'data_identification_percent': None,
            'source_backed_data_bytes':data_bytes if verified else 0,
            'source_data_scope':'Relocated local C data and included assets; not semantic format-identification credit.',
            'source_data_spans':data_spans if verified else [],
            'verification_issues': sorted(set(issues)), 'stale_inputs': stale,
            'source_inputs_sha256': inputs, 'source_hash_modes': modes,
            'compiler': compiler, 'compiler_binary_sha256': binaries, 'compiler_recipe': recipe,
            'source_manifest_sha256': receipt.get('source_manifest_sha256')}


def cells(report):
    result = []; cursor = 0
    boundaries = [{'start':4,'end':192,'excluded':True}] + [dict(s, excluded=False) for s in report['c_spans']]
    for span in sorted(boundaries, key=lambda s:s['start']):
        if cursor < span['start']:
            result.append({'name':'Uncredited code region','bytes':span['start']-cursor,'start':cursor,'c':False})
        if not span['excluded']:
            result.append({'name':span['name'],'source':span['source'],'bytes':span['bytes'],'start':span['start'],'c':True})
        cursor = span['end']
    if cursor < CODE_END:
        result.append({'name':'Uncredited code region','bytes':CODE_END-cursor,'start':cursor,'c':False})
    return result


def treemap(report, names=False):
    title = 'AmazingMirrorDecomp | Europe B8KP | '+('mapped function names' if names else 'verified compiled C')
    lines = [f"{report['credited_c_bytes']:,} / {report['code_bytes']:,} C bytes ({report['c_percent']:.3f}%) | ROM rebuild: "+('verified locally' if report['rom_match_verified'] else 'unverified'),
             f"Mapped C function spans: {report['verified_c_function_spans']:,}; existing names: {report['existing_names_in_c_spans']:,}. Full function total unknown."]
    inventory=report.get('function_inventory',{})
    if inventory.get('available'):
        lines[1]=f"Main-source functions: {inventory['all']['total']:,} | Game: {inventory['game']['total']:,} | SDK: {inventory['sdk']['total']:,} | Startup: {inventory['startup']['total']:,}"
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="680" viewBox="0 0 1000 680" role="img" aria-labelledby="title desc" font-family="Segoe UI,Helvetica,Arial,sans-serif"><title id="title">{escape(title)}</title><desc id="desc">European code byte spans. Pending raw code earns no C or function-name credit.</desc><rect width="1000" height="680" fill="{render.BG}"/>',f'<text x="14" y="27" fill="{render.FG}" font-size="17">{escape(title)}</text>']
    parts += [f'<text x="14" y="{49+20*i}" fill="{render.FG}" font-size="12">{escape(line)}</text>' for i,line in enumerate(lines)]
    for cell,x,y,w,h in render.squarify([(c['bytes'],c) for c in cells(report)], 8, 84, 984, 506):
        known = cell['c'] and not re.match(r'^(?:sub_|func_|FUN_|nullsub_)', cell['name'])
        color = render.GREEN if (known if names else cell['c']) else render.GREY
        tooltip = f"{cell.get('source','')} :: {cell['name']} | 0x{0x08000000+cell['start']:08X} | {cell['bytes']} bytes"
        parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{max(0,w-.5):.2f}" height="{max(0,h-.5):.2f}" fill="{color}"><title>{escape(tooltip)}</title></rect>')
    language_note = 'Original multilingual bytes preserved, including Spanish.' if report['rom_match_verified'] else 'Current receipt unverified; multilingual byte preservation not established.'
    footers = ['Green: existing names in verified C spans' if names else 'Green: verified compiled C | Grey: uncredited code-region bytes', 'Header: 188 bytes excluded. EU and USA percentages are separate.', language_note+' CI does not rebuild the owned ROM.']
    parts += [f'<text x="14" y="{615+i*23}" fill="{render.FG}" font-size="12">{escape(line)}</text>' for i,line in enumerate(footers)]
    return '\n'.join(parts+['</svg>'])


def markdown(report):
    language_note = 'All original multilingual bytes, including Spanish, are preserved by a verified full-ROM rebuild.' if report['rom_match_verified'] else 'Current source evidence does not establish a verified multilingual ROM rebuild.'
    from function_inventory import markdown as function_markdown
    return '\n'.join(['# AmazingMirrorDecomp Europe (B8KP)', '',
        f"Verified C: **{report['c_percent']:.3f}%** ({report['credited_c_bytes']:,} / {report['code_bytes']:,} executable bytes).", '',
        'ROM rebuild: **'+('verified locally against the owned European ROM' if report['rom_match_verified'] else 'unverified; no C credit')+'**.',
        f'Expected SHA1: `{SHA1}`.', '',
        f"Mapped C function spans: {report['verified_c_function_spans']:,}; existing names: {report['existing_names_in_c_spans']:,}. The total European function count is unknown; raw gaps are pending code.", '',
        language_note+' Language-specific gameplay testing is separate.', '',
        'Cartridge header: 188 excluded bytes. Data-format recovery is not measured. USA source metrics are a separate reference.', '',
        f"Verified source-backed local data: {report['source_backed_data_bytes']:,} unique bytes. C initializers and included assets remain distinct from audited semantic formats.", '',
        report['verification_scope'], '', function_markdown(report.get('function_inventory',{})), '', *report['verification_issues'], '']).rstrip()+'\n'


def write(report, out):
    out.mkdir(parents=True, exist_ok=True)
    color = render.GREEN if report['rom_match_verified'] else render.GREY
    language_note = 'Original English, French, German, Spanish and Italian bytes preserved by verified rebuild.' if report['rom_match_verified'] else 'Current receipt unverified; multilingual byte preservation not established.'
    data = f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="185" role="img" aria-label="European multilingual data; identification unmeasured"><rect width="1000" height="185" fill="{render.BG}"/><g fill="{render.FG}" font-family="Segoe UI,Helvetica,Arial,sans-serif"><text x="16" y="30" font-size="18">Europe B8KP | multilingual data</text><text x="16" y="64">Asset region: {report["preserved_asset_region_bytes"]:,} bytes. Format-identification progress: not measured.</text><text x="16" y="96">Verified local source-backed data: {report["source_backed_data_bytes"]:,} unique bytes (C initializers / included assets).</text><text x="16" y="128">{language_note}</text><text x="16" y="160">Source-backed bytes and preservation do not automatically identify semantic formats.</text></g></svg>'
    public_report=dict(report)
    if 'function_inventory' in public_report:
        public_report['function_inventory']={k:v for k,v in report['function_inventory'].items() if k!='functions'}
        if 'additional_inventory' in public_report['function_inventory']:
            public_report['function_inventory']['additional_inventory']={k:v for k,v in report['function_inventory']['additional_inventory'].items() if k!='functions'}
    outputs = {'progress.json':json.dumps(public_report,indent=2)+'\n', 'progress.md':markdown(report),
               'treemap.svg':treemap(report), 'names_treemap.svg':treemap(report,True), 'data.svg':data,
               'badge_decompiled.svg':render.badge_svg('EU verified C',f"{report['c_percent']:.3f}%",color),
               'badge_rom.svg':render.badge_svg('EU ROM','verified locally' if report['rom_match_verified'] else 'unverified',color),
               'badge_names.svg':render.badge_svg('EU mapped C names',str(report['existing_names_in_c_spans']),color),
               'badge_data.svg':render.badge_svg('EU source-backed data',f"{report['source_backed_data_bytes']:,} bytes" if report['rom_match_verified'] else 'unverified',color)}
    from function_inventory import svg as function_svg, treemap as function_treemap
    inventory=report.get('function_inventory',{'available':False})
    outputs.update({'functions.json':json.dumps(inventory,indent=2)+'\n',
                    'functions.svg':function_svg(inventory),'functions_treemap.svg':function_treemap(inventory)})
    if inventory.get('available'):
        outputs['badge_functions.svg']=render.badge_svg('catalogued functions',f"{inventory.get('known_source_function_instances',inventory['all']['total']):,}",render.GREEN)
        outputs['badge_names.svg']=render.badge_svg('existing main-source names',f"{inventory['all']['existing_names']:,}/{inventory['all']['total']:,}",render.GREEN)
    else:
        outputs['badge_functions.svg']=render.badge_svg('main-source functions','unavailable',render.GREY)
    for name,text in outputs.items():
        (out/name).write_text(text,encoding='utf-8',newline='\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--receipt',type=Path,default=ROOT/'config/regions/eu_verified.json')
    p.add_argument('--out',type=Path,default=ROOT/'docs/progress')
    p.add_argument('--record',type=Path,help='Record a compact successful owner-local verification receipt')
    args=p.parse_args()
    receipt=json.loads(args.receipt.read_text()) if args.receipt.is_file() else {}
    result=assess(receipt,ROOT)
    from function_inventory import load as function_inventory
    result['function_inventory']=function_inventory(ROOT,result)
    result['catalogued_function_instances']=result['function_inventory'].get('known_source_function_instances')
    result['main_source_functions']=result['function_inventory'].get('all',{}).get('total')
    if args.record:
        if not result['rom_match_verified']:
            raise ValueError('Cannot record an unverified receipt')
        fields = {'schema_version','analysis_only','rom_match_verified','full_rom_byte_compare','expected_sha1','rebuilt_sha1','eu_sha1','rom_size','code_end','credited_c_bytes','c_spans','inputs_sha256','source_hash_modes','compiler','compiler_binary_sha256','compiler_recipe','source_manifest_sha256','matcher_sha256','builder_sha256'}
        compact = {key:receipt[key] for key in sorted(fields)}
        compact['source_data_spans'] = source_data_spans(receipt)
        compact['c_spans'] = sorted(compact['c_spans'],key=lambda s:(s['start'],s['source']))
        args.record.parent.mkdir(parents=True,exist_ok=True)
        args.record.write_text(json.dumps(compact,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    write(result,args.out)
    print(json.dumps({k:result[k] for k in ('rom_match_verified','credited_c_bytes','c_percent','verification_issues')},indent=2))


if __name__ == '__main__':
    main()
