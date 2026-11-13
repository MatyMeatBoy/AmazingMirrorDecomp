"""Compile readable research alternatives without linking or awarding ROM credit."""
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
from metadata_build import COMPILER_COMMIT, function_kinds, read_elf

CFLAGS='-mthumb-interwork -Wimplicit -Wparentheses -Werror -O2 -fhex-asm -f2003-patch -ffix-debug-line -g'


def compile_source(root,source,nonmatching=False):
    root=Path(root);exe='.exe' if os.name=='nt' else ''
    gcc='C:/msys64/ucrt64/bin/gcc.exe' if os.name=='nt' else 'gcc'
    assembler='C:/msys64/ucrt64/bin/arm-none-eabi-as.exe' if os.name=='nt' else 'arm-none-eabi-as'
    env=os.environ.copy()
    if os.name=='nt':env['PATH']='C:/msys64/ucrt64/bin;C:/msys64/usr/bin;'+env['PATH']
    def run(args,data=None):
        result=subprocess.run([str(a) for a in args],input=data,cwd=root,env=env,capture_output=True)
        if result.returncode:raise ValueError('Draft compilation failed: '+result.stderr.decode(errors='replace'))
        return result.stdout
    flags=['-E','-iquote','include','-Wno-trigraphs','-DMODERN=0','-I','tools/agbcc/include','-I','tools/agbcc','-nostdinc','-DREVISION=0','-DENGLISH','-DREGION_EU']
    if nonmatching:flags.append('-DNONMATCHING')
    text=run([gcc,*flags,source])
    text=run([root/('tools/preproc/preproc'+exe),'-i',source],text)
    kinds=function_kinds(text.decode(errors='replace'))
    with tempfile.TemporaryDirectory(prefix='kirby-readable-draft-') as directory:
        directory=Path(directory);preprocessed=directory/'draft.i';obj=directory/'draft.o'
        preprocessed.write_bytes(text)
        asm=run([root/('tools/agbcc/bin/agbcc'+exe),*shlex.split(CFLAGS),'-o','-',preprocessed])
        run([assembler,'-mcpu=arm7tdmi','--defsym','REVISION=0','--defsym','ENGLISH=1','-o',obj,'-'],asm+b'\n.text\n.align 2,0\n')
        data=obj.read_bytes();sections=read_elf(data)
    names={s['name'] for section in sections for s in section['symbols'] if kinds.get(s['name'])=='c'}
    return {'source':source,'nonmatching':nonmatching,'compiled':True,'assembled':True,
            'compiler_flags':CFLAGS,'object_sha256':hashlib.sha256(data).hexdigest(),
            'c_functions':sorted(names),'text_bytes':sum(s['size'] for s in sections if s['name']=='.text')}


def recover(root):
    """Only current, compile-checked standalone drafts become yellow candidates."""
    root=Path(root);drafts=[];issues=[]
    for sidecar in sorted((root/'docs/research/drafts').glob('*.evidence.json')):
        try:
            evidence=json.loads(sidecar.read_text())
            if evidence['compiler']['commit']!=COMPILER_COMMIT or evidence['profile']['compiler_flags']!=CFLAGS:
                raise ValueError('Draft compiler profile changed')
            paths={evidence['source']:evidence['source_sha256'],**evidence['dependent_headers_sha256']}
            reference=evidence['eu_reference'];paths[reference['source_asm']]=reference['source_asm_sha256']
            for name,wanted in paths.items():
                path=(root/name).resolve()
                if not path.is_relative_to(root.resolve()) or hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()!=wanted:
                    raise ValueError('Draft dependency changed: '+name)
            proof=compile_source(root,evidence['source'])
            if evidence['symbol'] not in proof['c_functions']:raise ValueError('Draft function absent from compiled object')
            drafts.append({'symbol':evidence['symbol'],'owner':reference['source_asm'],
                           'source':evidence['source'],'evidence':sidecar.relative_to(root).as_posix(),
                           'compilation':proof})
        except (OSError,ValueError,KeyError,subprocess.SubprocessError) as exc:
            issues.append(sidecar.name+': '+str(exc))
    return drafts,issues
