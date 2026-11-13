import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools/progress'))
import draft_inventory as m


class DraftInventoryTests(unittest.TestCase):
    def test_only_fresh_and_compiling_draft_is_recovered(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);drafts=root/'docs/research/drafts';drafts.mkdir(parents=True)
            (root/'asm').mkdir();(root/'asm/example.s').write_bytes(b'asm\n')
            (drafts/'example.c').write_bytes(b'C\n')
            receipt={'symbol':'Example','source':'docs/research/drafts/example.c',
                     'source_sha256':hashlib.sha256(b'C\n').hexdigest(),'dependent_headers_sha256':{},
                     'compiler':{'commit':m.COMPILER_COMMIT},'profile':{'compiler_flags':m.CFLAGS},
                     'eu_reference':{'source_asm':'asm/example.s','source_asm_sha256':hashlib.sha256(b'asm\n').hexdigest()}}
            (drafts/'example.evidence.json').write_text(json.dumps(receipt))
            with patch.object(m,'compile_source',return_value={'c_functions':['Example'],'compiled':True}):
                recovered,issues=m.recover(root)
                self.assertEqual(len(recovered),1);self.assertEqual(issues,[])
                (drafts/'example.c').write_text('changed')
                self.assertEqual(m.recover(root)[0],[])
            (drafts/'example.c').write_bytes(b'C\n')
            with patch.object(m,'compile_source',side_effect=ValueError('compiler error')):
                self.assertEqual(m.recover(root)[0],[])

    def test_missing_dependencies_produce_no_yellow_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);drafts=root/'docs/research/drafts';drafts.mkdir(parents=True)
            receipt={'symbol':'Example','source':'missing.c','source_sha256':'a'*64,
                     'dependent_headers_sha256':{},'compiler':{'commit':m.COMPILER_COMMIT},
                     'profile':{'compiler_flags':m.CFLAGS},'eu_reference':{'source_asm':'missing.s','source_asm_sha256':'a'*64}}
            (drafts/'example.evidence.json').write_text(json.dumps(receipt))
            self.assertEqual(m.recover(root)[0],[])
