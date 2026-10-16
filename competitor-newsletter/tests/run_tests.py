#!/usr/bin/env python3
"""Check validate.py against the fixtures.

- data/sample must pass.
- The whole repo (data/items, data/sample, data/digest.js) must pass.
- Every entry in tests/bad_fixtures must fail, and the output must name the rule given
  by its rNN_ prefix.

Usage: python tests/run_tests.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VALIDATE = ROOT / "scripts" / "validate.py"


def run(*args: str) -> tuple[int, str]:
    proc = subprocess.run([sys.executable, str(VALIDATE), *args], capture_output=True, text=True, cwd=ROOT)
    return proc.returncode, proc.stdout + proc.stderr


def main() -> int:
    failures = 0

    for label, args in (("data/sample passes", ["data/sample"]), ("whole repo passes", [])):
        code, out = run(*args)
        ok = code == 0
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {label}")
        if not ok:
            print("      " + out.strip().replace("\n", "\n      "))

    for fixture in sorted((ROOT / "tests" / "bad_fixtures").iterdir()):
        m = re.match(r"r(\d+)_", fixture.name)
        if not m:
            continue
        rule = int(m.group(1))
        code, out = run(str(fixture))
        named = re.findall(r"FAIL rule (\d+) ", out)
        ok = code == 1 and str(rule) in named
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {fixture.name}: expected rule {rule}, exit {code}, rules named {sorted(set(named), key=int)}")
        if not ok:
            print("      " + out.strip().replace("\n", "\n      "))

    print(f"\n{'All checks passed.' if not failures else f'{failures} check(s) failed.'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
