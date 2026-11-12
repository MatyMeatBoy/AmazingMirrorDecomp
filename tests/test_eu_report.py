import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import subprocess
import unittest

TOOLS = Path(__file__).resolve().parents[1]/'tools/progress'
sys.path.insert(0, str(TOOLS))


class EuropeReportTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('eu_report', TOOLS/'eu_report.py')
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        paths = ['src/example.c', *self.m.RECIPES]
        hashes = {}; modes = {}
        for name in paths:
            path = self.root/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'example\n')
            hashes[name] = hashlib.sha256(b'example\n').hexdigest()
            modes[name] = 'lf'
        subprocess.run(['git','init','-q',str(self.root)],check=True)
        subprocess.run(['git','-C',str(self.root),'add','.'],check=True,capture_output=True)
        self.r = {'schema_version': 1, 'analysis_only': False, 'rom_match_verified': True,
                  'full_rom_byte_compare': True, 'expected_sha1': self.m.SHA1, 'rebuilt_sha1': self.m.SHA1,
                  'eu_sha1': self.m.SHA1, 'rom_size': self.m.ROM_SIZE, 'code_end': self.m.CODE_END,
                  'inputs_sha256': hashes, 'source_hash_modes': modes,
                  'compiler': {'commit': self.m.COMPILER_COMMIT, 'sha256': 'a'*64},
                  'compiler_binary_sha256': {'agbcc': 'a'*64, 'old_agbcc': 'b'*64},
                  'compiler_recipe': {'default_cflags': self.m.CFLAGS},
                  'source_manifest_sha256': 'a'*64, 'matcher_sha256': 'b'*64, 'builder_sha256': 'c'*64,
                  'credited_c_bytes': 20,
                  'c_spans': [{'source': 'src/example.c', 'name': 'ExampleFunction', 'start': 256,
                               'end': 276, 'bytes': 20, 'object_sha256': 'd'*64, 'linked_span_sha256': 'e'*64}]}

    def test_valid_current_receipt_and_full_partition(self):
        r = self.m.assess(self.r, self.root)
        self.assertTrue(r['rom_match_verified'])
        self.assertEqual(r['credited_c_bytes'], 20)
        self.assertEqual(sum(c['bytes'] for c in self.m.cells(r)), self.m.CODE_END-188)
        self.assertEqual(r['verified_c_function_spans'], 1)
        self.assertIsNone(r['total_functions'])

    def test_changed_source_or_missing_recipe_clears_credit(self):
        (self.root/'src/example.c').write_text('changed')
        r = self.m.assess(self.r, self.root)
        self.assertFalse(r['rom_match_verified'])
        self.assertEqual(r['credited_c_bytes'], 0)
        self.assertEqual(r['c_spans'], [])

    def test_missing_receipt_is_unverified(self):
        report = self.m.assess({}, self.root)
        self.assertFalse(report['rom_match_verified'])
        self.assertNotIn('preserved by a verified full-ROM rebuild',self.m.markdown(report))

    def test_new_source_invalidates_complete_inventory(self):
        (self.root/'src/new.c').write_text('new source')
        self.assertFalse(self.m.assess(self.r,self.root)['rom_match_verified'])

    def test_verified_local_data_is_deduplicated_without_format_credit(self):
        self.r['source_data_spans'] = [
            {'source':'src/example.c','section':'.rodata','start':self.m.CODE_END+256,
             'end':self.m.CODE_END+272,'bytes':16,'sha256':'a'*64,'object_sha256':'b'*64},
            {'source':'src/example.c','section':'.rodata','start':self.m.CODE_END+264,
             'end':self.m.CODE_END+280,'bytes':16,'sha256':'c'*64,'object_sha256':'b'*64}]
        report = self.m.assess(self.r,self.root)
        self.assertEqual(report['source_backed_data_bytes'],24)
        self.assertIsNone(report['data_identification_percent'])
        (self.root/'src/example.c').write_text('changed')
        self.assertEqual(self.m.assess(self.r,self.root)['source_backed_data_bytes'],0)

    def test_text_newlines_portable_binary_bytes_exact(self):
        (self.root/'src/example.c').write_bytes(b'example\r\n')
        self.assertTrue(self.m.assess(self.r, self.root)['rom_match_verified'])
        binary = self.root/'graphics/picture.bin'
        binary.parent.mkdir()
        binary.write_bytes(b'\r\n')
        self.r['inputs_sha256']['graphics/picture.bin'] = hashlib.sha256(b'\r\n').hexdigest()
        self.r['source_hash_modes']['graphics/picture.bin'] = 'raw'
        self.assertTrue(self.m.assess(self.r, self.root)['rom_match_verified'])
        binary.write_bytes(b'\n')
        self.assertFalse(self.m.assess(self.r, self.root)['rom_match_verified'])

    def test_overlap_header_boolean_and_traversal_rejected(self):
        for change in ({'start': 4, 'end': 24}, {'start': True}, {'source': '../escape.c'}):
            with self.subTest(change=change):
                r = json.loads(json.dumps(self.r))
                r['c_spans'][0].update(change)
                with self.assertRaises(ValueError):
                    self.m.assess(r, self.root)
        self.r['c_spans'].append(dict(self.r['c_spans'][0]))
        with self.assertRaises(ValueError):
            self.m.assess(self.r, self.root)

    def test_incomplete_proof_or_unsupported_mode_clears_credit(self):
        for key in ('compiler', 'matcher_sha256', 'compiler_binary_sha256'):
            r = dict(self.r)
            r.pop(key)
            self.assertFalse(self.m.assess(r, self.root)['rom_match_verified'])
        self.r['source_hash_modes']['src/example.c'] = 'unknown'
        self.assertFalse(self.m.assess(self.r, self.root)['rom_match_verified'])


if __name__ == '__main__':
    unittest.main()
