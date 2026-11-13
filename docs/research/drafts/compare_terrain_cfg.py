"""Read-only diagnostic. Raw CFGs preserve branch targets and memory offsets.
Register spelling alone is normalized. Ordered-edge matching is not semantic
or dataflow equivalence; differing effects remain explicit. No C credit.
Run from the repository root; JSON output belongs under ignored build/.
"""
from pathlib import Path
import re,subprocess,sys,json,collections,argparse,shutil,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'tools/progress'))
from eu_match import Elf,relocation_mask
parser=argparse.ArgumentParser(description="Diagnostic terrain CFG/ordered-effect comparison; never grants match credit")
parser.add_argument('reference',type=Path)
parser.add_argument('candidate',type=Path)
parser.add_argument('--rom',type=Path,default=Path('baserom_eu.gba'))
parser.add_argument('--out',type=Path,required=True)
parser.add_argument('--objdump',default=shutil.which('arm-none-eabi-objdump') or 'C:/msys64/ucrt64/bin/arm-none-eabi-objdump.exe')
args=parser.parse_args()
OBJDUMP=args.objdump
COND={'beq','bne','bgt','bge','blt','ble','bhi','bls','bcs','bcc','bmi','bpl','bvs','bvc'}
def read(path):
 e=Elf(path); symbol=next(z for z in e.symbols if z['name']=='sub_0800F044'); assert symbol['value']&~1==0, 'requires standalone function at text offset zero'; limit=(symbol['value']&~1)+(symbol['size'] or len(e.text)); raw=subprocess.check_output([OBJDUMP,'-d','--no-show-raw-insn',str(path)],text=True); rows=[];rr={r['offset']:r for r in e.relocs}
 for line in raw.splitlines():
  m=re.match(r'\s*([0-9a-f]+):\s+(\S+)\s*(.*)',line)
  if not m:continue
  a=int(m[1],16);op=m[2].removesuffix('.n');arg=m[3].split('@')[0].strip()
  if op.startswith('.')or a>=limit:continue
  target=None
  if op in COND|{'b'}:target=int(re.match('[0-9a-f]+',arg)[0],16)
  norm=re.sub(r'\b(?:r\d+|sl|sb|ip)\b','R',arg)
  if op=='bl':norm=rr[a]['symbol']['name']if a in rr else 'LOCAL_CALL'
  if op in COND|{'b'}:norm='TARGET'
  if op=='ldr'and'[pc,'in arg:
   imm=int(re.search(r'\[pc, #(\d+)\]',arg)[1]);site=((a+4)&~3)+imm;norm='LITERAL '+(rr[site]['symbol']['name']if site in rr else hex(int.from_bytes(e.text[site:site+4],'little')))
  rows.append({'offset':a,'op':op,'args':arg,'norm':op+' '+norm,'target':target})
 index={r['offset']:i for i,r in enumerate(rows)};starts={0}
 for i,r in enumerate(rows):
  if r['target']is not None:starts.add(r['target'])
  if r['op']in COND|{'b','bx'}or(r['op']=='pop'and'pc'in r['args']):
   if i+1<len(rows):starts.add(rows[i+1]['offset'])
 starts=sorted(s for s in starts if s in index);blocks={}
 for j,a in enumerate(starts):
  end=starts[j+1]if j+1<len(starts)else limit;ins=[r for r in rows if a<=r['offset']<end];last=ins[-1];edges={}
  nxt=rows[index[last['offset']]+1]['offset']if index[last['offset']]+1<len(rows)else None
  if last['op']in COND:edges={'taken':last['target'],'fallthrough':nxt}
  elif last['op']=='b':edges={'jump':last['target']}
  elif last['op']=='bx'or(last['op']=='pop'and'pc'in last['args']):pass
  elif nxt is not None:edges={'next':nxt}
  effects=[r for r in ins if r['op'].startswith(('ldr','str'))or r['op']in {'bl','push','pop'}]
  blocks[a]={'offset':a,'instructions':ins,'effects':effects,'edges':edges}
 return e,blocks
A,aa=read(args.reference);B,bb=read(args.candidate)
rom=args.rom.read_bytes();assert hashlib.sha1(rom).hexdigest()=='6f478a455383a2a12378f292581dfd7300300700', 'unexpected EU ROM';mask=relocation_mask(A.text,A.relocs);off=0xF06C;assert all(not x or A.text[i]==rom[off+i]for i,x in enumerate(mask))
# Ordered traversal compares actual edge structure. Stop on first incompatible terminator/arity;
# retaining differing instructions/effects separately avoids claiming graph equivalence.
queue=collections.deque([(0,0,[])]);seen=set();mapped={};reverse_mapped={};differences=[];failure=None
while queue:
 a,b,route=queue.popleft()
 if(a,b)in seen:continue
 seen.add((a,b));x,y=aa[a],bb[b]
 if a in mapped and mapped[a]!=b:failure={'reason':'join mismatch','reference':a,'candidate':b,'previous_candidate':mapped[a],'route':route};break
 if b in reverse_mapped and reverse_mapped[b]!=a:failure={'reason':'reverse join mismatch','reference':a,'candidate':b,'previous_reference':reverse_mapped[b],'route':route};break
 mapped[a]=b;reverse_mapped[b]=a
 xe=[r['norm']for r in x['effects']];ye=[r['norm']for r in y['effects']]
 if xe!=ye:differences.append({'reference':a,'candidate':b,'route':route,'reference_effects':xe,'candidate_effects':ye})
 if set(x['edges'])!=set(y['edges']) or ('taken' in x['edges'] and x['instructions'][-1]['op']!=y['instructions'][-1]['op']):
  failure={'reason':'terminator/edges mismatch','reference':a,'candidate':b,'route':route,'reference_block':x,'candidate_block':y};break
 for k in x['edges']:queue.append((x['edges'][k],y['edges'][k],route+[k]))
result={'reference_fixed_bytes_equal_owned_EU':True,'reference_base':hex(0x0800F06C),'reference_blocks':len(aa),'candidate_blocks':len(bb),'paired_before_failure':len(seen),'first_effect_difference':differences[0]if differences else None,'first_graph_failure':failure,'reference_graph':aa,'candidate_graph':bb}
args.out.parent.mkdir(parents=True,exist_ok=True)
args.out.write_text(json.dumps(result,indent=2),encoding='utf-8')
summary={k:v for k,v in result.items()if not k.endswith('_graph')};print(json.dumps(summary,indent=2))
