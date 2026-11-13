"""Reproduce linker-selected function inventory without linking or ROM credit.
Run: python tools/progress/compile_extra_functions.py
All ELF objects stay in a system temporary directory; output JSON has no bytes.
"""
import argparse,hashlib,json,os,re,shutil,subprocess,tempfile,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/progress'))
from eu_match import Elf
TEMP=Path(tempfile.mkdtemp(prefix='kirby-extra-functions-'))
ENV=os.environ.copy()
if os.name=='nt':ENV['PATH']='C:/msys64/ucrt64/bin;C:/msys64/usr/bin;'+ENV['PATH']
CPP=Path('C:/msys64/ucrt64/bin/gcc.exe') if os.name=='nt' else Path(shutil.which('gcc') or '/missing-gcc')
AS=Path('C:/msys64/ucrt64/bin/arm-none-eabi-as.exe') if os.name=='nt' else Path(shutil.which('arm-none-eabi-as') or '/missing-as')
CC=ROOT/('tools/agbcc/bin/old_agbcc'+('.exe' if os.name=='nt' else ''))
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out',type=Path,default=ROOT/'build/research/extra_function_inventory_portable.json')
args=parser.parse_args()
LIBC=ROOT/'tools/agbcc/libc';LIBGCC=ROOT/'tools/agbcc/libgcc'
def sha(data):return hashlib.sha256(data).hexdigest()
def lf(path):return sha(path.read_bytes().replace(b'\r\n',b'\n'))
def run(args,data=None,cwd=ROOT):
 p=subprocess.run([str(a) for a in args],input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=cwd,env=ENV)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace'))
 return p.stdout
def portable(arg):return str(arg).replace(str(ROOT),'<root>').replace('\\','/')
def rows(path):
 e=Elf(path);groups={}
 for s in e.symbols:
  if s['info']&15==2 and s['section']<len(e.sections) and e.sections[s['section']][2]&4:groups.setdefault((s['section'],s['value']&~1),[]).append(s)
 out=[]
 for (section,offset),symbols in sorted(groups.items()):
  symbols=sorted(symbols,key=lambda x:x['name']);out.append(dict(section=e.names[section],offset=offset,name=symbols[0]['name'],aliases=[s['name'] for s in symbols[1:]],elf_sizes=sorted({s['size'] for s in symbols}),bindings=sorted({s['info']>>4 for s in symbols})))
 return out,e
inputs={ROOT/'linker.ld',LIBC/'Makefile',LIBGCC/'Makefile',Path(__file__).resolve()}
inputs.update(p for base in (LIBC/'include',ROOT/'tools/agbcc/ginclude') for p in base.rglob('*') if p.is_file())
inputs.update((LIBC/'math/fdlibm.h',LIBGCC/'longlong.h'))
objects={};library=[];errors=[]
libc_cpp=['-I',ROOT/'tools/agbcc/ginclude','-I',LIBC/'include','-nostdinc','-undef','-DABORT_PROVIDED','-DHAVE_GETTIMEOFDAY','-D__thumb__','-DARM_RDI_MONITOR','-D__GNUC__','-DINTERNAL_NEWLIB','-D__USER_LABEL_PREFIX__=']
for archive,member in re.findall(r'\*(lib\w+\.a):(\S+\.o)\(\.text\)',(ROOT/'linker.ld').read_text()):
 key=archive+':'+member;stem=Path(member).stem;obj=TEMP/(archive+'-'+member)
 try:
  if archive=='libc.a':
   source=next(LIBC.rglob(stem+'.c'));cpp=['-E',*libc_cpp,source];flags=['-O2','-fno-builtin'];kind='library_c';asm=run([CC,*flags,'-o','-','-'],run([CPP,*cpp]))
  elif stem in {'_call_via_rX','_divsi3','_dvmd_tls','_modsi3','_udivsi3','_umodsi3'}:
   source=LIBGCC/'lib1thumb.asm';cpp=['-E','-undef','-nostdinc','-DL'+stem,'-x','assembler-with-cpp',source];flags=[];kind='library_assembly';asm=run([CPP,*cpp])
  else:
   source=LIBGCC/('fp-bit-base.c' if stem in {'fp-bit','dp-bit'} else 'libgcc2.c');defines=['-DFLOAT_BIT_ORDER_MISMATCH'] if stem in {'fp-bit','dp-bit'} else ['-DL'+stem]
   if stem=='fp-bit':defines+=['-DFLOAT']
   cpp=['-E','-undef','-I',ROOT/'tools/agbcc/ginclude','-nostdinc',*defines,source];flags=['-O2'];kind='library_c';asm=run([CC,*flags,'-o','-','-'],run([CPP,*cpp]))
  inputs.add(source);run([AS,'-mcpu=arm7tdmi','-o',obj,'-'],asm+b'\n.text\n.align 2,0\n');functions,e=rows(obj)
  record=dict(member=key,domain=kind,source=source.relative_to(ROOT).as_posix(),source_sha256=lf(source),source_hash_mode='lf',cpp_flags=[portable(a) for a in cpp[:-1]],compiler_flags=flags,assembler_flags=['-mcpu=arm7tdmi'],object_sha256=sha(obj.read_bytes()),text_size=len(e.text),function_count=len(functions),functions=functions)
  objects[key]=record;library.append(record)
 except Exception as error:errors.append(dict(member=key,error=str(error)))
aux=[]
for linker in sorted((ROOT/'multi_boot').rglob('linker.ld')):
 target=linker.parent;text=linker.read_text();records=[];inputs.update((linker,target/'Makefile'))
 for folder in ('asm','constants','include'):
  inputs.update(p for p in (target/folder).rglob('*') if p.is_file() and p.suffix not in {'.o','.gba','.elf','.map','.d'})
 for name in re.findall(r'(?<![:\w])([\w/]+\.o)\(\.text\)',text):
  source=target/Path(name).with_suffix('.s');obj=TEMP/(target.relative_to(ROOT).as_posix().replace('/','-')+'-'+name.replace('/','-'))
  try:
   run([AS,'-mcpu=arm7tdmi','--defsym','REVISION=0','--defsym','ENGLISH=1','-o',obj,source],cwd=target);functions,e=rows(obj);manual=[]
   if name=='asm/loader.o' and not any(f['name']=='__start' or '__start' in f['aliases'] for f in functions):
    found=[s for s in e.symbols if s['name']=='__start' and s['section']==e.text_index]
    if len(found)==1:manual=[dict(name='__start',section='.text',offset=found[0]['value']&~1,elf_type='NOTYPE',elf_size=found[0]['size'],section_size=len(e.text),function_extent=None,evidence='linker ENTRY(__start), explicit global assembly entry; internal branch labels are not additional functions')]
   domain='startup_assembly' if name in {'asm/crt0.o','asm/loader.o'} else ('sdk_wrapper_assembly' if name=='asm/libagbsyscall.o' else 'auxiliary_assembly')
   records.append(dict(source=source.relative_to(ROOT).as_posix(),domain=domain,source_sha256=lf(source),source_hash_mode='lf',object_sha256=sha(obj.read_bytes()),assembler_flags=['-mcpu=arm7tdmi','--defsym','REVISION=0','--defsym','ENGLISH=1'],function_count=len(functions),functions=functions,manual_entrypoints=manual,text_size=len(e.text)))
  except Exception as error:errors.append(dict(target=target.relative_to(ROOT).as_posix(),source=name,error=str(error)))
 refs=[dict(member=a+':'+b,domain=objects[a+':'+b]['domain'],function_count=objects[a+':'+b]['function_count'],object_sha256=objects[a+':'+b]['object_sha256']) for a,b in re.findall(r'\*(lib\w+\.a):(\S+\.o)\(\.text\)',text) if a+':'+b in objects]
 aux.append(dict(target=target.relative_to(ROOT).as_posix(),rom_verified=False,objects=records,selected_archive_members=refs,assembly_function_count=sum(r['function_count'] for r in records),manual_entrypoint_count=sum(len(r['manual_entrypoints']) for r in records),library_c_instances=sum(r['function_count'] for r in refs if r['domain']=='library_c'),library_assembly_instances=sum(r['function_count'] for r in refs if r['domain']=='library_assembly')))
compiler_commit=run(['git','rev-parse','HEAD'],cwd=ROOT/'tools/agbcc').decode().strip()
if compiler_commit!='59b966ed1b8f371856dcf99f1546c2fe89c678ca':raise ValueError('unexpected compiler source revision')
source_hashes={p.relative_to(ROOT).as_posix():lf(p) for p in sorted(inputs) if p.is_file()}
result=dict(schema_version=1,scope='linker-selected main archives and auxiliary executable objects; unlinked source inventory, not total EU functions',rom_verified=False,compiler_repository='https://github.com/jiangzhengwenjz/agbcc',compiler_commit=compiler_commit,tool_sha256={'old_agbcc':sha(CC.read_bytes()),'cpp':sha(CPP.read_bytes()),'as':sha(AS.read_bytes())},inputs_sha256=source_hashes,source_hash_modes={name:'lf' for name in source_hashes},main_selected_library_members=library,auxiliaries=aux,errors=errors)
out=args.out;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
print(out);print('main',sum(r['function_count'] for r in library));print('aux',[(r['target'],r['assembly_function_count'],r['manual_entrypoint_count'],r['library_c_instances'],r['library_assembly_instances']) for r in aux]);print('errors',errors)
if errors:sys.exit(1)
