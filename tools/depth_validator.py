"""Depth validation with hard gates"""
import sys
import yaml
sys.path.append('.')

from agents.intents import Intent
from agents.planner_agent import StrategicPlannerAgent
from agents.buyer_agent import SupplyBuyerAgent
from agents.scheduler_agent import ResourceSchedulerAgent
from agents.ops_pilot_agent import OpsPilotAgent

MIN_INDIVIDUAL_DEPTH = 3.0
MIN_CASCADE_DEPTH = 81.0  # 3^4

def validate_depth():
    # Load target from manifest
    with open("agents/manifest.yaml") as f:
        manifest = yaml.safe_load(f)
    
    orchestrator = manifest.get("orchestrator", {})
    target_cascade = float(orchestrator.get("min_total_impact", MIN_CASCADE_DEPTH))
    
    agents_specs = [
        (StrategicPlannerAgent, "HORIZON_SHIFT", {"affects_strategy": True}),
        (SupplyBuyerAgent, "SUPPLY_CHAIN_METAMORPHOSIS", {"affects_tempo": True}),
        (ResourceSchedulerAgent, "ELASTIC_CAPACITY_TRANSFORM", {"expands_envelope": True}),
        (OpsPilotAgent, "OPERATIONAL_ENVELOPE_EXPANSION", {"expands_envelope": True})
    ]
    
    results = []
    total_impact = 1.0
    
    for i, (AgentClass, kind, payload) in enumerate(agents_specs):
        agent = AgentClass(f"test-{i}", "agents/POLICY.md")
        intent = Intent(kind, payload)
        result = agent.execute(intent)
        
        if result.productivity_delta < MIN_INDIVIDUAL_DEPTH:
            print(f"❌ {agent.id} failed depth test: {result.productivity_delta:.1f}x < {MIN_INDIVIDUAL_DEPTH}x")
            sys.exit(1)
        
        results.append(result)
        total_impact *= result.productivity_delta
        print(f"✅ {AgentClass.__name__}: {result.productivity_delta:.1f}x depth")
    
    if total_impact < target_cascade:
        print(f"❌ Cascade failed: {total_impact:.1f}x < {target_cascade}x")
        sys.exit(1)
    
    print(f"✅ Cascade depth: {total_impact:.1f}x ≥ {target_cascade}x")
    print("✅ All depth requirements met!")
    return True

if __name__ == "__main__":
    validate_depth()