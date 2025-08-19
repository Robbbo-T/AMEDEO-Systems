"""Test agent depth validation and cascade calculations"""
import sys
sys.path.append('.')

from agents.intents import Intent
from agents.planner_agent import StrategicPlannerAgent
from agents.buyer_agent import SupplyBuyerAgent
from agents.scheduler_agent import ResourceSchedulerAgent
from agents.ops_pilot_agent import OpsPilotAgent

class TestAgentDepth:
    """Test agent depth requirements and cascade calculations."""

    def test_strategic_planner_depth(self):
        """Test Strategic Planner Agent meets depth requirements."""
        agent = StrategicPlannerAgent("test-planner", "agents/POLICY.md")
        intent = Intent("HORIZON_SHIFT", {"affects_strategy": True})
        result = agent.execute(intent)

        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0
        assert result.metadata["agent_id"] == "test-planner"

    def test_supply_buyer_depth(self):
        """Test Supply Buyer Agent meets depth requirements."""
        agent = SupplyBuyerAgent("test-buyer", "agents/POLICY.md")
        intent = Intent("SUPPLY_CHAIN_METAMORPHOSIS", {"affects_tempo": True})
        result = agent.execute(intent)

        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0
        assert result.metadata["agent_id"] == "test-buyer"

    def test_resource_scheduler_depth(self):
        """Test Resource Scheduler Agent meets depth requirements."""
        agent = ResourceSchedulerAgent("test-scheduler", "agents/POLICY.md")
        intent = Intent("ELASTIC_CAPACITY_TRANSFORM", {"expands_envelope": True})
        result = agent.execute(intent)

        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0
        assert result.metadata["agent_id"] == "test-scheduler"

    def test_ops_pilot_depth(self):
        """Test Ops Pilot Agent meets depth requirements."""
        agent = OpsPilotAgent("test-ops", "agents/POLICY.md")
        intent = Intent("OPERATIONAL_ENVELOPE_EXPANSION", {"expands_envelope": True})
        result = agent.execute(intent)

        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0
        assert result.metadata["agent_id"] == "test-ops"

    def test_cascade_depth_calculation(self):
        """Test that agent cascade meets minimum requirements."""
        agents_specs = [
            (StrategicPlannerAgent, "HORIZON_SHIFT", {"affects_strategy": True}),
            (SupplyBuyerAgent, "SUPPLY_CHAIN_METAMORPHOSIS", {"affects_tempo": True}),
            (ResourceSchedulerAgent, "ELASTIC_CAPACITY_TRANSFORM", {"expands_envelope": True}),
            (OpsPilotAgent, "OPERATIONAL_ENVELOPE_EXPANSION", {"expands_envelope": True})
        ]

        total_impact = 1.0
        results = []

        for i, (agent_class, kind, payload) in enumerate(agents_specs):
            agent = agent_class(f"cascade-test-{i}", "agents/POLICY.md")
            intent = Intent(kind, payload)
            result = agent.execute(intent)

            results.append(result)
            total_impact *= result.productivity_delta

            # Each agent must meet individual depth requirement
            assert result.productivity_delta >= 3.0

        # Cascade must meet minimum requirement (3^4 = 81)
        assert total_impact >= 81.0

        # Verify all agents executed successfully
        assert len(results) == 4
        assert all(r.status == "SUCCESS" for r in results)

    def test_intent_validation(self):
        """Test intent validation and error handling."""
        agent = StrategicPlannerAgent("test-validation", "agents/POLICY.md")

        # Test with invalid intent
        result = agent.execute("not_an_intent")
        assert result.status == "ERROR"
        assert "error" in result.metadata

        # Test with valid intent but minimal payload
        intent = Intent("UNKNOWN_KIND", {})
        result = agent.execute(intent)
        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0  # Should still meet depth requirement

    def test_agent_metadata(self):
        """Test that agents provide proper metadata."""
        agent = StrategicPlannerAgent("test-metadata", "agents/POLICY.md")
        intent = Intent("HORIZON_SHIFT", {"affects_strategy": True})
        result = agent.execute(intent)

        assert result.metadata is not None
        assert "agent_id" in result.metadata
        assert "execution_time" in result.metadata
        assert "intent_kind" in result.metadata
        assert result.metadata["agent_id"] == "test-metadata"
        assert result.metadata["intent_kind"] == "HORIZON_SHIFT"
