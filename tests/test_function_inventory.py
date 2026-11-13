import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools/progress'))
import function_inventory as m


class FunctionInventoryTests(unittest.TestCase):
    def inventory(self,root,verified=True):
        modules=[]
        for source,name,kind,aliases in [
            ('src/game.c','CreateThing','c',['CreateThing','Alias']),
            ('src/game.c','sub_08000100','c',['sub_08000100']),
            ('src/draft.c','sub_08000200','asm',['sub_08000200']),
            ('asm/terrain.s','sub_08000300','asm',['sub_08000300']),
            ('src/agb_sram.c','ReadSram','c',['ReadSram']),
            ('asm/libagbsyscall.s','CpuSet','original_asm',['CpuSet']),
            ('asm/crt0.s','IntrMain','original_asm',['IntrMain'])]:
            modules.append({'source':source,'cells':[{'name':name,'aliases':aliases,'kind':kind,'function':True,'named':not name.startswith('sub_'),'size':4}]})
        report={'rom_match_verified':verified,'c_spans':[{'source':'src/game.c','name':'Alias','bytes':4}]} if verified else {'rom_match_verified':False,'c_spans':[]}
        (root/'src').mkdir()
        (root/'src/draft.c').write_text('NAKED void sub_08000200(void) { asm("..."); }\n#else\nvoid sub_08000200(void) { return; }')
        return m.summarize({'modules':modules},report,root)

    def test_domains_states_alias_dedup_and_name_partition(self):
        with tempfile.TemporaryDirectory() as directory:
            r=self.inventory(Path(directory))
        self.assertEqual(r['all']['total'],7)
        self.assertEqual(r['game']['total'],4)
        self.assertEqual(r['sdk']['total'],2)
        self.assertEqual(r['startup']['total'],1)
        self.assertEqual(r['all']['verified_c'],1)
        self.assertEqual(r['all']['c_pending_eu'],2)
        self.assertEqual(r['all']['drafts'],1)
        self.assertEqual(r['all']['pending_asm'],1)
        self.assertEqual(r['all']['original_asm'],2)
        self.assertEqual(r['all']['existing_names']+r['all']['unnamed'],7)
        self.assertIn('SDK',m.svg(r))
        self.assertIn('7',m.markdown(r))
        self.assertIn('#e4bd4c',m.treemap(r))
        self.assertEqual(m.treemap(r).count('<rect x='),7)

    def test_unverified_eu_receipt_never_credits_c(self):
        with tempfile.TemporaryDirectory() as directory:
            r=self.inventory(Path(directory),False)
        self.assertEqual(r['all']['verified_c'],0)
        self.assertEqual(r['all']['c_pending_eu'],3)

    def test_missing_eu_symbol_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with self.assertRaises(ValueError):
                m.summarize({'modules':[]},{'rom_match_verified':True,'c_spans':[{'source':'src/no.c','name':'Missing'}]},root)

    def test_missing_metadata_does_not_invent_total(self):
        with tempfile.TemporaryDirectory() as directory:
            r=m.load(Path(directory),{'rom_match_verified':False,'c_spans':[]})
        self.assertFalse(r['available'])
        self.assertNotIn('all',r)
        self.assertIn('no disponible',m.svg(r))

    def test_naked_wrapper_without_c_alternative_is_not_a_draft(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'src').mkdir()
            (root/'src/only_asm.c').write_text('NAKED void OnlyAsm(void) { asm("..."); }')
            source={'modules':[{'source':'src/only_asm.c','cells':[{'name':'OnlyAsm','aliases':['OnlyAsm'],'kind':'asm','function':True,'named':True,'size':4}]}]}
            r=m.summarize(source,{'rom_match_verified':False,'c_spans':[]},root)
        self.assertEqual(r['all']['drafts'],0)
        self.assertEqual(r['all']['pending_asm'],1)


if __name__=='__main__':unittest.main()
