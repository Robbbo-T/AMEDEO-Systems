"""Final validation gate - hard requirements aggregation"""
import json
import sys
from pathlib import Path


HARD_GATES = {
    "min_individual_depth": 3.0,
    "min_cascade_depth": 81.0,
}


def check_gates() -> bool:
    failures = []

    # DET evidence
    det = Path("det_evidence.json")
    if det.exists():
        evidence = json.loads(det.read_text())
        dm = evidence.get("depth_metrics", {})
        if not dm.get("all_agents_min_3x", False):
            failures.append("Depth requirement not met (min < 3x)")
        if dm.get("cascade_total", 0.0) < HARD_GATES["min_cascade_depth"]:
            failures.append("Cascade depth < 81x")
    else:
        failures.append("DET evidence not found")

    # SBOM
    if not Path("sbom.spdx.json").exists():
        failures.append("SBOM not generated")

    # Signatures
    if not Path("signatures.json").exists():
        failures.append("PQC signatures not found")

    if failures:
        print("❌ Final gate FAILED:")
        for f in failures:
            print(f"   - {f}")
        return False
    print("✅ Final gate PASSED - All hard requirements met")
    return True


if __name__ == "__main__":
    ok = check_gates()
    sys.exit(0 if ok else 1)
