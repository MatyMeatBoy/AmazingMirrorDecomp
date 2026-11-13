"""Bounded EU Shotzo equivalence experiment; never awards matching C credit.

Requires Unicorn 2.1.4 and freshly compiled default/NONMATCHING Shotzo ELF objects.
See ../SHOTZO_AIMING_AUDIT.md for compilation and limitations.
"""
import argparse
import hashlib
import itertools
import json
import struct
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[3])
parser.add_argument('--rom', type=Path, required=True)
parser.add_argument('--reference-object', type=Path, required=True)
parser.add_argument('--candidate-object', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
sys.path.insert(0, str(args.root / 'tools/progress'))
from eu_match import Elf, relocation_mask, unique_sites, prove_module, validate_rom
from eu_build import relocate
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import *

rom = args.rom.read_bytes()
validate_rom(rom)
reference = Elf(args.reference_object)
candidate = Elf(args.candidate_object)
sites = unique_sites(reference.text, relocation_mask(reference.text, reference.relocs), rom, 0x15C714)
if len(sites) != 1:
    raise ValueError('default Shotzo module does not have a unique EU match')
base = sites[0]
bindings, evidence, sections, bases = prove_module(reference, rom, base)
linked_reference = relocate(reference.text, reference.relocs, base, bases, bindings)
if linked_reference != rom[base-0x08000000:base-0x08000000+len(reference.text)]:
    raise ValueError('reference relocation proof is not byte exact')
def symbol(elf,name):
    return next(s for s in elf.symbols if s['name']==name and s['section']==elf.text_index)
def address(elf,name): return base+(symbol(elf,name)['value']&~1)
candidate_text=relocate(candidate.text,candidate.relocs,base,{candidate.text_index:base},bindings)
OBJ=0x02010000; KIRBY=0x02020000; STOP=0x08000100
class Machine:
    def __init__(self,elf,code=None):
        self.elf=elf; self.uc=Uc(UC_ARCH_ARM,UC_MODE_THUMB)
        self.uc.mem_map(0x08000000,0x1000000); self.uc.mem_write(0x08000000,rom)
        self.uc.mem_map(0x02000000,0x40000);self.uc.mem_map(0x03000000,0x8000)
        if code:self.uc.mem_write(base,code)
        self.hooks={bindings[n]&~1:n for n in ('FindTargetKirby','ArcTan2')}
        self.hooks.update({address(elf,n):n for n in ('sub_0811AEDC','sub_0811A874')})
        self.uc.hook_add(UC_HOOK_CODE,self.hook)
    def hook(self,uc,addr,size,_):
        if addr==STOP:self.stopped=True;uc.emu_stop();return
        name=self.hooks.get(addr)
        if not name:return
        args=(uc.reg_read(UC_ARM_REG_R0),uc.reg_read(UC_ARM_REG_R1))
        state=bytes(uc.mem_read(OBJ,0xB0))
        # Internal callbacks move when the readable draft is two bytes smaller.
        callback=struct.unpack_from('<I',state,0x78)[0]
        normalized=bytearray(state)
        for entry in self.elf.symbols:
            if entry['section']==self.elf.text_index and entry['name'] and base+entry['value']==callback:
                normalized[0x78:0x7c]=b'CALL';callback=entry['name'];break
        self.calls.append((name,args if name=='ArcTan2' else args[:1],(bytes(normalized),callback)))
        if name=='FindTargetKirby':uc.reg_write(UC_ARM_REG_R0,KIRBY)
        elif name=='ArcTan2':uc.reg_write(UC_ARM_REG_R0,self.angle<<12)
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    def run(self,angle,direction,facing,armed,subtype):
        self.angle=angle;self.calls=[];self.stopped=False;uc=self.uc
        state=bytearray([0xA5]*0xB0)
        struct.pack_into('<H',state,4,0x1234);struct.pack_into('<I',state,8,0xA0011000|facing)
        struct.pack_into('<ii',state,0x40,0x12345678,-12345678)
        state[0x83]=direction;state[0x85]=armed;state[0x87]=subtype
        uc.mem_write(OBJ,bytes(state));uc.mem_write(KIRBY+0x40,struct.pack('<ii',0x76543210,12345678))
        for i,reg in enumerate((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12)):
            uc.reg_write(reg,0x10101010+i*0x01010101)
        uc.reg_write(UC_ARM_REG_R0,OBJ);uc.reg_write(UC_ARM_REG_SP,0x03007f00);uc.reg_write(UC_ARM_REG_LR,STOP|1)
        uc.emu_start(address(self.elf,'sub_0811AB74')|1,STOP,count=10000)
        if uc.reg_read(UC_ARM_REG_PC) != STOP: raise ValueError('function did not return within instruction limit')
        result=bytearray(uc.mem_read(OBJ,0xB0))
        callback=struct.unpack_from('<I',result,0x78)[0]
        for entry in self.elf.symbols:
            if entry['section']==self.elf.text_index and entry['name'] and base+entry['value']==callback:
                result[0x78:0x7c]=b'CALL';callback=entry['name'];break
        return (bytes(result),callback),self.calls,[uc.reg_read(r) for r in (UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_SP)]
a=Machine(reference)
b=Machine(candidate,candidate_text)
count=0
failures=[]
expected_saved=[0x10101010+i*0x01010101 for i in range(4,12)]+[0x03007f00]
for case in itertools.product(range(16),range(4),range(2),(0,1,255),(0,1,2,3,255)):
    old=a.run(*case)
    new=b.run(*case)
    count+=1
    if old!=new or old[2]!=expected_saved or new[2]!=expected_saved:
        failures.append({'case':case,'object_bytes':[i for i,(x,y) in enumerate(zip(old[0][0],new[0][0])) if x!=y], 'callback_equal':old[0][1]==new[0][1], 'calls_equal':old[1]==new[1], 'saved_registers_equal':old[2]==new[2]})
        if len(failures)>=10: break
result={
    'cases':count,'failures':failures,'matching_c_credit':False,
    'scope':'bounded execution with helper calls stubbed; not a ROM matching gate',
    'eu_sha1':hashlib.sha1(rom).hexdigest(),
    'reference_object_sha256':hashlib.sha256(args.reference_object.read_bytes()).hexdigest(),
    'candidate_object_sha256':hashlib.sha256(args.candidate_object.read_bytes()).hexdigest(),
    'reference_text_size':len(reference.text),'candidate_text_size':len(candidate.text),
    'module_start':hex(base),
    'function_sizes':{name:symbol(elf,'sub_0811AB74')['size'] for name,elf in [('reference',reference),('candidate',candidate)]},
    'recipe_sha256':hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if failures: raise SystemExit(1)
