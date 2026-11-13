import sys
from pathlib import Path
import struct
import unittest
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools/progress'))
import eu_match as m
from eu_build import relocate,check_layout


class ThumbConditionalRelocationTests(unittest.TestCase):
    def test_startup_entry_and_body_exclude_header(self):
        text=struct.pack('<I',0xEA00002E)+bytes(188)+bytes(range(32))
        entry={'name':'__start','value':0,'section':1,'info':0x12}
        elf=SimpleNamespace(text=text,text_index=1,symbols=[entry])
        self.assertEqual(m.startup_ranges(elf),[(0,4),(192,224)])
        elf.text=struct.pack('<I',0xEA00002F)+text[4:]
        with self.assertRaises(ValueError):m.startup_ranges(elf)
        check_layout([{'eu_start':0x08000000,'size':4},{'eu_start':0x080000C0,'size':32}])
        for start,size in ((0,8),(4,188),(188,8)):
            with self.assertRaises(ValueError):check_layout([{'eu_start':0x08000000+start,'size':size}])

    def test_only_immediate_byte_is_masked(self):
        self.assertEqual(m.relocation_mask(bytes.fromhex('fed1'),[{'offset':0,'type':103}]),b'\0\xff')

    def test_conditional_displacement_keeps_condition_and_signed_range(self):
        self.assertEqual(m.thumb_cond_displacement(bytes.fromhex('fed1')),-4)
        self.assertEqual(m.thumb_cond_displacement(bytes.fromhex('7fd0')),254)
        self.assertEqual(m.thumb_cond_displacement(bytes.fromhex('80dd')),-256)
        for word in (0xDEFE,0xDFFE,0xE7FE):
            with self.assertRaises(ValueError):m.thumb_cond_displacement(struct.pack('<H',word))

    def test_conditional_emission_and_overflow(self):
        symbol={'name':'Local','section':1,'value':0x5D,'info':0x12}
        reloc={'offset':0,'type':103,'symbol':symbol}
        self.assertEqual(relocate(bytes.fromhex('fed1'),[reloc],0x080000C0,{1:0x080000C0},{}),bytes.fromhex('2cd1'))
        for value in (0x201,0x80000001):
            with self.assertRaises(ValueError):relocate(bytes.fromhex('fed1'),[dict(reloc,symbol=dict(symbol,value=value))],0x080000C0,{1:0x080000C0},{})

    def test_object_addend_and_alignment_rejected(self):
        with self.assertRaises(ValueError):m.relocation_mask(bytes.fromhex('00d1'),[{'offset':0,'type':103}])
        with self.assertRaises(ValueError):m.relocation_mask(bytes.fromhex('00fed100'),[{'offset':1,'type':103}])

    def test_complete_module_proves_local_branch_and_rejects_other_targets(self):
        text=bytes.fromhex('fed1')+bytes(range(2,16))
        symbol={'name':'Local','section':1,'value':13,'info':0x12,'size':2}
        sections=[(0,0,0,0,0,0),(0,1,6,0,0,len(text))]
        elf=SimpleNamespace(text_index=1,text=text,sections=sections,names=['','.text'],symbols=[symbol])
        elf.data=lambda section:text
        reloc={'offset':0,'type':103,'symbol':symbol}
        rom=bytes(192)+bytes.fromhex('04d1')+text[2:]
        with patch.object(m,'section_relocations',lambda e,i:[reloc]):
            m.prove_module(elf,rom,0x080000C0)
            with self.assertRaises(ValueError):m.prove_module(elf,rom,0x080000C0,(0,len(text)))
            with self.assertRaises(ValueError):m.prove_module(elf,rom[:192]+bytes.fromhex('05d1')+text[2:],0x080000C0)
            symbol['section']=0
            with self.assertRaises(ValueError):m.prove_module(elf,rom,0x080000C0)
