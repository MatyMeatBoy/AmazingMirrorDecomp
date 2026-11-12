import importlib.util
from pathlib import Path
import unittest

PATH = Path(__file__).resolve().parents[1]/'tools/progress/data_inventory.py'
spec = importlib.util.spec_from_file_location('data_inventory', PATH)
m = importlib.util.module_from_spec(spec)
if PATH.exists():
    spec.loader.exec_module(m)


class DataInventoryTests(unittest.TestCase):
    def test_union_does_not_double_count_overlaps(self):
        self.assertEqual(m.union_bytes([(0, 8), (4, 12), (20, 22)]), 14)

    def test_ranges_are_offsets_not_symbol_guesses(self):
        text = 'gAsset::\n .incbin "baserom.gba", 0x10, 0x20\n .incbin "asset.bin"\n'
        self.assertEqual(m.raw_ranges(text), [{'symbol':'gAsset', 'offset':16, 'size':32, 'line':2}])

    def test_unknown_expression_is_rejected(self):
        with self.assertRaises(ValueError):
            m.raw_ranges('.incbin "baserom.gba", START, 20')


if __name__ == '__main__':
    unittest.main()
