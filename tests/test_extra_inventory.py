import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools/progress'))
import extra_inventory as m


class ExtraInventoryTests(unittest.TestCase):
    def receipt(self):
        member={'member':'libc.a:memcpy.o','source':'tools/agbcc/libc/string/memcpy.c','domain':'library_c','object_sha256':'a'*64,
                'function_count':1,'functions':[{'name':'memcpy','aliases':['__memcpy'],'section':'.text','offset':0}]}
        return {'schema_version':1,'rom_verified':False,'errors':[],'compiler_commit':m.COMPILER_COMMIT,
                'main_selected_library_members':[member],
                'auxiliaries':[{'target':'multi_boot/example','objects':[],
                                'selected_archive_members':[{'member':member['member'],'function_count':1,'object_sha256':'a'*64}]}]}

    def test_aliases_once_copies_in_separate_programs_separate(self):
        result=m.summarize(self.receipt())
        self.assertEqual(result['totals']['functions'],2)
        self.assertEqual(result['totals']['c_available'],2)
        self.assertEqual(len(result['groups']),2)
        self.assertNotIn('verified_c',result['totals'])

    def test_bad_member_count_cannot_inflate_inventory(self):
        receipt=self.receipt();receipt['main_selected_library_members'][0]['function_count']=2
        with self.assertRaises(ValueError):m.summarize(receipt)

    def test_changed_inputs_remove_additional_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'config/progress').mkdir(parents=True)
            (root/'multi_boot/example').mkdir(parents=True)
            (root/'multi_boot/example/linker.ld').write_text('ENTRY(__start)\n')
            linker=b'*libc.a:memcpy.o(.text)\n';(root/'linker.ld').write_bytes(linker)
            receipt=self.receipt();receipt['inputs_sha256']={'linker.ld':hashlib.sha256(linker).hexdigest()};receipt['source_hash_modes']={'linker.ld':'lf'}
            # Model the complete current dependency set, not a self-selected subset.
            (root/'multi_boot/example/linker.ld').write_text('ENTRY(__start)\n*libc.a:memcpy.o(.text)\n')
            required=m.expected_inputs(root,receipt)
            for name in required:
                path=root/name
                if not path.exists():path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b'source\n')
            receipt['inputs_sha256']={name:hashlib.sha256((root/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for name in required}
            receipt['source_hash_modes']={name:'lf' for name in required}
            (root/'config/progress/extra_functions.json').write_text(json.dumps(receipt))
            self.assertTrue(m.load(root)['available'])
            aux=root/'multi_boot/example/linker.ld'
            aux.write_bytes(b'asm/code.o(.text)\n*libc.a:memcpy.o(.text)\n')
            receipt['inputs_sha256']['multi_boot/example/linker.ld']=hashlib.sha256(aux.read_bytes()).hexdigest()
            (root/'config/progress/extra_functions.json').write_text(json.dumps(receipt))
            self.assertIn('object inventory changed',m.load(root)['issue'])
            (root/'linker.ld').write_text('changed')
            result=m.load(root)
            self.assertFalse(result['available'])
            self.assertNotIn('totals',result)

    def test_receipt_cannot_omit_a_compiled_source_fingerprint(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'config/progress').mkdir(parents=True)
            (root/'multi_boot/example').mkdir(parents=True)
            (root/'multi_boot/example/linker.ld').write_text('ENTRY(__start)\n')
            linker=b'*libc.a:memcpy.o(.text)\n';(root/'linker.ld').write_bytes(linker)
            receipt=self.receipt();receipt['inputs_sha256']={'linker.ld':hashlib.sha256(linker).hexdigest()};receipt['source_hash_modes']={'linker.ld':'lf'}
            (root/'config/progress/extra_functions.json').write_text(json.dumps(receipt))
            self.assertFalse(m.load(root)['available'])
