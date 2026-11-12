from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
MAKE = shutil.which('make')


@unittest.skipUnless(MAKE, 'GNU make is required')
class RegionDispatchTests(unittest.TestCase):
    def dry(self, *args):
        return subprocess.run([MAKE,'-n',*args],cwd=ROOT,text=True,capture_output=True)

    def test_default_compare_uses_owned_europe_profile(self):
        result = self.dry('compare')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('eu_build.py',result.stdout)
        self.assertIn('baserom_eu.gba',result.stdout)
        self.assertNotIn('katam.sha1',result.stdout)

    def test_usa_is_explicit_and_retains_original_checksum(self):
        result = self.dry('REGION=us','NODEP=1','SETUP_PREREQS=0','-o','katam.gba','compare')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('katam.sha1',result.stdout)
        self.assertNotIn('eu_build.py',result.stdout)

    def test_unknown_region_rejected(self):
        result = self.dry('REGION=wrong','compare')
        self.assertNotEqual(result.returncode,0)
        self.assertIn('Unsupported REGION',result.stderr)
