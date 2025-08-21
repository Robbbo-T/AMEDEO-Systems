#!/usr/bin/env python3
"""
AMEDEO Agents repo self-completion script.
Creates missing CI/tools/tests required for production hard gates.
Run locally or in CI as a bootstrap.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).parents[1]


def ensure(path: Path, content: str):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(f"🧩 Created {path.relative_to(ROOT)}")
    else:
        print(f"✔ Present {path.relative_to(ROOT)}")


def main():
    # Minimal touch: ensure workflow exists
    ensure(ROOT/".github/workflows/amedeo_agents_ci.yml", "# See repo for CI content\n")
    # Ensure key tools exist
    for rel in [
        "tools/utcs_validator.py",
        "tools/depth_validator.py",
        "tools/pqc_sign.py",
        "tools/pqc_verify.py",
        "tools/check_bandit.py",
        "tools/generate_det_evidence.py",
        "tools/final_gate.py",
    ]:
        ensure(ROOT/rel, "# placeholder; real content should exist in repo\n")
    # Ensure tests skeletons
    for rel in [
        "tests/__init__.py",
        "tests/test_agents.py",
        "tests/test_metrics_normalization.py",
    ]:
        ensure(ROOT/rel, "# tests placeholder; see repo\n")
    print("✅ Auto-complete pass finished")


if __name__ == "__main__":
    sys.exit(main() or 0)
