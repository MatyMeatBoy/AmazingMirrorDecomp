import importlib.util
from pathlib import Path
import struct
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

DIRECTORY=Path(__file__).resolve().parents[1]/'tools/progress'
sys.path.insert(0,str(DIRECTORY))
import eu_match as match
import eu_build as build


def fixture():
    text=bytes(range(16))+struct.pack('<II',0,8)
    data=b'ABCDEFGHabcdefgh'
    sections=[(0,0,0,0,0,0),(0,1,6,0,0,len(text)),(0,1,2,0,0,len(data))]
    section_symbol=dict(name='',section=2,value=0,size=0,info=3)
    objects=[dict(name=n,section=2,value=lo,size=8,info=1) for n,lo in [('A',0),('B',8)]]
    elf=SimpleNamespace(text_index=1,text=text,sections=sections,names=['','.text','.rodata'],symbols=objects)
    elf.data=lambda s:text if s is sections[1] else data
    relocs={1:[dict(offset=i,type=2,symbol=section_symbol) for i in [16,20]],2:[]}
    rom=bytearray(0x300);rom[0xC0:0xD8]=text
    struct.pack_into('<II',rom,0xD0,0x08000200,0x08000240)
    rom[0x200:0x208]=data[:8];rom[0x240:0x248]=data[8:]
    return elf,relocs,rom


class RegionalObjectTests(unittest.TestCase):
    def prove(self,elf,relocs,rom):
        with patch.object(match,'section_relocations',lambda e,i:relocs.get(i,[])):
            return match.prove_module(elf,rom,0x080000C0,(0,len(elf.text)))

    def test_separate_complete_objects_have_independent_regional_addresses(self):
        elf,relocs,rom=fixture();_,_,scopes,bases=self.prove(elf,relocs,rom)
        self.assertNotIn(2,bases)
        self.assertEqual({(s['object_offset'],s['address']) for s in scopes if s['section_index']==2},{(0,0x08000200),(8,0x08000240)})
        emitted=build.relocate(elf.text,relocs[1],0x080000C0,bases,{},object_mappings=scopes)
        self.assertEqual(emitted,rom[0xC0:0xD8])

    def test_whole_object_including_unread_tail_is_checked(self):
        elf,relocs,rom=fixture();rom[0x247]^=1
        with self.assertRaisesRegex(ValueError,'fixed bytes differ'):self.prove(elf,relocs,rom)

    def test_repeated_object_reference_cannot_move(self):
        elf,relocs,rom=fixture();elf.text=elf.text[:20]+struct.pack('<I',0)
        elf.data=lambda s:elf.text if s is elf.sections[1] else b'ABCDEFGHabcdefgh'
        rom[0x240:0x248]=rom[0x200:0x208]
        with self.assertRaisesRegex(ValueError,'conflicting local object mapping'):self.prove(elf,relocs,rom)

    def test_interior_pointer_maps_the_whole_object(self):
        elf,relocs,rom=fixture();elf.text=elf.text[:16]+struct.pack('<II',3,8)
        elf.data=lambda s:elf.text if s is elf.sections[1] else b'ABCDEFGHabcdefgh'
        struct.pack_into('<I',rom,0xD0,0x08000203)
        _,_,scopes,bases=self.prove(elf,relocs,rom)
        self.assertEqual(build.relocate(elf.text,relocs[1],0x080000C0,bases,{},object_mappings=scopes),rom[0xC0:0xD8])

    def test_named_one_past_and_overlapping_extents_are_rejected(self):
        elf,relocs,rom=fixture()
        with self.assertRaises(ValueError):match.local_object_extent(elf,2,elf.symbols[0],8)
        elf.symbols.append(dict(name='overlap',section=2,value=4,size=8,info=1))
        with self.assertRaises(ValueError):match.local_object_extent(elf,2,relocs[1][0]['symbol'],0)

    def test_partial_relocation_at_object_boundary_is_rejected(self):
        elf,relocs,rom=fixture();relocs[2]=[dict(offset=6,type=2,symbol=dict(name='X',section=0,value=0,size=0,info=1))]
        with self.assertRaisesRegex(ValueError,'straddles'):self.prove(elf,relocs,rom)

    def test_local_object_relocation_is_checked_and_emitted(self):
        elf,relocs,rom=fixture();external=dict(name='X',section=0,value=0,size=0,info=1)
        data=struct.pack('<I',4)+b'EFGHabcdefgh'
        elf.data=lambda s:elf.text if s is elf.sections[1] else data
        relocs[2]=[dict(offset=0,type=2,symbol=external)]
        struct.pack_into('<I',rom,0x200,0x08000284)
        bindings,_,scopes,bases=self.prove(elf,relocs,rom)
        emitted=build.relocate(data[:8],relocs[2],0x08000200,bases,bindings,object_mappings=scopes)
        self.assertEqual(emitted,rom[0x200:0x208])
        self.assertEqual(bindings['X'],0x08000280)

    def test_missing_mapping_cannot_fall_back_to_rom_bytes(self):
        elf,relocs,_=fixture()
        with self.assertRaises(ValueError):build.relocate(elf.text,relocs[1],0x080000C0,{1:0x080000C0},{})

    def callback_fixture(self):
        elf,relocs,rom=fixture();callback=dict(name='Callback',section=1,value=25,size=2,info=2)
        elf.text=elf.text+b'\x70\x47';elf.sections[1]=(0,1,6,0,0,len(elf.text));elf.symbols.append(callback)
        data=struct.pack('<I',0)+b'EFGHabcdefgh'
        elf.data=lambda s:elf.text if s is elf.sections[1] else data
        relocs[2]=[dict(offset=0,type=2,symbol=callback)]
        struct.pack_into('<I',rom,0x200,0x08000281);rom[0x280:0x282]=b'\x70\x47'
        return elf,relocs,rom

    def test_short_thumb_callback_uses_caller_pointer_and_complete_body(self):
        elf,relocs,rom=self.callback_fixture()
        with patch.object(match,'section_relocations',lambda e,i:relocs.get(i,[])):
            _,evidence,scopes,_=match.prove_module(elf,rom,0x080000C0,(0,24))
        self.assertTrue(any(r['symbol']=='Callback' and r['anchored_function'] for r in evidence))
        self.assertTrue(any(s['address']==0x08000280 and s['size']==2 for s in scopes))
        rom[0x281]^=1
        with patch.object(match,'section_relocations',lambda e,i:relocs.get(i,[])):
            with self.assertRaises(ValueError):match.prove_module(elf,rom,0x080000C0,(0,24))

    def test_even_thumb_pointer_is_rejected(self):
        elf,relocs,rom=self.callback_fixture();struct.pack_into('<I',rom,0x200,0x08000280)
        with patch.object(match,'section_relocations',lambda e,i:relocs.get(i,[])):
            with self.assertRaisesRegex(ValueError,'Thumb function pointer'):match.prove_module(elf,rom,0x080000C0,(0,24))

    def test_same_short_callback_cannot_bind_to_two_identical_bodies(self):
        elf,relocs,rom=self.callback_fixture()
        callback=relocs[2][0]['symbol']
        data=struct.pack('<II',0,0)+b'abcdefgh'
        elf.data=lambda s:elf.text if s is elf.sections[1] else data
        relocs[2].append(dict(offset=4,type=2,symbol=callback))
        struct.pack_into('<I',rom,0x204,0x08000291)
        rom[0x290:0x292]=b'\x70\x47'
        with patch.object(match,'section_relocations',lambda e,i:relocs.get(i,[])):
            with self.assertRaisesRegex(ValueError,'conflicting local object mapping'):
                match.prove_module(elf,rom,0x080000C0,(0,24))

    def test_anonymous_literals_require_complete_section_and_whole_text(self):
        elf,relocs,rom=fixture();elf.symbols=[]
        struct.pack_into('<I',rom,0xD4,0x08000208)
        rom[0x200:0x210]=b'ABCDEFGHabcdefgh'
        with patch.object(match,'section_relocations',lambda e,i:relocs.get(i,[])):
            _,_,scopes,_=match.prove_module(elf,rom,0x080000C0)
            self.assertTrue(any(s['section_index']==2 and s['size']==16 for s in scopes))
            with self.assertRaises(ValueError):match.prove_module(elf,rom,0x080000C0,(0,24))
            rom[0x20F]^=1
            with self.assertRaises(ValueError):match.prove_module(elf,rom,0x080000C0)
