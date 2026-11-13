"""Source-current ELF inventory of selected archives and auxiliary programs."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from metadata_build import COMPILER_COMMIT
from report import named


def expected_inputs(root,receipt):
    root=Path(root);libc=root/'tools/agbcc/libc';libgcc=root/'tools/agbcc/libgcc'
    paths={root/'linker.ld',libc/'Makefile',libgcc/'Makefile',libc/'math/fdlibm.h',libgcc/'longlong.h',
           root/'tools/progress/compile_extra_functions.py'}
    for base in (libc/'include',root/'tools/agbcc/ginclude'):
        paths.update(p for p in base.rglob('*') if p.is_file())
    paths.update(root/member['source'] for member in receipt['main_selected_library_members'])
    for auxiliary in receipt['auxiliaries']:
        target=root/auxiliary['target'];linker=target/'linker.ld'
        paths.update((linker,target/'Makefile'))
        expected=[(target/Path(n).with_suffix('.s')).relative_to(root).as_posix() for n in re.findall(r'(?<![:\w])([\w/]+\.o)\(\.text\)',linker.read_text())]
        if expected!=[o['source'] for o in auxiliary['objects']]:raise ValueError('Auxiliary executable object inventory changed')
        refs=[a+':'+b for a,b in re.findall(r'\*(lib\w+\.a):(\S+\.o)\(\.text\)',linker.read_text())]
        if refs!=[m['member'] for m in auxiliary['selected_archive_members']]:raise ValueError('Auxiliary archive selection changed')
        for folder in ('asm','constants','include'):
            paths.update(p for p in (target/folder).rglob('*') if p.is_file() and p.suffix not in {'.o','.gba','.elf','.map','.d'})
    return {p.relative_to(root).as_posix() for p in paths}


def summarize(receipt):
    if receipt.get('schema_version')!=1 or receipt.get('rom_verified') is not False or receipt.get('errors')!=[] or receipt.get('compiler_commit')!=COMPILER_COMMIT:
        raise ValueError('Invalid additional source inventory evidence')
    members={};functions=[];groups=[]
    def add(records,program,source,kind):
        keys=set()
        for f in records:
            key=(f['section'],f['offset'])
            if key in keys:raise ValueError('Duplicate function extent in archive inventory')
            keys.add(key)
            functions.append({'program':program,'source':source,'name':f['name'],
                              'aliases':f.get('aliases',[]),'kind':kind,
                              'existing_name':any(named(n) for n in [f['name'],*f.get('aliases',[])])})
    for member in receipt['main_selected_library_members']:
        if member['member'] in members or member['function_count']!=len(member['functions']):
            raise ValueError('Invalid selected archive member count')
        if member['domain'] not in ('library_c','library_assembly'):raise ValueError('Unknown library source kind')
        members[member['member']]=member
        add(member['functions'],'main archives',member['member'],member['domain'])
    def group(label,start):
        records=functions[start:]
        names=sum(f['existing_name'] for f in records)
        return {'program':label,'functions':len(records),
                'c_available':sum(f['kind']=='library_c' for f in records),
                'assembly':sum(f['kind']!='library_c' for f in records),
                'existing_names':names,'unnamed':len(records)-names}
    groups.append(group('Principal: libc/libgcc',0))
    targets=set()
    for auxiliary in receipt['auxiliaries']:
        target=auxiliary['target'];start=len(functions)
        if target in targets:raise ValueError('Duplicate auxiliary target')
        targets.add(target)
        for obj in auxiliary['objects']:
            if obj['function_count']!=len(obj['functions']):raise ValueError('Invalid auxiliary function count')
            add(obj['functions'],target,obj['source'],'auxiliary_assembly')
            for entry in obj.get('manual_entrypoints',[]):
                if entry.get('elf_type')!='NOTYPE' or entry['name']!='__start' or not entry.get('evidence'):
                    raise ValueError('Unsupported manual entrypoint')
                add([entry],target,obj['source'],'explicit_entrypoint')
        for reference in auxiliary['selected_archive_members']:
            member=members[reference['member']]
            if reference['function_count']!=member['function_count'] or reference['object_sha256']!=member['object_sha256']:
                raise ValueError('Auxiliary archive reference disagrees with compiled member')
            add(member['functions'],target,member['member'],member['domain'])
        groups.append(group(target,start))
    total=group('Total adicional',0)
    return {'available':True,'scope':'Compiled source function instances in separate programs; no European matching credit.',
            'groups':groups,'totals':total,'functions':functions}


def load(root):
    root=Path(root)
    try:
        receipt=json.loads((root/'config/progress/extra_functions.json').read_text())
        inputs=receipt['inputs_sha256'];modes=receipt['source_hash_modes']
        if not inputs or set(inputs)!=set(modes):raise ValueError('Missing source fingerprints')
        if set(inputs)!=expected_inputs(root,receipt):raise ValueError('Incomplete additional source fingerprints')
        for name,expected in inputs.items():
            path=PurePosixPath(name)
            if path.is_absolute() or '..' in path.parts or ':' in name or '\\' in name or path.as_posix()!=name or modes[name]!='lf' or not re.fullmatch('[0-9a-f]{64}',expected):
                raise ValueError('Invalid additional input fingerprint')
            resolved=(root/name).resolve()
            if not resolved.is_relative_to(root.resolve()):raise ValueError('Input outside repository')
            if hashlib.sha256(resolved.read_bytes().replace(b'\r\n',b'\n')).hexdigest()!=expected:
                raise ValueError('Additional source inputs changed: '+name)
        # New auxiliary targets must not disappear from the complete inventory.
        actual={p.parent.relative_to(root).as_posix() for p in (root/'multi_boot').rglob('linker.ld')}
        if actual!={a['target'] for a in receipt['auxiliaries']}:raise ValueError('Auxiliary target set changed')
        selected=re.findall(r'\*(lib\w+\.a):(\S+\.o)\(\.text\)',(root/'linker.ld').read_text())
        if [a+':'+b for a,b in selected]!=[r['member'] for r in receipt['main_selected_library_members']]:raise ValueError('Selected main archive members changed')
        return summarize(receipt)
    except (OSError,ValueError,KeyError,TypeError) as exc:
        return {'available':False,'issue':'Additional compiled inventory unavailable: '+str(exc)}
