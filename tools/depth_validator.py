#!/usr/bin/env python3
"""
UTCS-MI: AQUART-TOOL-VALIDATOR-depth_check-v1.0
Depth validator for AMEDEO agent actions
"""

import sys
import json
from pathlib import Path
import importlib.util

# Add agents to path
agents_path = Path(__file__).parent.parent / "agents"
sys.path.insert(0, str(agents_path))

from base_agent import Intent
from planner_agent import StrategicPlannerAgent
from buyer_agent import SupplyBuyerAgent
from scheduler_agent import ResourceSchedulerAgent
from ops_pilot_agent import OpsPilotAgent


MIN_INDIVIDUAL_DEPTH = 3.0
MIN_CASCADE_DEPTH = 81.0  # 3^4


def validate_agent_depth():
    """Validate that all agents meet depth requirements"""
    
    print("🧪 AMEDEO Agent Depth Validation")
    print("=" * 50)
    
    # Test agent specifications
    agents_specs = [
        (StrategicPlannerAgent, "HORIZON_SHIFT", {
            "affects_strategy": True,
            "expected_gain": 4.2
        }),
        (SupplyBuyerAgent, "SUPPLY_CHAIN_METAMORPHOSIS", {
            "affects_tempo": True,
            "carbon_limit": 1000
        }),
        (ResourceSchedulerAgent, "ELASTIC_CAPACITY_TRANSFORM", {
            "expands_envelope": True,
            "qubit_pool_size": 64
        }),
        (OpsPilotAgent, "OPERATIONAL_ENVELOPE_EXPANSION", {
            "expands_envelope": True,
            "entanglement_layers": 3
        })
    ]
    
    results = []
    total_impact = 1.0
    
    print("\n📊 Individual Agent Depth Tests:")
    
    for i, (AgentClass, kind, payload) in enumerate(agents_specs):
        agent = AgentClass(f"depth-test-{i}", "agents/POLICY.md")
        intent = Intent(kind, payload)
        result = agent.execute(intent)
        
        if result.productivity_delta < MIN_INDIVIDUAL_DEPTH:
            print(f"❌ {agent.id} failed depth test: {result.productivity_delta:.1f}x < {MIN_INDIVIDUAL_DEPTH}x")
            return False
        else:
            print(f"✅ {agent.id}: {result.productivity_delta:.1f}x depth achieved")
            
        results.append(result)
        total_impact *= result.productivity_delta
    
    print(f"\n🚀 Cascade Impact Analysis:")
    print(f"   Individual impacts: {[f'{r.productivity_delta:.1f}x' for r in results]}")
    print(f"   Total cascade: {total_impact:.1f}x")
    
    if total_impact < MIN_CASCADE_DEPTH:
        print(f"❌ Cascade depth insufficient: {total_impact:.1f}x < {MIN_CASCADE_DEPTH}x")
        return False
    
    print(f"✅ Cascade depth requirement met: {total_impact:.1f}x ≥ {MIN_CASCADE_DEPTH}x")
    
    # Generate evidence
    evidence = {
        "validation_timestamp": "2024-08-20T09:19:00Z",
        "depth_metrics": {
            "all_agents_min_3x": all(r.productivity_delta >= MIN_INDIVIDUAL_DEPTH for r in results),
            "cascade_total": total_impact,
            "individual_deltas": [r.productivity_delta for r in results]
        },
        "agents_tested": len(agents_specs),
        "validation_passed": True
    }
    
    # Save evidence
    with open("det_evidence.json", "w") as f:
        json.dump(evidence, f, indent=2)
    
    print(f"\n📋 Evidence saved to det_evidence.json")
    print(f"✅ All depth requirements validated successfully")
    
    return True


if __name__ == "__main__":
    success = validate_agent_depth()
    sys.exit(0 if success else 1)