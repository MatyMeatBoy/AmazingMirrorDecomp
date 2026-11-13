#!/usr/bin/env python3
"""Compile the defined terrain draft using an isolated header/reader overlay.

Never edits core files, links a ROM, publishes bytes, or grants matching credit.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import struct
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/progress'))
from eu_match import Elf, relocation_mask, unique_sites, CODE_END

FLAGS = '-mthumb-interwork -Wimplicit -Wparentheses -Werror -O2 -fhex-asm -f2003-patch -ffix-debug-line -g'
PIN = '59b966ed1b8f371856dcf99f1546c2fe89c678ca'
SHA1 = '6f478a455383a2a12378f292581dfd7300300700'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def lf_sha(path):
    return hashlib.sha256(Path(path).read_text().encode()).hexdigest()


def overlay_patch(patch, out):
    lines = patch.splitlines(keepends=True)
    index = 0
    while index < len(lines):
        if not lines[index].startswith('--- a/'):
            index += 1
            continue
        name = lines[index][6:].strip()
        if name not in {'include/data.h', 'src/code_0800ECAC_2.c'}:
            raise ValueError('unexpected patch target')
        original = (ROOT / name).read_text().splitlines(keepends=True)
        result, cursor = [], 0
        index += 2
        while index < len(lines) and not lines[index].startswith('--- a/'):
            match = re.match(r'@@ -(\d+)(?:,\d+)? \+\d+(?:,\d+)? @@', lines[index])
            if not match:
                raise ValueError('expected patch hunk')
            start = int(match[1]) - 1
            result += original[cursor:start]
            cursor = start
            index += 1
            while index < len(lines) and not lines[index].startswith(('@@ ', '--- a/')):
                line = lines[index]
                if line[0] in ' -':
                    if cursor >= len(original) or original[cursor] != line[1:]:
                        raise ValueError('patch context changed: ' + name)
                    cursor += 1
                if line[0] in ' +':
                    result.append(line[1:])
                index += 1
        result += original[cursor:]
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(''.join(result))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bash', default='C:/msys64/usr/bin/bash.exe' if os.name == 'nt' else 'bash')
    parser.add_argument('--evidence', type=Path)
    args = parser.parse_args()
    commit = subprocess.check_output(['git', '-C', str(ROOT / 'tools/agbcc'), 'rev-parse', 'HEAD'], text=True).strip()
    if commit != PIN:
        raise ValueError('unexpected compiler commit')
    rom = (ROOT / 'baserom_eu.gba').read_bytes()
    if hashlib.sha1(rom).hexdigest() != SHA1:
        raise ValueError('wrong owned European ROM')
    parent = ROOT / 'build/research'
    parent.mkdir(parents=True, exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix='terrain-defined-', dir=parent))
    shutil.copytree(ROOT / 'include', out / 'include')
    patch = ROOT / 'docs/research/drafts/terrain_layout.patch'
    overlay_patch(patch.read_text(), out)
    exe = '.exe' if os.name == 'nt' else ''
    cwd = ROOT.as_posix()
    if os.name == 'nt':
        cwd = '/' + ROOT.drive[0].lower() + cwd[2:]
    prefix = 'export PATH=/ucrt64/bin:/usr/bin:$PATH; set -e -o pipefail; cd ' + shlex.quote(cwd) + '; '

    def compile_unit(source, stem, overlay):
        source = source.relative_to(ROOT).as_posix()
        dest = (out / stem).relative_to(ROOT).as_posix()
        includes = ('-iquote ' + shlex.quote((out / 'include').relative_to(ROOT).as_posix()) + ' ') if overlay else ''
        cpp = 'gcc -E ' + includes + '-iquote include -Wno-trigraphs -DMODERN=0 -DREGION_EU -I tools/agbcc/include -I tools/agbcc -nostdinc -DREVISION=0 -DENGLISH '
        command = cpp + shlex.quote(source) + ' | tools/preproc/preproc' + exe + ' -i ' + shlex.quote(source) + ' > ' + shlex.quote(dest + '.i')
        command += '; tools/agbcc/bin/agbcc' + exe + ' ' + FLAGS + ' -o ' + shlex.quote(dest + '.s') + ' ' + shlex.quote(dest + '.i')
        command += '; arm-none-eabi-as -mcpu=arm7tdmi --defsym REVISION=0 --defsym ENGLISH=1 -o ' + shlex.quote(dest + '.o') + ' ' + shlex.quote(dest + '.s')
        subprocess.run([args.bash, '-lc', prefix + command], cwd=ROOT, check=True)
        return out / (stem + '.o')

    layout_source = out / 'layout.c'
    layout_source.write_text('#include "code_0800ECAC.h"\n#include <stddef.h>\nconst u32 proof[] = { sizeof(struct Unk_02038590), offsetof(struct Unk_02038590, terrain), sizeof(((struct Unk_02038590 *)0)->terrain), offsetof(struct Unk_02038590, terrain.legacy.unk1C), offsetof(struct Unk_02038590, terrain.legacy.unk26), offsetof(struct Unk_02038590, terrain.legacy.unk2B), offsetof(struct Unk_02038590, unk3C), offsetof(struct Unk_02038590, unk40) };\n')
    layout_elf = Elf(compile_unit(layout_source, 'layout', True))
    layout_bytes = layout_elf.data(layout_elf.sections[layout_elf.names.index('.rodata')])
    layout_values = list(struct.unpack('<8I', layout_bytes))
    if layout_values != [0xF4, 0x1C, 0x20, 0x1C, 0x26, 0x2B, 0x3C, 0x40]:
        raise ValueError('compiled layout changed')
    draft = ROOT / 'docs/research/drafts/sub_0800F044_defined.c'
    objpath = compile_unit(draft, 'draft', True)
    before = Elf(compile_unit(ROOT / 'src/code_0800ECAC_2.c', 'readers_before', False))
    after = Elf(compile_unit(out / 'src/code_0800ECAC_2.c', 'readers_after', True))
    signature = lambda e: [(r['offset'], r['type'], r['symbol']['name'], r['symbol']['value']) for r in e.relocs]
    if before.text != after.text or signature(before) != signature(after):
        raise ValueError('reader instructions or relocations changed')
    if before.data(before.sections[before.names.index('.rodata')]) != after.data(after.sections[after.names.index('.rodata')]):
        raise ValueError('reader local data changed')
    e = Elf(objpath)
    sym = next(s for s in e.symbols if s['name'] == 'sub_0800F044' and s['section'] == e.text_index)
    start = sym['value'] & ~1
    code = e.text[start:start + sym['size']]
    relocs = [dict(r, offset=r['offset'] - start) for r in e.relocs if start <= r['offset'] < start + len(code)]
    mask = relocation_mask(code, relocs)
    diffs = [i for i, byte in enumerate(mask) if byte and code[i] != rom[0xF06C + i]]
    headers = {}
    for name in re.findall(r'^#\s+\d+\s+"([^"]+\.h)"', (out / 'draft.i').read_text(), re.M):
        path = ROOT / name
        if path.is_relative_to(out / 'include'):
            logical = 'include/' + path.relative_to(out / 'include').as_posix()
        else:
            logical = path.relative_to(ROOT).as_posix()
        headers[logical] = lf_sha(path)
    frame = struct.unpack_from('<H', code, 10)[0]
    if frame & 0xFF80 != 0xB080:
        raise ValueError('unexpected Thumb stack-allocation instruction')
    result = {
        'status': 'research_compiled_draft_not_production_receipt',
        'symbol': 'sub_0800F044', 'source': draft.relative_to(ROOT).as_posix(),
        'source_sha256_lf': lf_sha(draft), 'layout_patch_sha256_lf': lf_sha(patch),
        'verification_script_sha256_lf': lf_sha(Path(__file__)),
        'dependent_headers_sha256_lf': dict(sorted(headers.items())),
        'header_mode': 'isolated_named_union_overlay',
        'layout_values': layout_values,
        'layout_value_order': ['state_size', 'region_offset', 'region_size', 'legacy_first', 'legacy_middle', 'legacy_last', 'next_field', 'kirby_pointer'],
        'baseline_data_header_sha256_lf': lf_sha(ROOT / 'include/data.h'),
        'overlay_data_header_sha256_lf': lf_sha(out / 'include/data.h'),
        'compiler_commit': commit, 'compiler_flags': FLAGS,
        'cpp_defines': ['MODERN=0', 'REGION_EU', 'REVISION=0', 'ENGLISH'],
        'text_section_size': len(e.text), 'function_size': len(code),
        'object_sha256': sha(objpath), 'actual_relocations': len(relocs),
        'stack_frame_bytes': (frame & 0x7F) * 4,
        'eu_reference': {'rom_sha1': SHA1, 'start': '0x0800F06C', 'end_exclusive': '0x0800FE78', 'size': 3596},
        'full_eu_match': not diffs and len(code) == 3596,
        'first_fixed_difference': hex(diffs[0]) if diffs else None,
        'fixed_difference_count_unaligned': len(diffs),
        'masked_candidate_sites': [hex(x) for x in unique_sites(code, mask, rom, CODE_END)],
        'reader_text_size': len(before.text), 'reader_text_relocations_and_rodata_exact': True,
        'semantic_equivalence_verified': False, 'matching_c_credit': 0,
        'duplicate_of': 'docs/research/drafts/sub_0800F044.c',
        'artifacts': out.relative_to(ROOT).as_posix(),
    }
    if args.evidence:
        args.evidence.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['function_size', 'stack_frame_bytes', 'actual_relocations', 'full_eu_match', 'reader_text_size', 'reader_text_relocations_and_rodata_exact', 'artifacts']}))


if __name__ == '__main__':
    main()
