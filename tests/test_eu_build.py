import importlib.util
from pathlib import Path
import struct
import sys
import unittest
import tempfile
import os
from unittest.mock import patch

DIRECTORY=Path(__file__).resolve().parents[1]/'tools/progress'
sys.path.insert(0,str(DIRECTORY))
spec=importlib.util.spec_from_file_location('eu_build',DIRECTORY/'eu_build.py')
m=importlib.util.module_from_spec(spec)
if (DIRECTORY/'eu_build.py').exists():spec.loader.exec_module(m)

class EuBuildTests(unittest.TestCase):
    def test_auxiliary_text_provenance_is_portable(self):
        names=['tools/preproc/.gitignore','tools/preproc/LICENSE','tools/preproc/io.cpp']
        names += ['tools/progress/'+n+'.py' for n in ('eu_match','eu_build','metadata_build','library_metadata')]
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in names:
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b'a\r\nb\r\n')
            with patch.object(m.subprocess,'check_output',return_value=('\0'.join(names)+'\0').encode()):
                hashes,modes=m.provenance(root)
                for name in names:
                    self.assertEqual(modes[name],'lf')
                    self.assertEqual(hashes[name],m.source_digest(b'a\nb\n','lf'))

    def test_abs32_is_emitted_from_object_addend(self):
        reloc={'offset':0,'type':2,'symbol':{'name':'external','section':0,'value':0}}
        self.assertEqual(m.relocate(struct.pack('<I',4),[reloc],0x08000100,{}, {'external':0x08200000}),struct.pack('<I',0x08200004))

    def test_thumb_call_is_emitted_from_binding(self):
        reloc={'offset':0,'type':10,'symbol':{'name':'callee','section':0,'value':0}}
        output=m.relocate(bytes.fromhex('fff7feff'),[reloc],0x08000100,{}, {'callee':0x08000201})
        self.assertEqual(m.thumb_displacement(output),0xFC)

    def test_conflicting_overlays_rejected(self):
        with self.assertRaises(ValueError):m.check_layout([{'eu_start':0x080000C0,'size':8},{'eu_start':0x080000C4,'size':8}])

    def test_text_hash_portable_binary_hash_exact(self):
        self.assertEqual(m.source_digest(b'a\r\nb','lf'),m.source_digest(b'a\nb','lf'))
        self.assertNotEqual(m.source_digest(b'a\r\nb','raw'),m.source_digest(b'a\nb','raw'))

    def test_existing_output_hardlink_to_rom_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);original=root/'original.gba';original.write_bytes(b'owned')
            out=root/'build';out.mkdir();target=out/'copy.gba';os.link(original,target)
            with self.assertRaises(ValueError):m.guard_output(target,original,out)
