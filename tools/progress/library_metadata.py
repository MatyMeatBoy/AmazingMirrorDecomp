"""Compile only linker-selected runtime archive members; no ROM is read.

EU uses the existing double-word-order configuration of fp-bit-base.c.
The original archive Makefiles are left untouched. Object sections, aliases,
preprocessed inputs and complete CPP header dependencies are recorded.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess

from metadata_build import COMPILER_COMMIT, function_kinds, partition_symbols, read_elf


def digest(data):
    return hashlib.sha256(data).hexdigest()


def text_digest(data):
    return digest(data.replace(b'\r\n',b'\n'))


def selected_members(root):
    text=(Path(root)/'linker.ld').read_text()
    text=re.sub(r'/\*.*?\*/|//[^\n]*','',text,flags=re.S)
    result=[archive+':'+member for archive,member in re.findall(r'\*(lib\w+\.a):(\w[\w.-]*\.o)\(\.text\)',text)]
    if not result or len(result)!=len(set(result)):
        raise ValueError('empty or duplicate linker-selected library members')
    return result


def library_spec(root,member):
    root=Path(root)
    compiler=root/'tools/agbcc'
    archive,name=member.split(':')
    stem=Path(name).stem
    if archive=='libc.a':
        sources=list((compiler/'libc').rglob(stem+'.c'))
        if len(sources)!=1:
            raise ValueError('library member has no unique C source: '+member)
        source=sources[0]
        cpp=['-I',str(compiler/'ginclude'),'-I',str(compiler/'libc/include'),'-nostdinc','-undef','-DABORT_PROVIDED','-DHAVE_GETTIMEOFDAY','-D__thumb__','-DARM_RDI_MONITOR','-D__GNUC__','-DINTERNAL_NEWLIB','-D__USER_LABEL_PREFIX__=']
        flags=['-O2','-fno-builtin']
        kind='c'
    elif archive=='libgcc.a' and stem in {'_call_via_rX','_divsi3','_dvmd_tls','_modsi3','_udivsi3','_umodsi3'}:
        source=compiler/'libgcc/lib1thumb.asm'
        cpp=['-undef','-nostdinc','-DL'+stem,'-x','assembler-with-cpp']
        flags=[]
        kind='asm'
    elif archive=='libgcc.a' and stem in {'dp-bit','fp-bit','_lshrdi3','_muldi3','_negdi2'}:
        source=compiler/('libgcc/fp-bit-base.c' if stem in {'dp-bit','fp-bit'} else 'libgcc/libgcc2.c')
        cpp=['-undef','-I',str(compiler/'ginclude'),'-nostdinc']
        if stem=='dp-bit':
            cpp+=['-DFLOAT_BIT_ORDER_MISMATCH','-DFLOAT_WORD_ORDER_MISMATCH']
        elif stem=='fp-bit':
            cpp+=['-DFLOAT','-DFLOAT_BIT_ORDER_MISMATCH']
        else:
            cpp+=['-DL'+stem]
        flags=['-O2']
        kind='c'
    else:
        raise ValueError('unsupported selected archive member: '+member)
    return dict(source=source,cpp_flags=cpp,compiler_flags=flags,assembler_flags=['-mcpu=arm7tdmi'],kind=kind)


def classify_functions(preprocessed,kind):
    if kind=='asm':
        return {}
    kinds=function_kinds(preprocessed)
    cleaned=re.sub(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',' ',preprocessed,flags=re.S)
    if re.search(r'\b(?:asm|__asm__|__asm)\s*\(',cleaned) and any(value=='c' for value in kinds.values()):
        raise ValueError('active library inline assembly requires explicit classification')
    return kinds


def header_dependencies(trace,root):
    root=Path(root).resolve()
    result=set()
    for line in trace.decode(errors='replace').splitlines():
        match=re.match(r'^\.+\s+(.+)$',line)
        if not match:
            continue
        path=Path(match[1]).resolve()
        if not path.is_relative_to(root):
            raise ValueError('preprocessor dependency outside repository: '+str(path))
        if not path.is_file():
            raise ValueError('missing preprocessor dependency')
        result.add(path)
    return result


def tools(root):
    suffix='.exe' if os.name=='nt' else ''
    result={'compiler':Path(root)/('tools/agbcc/bin/old_agbcc'+suffix)}
    for key,name in [('cpp','gcc'),('assembler','arm-none-eabi-as')]:
        candidate=shutil.which(name)
        if candidate is None and os.name=='nt':
            candidate=str(Path('C:/msys64/ucrt64/bin')/(name+suffix))
        result[key]=Path(candidate or '/missing-tool')
    if any(not path.is_file() for path in result.values()):
        raise ValueError('missing library metadata toolchain')
    return result


def run(command,root,data=None):
    env=os.environ.copy()
    if os.name=='nt':
        env['PATH']='C:/msys64/ucrt64/bin;C:/msys64/usr/bin;'+env.get('PATH','')
    result=subprocess.run([str(arg) for arg in command],input=data,cwd=root,env=env,capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.decode(errors='replace'))
    return result


def compiler_identity(root,executables):
    commit=run(['git','rev-parse','HEAD'],Path(root)/'tools/agbcc').stdout.decode().strip()
    if commit!=COMPILER_COMMIT:
        raise ValueError('library compiler source revision differs from pinned commit')
    return dict(commit=commit,binaries={name:digest(path.read_bytes()) for name,path in executables.items()})


def preprocess(root,spec,executables):
    result=run([executables['cpp'],'-E','-H',*spec['cpp_flags'],spec['source']],root)
    deps=header_dependencies(result.stderr,root)|{spec['source']}
    return result.stdout,deps


def portable_flags(root,flags):
    return [str(arg).replace(str(root),'<root>').replace('\\','/') for arg in flags]


def object_metadata(path,preprocessed,spec,source,member):
    raw=path.read_bytes()
    sections=read_elf(raw)
    kinds=classify_functions(preprocessed.decode(errors='replace'),spec['kind'])
    symbols=[]
    for section in sections:
        if spec['kind']=='asm':
            kinds.update({symbol['name']:'asm' for symbol in section['symbols']})
        spans=partition_symbols(section['size'],section.pop('symbols'),kinds)
        symbols.extend(dict(span,section=section['name'],source=source,library_member=member) for span in spans)
    if any(symbol['kind']=='unknown' and symbol['name']!='<unattributed>' for symbol in symbols):
        raise ValueError('unclassified library function')
    header=struct.unpack_from('<16sHHIIIIIHHHHHH',raw)
    table=[struct.unpack_from('<10I',raw,header[6]+i*40) for i in range(header[12])]
    names=table[header[13]]
    strings=raw[names[4]:names[4]+names[5]]
    all_sections=[dict(name=strings[s[0]:].split(b'\0')[0].decode(),type=s[1],flags=s[2],size=s[5],alignment=s[8]) for s in table]
    return sections,symbols,all_sections


def input_hashes(root,paths):
    return {path.relative_to(root).as_posix():text_digest(path.read_bytes()) for path in sorted(paths)}


def fixed_inputs(root):
    return {root/'linker.ld',root/'tools/agbcc/libc/Makefile',root/'tools/agbcc/libgcc/Makefile',root/'tools/progress/library_metadata.py',root/'tools/progress/metadata_build.py'}


def check_compiler_sources(root,paths):
    compiler=root/'tools/agbcc'
    relative=[path.relative_to(compiler).as_posix() for path in sorted(paths) if path.is_relative_to(compiler)]
    if not relative:
        raise ValueError('missing compiler source dependencies')
    run(['git','ls-files','--error-unmatch',*relative],compiler)
    run(['git','diff','--exit-code','--ignore-cr-at-eol','HEAD','--',*relative],compiler)


def build(root):
    root=Path(root).resolve()
    executables=tools(root)
    identity=compiler_identity(root,executables)
    directory=root/'build/metadata'
    object_dir=directory/'objects/libraries'
    if object_dir.resolve()!=object_dir:
        raise ValueError('library output directory redirects outside metadata')
    object_dir.mkdir(parents=True,exist_ok=True)
    output=directory/'library_manifest.json'
    output.unlink(missing_ok=True)
    paths=fixed_inputs(root)
    expected=input_hashes(root,paths)
    records=[]
    for member in selected_members(root):
        spec=library_spec(root,member)
        preprocessed,deps=preprocess(root,spec,executables)
        before=input_hashes(root,deps)
        repeated,repeated_deps=preprocess(root,spec,executables)
        if repeated!=preprocessed or deps!=repeated_deps or before!=input_hashes(root,deps):
            raise ValueError('library preprocessor inputs changed during compilation')
        if any(name in expected and expected[name]!=value for name,value in before.items()):
            raise ValueError('library dependencies changed during build')
        expected.update(before)
        paths.update(deps)
        archive,name=member.split(':')
        obj=object_dir/(archive.removesuffix('.a')+'__'+name)
        obj.unlink(missing_ok=True)
        pp=obj.with_suffix(obj.suffix+'.i')
        pp.unlink(missing_ok=True)
        pp.write_bytes(preprocessed)
        assembly=preprocessed if spec['kind']=='asm' else run([executables['compiler'],*spec['compiler_flags'],'-o','-','-'],root,preprocessed).stdout
        run([executables['assembler'],*spec['assembler_flags'],'-o',obj,'-'],root,assembly+b'\n.text\n.align 2,0\n')
        source=spec['source'].relative_to(root).as_posix()
        sections,symbols,all_sections=object_metadata(obj,preprocessed,spec,source,member)
        records.append(dict(library_member=member,source=source,object=obj.relative_to(directory).as_posix(),sha256=digest(obj.read_bytes()),preprocessed_sha256=digest(preprocessed),sections=sections,symbols=symbols,all_sections=all_sections,cpp_flags=portable_flags(root,spec['cpp_flags']),compiler_flags=spec['compiler_flags'],assembler_flags=spec['assembler_flags'],source_kind=spec['kind']))
    if expected!=input_hashes(root,paths) or identity!=compiler_identity(root,executables):
        raise ValueError('library source/toolchain changed during build')
    check_compiler_sources(root,paths)
    manifest=dict(schema_version=1,scope='main_linker_libraries',rom_verified=False,compiler=identity,inputs_sha256=expected,source_hash_modes={name:'lf' for name in expected},sources=records)
    validate(manifest,root)
    output.write_text(json.dumps(manifest,indent=2)+'\n')
    print(len(records),'library objects;',sum(s['size'] for r in records for s in r['symbols'] if s['kind']=='c'),'C bytes; ROM not read')
    return manifest


def validate(manifest,root):
    root=Path(root).resolve()
    if manifest.get('schema_version')!=1 or manifest.get('scope')!='main_linker_libraries' or manifest.get('rom_verified') is not False:
        raise ValueError('unsupported library metadata manifest')
    executables=tools(root)
    if manifest.get('compiler')!=compiler_identity(root,executables):
        raise ValueError('stale library compiler/toolchain')
    members=selected_members(root)
    if [record['library_member'] for record in manifest.get('sources',[])]!=members:
        raise ValueError('incomplete or duplicate selected library inventory')
    paths=fixed_inputs(root)
    directory=root/'build/metadata'
    for record in manifest['sources']:
        member=record['library_member']
        spec=library_spec(root,member)
        source=spec['source'].relative_to(root).as_posix()
        if record['source']!=source or record['source_kind']!=spec['kind'] or record['cpp_flags']!=portable_flags(root,spec['cpp_flags']) or record['compiler_flags']!=spec['compiler_flags'] or record['assembler_flags']!=spec['assembler_flags']:
            raise ValueError('library source or flags disagree with selected member')
        archive,name=member.split(':')
        expected='objects/libraries/'+archive.removesuffix('.a')+'__'+name
        lexical=directory/record['object']
        obj=lexical.resolve()
        if record['object']!=expected or obj!=lexical or not obj.is_relative_to((directory/'objects/libraries').resolve()) or not obj.is_file() or digest(obj.read_bytes())!=record['sha256']:
            raise ValueError('missing, redirected or stale library object')
        pp=obj.with_suffix(obj.suffix+'.i')
        if pp.resolve()!=pp or not pp.is_file() or digest(pp.read_bytes())!=record['preprocessed_sha256']:
            raise ValueError('missing or stale preprocessed library input')
        current,deps=preprocess(root,spec,executables)
        if current!=pp.read_bytes():
            raise ValueError('library preprocessed input differs from current sources')
        paths.update(deps)
        sections,symbols,all_sections=object_metadata(obj,current,spec,source,member)
        if record['sections']!=sections or record['symbols']!=symbols or record['all_sections']!=all_sections:
            raise ValueError('library ELF symbols/sections disagree with manifest')
    hashes=input_hashes(root,paths)
    if manifest.get('inputs_sha256')!=hashes or manifest.get('source_hash_modes')!={name:'lf' for name in hashes}:
        raise ValueError('stale or incomplete library source dependencies')
    check_compiler_sources(root,paths)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--validate',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[2]
    if args.validate:
        validate(json.loads((root/'build/metadata/library_manifest.json').read_text()),root)
    else:
        build(root)
