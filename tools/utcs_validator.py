"""UTCS-MI v5.0+ strict validator"""
import yaml
import hashlib
import re
from pathlib import Path
import sys

VALID_TYPES = ["Codigo", "Prueba", "Documento", "Especificacion", "Gobernanza"]
VALID_ORIGINS = ["Manual", "Hibrida", "Autogenesis"]
VALID_STATES = ["Desarrollo", "Validacion", "Certificacion", "Operacion"]
HASH_PATTERN = re.compile(r"^sha256:[a-f0-9]{8}$")

def validate_manifest(manifest_path="agents/manifest.yaml"):
    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)
    
    errors = []
    warnings = []
    
    # Check version
    if manifest.get("version") != "5.0+":
        errors.append(f"Invalid UTCS version: {manifest.get('version')}")
    
    for artifact in manifest.get("artifacts", []):
        aid = artifact.get("id", "unknown")
        
        # Required fields
        required = ["id", "path", "type", "origin", "hash", "state"]
        for field in required:
            if field not in artifact:
                errors.append(f"{aid}: missing required field '{field}'")
        
        # Validate enums
        if artifact.get("type") not in VALID_TYPES:
            errors.append(f"{aid}: invalid type '{artifact.get('type')}'")
        
        if artifact.get("origin") not in VALID_ORIGINS:
            errors.append(f"{aid}: invalid origin '{artifact.get('origin')}'")
            
        if artifact.get("state") not in VALID_STATES:
            errors.append(f"{aid}: invalid state '{artifact.get('state')}'")
        
        # Validate hash format
        hash_value = artifact.get("hash", "")
        if hash_value == "sha256:placeholder":
            # Generate actual hash for placeholder
            path = artifact.get("path")
            if path and Path(path).exists():
                with open(path, "rb") as f:
                    actual_hash = f"sha256:{hashlib.sha256(f.read()).hexdigest()[:8]}"
                    warnings.append(f"{aid}: using placeholder hash, actual: {actual_hash}")
        elif not HASH_PATTERN.match(hash_value):
            errors.append(f"{aid}: invalid hash format")
        else:
            # Verify actual file hash
            path = artifact.get("path")
            if path and Path(path).exists():
                with open(path, "rb") as f:
                    actual_hash = f"sha256:{hashlib.sha256(f.read()).hexdigest()[:8]}"
                    if artifact.get("hash") != actual_hash:
                        errors.append(f"{aid}: hash mismatch (expected {artifact.get('hash')}, got {actual_hash})")
            elif path:
                warnings.append(f"{aid}: file not found at {path}")
    
    # Print results
    if warnings:
        print("⚠️  UTCS-MI warnings:")
        for w in warnings:
            print(f"   {w}")
    
    if errors:
        print("❌ UTCS-MI validation failed:")
        for e in errors:
            print(f"   {e}")
        sys.exit(1)
    else:
        print(f"✅ UTCS-MI validation passed: {len(manifest.get('artifacts', []))} artifacts compliant")
        return True

if __name__ == "__main__":
    validate_manifest()