#!/usr/bin/env python3
import json, os, sys

MANIFEST_PATH = os.path.join(os.path.dirname(__file__), '..', 'UTCS', 'manifest.json')

EXPECTED_PREFIX = "EstándarUniversal:"
EXPECTED_SEGMENTS = 13  # fields separated by '-'

def canonical_ok(ident: str) -> bool:
    if not isinstance(ident, str):
        return False
    if not ident.startswith(EXPECTED_PREFIX):
        return False
    payload = ident[len(EXPECTED_PREFIX):]
    parts = payload.split('-')
    return len(parts) == EXPECTED_SEGMENTS and all(len(p) > 0 for p in parts)

def main() -> int:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    man_path = os.path.abspath(MANIFEST_PATH)
    if not os.path.exists(man_path):
        print(f"[UTCS] manifest not found: {man_path}")
        return 2
    with open(man_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    ok = True
    for rel, ident in sorted(data.items()):
        path = os.path.join(root, rel)
        if not canonical_ok(ident):
            print(f"[UTCS FAIL] {rel}: invalid canonical identifier")
            ok = False
        if not os.path.exists(path):
            print(f"[UTCS FAIL] {rel}: file missing")
            ok = False
    if ok:
        print(f"[UTCS OK] {len(data)} artifacts validated.")
        return 0
    return 1

if __name__ == '__main__':
    sys.exit(main())
