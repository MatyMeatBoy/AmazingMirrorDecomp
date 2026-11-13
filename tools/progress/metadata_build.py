"""Compile isolated main-target objects for progress; never link or generate a ROM.

Run on MSYS2: python tools/progress/metadata_build.py [--jobs 4].
The manifest measures unlinked executable input sections, including their padding.
It is not a matching check or a whole-ROM completion measurement.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import struct
import subprocess

COMPILER_COMMIT = '59b966ed1b8f371856dcf99f1546c2fe89c678ca'


def preprocessor_flags(region):
    if region not in ('eu','us'):raise ValueError('unsupported metadata region')
    common='-E -iquote include -Wno-trigraphs -DMODERN=0 -I tools/agbcc/include -I tools/agbcc -nostdinc -iquote include -DREVISION=0 -DENGLISH'
    return common+(' -DREGION_EU' if region=='eu' else '')


def metadata_directory(root,region):
    preprocessor_flags(region)
    return Path(root)/'build'/('metadata' if region=='eu' else 'metadata-us')


def code_sources(root):
    c = [p for p in root.glob('src/**/*.c') if '.inc.c' not in p.name and len(p.relative_to(root).parts) <= 4 and 'data' not in p.relative_to(root).parts]
    return sorted(c) + sorted(root.glob('src/**/*.s')) + sorted(root.glob('asm/*.s'))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def function_kinds(text):
    # Input is the actual default-build preprocessed C, so inactive NONMATCHING
    # branches cannot accidentally receive C credit. Only definitions count.
    text = re.sub(r'/\*.*?\*/|//[^\n]*', '', text, flags=re.S)
    # Attributes may have nested arguments and may precede or follow the
    # declarator. Remove their syntax before recognizing function definitions.
    def attribute(match):
        return ' naked ' if re.search(r'\bnaked\b', match[0]) else ' '
    text = re.sub(r'__attribute__\s*\(\((?:[^()]|\([^()]*\))*\)\)', attribute, text)
    text = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '""', text)
    result = {}
    depth, start = 0, 0
    for pos, char in enumerate(text):
        if char == '{':
            if depth == 0:
                prefix = text[start:pos]
                match = re.search(r'\b([A-Za-z_]\w*)\s*\([^{};]*\)\s*$', prefix)
                if match and match[1] not in {'if','while','switch','for'}:
                    result[match[1]] = 'asm' if 'naked' in prefix else 'c'
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                start = pos + 1
        elif char == ';' and depth == 0:
            start = pos + 1
    return result


def partition_symbols(size, symbols, kinds):
    groups = {}
    for symbol in symbols:
        offset = symbol['offset']
        if offset < 0 or offset > size or symbol['size'] < 0:
            raise ValueError('symbol outside section')
        groups.setdefault(offset, []).append(symbol)
    spans = []
    cursor = 0
    starts = sorted(groups)
    for i, start in enumerate(starts):
        group = sorted(groups[start], key=lambda x: x['name'])
        explicit = {x['size'] for x in group if x['size']}
        if len(explicit) > 1:
            raise ValueError('aliases have conflicting sizes')
        end = start + next(iter(explicit)) if explicit else (starts[i + 1] if i + 1 < len(starts) else size)
        if start < cursor or end > size or (i + 1 < len(starts) and end > starts[i + 1]):
            raise ValueError('overlapping symbol spans')
        if start > cursor:
            spans.append(dict(name='<unattributed>', offset=cursor, size=start-cursor, kind='unknown', size_basis='gap', aliases=[]))
        names = [x['name'] for x in group]
        classifications = {kinds.get(name, 'unknown') for name in names}
        spans.append(dict(name=names[0], aliases=names[1:], offset=start, size=end-start, kind=next(iter(classifications)) if len(classifications) == 1 else 'unknown', size_basis='elf' if explicit else 'next_symbol_or_section_end'))
        cursor = end
    if cursor < size:
        spans.append(dict(name='<unattributed>', offset=cursor, size=size-cursor, kind='unknown', size_basis='gap', aliases=[]))
    return spans


def read_elf(data):
    if len(data) < 52 or data[:7] != b'\x7fELF\x01\x01\x01':
        raise ValueError('expected little-endian ELF32')
    header = struct.unpack_from('<16sHHIIIIIHHHHHH', data)
    if header[1] != 1 or header[2] != 40:
        raise ValueError('expected relocatable ARM object')
    off, entsize, count, names_index = header[6], header[11], header[12], header[13]
    if entsize != 40 or off + count * entsize > len(data) or names_index >= count:
        raise ValueError('invalid section table')
    sections = [struct.unpack_from('<10I', data, off + i*40) for i in range(count)]
    def payload(section):
        start, size = section[4:6]
        if start + size > len(data):
            raise ValueError('truncated section')
        return data[start:start+size]
    def string(table, start):
        if start >= len(table):
            raise ValueError('invalid string offset')
        end = table.find(b'\0', start)
        if end < 0:
            raise ValueError('unterminated string')
        return table[start:end].decode('ascii')
    names = payload(sections[names_index])
    result = {i: dict(name=string(names, s[0]), size=s[5], symbols=[]) for i, s in enumerate(sections) if s[2] & 4 and s[5]}
    for index in result:
        payload(sections[index])
    for section in sections:
        if section[1] != 2:
            continue
        if section[9] != 16 or section[5] % 16 or section[6] >= count:
            raise ValueError('invalid symbol table')
        strings = payload(sections[section[6]])
        table = payload(section)
        for pos in range(0, len(table), 16):
            name, value, size, info, other, index = struct.unpack_from('<IIIBBH', table, pos)
            if index in result and info & 15 == 2:
                result[index]['symbols'].append(dict(name=string(strings, name), offset=value & ~1, size=size))
    return list(result.values())


def run(command, cwd):
    try:
        return subprocess.check_output(command, cwd=cwd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(error.output.decode(errors='replace')) from error


def asset_make_command(assets):
    if not assets:
        return None
    return 'make NODEP=1 SETUP_PREREQS=0 ' + ' '.join(shlex.quote(a) for a in assets)


def input_fingerprint(root,region='eu'):
    paths = list(root.glob('src/**/*')) + list(root.glob('asm/**/*')) + list(root.glob('include/**/*'))
    paths += [root/'Makefile', root/'linker.ld', root/'tools/progress/metadata_build.py']
    paths += [root/'graphics_file_rules.mk', root/'graphics.mk']
    paths += [root/'make_tools.mk', root/'audio_rules.mk']
    paths += list(root.glob('constants/**/*'))
    paths += list(root.glob('graphics/**/*'))
    paths += [p for directory in ('tools/preproc', 'tools/gbagfx') for p in (root/directory).glob('*') if p.suffix in {'.c', '.cpp', '.h'} or p.name == 'Makefile']
    paths += [root/('tools/gbagfx/gbagfx'+('.exe' if os.name == 'nt' else ''))]
    paths += list((root/'tools/agbcc/include').glob('**/*'))
    paths += list((root/'tools/agbcc/bin').glob('*'))
    paths += [root/('tools/preproc/preproc' + ('.exe' if os.name == 'nt' else ''))]
    game_inputs = preprocessor_flags(region).encode()+b'\0'+b''.join(p.relative_to(root).as_posix().encode()+b'\0'+p.read_bytes() for p in sorted(set(paths)) if p.is_file())
    for name in ('gcc', 'arm-none-eabi-as'):
        tool = Path('C:/msys64/ucrt64/bin')/(name+'.exe') if os.name == 'nt' else Path(shutil.which(name) or '/missing-tool')
        if not tool.is_file():
            raise ValueError('missing tool: '+name)
        game_inputs += name.encode()+b'\0'+tool.read_bytes()
    return digest(game_inputs)


def validate_manifest(manifest, root):
    root = Path(root)
    if manifest.get('schema_version') != 1 or manifest.get('scope') != 'main_object_text' or manifest.get('rom_verified') is not False:
        raise ValueError('unsupported metadata manifest')
    region=manifest.get('region')
    output=metadata_directory(root,region)
    if manifest.get('recipe',{}).get('preprocessor_flags')!=preprocessor_flags(region):
        raise ValueError('metadata regional preprocessing profile differs')
    if manifest.get('input_sha256') != input_fingerprint(root,region):
        raise ValueError('stale metadata inputs; rebuild metadata')
    expected = [p.relative_to(root).as_posix() for p in code_sources(root)]
    if [record['source'] for record in manifest.get('sources', [])] != expected or not expected:
        raise ValueError('metadata source inventory is incomplete')
    if manifest.get('compiler', {}).get('commit') != COMPILER_COMMIT:
        raise ValueError('metadata compiler does not match pinned upstream')
    for record in manifest.get('sources', []):
        path = (output/record['object']).resolve()
        if not path.is_relative_to((output/'objects').resolve()):
            raise ValueError('object path outside metadata directory')
        if not path.is_file() or digest(path.read_bytes()) != record['sha256']:
            raise ValueError('missing or stale metadata object')
        actual = read_elf(path.read_bytes())
        if [{k:v for k,v in s.items() if k != 'symbols'} for s in actual] != record['sections']:
            raise ValueError('metadata sections disagree with object')
        source = root/record['source']
        kinds = {}
        if source.suffix == '.c':
            preprocessed = path.with_suffix(path.suffix+'.i')
            if digest(preprocessed.read_bytes()) != record['preprocessed_sha256']:
                raise ValueError('stale preprocessed metadata')
            kinds = function_kinds(preprocessed.read_text(errors='replace'))
        derived = []
        for section in actual:
            if source.suffix == '.s':
                kinds.update({s['name']: 'asm' for s in section['symbols']})
            derived += [dict(span, section=section['name']) for span in partition_symbols(section['size'], section['symbols'], kinds)]
        if derived != record['symbols']:
            raise ValueError('symbol metadata disagrees with compiled input')
        for section in record['sections']:
            spans = sorted((s for s in record['symbols'] if s['section'] == section['name']), key=lambda s:s['offset'])
            cursor = 0
            for span in spans:
                if span['offset'] != cursor or span['size'] < 0 or span['kind'] not in {'c','asm','unknown'}:
                    raise ValueError('invalid metadata coverage')
                cursor += span['size']
            if cursor != section['size']:
                raise ValueError('incomplete metadata coverage')


def build(root, jobs, bash,region='eu'):
    output = metadata_directory(root,region)
    output.mkdir(parents=True, exist_ok=True)
    manifest = output / 'manifest.json'
    manifest.unlink(missing_ok=True)  # A failed rebuild must not leave valid-looking stale data.
    compiler = root / 'tools/agbcc'
    exe = '.exe' if os.name == 'nt' else ''
    commit = run(['git', 'rev-parse', 'HEAD'], compiler).decode().strip()
    if commit != COMPILER_COMMIT:
        raise ValueError('agbcc checkout does not match pinned upstream commit')
    sources = code_sources(root)
    # Generate only real tracked graphics sources required by code INCBINs,
    # through the repository's unchanged conversion rules. No stand-in bytes.
    assets = sorted({asset for source in sources if source.suffix == '.c' for asset in re.findall(r'INCBIN_\w+\("([^"]+)"\)', source.read_text())})
    asset_script = 'export PATH=/ucrt64/bin:/usr/bin:$PATH; set -e -o pipefail; '
    if os.name == 'nt':
        asset_script += 'cd ' + shlex.quote('/' + root.drive[0].lower() + root.as_posix()[2:]) + '; '
    command = asset_make_command(assets)
    if command:
        asset_script += 'make -C tools/gbagfx; ' + command
        run([bash, '-lc', asset_script], root)
    fingerprint = input_fingerprint(root,region)
    def compile_one(source):
        relative = source.relative_to(root).as_posix()
        obj = output / 'objects' / Path(relative).with_suffix('.o')
        obj.parent.mkdir(parents=True, exist_ok=True)
        obj.unlink(missing_ok=True)
        q = shlex.quote
        objrel = obj.relative_to(root).as_posix()
        common = '-mthumb-interwork -Wimplicit -Wparentheses -Werror -O2 -fhex-asm -f2003-patch -ffix-debug-line -g'
        if relative == 'src/task.c':
            common = common.replace('-Werror ', '')
        cc = 'old_agbcc' if relative in {'src/m4a.c', 'src/agb_sram.c'} else 'agbcc'
        if relative == 'src/agb_sram.c':
            common = common.replace('-O2', '-O1').replace(' -f2003-patch', '')
        preprocessed = objrel + '.i'
        if source.suffix == '.c':
            script = f'gcc {preprocessor_flags(region)} {q(relative)} | tools/preproc/preproc{exe} -i {q(relative)} > {q(preprocessed)}; tools/agbcc/bin/{cc}{exe} {common} -o - {q(preprocessed)} | {{ cat; printf "\\n.text\\n.align 2, 0\\n"; }} | arm-none-eabi-as -mcpu=arm7tdmi --defsym REVISION=0 --defsym ENGLISH=1 -o {q(objrel)} -'
        else:
            script = f'arm-none-eabi-as -mcpu=arm7tdmi --defsym REVISION=0 --defsym ENGLISH=1 -o {q(objrel)} {q(relative)}'
        prefix = 'export PATH=/ucrt64/bin:/usr/bin:$PATH; set -e -o pipefail; '
        if os.name == 'nt':
            prefix += 'cd ' + q('/' + root.drive[0].lower() + root.as_posix()[2:]) + '; '
        run([bash, '-lc', prefix + script], root)
        kinds = function_kinds((root/preprocessed).read_text(errors='replace')) if source.suffix == '.c' else {}
        sections = read_elf(obj.read_bytes())
        symbols = []
        for section in sections:
            if source.suffix == '.s':
                kinds.update({s['name']: 'asm' for s in section['symbols']})
            symbols += [dict(span, section=section['name']) for span in partition_symbols(section['size'], section.pop('symbols'), kinds)]
        record = dict(source=relative, object=obj.relative_to(output).as_posix(), sha256=digest(obj.read_bytes()), sections=sections, symbols=symbols)
        if source.suffix == '.c':
            record['preprocessed_sha256'] = digest((root/preprocessed).read_bytes())
        return record
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        records = list(pool.map(compile_one, sources))
    current = input_fingerprint(root,region)
    if current != fingerprint:
        raise ValueError('source inputs changed during metadata compilation')
    result = dict(schema_version=1, scope='main_object_text', region=region,rom_verified=False, baseline_commit=run(['git','rev-parse','HEAD'],root).decode().strip(), input_sha256=fingerprint, compiler=dict(commit=commit, branch='new_newlib_pret', sha256=digest((compiler/('bin/agbcc'+exe)).read_bytes())), sources=records)
    result['recipe'] = {'sha256': digest(Path(__file__).read_bytes()), 'default_cflags': '-mthumb-interwork -Wimplicit -Wparentheses -Werror -O2 -fhex-asm -f2003-patch -ffix-debug-line -g', 'exceptions': {'src/task.c': 'omit -Werror', 'src/agb_sram.c': 'old_agbcc -O1, omit -f2003-patch', 'src/m4a.c': 'old_agbcc'}, 'excluded': ['src/data/**/*.c (data-only)', 'multi_boot/**', 'linked libraries'], 'sizes': 'ELF STT_FUNC sizes; zero sizes inferred to next function or section end; gaps unattributed'}
    result['recipe'].update(region=region,preprocessor_flags=preprocessor_flags(region))
    manifest.write_text(json.dumps(result, indent=2)+'\n')
    print(f'{manifest}: {len(records)} objects, {sum(s["size"] for r in records for s in r["sections"])} executable section bytes; ROM not verified')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--bash', default='C:/msys64/usr/bin/bash.exe' if os.name == 'nt' else 'bash')
    parser.add_argument('--region',choices=('eu','us'),default='eu')
    args = parser.parse_args()
    build(Path(__file__).resolve().parents[2], args.jobs, args.bash,args.region)
