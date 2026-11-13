import importlib.util
from pathlib import Path
import sys
import tempfile
import struct
import unittest
from unittest.mock import patch

DIRECTORY=Path(__file__).resolve().parents[1]/'tools/progress'
sys.path.insert(0,str(DIRECTORY))
spec=importlib.util.spec_from_file_location('library_metadata',DIRECTORY/'library_metadata.py')
m=importlib.util.module_from_spec(spec)
if (DIRECTORY/'library_metadata.py').exists():spec.loader.exec_module(m)


class LibraryMetadataTests(unittest.TestCase):
    @staticmethod
    def alias_elf():
        names=b'\0.text\0.symtab\0.strtab\0.shstrtab\0'
        strings=b'\0Foo\0Alias\0'
        header=struct.pack('<16sHHIIIIIHHHHHH',b'\x7fELF\x01\x01\x01'+bytes(9),1,40,1,0,0,52,0,52,0,0,40,5,4)
        sections=[bytes(40),struct.pack('<10I',1,1,6,0,252,8,0,0,4,0),struct.pack('<10I',7,2,0,0,260,48,3,1,4,16),struct.pack('<10I',15,3,0,0,308,len(strings),0,0,1,0),struct.pack('<10I',23,3,0,0,308+len(strings),len(names),0,0,1,0)]
        symbols=bytes(16)+struct.pack('<IIIBBH',1,1,2,0x12,0,1)+struct.pack('<IIIBBH',5,1,2,0x12,0,1)
        return header+b''.join(sections)+b'\x70\x47'+bytes(6)+symbols+strings+names

    def test_real_elf_aliases_count_once_and_padding_stays_unknown(self):
        with tempfile.TemporaryDirectory() as directory:
            obj=Path(directory)/'foo.o';obj.write_bytes(self.alias_elf())
            _,symbols,_=m.object_metadata(obj,b'void Foo(void) {} void Alias(void) {}',{'kind':'c'},'foo.c','libc.a:foo.o')
            self.assertEqual([(s['size'],s['kind']) for s in symbols],[(2,'c'),(6,'unknown')])
            self.assertEqual(symbols[0]['aliases'],['Foo'])

    def test_validate_rejects_tampered_symbols_and_missing_dependencies(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve()
            for name in ['linker.ld','tools/agbcc/libc/Makefile','tools/agbcc/libgcc/Makefile','tools/progress/library_metadata.py','tools/progress/metadata_build.py','tools/agbcc/libc/foo.c']:
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text('*libc.a:foo.o(.text);' if name=='linker.ld' else '')
            source=root/'tools/agbcc/libc/foo.c';spec=m.library_spec(root,'libc.a:foo.o')
            preprocessed=b'void Foo(void) {} void Alias(void) {}'
            obj=root/'build/metadata/objects/libraries/libc__foo.o';obj.parent.mkdir(parents=True);obj.write_bytes(self.alias_elf());obj.with_suffix('.o.i').write_bytes(preprocessed)
            sections,symbols,all_sections=m.object_metadata(obj,preprocessed,spec,source.relative_to(root).as_posix(),'libc.a:foo.o')
            identity={'commit':m.COMPILER_COMMIT,'binaries':{}}
            hashes=m.input_hashes(root,m.fixed_inputs(root)|{source})
            record=dict(library_member='libc.a:foo.o',source=source.relative_to(root).as_posix(),object='objects/libraries/libc__foo.o',sha256=m.digest(obj.read_bytes()),preprocessed_sha256=m.digest(preprocessed),sections=sections,symbols=symbols,all_sections=all_sections,cpp_flags=m.portable_flags(root,spec['cpp_flags']),compiler_flags=spec['compiler_flags'],assembler_flags=spec['assembler_flags'],source_kind='c')
            manifest=dict(schema_version=1,scope='main_linker_libraries',rom_verified=False,compiler=identity,inputs_sha256=hashes,source_hash_modes={name:'lf' for name in hashes},sources=[record])
            with patch.object(m,'tools',return_value={}),patch.object(m,'compiler_identity',return_value=identity),patch.object(m,'preprocess',return_value=(preprocessed,{source})),patch.object(m,'check_compiler_sources'):
                m.validate(manifest,root)
                record['symbols'][0]['kind']='asm'
                with self.assertRaises(ValueError):m.validate(manifest,root)
                record['symbols'][0]['kind']='c'
                del manifest['inputs_sha256'][source.relative_to(root).as_posix()]
                with self.assertRaises(ValueError):m.validate(manifest,root)

    def test_only_linker_selected_executable_members_count(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'linker.ld').write_text('*libc.a:memcpy.o(.text);\n*libc.a:impure.o(.data);\n*libgcc.a:fp-bit.o(.text);\n')
            self.assertEqual(m.selected_members(root),['libc.a:memcpy.o','libgcc.a:fp-bit.o'])

    def test_duplicate_selected_member_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'linker.ld').write_text('*libc.a:memcpy.o(.text);\n*libc.a:memcpy.o(.text);\n')
            with self.assertRaises(ValueError):m.selected_members(root)

    def test_eu_double_word_order_is_explicit(self):
        spec=m.library_spec(Path('/compiler-parent'),'libgcc.a:dp-bit.o')
        self.assertIn('-DFLOAT_WORD_ORDER_MISMATCH',spec['cpp_flags'])
        self.assertEqual(spec['compiler_flags'],['-O2'])
        self.assertEqual(spec['kind'],'c')

    def test_inline_assembly_never_gets_c_credit(self):
        with self.assertRaises(ValueError):m.classify_functions('void A(void) { asm("nop"); }','c')
        self.assertEqual(m.classify_functions('void A(void) { }','c'),{'A':'c'})

    def test_hash_mode_normalizes_only_line_endings(self):
        self.assertEqual(m.text_digest(b'a\r\nb'),m.text_digest(b'a\nb'))
        self.assertNotEqual(m.text_digest(b'a \nb'),m.text_digest(b'a\nb'))

    def test_header_trace_rejects_external_dependency(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with self.assertRaises(ValueError):m.header_dependencies(b'. /outside/header.h\n',root)


if __name__=='__main__':unittest.main()
