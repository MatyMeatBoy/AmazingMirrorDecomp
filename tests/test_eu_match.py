import importlib.util
from pathlib import Path
import unittest
import struct
from types import SimpleNamespace
from unittest.mock import patch

PATH=Path(__file__).resolve().parents[1]/'tools/progress/eu_match.py'
spec=importlib.util.spec_from_file_location('eu_match',PATH)
m=importlib.util.module_from_spec(spec)
if PATH.exists(): spec.loader.exec_module(m)

class EuMatchTests(unittest.TestCase):
    def test_progbits_noload_requires_linker_ownership_zero_bytes_and_no_relocations(self):
        section=(0,1,3,0,0,16,0,0,4,0)
        elf=SimpleNamespace(sections=[section],names=['common_data'],symbols=[],data=lambda s:bytes(16))
        with patch.object(m,'section_relocations',return_value=[]):
            self.assertEqual(m.validate_noload(elf,0,0x03000560,'iwram')['kind'],'ram_noload')
            for address in (0x02000560,0x03007FFC,0x03000561):
                with self.assertRaises(ValueError):m.validate_noload(elf,0,address,'iwram')
            elf.data=lambda s:b'\x01'+bytes(15)
            with self.assertRaises(ValueError):m.validate_noload(elf,0,0x03000560,'iwram')
        elf.data=lambda s:bytes(16)
        with patch.object(m,'section_relocations',return_value=[{'offset':0}]):
            with self.assertRaises(ValueError):m.validate_noload(elf,0,0x03000560,'iwram')

    def test_noload_ownership_is_specific_to_output_region_object_and_input_pattern(self):
        linker='''iwram (NOLOAD) : ALIGN(4) { src/m4a.o(common_data .bss*); } >iwram
        .rodata : { src/other.o(common_data); } >rom'''
        self.assertEqual(m.noload_inputs(linker,'src/m4a.o'),{'common_data':'iwram','.bss*':'iwram'})
        self.assertEqual(m.noload_inputs(linker,'src/other.o'),{})

    def test_runtime_progbits_cannot_be_treated_as_noload_without_policy(self):
        text=bytes(range(16))+bytes(4)
        sections=[(0,0,0,0,0,0,0,0,0,0),(0,1,6,0,0,20,0,0,4,0),(0,1,3,0,0,16,0,0,4,0)]
        symbol={'name':'Work','section':2,'value':0,'size':16,'info':1}
        elf=SimpleNamespace(text_index=1,text=text,sections=sections,names=['','.text','common_data'],symbols=[symbol])
        elf.data=lambda section:text if section is sections[1] else bytes(16)
        reloc={'offset':16,'type':2,'symbol':symbol}
        rom=bytearray(0x100);rom[0xC0:0xD4]=text;struct.pack_into('<I',rom,0xD0,0x03000560)
        with patch.object(m,'section_relocations',lambda e,i:[reloc] if i==1 else []):
            with self.assertRaises(ValueError):m.prove_module(elf,rom,0x080000C0)
            _,_,proof,_=m.prove_module(elf,rom,0x080000C0,noload_sections={'common_data':'iwram'})
            self.assertEqual(sum(p['size'] for p in proof if p.get('kind')=='ram_noload'),16)
    def test_short_function_needs_proven_context_and_all_fixed_bytes(self):
        rom=bytes(192)+b'\x70\x47'+bytes(10)
        self.assertIsNone(m.choose_site(b'\x70\x47',b'\xff\xff',rom,len(rom)))
        self.assertEqual(m.choose_site(b'\x70\x47',b'\xff\xff',rom,len(rom),0x080000C0),0x080000C0)
        self.assertIsNone(m.choose_site(b'\x70\x47',b'\xff\xff',rom,len(rom),0x080000C4))

    def test_nobits_requires_aligned_complete_ram_extent(self):
        section=(0,8,3,0,0,32,0,0,4,0)
        elf=SimpleNamespace(sections=[section],names=['.bss'],symbols=[])
        self.assertEqual(m.validate_nobits(elf,0,0x02000000)['kind'],'ram_noload')
        for address in (0x08000000,0x0203FFF0,0x02000001):
            with self.assertRaises(ValueError):m.validate_nobits(elf,0,address)

    def test_repeated_nobits_references_must_agree(self):
        text=bytes(range(16))+struct.pack('<II',0,4)
        sections=[(0,0,0,0,0,0,0,0,0,0),(0,1,6,0,0,24,0,0,4,0),(0,8,3,0,0,16,0,0,4,0)]
        symbol={'name':'buffer','section':2,'value':0,'size':16,'info':1}
        elf=SimpleNamespace(text_index=1,sections=sections,names=['','.text','.bss'],symbols=[symbol],text=text)
        elf.data=lambda section:text
        relocations=[{'offset':16,'type':2,'symbol':symbol},{'offset':20,'type':2,'symbol':symbol}]
        rom=bytearray(0x100);rom[0xC0:0xD8]=text;struct.pack_into('<II',rom,0xD0,0x02000000,0x02000008)
        with patch.object(m,'section_relocations',lambda e,i:relocations if i==1 else []):
            with self.assertRaises(ValueError):m.prove_module(elf,rom,0x080000C0,(0,24))

    def test_thumb_target(self):
        self.assertEqual(m.thumb_displacement(bytes.fromhex('fff7feff')), -4)

    def test_unique_mask_keeps_all_fixed_bytes(self):
        text=bytes(range(32)); mask=bytearray([255]*32);mask[16:20]=bytes(4)
        rom=bytes(192)+text+bytes(4)
        self.assertEqual(m.unique_sites(text,mask,rom,len(rom)),[0x080000C0])
        self.assertEqual(len(m.unique_sites(text,mask,rom+text,len(rom+text))),2)

    def test_unsupported_relocation_rejected(self):
        with self.assertRaises(ValueError):m.relocation_mask(bytes(20),[{'offset':0,'type':999}])

    def test_relocation_markers_and_overlaps_are_validated(self):
        with self.assertRaises(ValueError):m.relocation_mask(bytes(8),[{'offset':10,'type':40}])
        with self.assertRaises(ValueError):m.relocation_mask(bytes(8),[{'offset':0,'type':2},{'offset':0,'type':2}])

    def test_function_data_callback_requires_actual_function_anchor(self):
        text=bytes(range(12))+struct.pack('<I',0)+bytes(32)
        rodata=struct.pack('<I',0)+b'unused!!'
        sections=[(0,1,6,0,0,len(text)),(0,1,2,0,0,len(rodata))]
        callback={'name':'Callback','section':0,'value':33,'info':2}
        array={'name':'Table','section':1,'value':0,'info':1,'size':4}
        # Use real section indices starting at one; zero means undefined.
        sections=[(0,0,0,0,0,0)]+sections
        callback['section']=1;array['section']=2
        elf=SimpleNamespace(text_index=1,sections=sections,names=['','.text','.rodata'],symbols=[array])
        elf.data=lambda section: text if section is sections[1] else rodata
        relocs={1:[{'offset':12,'type':2,'symbol':array}],2:[{'offset':0,'type':2,'symbol':callback}]}
        rom=bytearray(0x300);rom[0xC0:0xD0]=text[:16];struct.pack_into('<I',rom,0xCC,0x08000200);struct.pack_into('<I',rom,0x200,0x08000101)
        with patch.object(m,'section_relocations',lambda e,i:relocs[i]):
            _,evidence,_,_=m.prove_module(elf,rom,0x080000C0,(0,16),{'Callback':[0x08000100]})
            self.assertTrue(evidence[-1]['anchored_function'])
            with self.assertRaises(ValueError):m.prove_module(elf,rom,0x080000C0,(0,16),{'Callback':[0x08000120]})
