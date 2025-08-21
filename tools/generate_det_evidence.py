"""Generate DET evidence for CI/CD"""
import json
from agents.base_agent import Intent
from agents.planner_agent import StrategicPlannerAgent
from agents.buyer_agent import SupplyBuyerAgent
from agents.scheduler_agent import ResourceSchedulerAgent
from agents.ops_pilot_agent import OpsPilotAgent


def generate_evidence() -> str:
    agents_specs = [
        (StrategicPlannerAgent, "HORIZON_SHIFT", {"affects_strategy": True, "expected_gain": 4.2}),
        (SupplyBuyerAgent, "SUPPLY_CHAIN_METAMORPHOSIS", {"affects_tempo": True, "expected_gain": 4.0}),
        (ResourceSchedulerAgent, "ELASTIC_CAPACITY_TRANSFORM", {"expands_envelope": True, "expected_gain": 4.0}),
        (OpsPilotAgent, "OPERATIONAL_ENVELOPE_EXPANSION", {"expands_envelope": True, "expected_gain": 4.0})
    ]

    results = []
    total_impact = 1.0
    productivity_deltas = []

    for i, (AgentClass, kind, payload) in enumerate(agents_specs):
        agent = AgentClass(f"evidence-{i}", "agents/POLICY.md")
        intent = Intent(kind=kind, payload=payload)
        res = agent.execute(intent)
        results.append({
            "agent": AgentClass.__name__,
            "intent": kind,
            "status": res.status,
            "productivity_delta": res.productivity_delta,
            "trace_id": res.trace_id,
        })
        total_impact *= res.productivity_delta
        min_impact = min(min_impact, res.productivity_delta)

    evidence = {
        "depth_metrics": {
            "all_agents_min_3x": min_impact >= 3.0,
            "min_individual_impact": min_impact,
            "cascade_total": total_impact,
            "cascade_meets_81x": total_impact >= 81.0
        },
        "agent_results": results,
    }
    return json.dumps(evidence, indent=2)


if __name__ == "__main__":
    print(generate_evidence())
