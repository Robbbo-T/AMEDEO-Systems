#!/usr/bin/env python3
"""
UTCS-MI: AQUART-TOOL-VALIDATOR-utcs_agents-v1.0
Enhanced UTCS validator for AMEDEO agent artifacts
"""

import json
import os
import sys
import hashlib
from pathlib import Path
import yaml


def validate_agent_manifest():
    """Validate UTCS-MI compliance for agent artifacts"""
    
    print("🔍 UTCS-MI Agent Validation")
    print("=" * 40)
    
    # Load agent manifest
    manifest_path = Path(__file__).parent.parent / "agents" / "manifest.yaml"
    if not manifest_path.exists():
        print(f"❌ Agent manifest not found: {manifest_path}")
        return False
    
    with open(manifest_path, 'r') as f:
        manifest = yaml.safe_load(f)
    
    errors = []
    warnings = []
    
    # Validate manifest structure
    required_fields = ["utcs_mi_version", "agents", "infrastructure", "validation_gates"]
    for field in required_fields:
        if field not in manifest:
            errors.append(f"Missing required field: {field}")
    
    # Validate agents
    if "agents" in manifest:
        for agent in manifest["agents"]:
            # Check required agent fields
            required_agent_fields = ["id", "type", "depth_dimension", "capabilities", "min_impact_factor"]
            for field in required_agent_fields:
                if field not in agent:
                    errors.append(f"Agent {agent.get('id', 'unknown')} missing field: {field}")
            
            # Validate UTCS-MI ID format
            if "id" in agent:
                if not agent["id"].startswith("AQUART-AGT-"):
                    errors.append(f"Agent {agent['id']} has invalid UTCS-MI ID format")
                if not agent["id"].endswith("-v1.0"):
                    warnings.append(f"Agent {agent['id']} should end with version")
            
            # Validate minimum impact factor
            if agent.get("min_impact_factor", 0) < 3.0:
                errors.append(f"Agent {agent.get('id')} has insufficient min_impact_factor: {agent.get('min_impact_factor')}")
    
    # Validate artifacts exist
    if "artifacts" in manifest:
        base_path = Path(__file__).parent.parent
        for artifact in manifest["artifacts"]:
            if "path" in artifact:
                artifact_path = base_path / artifact["path"]
                if not artifact_path.exists():
                    errors.append(f"Artifact file missing: {artifact['path']}")
                else:
                    # Calculate hash if file exists
                    with open(artifact_path, 'rb') as f:
                        content = f.read()
                        actual_hash = f"sha256:{hashlib.sha256(content).hexdigest()[:8]}"
                        
                    # Note: In production, would validate against stored hash
                    print(f"📄 {artifact['path']}: {actual_hash}")
    
    # Validate cascade requirements
    if "cascade_requirements" in manifest:
        cascade = manifest["cascade_requirements"]
        if cascade.get("individual_minimum", 0) < 3.0:
            errors.append("Cascade individual_minimum must be >= 3.0")
        if cascade.get("cascade_total_minimum", 0) < 81.0:
            errors.append("Cascade total_minimum must be >= 81.0 (3^4)")
    
    # Print results
    if warnings:
        print("⚠️  UTCS-MI warnings:")
        for w in warnings:
            print(f"   {w}")
    
    if errors:
        print("❌ UTCS-MI validation failed:")
        for e in errors:
            print(f"   {e}")
        return False
    else:
        agent_count = len(manifest.get("agents", []))
        artifact_count = len(manifest.get("artifacts", []))
        print(f"✅ UTCS-MI validation passed: {agent_count} agents, {artifact_count} artifacts compliant")
        return True


def validate_policy_compliance():
    """Validate policy compliance"""
    
    policy_path = Path(__file__).parent.parent / "agents" / "POLICY.md"
    if not policy_path.exists():
        print("❌ POLICY.md not found")
        return False
    
    with open(policy_path, 'r') as f:
        policy_content = f.read()
    
    # Check for key policy elements
    required_elements = [
        "hacen recados",
        "bordean el futuro",
        "profundidad",
        "decisiones, ritmos o límites",
        "≥ 3×",
        "AMOReS",
        "DET",
        "PQC"
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in policy_content:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ Policy missing elements: {missing_elements}")
        return False
    
    print("✅ Policy compliance validated")
    return True


if __name__ == "__main__":
    manifest_ok = validate_agent_manifest()
    policy_ok = validate_policy_compliance()
    
    success = manifest_ok and policy_ok
    
    if success:
        print("\n🎉 All UTCS-MI agent validations passed!")
    else:
        print("\n💥 UTCS-MI agent validation failed!")
    
    sys.exit(0 if success else 1)