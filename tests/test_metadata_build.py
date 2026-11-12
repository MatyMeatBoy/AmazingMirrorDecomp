import importlib.util
import pathlib
import tempfile
import struct
import unittest

PATH = pathlib.Path(__file__).resolve().parents[1] / 'tools/progress/metadata_build.py'
spec = importlib.util.spec_from_file_location('metadata_build', PATH)
m = importlib.util.module_from_spec(spec)
if PATH.exists():
    spec.loader.exec_module(m)


class MetadataTests(unittest.TestCase):
    def test_aliases_and_padding_count_once(self):
        spans = m.partition_symbols(12, [dict(name='a', offset=2, size=4), dict(name='alias', offset=2, size=4), dict(name='b', offset=8, size=0)], {'a': 'c', 'alias': 'c', 'b': 'asm'})
        self.assertEqual(sum(x['size'] for x in spans), 12)
        self.assertEqual([x['size'] for x in spans], [2, 4, 2, 4])
        self.assertEqual(spans[1]['aliases'], ['alias'])
        self.assertEqual(spans[-1]['size_basis'], 'next_symbol_or_section_end')

    def test_reject_overlaps(self):
        with self.assertRaises(ValueError):
            m.partition_symbols(8, [dict(name='a', offset=0, size=6), dict(name='b', offset=4, size=4)], {})

    def test_active_naked_and_inline_asm_are_conservative(self):
        text = 'void Normal(void) { asm("" ::: "r4"); }\n__attribute__((naked)) void Raw(void) { asm("bx lr"); }'
        self.assertEqual(m.function_kinds(text), {'Normal': 'c', 'Raw': 'asm'})

    def test_bad_elf_rejected(self):
        with self.assertRaises(ValueError):
            m.read_elf(b'not an elf')

    def test_stale_manifest_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            with self.assertRaises(ValueError):
                m.validate_manifest(dict(schema_version=1, scope='main_object_text', rom_verified=False, input_sha256='wrong'), root)

    def test_nested_body_does_not_create_false_functions(self):
        text = 'void A(void) { if (1) { x(); } }\nvoid B(void) { }'
        self.assertEqual(m.function_kinds(text), {'A': 'c', 'B': 'c'})

    def test_attributes_and_function_pointer_are_not_definitions(self):
        text = 'static void __attribute__((unused)) Real(void) { asm("" ::: "r4"); }\n__attribute__((naked, unused)) void Raw(void) { asm("bx lr"); }\nvoid (*callback)(void);'
        self.assertEqual(m.function_kinds(text), {'Real': 'c', 'Raw': 'asm'})

    def test_empty_assets_never_selects_default_make_target(self):
        self.assertIsNone(m.asset_make_command([]))
        self.assertIn('graphics/a.4bpp', m.asset_make_command(['graphics/a.4bpp']))

    def test_truncated_executable_section_is_rejected(self):
        names = b'\0.shstrtab\0.text\0'
        header = struct.pack('<16sHHIIIIIHHHHHH', b'\x7fELF\x01\x01\x01'+bytes(9), 1, 40, 1, 0, 0, 52, 0, 52, 0, 0, 40, 3, 1)
        null = bytes(40)
        strings = struct.pack('<10I', 1, 3, 0, 0, 172, len(names), 0, 0, 1, 0)
        text = struct.pack('<10I', 11, 1, 6, 0, 10000, 8, 0, 0, 4, 0)
        with self.assertRaises(ValueError):
            m.read_elf(header + null + strings + text + names)


if __name__ == '__main__':
    unittest.main()
