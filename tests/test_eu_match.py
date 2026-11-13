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
    def test_global_callback_can_use_its_own_proven_caller_context(self):
        self.assertEqual(m.context_hint('Cb',True,{}, {'Cb':0x08000101}),0x08000101)
        self.assertEqual(m.context_hint('Cb',False,{'Cb':0x08000201},{'Cb':0x08000101}),0x08000101)
        with self.assertRaises(ValueError):m.context_hint('Cb',True,{'Cb':0x08000201},{'Cb':0x08000101})
    def test_library_chain_uses_unique_final_object_and_exact_ordered_extents(self):
        last=SimpleNamespace(text=bytes(range(32)),relocs=[])
        first=SimpleNamespace(text=b'\x70\x47\x00\x00',relocs=[])
        rom=bytes(192)+first.text+last.text
        starts=m.library_chain_starts([('first',first),('last',last)],rom,len(rom))
        self.assertEqual(starts,{'first':0x080000C0,'last':0x080000C4})
        with self.assertRaises(ValueError):m.library_chain_starts([('last',last)],rom,len(rom)+4)
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

    def test_rejected_caller_cannot_leak_partial_callback_context(self):
        import json
        import sys
        import tempfile
        text=b"\x70\x47\0\0"+b"\x11"*16+b"\x22"*16+b"\x70\x47"
        symbols=[dict(name=name,value=offset|1,size=size,info=0x12,section=1)
                 for name,offset,size in [('A',0,2),('OldCaller',4,16),('RejectedCaller',20,16),('B',36,2)]]
        elf=SimpleNamespace(text=text,text_index=1,relocs=[],symbols=symbols,
                            sections=[(0,0,0,0,0,0),(0,1,6,0,0,len(text))],names=['','.text'])
        inventory=[dict(name=symbol['name'],offset=symbol['value']&~1,size=symbol['size'],section='.text',kind='c')
                   for symbol in symbols]
        manifest=dict(region='eu',sources=[dict(source='src/fake.c',object='fake.o',sha256='0'*64,symbols=inventory)])
        rom=bytearray(0x200)
        rom[0x100:0x110]=b"\x11"*16;rom[0x140:0x150]=b"\x22"*16
        rom[0x180:0x182]=rom[0x1C0:0x1C2]=b"\x70\x47"
        def sites(data,mask,image,end):
            return [0x08000100] if data==b"\x11"*16 else [0x08000140] if data==b"\x22"*16 else []
        def proof(obj,image,start,text_range=None,*args,**kwargs):
            if text_range==(4,20):
                evidence=[dict(symbol='B',inferred_value=0x08000181,external=False,anchored_function=True)]
            elif text_range==(20,36):
                # A is encountered first; B contradicts an already proven caller.
                evidence=[dict(symbol='A',inferred_value=0x080001C1,external=False,anchored_function=True),
                          dict(symbol='B',inferred_value=0x080001A1,external=False,anchored_function=True)]
            else:
                evidence=[]
            return {},evidence,[],{1:start}
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);metadata=root/'build/metadata';metadata.mkdir(parents=True)
            (metadata/'manifest.json').write_text(json.dumps(manifest))
            (metadata/'library_manifest.json').write_text(json.dumps(dict(sources=[],compiler={},inputs_sha256={})))
            (root/'linker.ld').write_text('')
            image=root/'owned.gba';image.write_bytes(rom)
            dependencies={'metadata_build':SimpleNamespace(validate_manifest=lambda *args:None),
                          'library_metadata':SimpleNamespace(validate=lambda *args:None)}
            with patch.dict(sys.modules,dependencies),patch.object(m,'validate_rom'),patch.object(m,'Elf',return_value=elf), \
                 patch.object(m,'library_chain_starts',return_value={}),patch.object(m,'unique_sites',side_effect=sites), \
                 patch.object(m,'prove_module',side_effect=proof):
                result=m.analyze(root,image)
        names={symbol['name'] for candidate in result['candidates'] for symbol in candidate['symbols']}
        self.assertIn('OldCaller',names)
        self.assertIn('B',names)
        self.assertNotIn('RejectedCaller',names)
        self.assertNotIn('A',names)

    def _analyze_pending_global_targets(self, second_mode, callback_binding=0x12):
        import json
        import sys
        import tempfile
        def make_elf(byte,caller,internal):
            text=bytes([byte])*16+(b"\0"*4+b"\x70\x47" if internal else b"")
            callback=dict(name='Cb',value=21 if internal else 0,size=2 if internal else 0,
                          info=callback_binding if internal else 0x10,section=1 if internal else 0)
            symbols=[dict(name=caller,value=1,size=16,info=0x12,section=1),callback]
            elf=SimpleNamespace(text=text,text_index=1,relocs=[],symbols=symbols,
                                sections=[(0,0,0,0,0,0),(0,1,6,0,0,len(text))],names=['','.text'])
            inventory=[dict(name=caller,offset=0,size=16,section='.text',kind='c')]
            if internal:inventory.append(dict(name='Cb',offset=20,size=2,section='.text',kind='c'))
            return elf,inventory
        first,first_symbols=make_elf(0x11,'FirstCaller',True)
        second,second_symbols=make_elf(0x22,'SecondCaller',second_mode=='internal')
        records=[dict(source='src/'+name+'.c',object=name+'.o',sha256='0'*64,symbols=inventory)
                 for name,inventory in [('first',first_symbols),('second',second_symbols)]]
        rom=bytearray(0x200);rom[0x100:0x110]=b"\x11"*16;rom[0x140:0x150]=b"\x22"*16
        # Callback bodies deliberately remain pending: neither address has bx lr.
        def sites(data,mask,image,end):
            return [0x08000100] if data==b"\x11"*16 else [0x08000140] if data==b"\x22"*16 else []
        def proof(obj,image,start,*args,**kwargs):
            if obj is second and second_mode=='external':return {'Cb':0x080001A1},[],[],{1:start}
            value=0x08000181 if obj is first else 0x080001A1
            return {},[dict(symbol='Cb',inferred_value=value,external=False,anchored_function=False)],[],{1:start}
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);metadata=root/'build/metadata';metadata.mkdir(parents=True)
            (metadata/'manifest.json').write_text(json.dumps(dict(region='eu',sources=records)))
            (metadata/'library_manifest.json').write_text(json.dumps(dict(sources=[],compiler={},inputs_sha256={})))
            (root/'linker.ld').write_text('');image=root/'owned.gba';image.write_bytes(rom)
            dependencies={'metadata_build':SimpleNamespace(validate_manifest=lambda *args:None),
                          'library_metadata':SimpleNamespace(validate=lambda *args:None)}
            with patch.dict(sys.modules,dependencies),patch.object(m,'validate_rom'), \
                 patch.object(m,'Elf',side_effect=lambda path:first if Path(path).name=='first.o' else second), \
                 patch.object(m,'library_chain_starts',return_value={}),patch.object(m,'unique_sites',side_effect=sites), \
                 patch.object(m,'prove_module',side_effect=proof):
                return m.analyze(root,image)

    def test_pending_global_body_cannot_hide_internal_external_target_conflict(self):
        with self.assertRaisesRegex(ValueError,'internal global target differs from external'):
            self._analyze_pending_global_targets('external')

    def test_pending_global_body_has_one_target_across_translation_units(self):
        with self.assertRaisesRegex(ValueError,'conflicting internal global function target'):
            self._analyze_pending_global_targets('internal')

    def test_same_static_name_in_separate_translation_units_is_not_global_conflict(self):
        result=self._analyze_pending_global_targets('internal',callback_binding=0x02)
        names={symbol['name'] for candidate in result['candidates'] for symbol in candidate['symbols']}
        self.assertEqual(names,{'FirstCaller','SecondCaller'})
