#!/usr/bin/env python3
"""Strict relocation-based EU module candidates. Analysis never grants C credit."""
import argparse
import hashlib
import json
import pathlib
import re
import struct
from fnmatch import fnmatchcase

EU_SHA1 = '6f478a455383a2a12378f292581dfd7300300700'
BASE = 0x08000000
CODE_END = 0x15C714


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Elf:
    """Minimal ELF32 little-endian ARM REL reader; no external dependencies."""
    def __init__(self, path):
        self.raw = pathlib.Path(path).read_bytes()
        b = self.raw
        if b[:6] != b'\x7fELF\x01\x01' or struct.unpack_from('<H', b, 18)[0] != 40:
            raise ValueError('expected ELF32 little-endian ARM')
        off = struct.unpack_from('<I', b, 32)[0]
        ent, num, names = struct.unpack_from('<HHH', b, 46)
        self.sections = [struct.unpack_from('<10I', b, off+i*ent) for i in range(num)]
        strings = self.data(self.sections[names])
        self.names = [self.string(strings, s[0]) for s in self.sections]
        self.text_index = self.names.index('.text')
        self.text = self.data(self.sections[self.text_index])
        sym = self.sections[self.names.index('.symtab')]
        strings = self.data(self.sections[sym[6]])
        self.symbols = []
        for off in range(sym[4], sym[4]+sym[5], sym[9]):
            n, value, size, info, other, section = struct.unpack_from('<IIIBBH', b, off)
            self.symbols.append(dict(name=self.string(strings, n), value=value,
                                     size=size, info=info, section=section))
        self.relocs = []
        for section in self.sections:
            if section[1] == 4 and section[7] == self.text_index:
                raise ValueError('RELA unsupported')
            if section[1] != 9 or section[7] != self.text_index:
                continue
            for off in range(section[4], section[4]+section[5], section[9]):
                site, info = struct.unpack_from('<II', b, off)
                self.relocs.append(dict(offset=site, type=info & 255,
                                        symbol=self.symbols[info >> 8]))

    def data(self, section):
        return self.raw[section[4]:section[4]+section[5]]

    @staticmethod
    def string(strings, off):
        return strings[off:strings.index(b'\0', off)].decode()


def thumb_displacement(data, offset=0):
    hi, lo = struct.unpack_from('<HH', data, offset)
    if hi & 0xF800 != 0xF000 or lo & 0xF800 != 0xF800:
        raise ValueError('relocation site is not ARMv4T Thumb BL')
    value = ((hi & 0x7FF) << 12) | ((lo & 0x7FF) << 1)
    return value - (1 << 23) if value & (1 << 22) else value


def thumb_target(data, offset, address):
    return address + 4 + thumb_displacement(data, offset)


def relocation_mask(text, relocs):
    mask = bytearray(b'\xff' * len(text))
    claimed=set()
    for r in relocs:
        off, kind = r['offset'], r['type']
        if off < 0 or off + 4 > len(text):
            raise ValueError('relocation outside text')
        if kind == 40:  # R_ARM_V4BX is a marker; instruction remains fixed.
            continue
        if kind not in (2, 10):
            raise ValueError('unsupported relocation type %s' % kind)
        sites=set(range(off,off+4))
        if sites&claimed:
            raise ValueError('overlapping relocations')
        claimed.update(sites)
        if kind==10 and off%2:
            raise ValueError('unaligned Thumb BL relocation')
        if kind == 10 and thumb_displacement(text, off) != -4:
            raise ValueError('nonstandard Thumb BL object addend')
        mask[off:off+4] = b'\0' * 4
    return mask


def unique_sites(text, mask, rom, end):
    runs = list(re.finditer(b'\xff+', mask))
    run = max(runs, key=lambda m: m.end()-m.start(), default=None)
    if run is None or run.end()-run.start() < 6 or sum(bool(b) for b in mask) < 16:
        return []
    a, b = run.span()
    fixed = [i for i, m in enumerate(mask) if m]
    sites = []
    pos = rom.find(text[a:b], 0, end)
    while pos >= 0:
        start = pos-a
        if start >= 0 and start % 4 == 0 and start+len(text) <= end:
            if all(rom[start+i] == text[i] for i in fixed):
                sites.append(BASE+start)
        pos = rom.find(text[a:b], pos+1, end)
    return sites


def choose_site(text,mask,rom,end,hint=None):
    sites=unique_sites(text,mask,rom,end)
    if len(sites)==1:
        return sites[0]
    if hint is None:
        return None
    start=(hint&~1)-BASE
    if start<0xC0 or start%2 or start+len(text)>end:
        return None
    if all(not mask[i] or rom[start+i]==byte for i,byte in enumerate(text)):
        return BASE+start
    return None


def bind_relocations(elf, rom, start):
    bindings, evidence = {}, []
    for r in elf.relocs:
        off, kind, symbol = r['offset'], r['type'], r['symbol']
        if kind == 40:
            continue
        actual = rom[start-BASE+off:start-BASE+off+4]
        if kind == 2:
            addend = struct.unpack_from('<I', elf.text, off)[0]
            value = (struct.unpack('<I', actual)[0]-addend) & 0xFFFFFFFF
        elif kind == 10:
            addend = thumb_displacement(elf.text, off)
            if addend != -4:
                raise ValueError('nonstandard Thumb BL object addend')
            value = thumb_target(actual, 0, start+off) | 1
        else:
            raise ValueError('unsupported relocation')
        name = symbol['name']
        if symbol['section'] == 0:
            if not name:
                raise ValueError('unnamed undefined symbol')
            if name in bindings and bindings[name] != value:
                raise ValueError('conflicting external binding: '+name)
            bindings[name] = value
        else:
            if symbol['section'] == elf.text_index:
                expected = start + symbol['value']
            elif symbol['section'] == 0xFFF1:
                expected = symbol['value']
            else:
                raise ValueError('internal relocation outside .text')
            if kind == 10:
                expected |= 1
            if value != expected:
                raise ValueError('internal symbol relocation differs: '+name)
        evidence.append(dict(offset=off, type=kind, symbol=name, addend=addend,
                             inferred_value=value, external=symbol['section'] == 0))
    return bindings, evidence


def section_relocations(elf, index):
    result = []
    for section in elf.sections:
        if section[1] == 4 and section[7] == index:
            raise ValueError('RELA unsupported')
        if section[1] != 9 or section[7] != index:
            continue
        if section[9] != 8 or section[5] % 8:
            raise ValueError('invalid REL table')
        for off in range(section[4], section[4]+section[5], 8):
            site, info = struct.unpack_from('<II', elf.raw, off)
            result.append(dict(offset=site, type=info & 255, symbol=elf.symbols[info >> 8]))
    return result


def validate_nobits(elf,index,address):
    section=elf.sections[index]
    size=section[5];alignment=section[8] or 1
    if alignment&(alignment-1) or address%alignment:
        raise ValueError('misaligned NOBITS mapping')
    if not any(lo<=address and address+size<=hi for lo,hi in ((0x02000000,0x02040000),(0x03000000,0x03008000))):
        raise ValueError('NOBITS extent outside GBA RAM')
    for symbol in elf.symbols:
        if symbol['section']==index and symbol['info']&15==1 and symbol['value']+symbol['size']>size:
            raise ValueError('NOBITS object outside section')
    return dict(name=elf.names[index],address=address,object_offset=0,size=size,kind='ram_noload')


def noload_inputs(linker,object_name):
    """Only explicit source-object selectors inside a NOLOAD RAM output qualify."""
    linker=re.sub(r'/\*.*?\*/','',linker,flags=re.S)
    result={}
    for block in re.finditer(r'\b\w+\s*\(NOLOAD\)\s*:\s*(?:ALIGN\([^)]*\)\s*)?\{(.*?)\}\s*>\s*(iwram|ewram)\b',linker,re.S):
        for obj,selectors in re.findall(r'(?<![\w:*])([\w/.-]+\.o)\(([^)]+)\)',block[1]):
            if obj==object_name:
                for selector in selectors.split():
                    if selector in result and result[selector]!=block[2]:raise ValueError('Conflicting NOLOAD ownership')
                    result[selector]=block[2]
    return result


def validate_noload(elf,index,address,region):
    section=elf.sections[index]
    if region not in ('iwram','ewram') or section[1] not in (1,8) or section[2]&3!=3:
        raise ValueError('NOLOAD input must be allocated writable data')
    if section[1]==1 and (any(elf.data(section)) or section_relocations(elf,index)):
        raise ValueError('NOLOAD PROGBITS requires zero initializer and no relocations')
    result=validate_nobits(elf,index,address)
    lo,hi={'iwram':(0x03000000,0x03008000),'ewram':(0x02000000,0x02040000)}[region]
    if not lo<=address or address+section[5]>hi:raise ValueError('NOLOAD input outside declared RAM region')
    result['linker_region']=region
    return result


def local_object_extent(elf, index, symbol, addend):
    """Resolve one real ELF object; never infer an extent from the next symbol."""
    point = symbol['value'] + addend
    if symbol.get('info', 0) & 15 == 1 and symbol.get('size', 0):
        if not symbol['value'] <= point < symbol['value'] + symbol['size']:
            raise ValueError('local object reference is outside its declared extent')
    extents = {(s['value'], s['value'] + s['size']) for s in elf.symbols
               if s['section'] == index and s.get('info', 0) & 15 == 1 and s.get('size', 0) > 0}
    candidates = [(lo, hi) for lo, hi in extents if lo <= point < hi]
    if len(candidates) != 1:
        raise ValueError('local data reference has no exact ELF object extent')
    lo, hi = candidates[0]
    if lo < 0 or hi > elf.sections[index][5]:
        raise ValueError('local object outside section')
    if any(a < hi and lo < b for a, b in extents if (a, b) != (lo, hi)):
        raise ValueError('overlapping local ELF objects')
    return lo, hi


def prove_module(elf, rom, start, text_range=None, function_anchors=None,noload_sections=None):
    """Prove complete referenced objects with explicit RAM output ownership."""
    bases = {elf.text_index: start}
    initial = (elf.text_index, *(text_range or (0, len(elf.text))))
    locations = {initial: start + initial[1]}
    pending = [initial]
    processed = set()
    verified, bindings, evidence = {}, {}, []

    def enqueue(scope, address):
        if scope in locations and locations[scope] != address:
            raise ValueError('conflicting local object mapping')
        for other, mapped in locations.items():
            if scope[0] == other[0] and scope != other and scope[0] != elf.text_index:
                if address < mapped + other[2] - other[1] and mapped < address + scope[2] - scope[1]:
                    raise ValueError('overlapping mapped local objects')
        locations[scope] = address
        pending.append(scope)

    while pending:
        scope = pending.pop()
        if scope in processed:
            continue
        processed.add(scope)
        index, segment_offset, stop = scope
        section = elf.sections[index]
        address = locations[scope]
        region=next((region for pattern,region in (noload_sections or {}).items() if fnmatchcase(elf.names[index],pattern)),None)
        if region:
            verified[scope]=dict(validate_noload(elf,index,bases[index],region),section_index=index)
            continue
        if section[1]==8:
            verified[scope]=dict(validate_nobits(elf,index,bases[index]),section_index=index)
            continue
        if section[1] != 1 or not section[2] & 2:
            raise ValueError('referenced local section is not allocated file data')
        data = elf.data(section)[segment_offset:stop]
        offset = address - BASE
        if segment_offset < 0 or stop > section[5] or stop <= segment_offset:
            raise ValueError('invalid complete local extent')
        if offset < 0 or offset + len(data) > len(rom):
            raise ValueError('mapped local object outside ROM')
        all_relocs = section_relocations(elf, index)
        for r in all_relocs:
            if r['offset'] < stop and r['offset'] + 4 > segment_offset:
                if r['offset'] < segment_offset or r['offset'] + 4 > stop:
                    raise ValueError('relocation straddles complete object boundary')
        relocs = [dict(r, offset=r['offset'] - segment_offset) for r in all_relocs
                  if segment_offset <= r['offset'] < stop]
        mask = relocation_mask(data, relocs)
        if any(rom[offset + i] != byte for i, byte in enumerate(data) if mask[i]):
            raise ValueError('mapped section fixed bytes differ: ' + elf.names[index])
        for reloc in relocs:
            off, kind, symbol = reloc['offset'], reloc['type'], reloc['symbol']
            if kind == 40:
                continue
            actual = rom[offset + off:offset + off + 4]
            if kind == 2:
                addend = struct.unpack_from('<I', data, off)[0]
                value = (struct.unpack('<I', actual)[0] - addend) & 0xFFFFFFFF
            else:
                addend = thumb_displacement(data, off)
                value = thumb_target(actual, 0, address + off) | 1
            target, name = symbol['section'], symbol['name']
            anchored = False
            if target == 0:
                if not name or (name in bindings and bindings[name] != value):
                    raise ValueError('conflicting or unnamed external binding')
                bindings[name] = value
            elif target == 0xFFF1:
                if value != symbol['value']:
                    raise ValueError('absolute symbol differs')
            elif target == elf.text_index and function_anchors and name in function_anchors:
                if symbol.get('info', 0) & 15 == 2 and symbol['value'] & 1 and not value & 1:
                    raise ValueError('invalid local Thumb function pointer')
                if (value & ~1) not in function_anchors[name]:
                    raise ValueError('local function target has no fixed-byte anchor')
                anchored = True
            elif target == elf.text_index and symbol.get('info', 0) & 15 == 2 and 0 < symbol.get('size', 0) < 16 and symbol['value'] & 1:
                if not value & 1 or (kind == 2 and addend != 0):
                    raise ValueError('invalid local Thumb function pointer')
                lo = symbol['value'] & ~1
                hi = lo + symbol['size']
                if hi > elf.sections[target][5] or value < BASE + 0xC0 or (value & ~1) + symbol['size'] > BASE + CODE_END:
                    raise ValueError('local Thumb function outside code extent')
                if function_anchors and name in function_anchors and (value & ~1) not in function_anchors[name]:
                    raise ValueError('local function target has no fixed-byte anchor')
                if text_range is None:
                    if value != start + symbol['value']:
                        raise ValueError('local function differs from complete text mapping')
                else:
                    enqueue((target, lo, hi), value & ~1)
                    anchored = True
            else:
                if target >= len(elf.sections):
                    raise ValueError('unsupported special symbol section')
                if target == elf.text_index or elf.sections[target][1] == 8 or any(fnmatchcase(elf.names[target],pattern) for pattern in (noload_sections or {})):
                    inferred = value - symbol['value']
                    if target in bases and bases[target] != inferred:
                        raise ValueError('conflicting local section binding')
                    bases[target] = inferred
                    if target != elf.text_index:
                        enqueue((target, 0, elf.sections[target][5]), inferred)
                else:
                    if kind != 2:
                        raise ValueError('non-ABS32 local data reference')
                    point = symbol['value'] + addend
                    # Anonymous aggregate literals may have no STT_OBJECT records.
                    # Preserve the older, stronger complete-section proof only for
                    # an already complete text module; partial callers never guess.
                    has_objects = any(s['section'] == target and s.get('info', 0) & 15 == 1 and s.get('size', 0) > 0 for s in elf.symbols)
                    if text_range is None and not has_objects and 0 <= point < elf.sections[target][5]:
                        lo, hi = 0, elf.sections[target][5]
                    else:
                        lo, hi = local_object_extent(elf, target, symbol, addend)
                    object_address = struct.unpack('<I', actual)[0] - (point - lo)
                    enqueue((target, lo, hi), object_address)
            evidence.append(dict(section=elf.names[index], offset=off,
                                 object_offset=segment_offset, type=kind, symbol=name,
                                 addend=addend, inferred_value=value, external=target == 0,
                                 anchored_function=anchored))
        verified[scope] = dict(name=elf.names[index], section_index=index, address=address,
                               object_offset=segment_offset, size=len(data),
                               sha256=hashlib.sha256(rom[offset:offset+len(data)]).hexdigest())
    return bindings, evidence, list(verified.values()), bases


def validate_rom(rom):
    if len(rom) != 0x1000000 or rom[0xAC:0xB0] != b'B8KP' or hashlib.sha1(rom).hexdigest() != EU_SHA1:
        raise ValueError('expected owned 16 MiB B8KP EU ROM with supported SHA1')


def analyze(root, rom_path):
    from metadata_build import validate_manifest
    root = pathlib.Path(root).resolve()
    directory = root/'build/metadata'
    manifest_path = directory/'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    validate_manifest(manifest,root)
    if manifest.get('region')!='eu':raise ValueError('European reconstruction requires EU-profile metadata')
    rom = pathlib.Path(rom_path).read_bytes()
    validate_rom(rom)
    linker=(root/'linker.ld').read_text()
    noload={module['source']:noload_inputs(linker,str(pathlib.PurePosixPath(module['source']).with_suffix('.o'))) for module in manifest['sources']}
    report = dict(schema_version=1, analysis_only=True, rom_match_verified=False, eu_sha1=EU_SHA1, code_end=CODE_END, source_manifest_sha256=digest(manifest_path), candidates=[], rejected=[])
    for module in manifest['sources']:
        if not module['source'].endswith('.c'):
            continue
        path = directory/module['object']
        try:
            elf = Elf(path)
            if not elf.text:
                continue
            sites = unique_sites(elf.text,relocation_mask(elf.text,elf.relocs),rom,CODE_END)
            if len(sites) != 1:
                raise ValueError('absent or ambiguous full module match: '+str(len(sites)))
            start = sites[0]
            bindings,relocs,sections,bases = prove_module(elf,rom,start,noload_sections=noload[module['source']])
            symbols = [dict(s,eu_address=start+s['offset']) for s in module['symbols'] if s['section']=='.text']
            report['candidates'].append(dict(source=module['source'],object=module['object'],object_sha256=module['sha256'],eu_start=start,size=len(elf.text),bindings=bindings,relocations=relocs,sections=sections,section_bases={str(k):v for k,v in bases.items()},symbols=symbols))
        except ValueError as error:
            report['rejected'].append(dict(source=module['source'],reason=str(error)))
    all_bindings = {}
    for candidate in report['candidates']:
        for name,value in candidate['bindings'].items():
            if name in all_bindings and all_bindings[name] != value:
                raise ValueError('cross-module external binding conflict: '+name)
            all_bindings[name] = value
    covered={c['source'] for c in report['candidates']}
    occupied=[(c['eu_start'],c['eu_start']+c['size']) for c in report['candidates']]
    for module in manifest['sources']:
        if module['source'] in covered or not module['source'].endswith('.c'):
            continue
        elf=Elf(directory/module['object'])
        functions={s['name']:s for s in elf.symbols if s['section']==elf.text_index and s['info']&15==2}
        local_context={}
        anchors={}
        for symbol in module['symbols']:
            if symbol['section']!='.text' or symbol['kind']=='unknown' or symbol['size']<16:
                continue
            a=symbol['offset'];b=a+symbol['size']
            rs=[dict(r,offset=r['offset']-a) for r in elf.relocs if a<=r['offset']<b]
            try:
                positions=unique_sites(elf.text[a:b],relocation_mask(elf.text[a:b],rs),rom,CODE_END)
                if positions:
                    for name in [symbol['name']]+symbol.get('aliases',[]):
                        anchors[name]=positions
            except ValueError:
                pass
        while True:
            before = len(report['candidates'])
            for symbol in module['symbols']:
                if symbol['section']!='.text' or symbol['kind']!='c' or symbol['size']<2:
                    continue
                a=symbol['offset'];b=a+symbol['size']
                try:
                    relocs=[dict(r,offset=r['offset']-a) for r in elf.relocs if a<=r['offset']<b]
                    name=symbol['name']
                    definition=functions.get(name,{})
                    hint=all_bindings.get(name) if definition.get('info',0)>>4 in (1,2) else local_context.get(name)
                    site=choose_site(elf.text[a:b],relocation_mask(elf.text[a:b],relocs),rom,CODE_END,hint)
                    if site is None:
                        continue
                    if any(site<end and site+symbol['size']>start for start,end in occupied):
                        continue
                    bindings,evidence,sections,bases=prove_module(elf,rom,site-a,(a,b),anchors,noload_sections=noload[module['source']])
                    if any(name in all_bindings and all_bindings[name]!=value for name,value in bindings.items()):
                        continue
                    for relocation in evidence:
                        if relocation.get('anchored_function'):
                            previous=local_context.get(relocation['symbol'])
                            if previous is not None and previous!=relocation['inferred_value']:
                                raise ValueError('conflicting local callback context')
                            local_context[relocation['symbol']]=relocation['inferred_value']
                    all_bindings.update(bindings)
                    occupied.append((site,site+symbol['size']))
                    span=dict(symbol,offset=0,eu_address=site)
                    report['candidates'].append(dict(source=module['source'],object=module['object'],object_sha256=module['sha256'],eu_start=site,size=symbol['size'],object_text_offset=a,unit='function',bindings=bindings,relocations=evidence,sections=sections,section_bases={str(k):v for k,v in bases.items()},symbols=[span]))
                except ValueError:
                    continue
            if len(report['candidates']) == before:
                break
    report['external_bindings'] = all_bindings
    definitions={}
    local_definitions={}
    ram_bases={}
    for candidate in report['candidates']:
        elf=Elf(directory/candidate['object'])
        ram_indices={elf.names.index(s['name']) for s in candidate['sections'] if s.get('kind')=='ram_noload'}
        for index,base in candidate['section_bases'].items():
            index=int(index)
            if elf.sections[index][1]==8 or index in ram_indices:
                key=(candidate['object'],index)
                if key in ram_bases and ram_bases[key]!=base:
                    raise ValueError('inconsistent NOBITS mapping across units')
                ram_bases[key]=base
        a=candidate.get('object_text_offset',0)
        for symbol in elf.symbols:
            if symbol['section']<len(elf.sections) and (elf.sections[symbol['section']][1]==8 or symbol['section'] in ram_indices) and str(symbol['section']) in candidate['section_bases'] and symbol['name'] and symbol['info']&15==1:
                address=candidate['section_bases'][str(symbol['section'])]+symbol['value']
                local_definitions[(candidate['object'],symbol['name'])]=address
                if symbol['info']>>4 in (1,2):
                    if symbol['name'] in definitions and definitions[symbol['name']]!=address:
                        raise ValueError('conflicting global RAM definition')
                    definitions[symbol['name']]=address
            if symbol['section']==elf.text_index and symbol['name'] and a<=(symbol['value']&~1)<a+candidate['size']:
                address=candidate['eu_start']+symbol['value']-a
                name=symbol['name']
                local_definitions[(candidate['object'],name)]=address
                if symbol['info']>>4 not in (1,2):
                    continue
                if name in definitions and definitions[name]!=address:
                    raise ValueError('conflicting global definition: '+name)
                definitions[name]=address
    mapped_objects = {}
    for candidate in report['candidates']:
        elf = Elf(directory/candidate['object'])
        for mapped in candidate['sections']:
            index = mapped.get('section_index', elf.names.index(mapped['name']))
            if index == elf.text_index or mapped.get('kind') == 'ram_noload':
                continue
            lo = mapped['object_offset']; hi = lo + mapped['size']
            key = (candidate['object'], index, lo, hi)
            address = mapped['address']
            if key in mapped_objects and mapped_objects[key] != address:
                raise ValueError('inconsistent local object mapping across units')
            for other, previous in mapped_objects.items():
                if other[:2] == key[:2] and other != key and address < previous + other[3] - other[2] and previous < address + hi - lo:
                    raise ValueError('overlapping local object mappings across units')
            mapped_objects[key] = address
            for symbol in elf.symbols:
                if symbol['section'] != index or symbol['info'] & 15 != 1 or not symbol['size'] or not lo <= symbol['value'] or symbol['value'] + symbol['size'] > hi:
                    continue
                name = symbol['name']; value = address + symbol['value'] - lo
                local_definitions[(candidate['object'], name)] = value
                if symbol['info'] >> 4 in (1, 2):
                    if name in definitions and definitions[name] != value:
                        raise ValueError('conflicting global data definition')
                    definitions[name] = value
    for name,address in definitions.items():
        if name in all_bindings and all_bindings[name]!=address:
            raise ValueError('external binding differs from verified global definition: '+name)
    for candidate in report['candidates']:
        for relocation in candidate['relocations']:
            key=(candidate['object'],relocation['symbol'])
            if not relocation['external'] and key in local_definitions and relocation['inferred_value']!=local_definitions[key]:
                raise ValueError('local binding differs from verified definition: '+relocation['symbol'])
    report['verified_global_definitions']=definitions
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom',type=pathlib.Path,default=pathlib.Path('baserom_eu.gba'))
    parser.add_argument('--output',type=pathlib.Path,default=pathlib.Path('build/eu/candidates.json'))
    args = parser.parse_args()
    result = analyze(pathlib.Path(__file__).resolve().parents[2],args.rom)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(len(result['candidates']),'whole modules;',sum(c['size'] for c in result['candidates']),'text bytes')
