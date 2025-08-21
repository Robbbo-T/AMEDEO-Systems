#!/usr/bin/env python3
"""Comprehensive agent tests (cascade + individual)"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from base_agent import Intent, DET
from planner_agent import StrategicPlannerAgent
from buyer_agent import SupplyBuyerAgent
from scheduler_agent import ResourceSchedulerAgent
from ops_pilot_agent import OpsPilotAgent


@pytest.mark.parametrize("agent_class,kind,payload", [
    (StrategicPlannerAgent, "HORIZON_SHIFT", {"affects_strategy": True, "expected_gain": 4.2}),
    (SupplyBuyerAgent, "SUPPLY_CHAIN_METAMORPHOSIS", {"affects_tempo": True, "expected_gain": 4.0}),
    (ResourceSchedulerAgent, "ELASTIC_CAPACITY_TRANSFORM", {"expands_envelope": True, "expected_gain": 4.0}),
    (OpsPilotAgent, "OPERATIONAL_ENVELOPE_EXPANSION", {"expands_envelope": True, "expected_gain": 4.0}),
])
def test_agent_depth_requirements(agent_class, kind, payload):
    agent = agent_class("test-agent", "agents/POLICY.md")
    intent = Intent(kind=kind, payload=payload)
    res = agent.execute(intent)
    assert res.productivity_delta >= 3.0


def test_cascade_impact():
    agents = [
        StrategicPlannerAgent("planner", "agents/POLICY.md"),
        SupplyBuyerAgent("buyer", "agents/POLICY.md"),
        ResourceSchedulerAgent("scheduler", "agents/POLICY.md"),
        OpsPilotAgent("pilot", "agents/POLICY.md"),
    ]

    intents = [
        Intent("HORIZON_SHIFT", {"affects_strategy": True, "expected_gain": 4.2}),
        Intent("SUPPLY_CHAIN_METAMORPHOSIS", {"affects_tempo": True, "expected_gain": 4.0}),
        Intent("ELASTIC_CAPACITY_TRANSFORM", {"expands_envelope": True, "expected_gain": 4.0}),
        Intent("OPERATIONAL_ENVELOPE_EXPANSION", {"expands_envelope": True, "expected_gain": 4.0}),
    ]

    total = 1.0
    traces = []
    for ag, it in zip(agents, intents):
        r = ag.execute(it)
        total *= r.productivity_delta
        traces.append(r.trace_id)

    assert total >= 81.0
    assert DET.verify_cascade_trace(traces)
