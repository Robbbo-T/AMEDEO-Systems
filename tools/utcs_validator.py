"""UTCS-MI v5.0+ strict validator (agents manifest aware)"""
import yaml
import hashlib
import re
from pathlib import Path
import sys



def validate_manifest(manifest_path="agents/manifest.yaml") -> bool:
    path = Path(manifest_path)
    if not path.exists():
        print(f"❌ Manifest not found: {manifest_path}")
        return False

    with open(path, "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    errors = []
    warnings = []

    # Basic headers present
    for field in ("utcs_mi_version", "artifacts"):
        if field not in manifest:
            errors.append(f"Missing manifest field: {field}")

    # Artifacts must exist and hash must be computable (store/print actual)
    base = Path(__file__).parent.parent
    for art in manifest.get("artifacts", []):
        apath = base / art.get("path", "")
        if not apath.exists():
            errors.append(f"Artifact missing: {art.get('path')}")
            continue
        with open(apath, "rb") as af:
            actual_hash = f"sha256:{hashlib.sha256(af.read()).hexdigest()[:8]}"
        # Print hash for traceability
        print(f"📄 {art.get('path')}: {art.get('utcs_id','?')} -> {actual_hash}")

    if errors:
        print("❌ UTCS-MI validation failed:")
        for e in errors:
            print(f"   {e}")
        return False

    print("✅ UTCS-MI validation passed")
    return True


if __name__ == "__main__":
    ok = validate_manifest()
    sys.exit(0 if ok else 1)
