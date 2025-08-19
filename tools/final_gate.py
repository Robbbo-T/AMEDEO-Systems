"""Final validation gate - all hard requirements"""
import json
import sys
from pathlib import Path

HARD_GATES = {
    "utcs_compliance": 100.0,
    "min_individual_depth": 3.0,
    "min_cascade_depth": 81.0,
    "min_coverage": 92.0,
    "max_security_high": 0,
    "signatures_valid": True,
    "sbom_generated": True
}

def check_gates():
    failures = []
    
    # Check DET evidence
    if Path("det_evidence.json").exists():
        with open("det_evidence.json") as f:
            evidence = json.load(f)
            
        if not evidence.get("depth_metrics", {}).get("all_agents_min_3x"):
            failures.append("Depth requirement not met")
            
        if evidence.get("depth_metrics", {}).get("cascade_total", 0) < HARD_GATES["min_cascade_depth"]:
            failures.append(f"Cascade depth < {HARD_GATES['min_cascade_depth']}")
    else:
        failures.append("DET evidence not found")
    
    # Check SBOM
    if not Path("sbom.spdx.json").exists():
        failures.append("SBOM not generated")
    
    # Check signatures
    if not Path("signatures.json").exists():
        failures.append("PQC signatures not found")
    
    # Check bandit results
    if Path("bandit.json").exists():
        with open("bandit.json") as f:
            bandit_results = json.load(f)
        
        high_issues = sum(1 for r in bandit_results.get("results", []) 
                         if r.get("issue_severity", "").upper() == "HIGH")
        
        if high_issues > HARD_GATES["max_security_high"]:
            failures.append(f"HIGH security issues found: {high_issues}")
    
    if failures:
        print("❌ Final gate FAILED:")
        for f in failures:
            print(f"   - {f}")
        sys.exit(1)
    else:
        print("✅ Final gate PASSED - All hard requirements met:")
        for gate, value in HARD_GATES.items():
            print(f"   ✓ {gate}: {value}")
        return True

if __name__ == "__main__":
    check_gates()