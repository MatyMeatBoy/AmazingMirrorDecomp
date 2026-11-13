#!/usr/bin/env python3
"""Regenerate European primary views and the separate USA source reference."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def main():
    for args in [
        ['tools/progress/metadata_build.py','--jobs','4','--region','eu'],
        ['tools/progress/metadata_build.py','--jobs','4','--region','us'],
        ['tools/progress/library_metadata.py'],
        ['tools/progress/report.py','--metadata-dir','build/metadata-us','--out','docs/progress/usa'],
        ['tools/progress/eu_report.py','--out','docs/progress'],
    ]:
        subprocess.run([sys.executable,*args],cwd=ROOT,check=True)


if __name__ == '__main__':
    main()
