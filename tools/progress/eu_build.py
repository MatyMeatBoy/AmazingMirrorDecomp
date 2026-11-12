"""Reproduce owned EU ROM using verified compiled sections and explicit raw gaps.

The small ARM REL relocator supports only ABS32, ARMv4T Thumb BL and V4BX
markers. It never copies relocation-site bytes from the ROM into C sections.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess

from eu_match import BASE,CODE_END,EU_SHA1,Elf,analyze,digest,section_relocations,thumb_displacement,validate_rom

TEXT_SUFFIXES={'.c','.cpp','.h','.s','.inc','.mk','.ld','.py','.txt','.sha1','.json','.pal'}


def source_digest(data,mode):
    if mode=='lf':
        data=data.replace(b'\r\n',b'\n')
    elif mode!='raw':
        raise ValueError('unknown hash mode')
    return hashlib.sha256(data).hexdigest()


def provenance(root):
    tracked=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=root).decode().split('\0')
    prefixes=('src/','include/','asm/','constants/','graphics/','tools/preproc/','tools/gbagfx/')
    paths={name for name in tracked if name and (name.startswith(prefixes) or name in {'Makefile','GNUmakefile','make_tools.mk','graphics_file_rules.mk','audio_rules.mk'})}
    paths.update('tools/progress/'+name+'.py' for name in ('eu_match','eu_build','metadata_build'))
    hashes,modes={},{}
    for name in sorted(paths):
        path=root/name
        if not path.is_file():
            raise ValueError('missing source provenance file: '+name)
        mode='lf' if path.suffix.lower() in TEXT_SUFFIXES or path.name in {'Makefile','GNUmakefile','.gitignore','LICENSE'} else 'raw'
        hashes[name]=source_digest(path.read_bytes(),mode)
        modes[name]=mode
    return hashes,modes


def relocate(data,relocs,address,bases,bindings,symbol_addresses=None):
    output=bytearray(data)
    for reloc in relocs:
        off,kind,symbol=reloc['offset'],reloc['type'],reloc['symbol']
        if kind==40:
            continue
        if off<0 or off+4>len(data):
            raise ValueError('relocation outside section')
        section=symbol['section']
        if symbol_addresses and section not in (0,0xFFF1) and symbol['name'] in symbol_addresses:
            value=symbol_addresses[symbol['name']]
        elif section==0:
            value=bindings[symbol['name']]
        elif section==0xFFF1:
            value=symbol['value']
        else:
            value=bases[section]+symbol['value']
        if kind==2:
            addend=struct.unpack_from('<I',data,off)[0]
            struct.pack_into('<I',output,off,(value+addend)&0xFFFFFFFF)
        elif kind==10:
            addend=thumb_displacement(data,off)
            displacement=(value&~1)+addend-(address+off)
            if displacement%2 or not -(1<<22)<=displacement<(1<<22):
                raise ValueError('Thumb BL target out of range or unaligned')
            struct.pack_into('<HH',output,off,0xF000|((displacement>>12)&0x7FF),0xF800|((displacement>>1)&0x7FF))
        else:
            raise ValueError('unsupported relocation')
    return bytes(output)


def check_layout(modules):
    end=0xC0
    for module in sorted(modules,key=lambda m:m['eu_start']):
        start=module['eu_start']-BASE
        if start<end or module['size']<=0 or start+module['size']>CODE_END:
            raise ValueError('module outside code or overlapping')
        end=start+module['size']


def guard_output(path,original,base):
    if not path.resolve().is_relative_to(base.resolve()):
        raise ValueError('output redirects outside generated EU directory')
    if path.exists() and path.samefile(original):
        raise ValueError('output aliases original ROM')


def build(root,rom_path):
    root=Path(root).resolve()
    rom_path=Path(rom_path).resolve()
    out=root/'build/eu'
    if out.resolve()!=root/'build/eu':
        raise ValueError('EU output directory redirects outside build/eu')
    if rom_path.is_relative_to(out.resolve()):
        raise ValueError('original ROM must be outside generated EU directory')
    original=rom_path.read_bytes()
    validate_rom(original)
    initial_hashes,initial_modes=provenance(root)
    out.mkdir(parents=True,exist_ok=True)
    for name in ('receipt.json','katam_eu.gba'):
        guard_output(out/name,rom_path,out)
    (out/'receipt.json').unlink(missing_ok=True)
    receipt=analyze(root,rom_path)
    modules=receipt['candidates']
    check_layout(modules)
    rebuilt=bytearray(original)
    c_spans=[]
    for module in modules:
        elf=Elf(root/'build/metadata'/module['object'])
        bases={int(k):v for k,v in module['section_bases'].items()}
        symbol_addresses={r['symbol']:r['inferred_value'] for r in module['relocations'] if r.get('anchored_function')}
        a=module.get('object_text_offset',0);b=a+module['size']
        relocs=[dict(r,offset=r['offset']-a) for r in elf.relocs if a<=r['offset']<b]
        emitted=relocate(elf.text[a:b],relocs,module['eu_start'],bases,module['bindings'],symbol_addresses)
        offset=module['eu_start']-BASE
        if emitted!=original[offset:offset+len(emitted)]:
            raise ValueError('compiled relocated text differs: '+module['source'])
        rebuilt[offset:offset+len(emitted)]=emitted
        module['emitted_text_sha256']=hashlib.sha256(emitted).hexdigest()
        for section in module['sections']:
            if section.get('kind')=='ram_noload':
                continue
            index=elf.names.index(section['name'])
            section_start=section.get('object_offset',0);section_end=section_start+section['size']
            relocs=[dict(r,offset=r['offset']-section_start) for r in section_relocations(elf,index) if section_start<=r['offset']<section_end]
            data=relocate(elf.data(elf.sections[index])[section_start:section_end],relocs,section['address'],bases,module['bindings'],symbol_addresses)
            start=section['address']-BASE
            if data!=original[start:start+len(data)]:
                raise ValueError('compiled relocated local section differs')
        for symbol in module['symbols']:
            if symbol['kind']=='c' and symbol['size']:
                start=symbol['eu_address']-BASE
                span_hash=hashlib.sha256(emitted[symbol['offset']:symbol['offset']+symbol['size']]).hexdigest()
                c_spans.append(dict(source=module['source'],name=symbol['name'],offset=start,start=start,end=start+symbol['size'],size=symbol['size'],bytes=symbol['size'],sha256=span_hash,linked_span_sha256=span_hash,object_sha256=module['object_sha256']))
    pending=[]
    cursor=0
    for span in sorted(c_spans,key=lambda s:s['offset']):
        if span['offset']<cursor:
            raise ValueError('overlapping C credits')
        if cursor<span['offset']:
            pending.append(dict(offset=cursor,size=span['offset']-cursor,kind='owned_rom_fallback'))
        cursor=span['offset']+span['size']
    if cursor<len(original):
        pending.append(dict(offset=cursor,size=len(original)-cursor,kind='owned_rom_fallback'))
    if bytes(rebuilt)!=original or hashlib.sha1(rebuilt).hexdigest()!=EU_SHA1:
        raise ValueError('full EU ROM comparison failed')
    receipt.update(analysis_only=False,rom_match_verified=True,full_rom_byte_compare=True,expected_sha1=EU_SHA1,rebuilt_sha1=hashlib.sha1(rebuilt).hexdigest(),rom_size=len(original),credited_c_bytes=sum(s['size'] for s in c_spans),code_bytes=CODE_END-188,c_spans=c_spans,pending_spans=pending,modules=modules,matcher_sha256=digest(root/'tools/progress/eu_match.py'),builder_sha256=digest(Path(__file__)),method='compiled ELF ARM REL relocation; complete local-section proof; owned ROM fallback outside credited spans')
    receipt['inputs_sha256'],receipt['source_hash_modes']=provenance(root)
    if receipt['inputs_sha256']!=initial_hashes or receipt['source_hash_modes']!=initial_modes:
        raise ValueError('source inputs changed during EU build')
    from metadata_build import validate_manifest
    metadata=json.loads((root/'build/metadata/manifest.json').read_text())
    validate_manifest(metadata,root)
    if digest(root/'build/metadata/manifest.json')!=receipt['source_manifest_sha256']:
        raise ValueError('metadata manifest changed during EU build')
    receipt['compiler']=metadata['compiler']
    receipt['compiler_recipe']=metadata['recipe']
    receipt['compiler_binary_sha256']={path.name:digest(path) for path in (root/'tools/agbcc/bin').glob('*') if path.is_file()}
    del receipt['candidates']
    out.mkdir(parents=True,exist_ok=True)
    (out/'receipt.json').unlink(missing_ok=True)
    (out/'katam_eu.gba').write_bytes(rebuilt)
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(len(modules),'verified modules;',receipt['credited_c_bytes'],'C bytes;',100*receipt['credited_c_bytes']/receipt['code_bytes'],'%; full16MiB compare+SHA1 OK')
    return receipt


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom',type=Path,default=Path('baserom_eu.gba'))
    args=parser.parse_args()
    build(Path(__file__).resolve().parents[2],args.rom)
