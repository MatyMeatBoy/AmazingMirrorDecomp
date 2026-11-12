import copy
import importlib.util
from pathlib import Path
import sys
import json
import subprocess
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1] / 'tools/progress'
sys.path.insert(0, str(TOOLS))


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.spec = importlib.util.spec_from_file_location('report', TOOLS / 'report.py')
        self.mod = importlib.util.module_from_spec(self.spec)
        self.spec.loader.exec_module(self.mod)
        self.manifest = {'schema_version': 1, 'scope': 'main_object_text', 'rom_verified': False,
                         'sources': [self.source('src/test.c', 100, [
                             self.symbol('KnownFunction', 0, 60, 'c'),
                             self.symbol('sub_08000100', 60, 30, 'asm')])]}

    def symbol(self, name, offset, size, kind):
        return {'name': name, 'section': '.text', 'offset': offset, 'size': size, 'kind': kind}

    def source(self, name, size, symbols):
        return {'source': name, 'sections': [{'name': '.text', 'size': size}], 'symbols': symbols}

    def test_all_bytes_counted_and_embedded_asm_stays_pending(self):
        report = self.mod.summarize(self.manifest)
        self.assertEqual(report['totals']['bytes'], 100)
        self.assertEqual(report['totals']['c_bytes'], 60)
        self.assertEqual(report['totals']['pending_asm_bytes'], 30)
        self.assertEqual(report['totals']['unattributed_bytes'], 10)
        self.assertEqual(report['totals']['functions'], 2)
        self.assertEqual(report['totals']['named_functions'], 1)
        self.assertFalse(report['rom_match_verified'])

    def test_aliases_are_one_function_and_one_byte_span(self):
        self.manifest['sources'][0]['symbols'].append(self.symbol('Alias', 0, 60, 'c'))
        report = self.mod.summarize(self.manifest)
        self.assertEqual(report['totals']['c_bytes'], 60)
        self.assertEqual(report['totals']['functions'], 2)

    def test_original_asm_and_header_are_separate_from_c(self):
        self.manifest['sources'].append(self.source('asm/crt0.s', 256, [self.symbol('__start', 0, 256, 'asm')]))
        report = self.mod.summarize(self.manifest)
        self.assertEqual(report['excluded_header_bytes'], 188)
        self.assertEqual(report['totals']['bytes'], 168)
        self.assertEqual(report['totals']['original_asm_bytes'], 68)
        self.assertEqual(report['totals']['c_bytes'], 60)

    def test_overlapping_or_out_of_bounds_spans_fail(self):
        for offset, size in [(50, 20), (100, 4), (-1, 4)]:
            with self.subTest(offset=offset):
                m = copy.deepcopy(self.manifest)
                m['sources'][0]['symbols'].append(self.symbol('Other', offset, size, 'c'))
                with self.assertRaises(ValueError):
                    self.mod.summarize(m)

    def test_conflicting_alias_attribution_fails(self):
        self.manifest['sources'][0]['symbols'].append(self.symbol('Alias', 0, 60, 'asm'))
        with self.assertRaises(ValueError):
            self.mod.summarize(self.manifest)

    def test_invalid_metadata_names_sizes_and_sections_fail(self):
        mutations = [
            lambda s: s.update(source='../src/test.c'),
            lambda s: s.update(source='src\\test.c'),
            lambda s: s['sections'].append(dict(s['sections'][0])),
            lambda s: s['sections'][0].update(name=None),
            lambda s: s['sections'][0].update(size=True),
            lambda s: s['symbols'][0].update(size=True),
            lambda s: s['symbols'][0].update(offset=False),
            lambda s: s['symbols'][0].update(name=''),
            lambda s: s['symbols'][0].update(section='.missing'),
            lambda s: s['symbols'][0].update(aliases='WrongType'),
            lambda s: s['symbols'][0].update(section=None),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                m = copy.deepcopy(self.manifest)
                mutate(m['sources'][0])
                with self.assertRaises(ValueError):
                    self.mod.summarize(m)

    def test_builder_alias_names_survive_and_extent_conflicts_fail(self):
        symbol = self.manifest['sources'][0]['symbols'][0]
        symbol.update(name='sub_08000100', aliases=['MeaningfulAlias'])
        report = self.mod.summarize(self.manifest)
        self.assertEqual(report['totals']['named_functions'], 1)
        self.assertEqual(report['modules'][0]['cells'][0]['aliases'], ['MeaningfulAlias', 'sub_08000100'])
        self.manifest['sources'][0]['symbols'].append(self.symbol('Alias', 0, 59, 'c'))
        with self.assertRaises(ValueError):
            self.mod.summarize(self.manifest)

    def test_header_split_counts_original_function_once(self):
        self.manifest['sources'] = [self.source('asm/crt0.s', 256, [self.symbol('__start', 0, 256, 'asm')])]
        self.assertEqual(self.mod.summarize(self.manifest)['totals']['functions'], 1)

    def test_text_prefix_alone_is_not_executable_text_scope(self):
        source = self.manifest['sources'][0]
        source['sections'].append({'name': '.textual_data', 'size': 10})
        source['symbols'].append(dict(self.symbol('Data', 0, 10, 'c'), section='.textual_data'))
        self.assertEqual(self.mod.summarize(self.manifest)['totals']['bytes'], 100)

    def test_invalid_cli_metadata_fails_before_replacing_outputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            metadata = root / 'metadata'
            output = root / 'output'
            metadata.mkdir()
            output.mkdir()
            (metadata / 'manifest.json').write_text(json.dumps({'schema_version': 999}))
            badge = output / 'badge_decompiled.svg'
            badge.write_text('previous-output')
            result = subprocess.run([sys.executable, str(TOOLS / 'report.py'), '--metadata-dir', str(metadata), '--out', str(output)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('unsupported metadata manifest', result.stderr)
            self.assertEqual(badge.read_text(), 'previous-output')
            self.assertEqual(list(output.iterdir()), [badge])

    def test_duplicate_sources_and_false_verification_fail(self):
        for mutation in ('duplicate', 'verified', 'scope'):
            m = copy.deepcopy(self.manifest)
            if mutation == 'duplicate':
                m['sources'].append(copy.deepcopy(m['sources'][0]))
            elif mutation == 'verified':
                m['rom_verified'] = True
            else:
                m['scope'] = 'whole_game'
            with self.assertRaises(ValueError):
                self.mod.summarize(m)

    def test_render_discloses_scope_and_escapes_names(self):
        self.manifest['sources'][0]['symbols'][0]['name'] = 'Unsafe<&Name'
        report = self.mod.summarize(self.manifest)
        svg = self.mod.render.treemap(report)
        self.assertIn('Unsafe&lt;&amp;Name', svg)
        self.assertIn('unlinked', svg)
        self.assertIn('ROM', self.mod.markdown(report))


if __name__ == '__main__':
    unittest.main()
