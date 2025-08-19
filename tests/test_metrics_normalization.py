"""Test metric normalization edge cases"""
import sys
import pytest
sys.path.append('.')

from agents.base_agent import to_factor

class TestMetricsNormalization:
    """Test metric normalization edge cases for coverage."""

    def test_to_factor_gain(self):
        """Test gain mode factor calculation."""
        assert to_factor(4.2, "gain") == 4.2
        assert to_factor(0.5, "gain") == 1.0  # Floor at 1.0
        assert to_factor(-1.0, "gain") == 1.0  # Floor at 1.0
        assert to_factor(1.0, "gain") == 1.0
        assert to_factor(100.0, "gain") == 100.0

    def test_to_factor_reduce(self):
        """Test reduce mode factor calculation."""
        assert to_factor(0.72, "reduce") == pytest.approx(1.389, rel=0.01)  # 1/0.72
        assert to_factor(0.0, "reduce") >= 1e6  # Avoid div by zero
        assert to_factor(1.0, "reduce") >= 1e6  # Perfect reduction = massive gain
        assert to_factor(0.5, "reduce") == pytest.approx(2.0, rel=0.01)  # 1/0.5 = 2
        assert to_factor(0.1, "reduce") == pytest.approx(10.0, rel=0.01)  # 1/0.1 = 10

    def test_to_factor_edge_cases(self):
        """Test edge cases and invalid inputs."""
        # Invalid mode
        assert to_factor(5.0, "invalid") == 1.0
        assert to_factor(0.5, "unknown") == 1.0

        # Edge values
        assert to_factor(0.0, "gain") == 1.0
        assert to_factor(-100.0, "gain") == 1.0

        # Very small values in reduce mode
        assert to_factor(1e-10, "reduce") >= 1e6
        assert to_factor(1.0, "reduce") >= 1e6  # Perfect reduction = massive gain

    def test_to_factor_precision(self):
        """Test precision handling in calculations."""
        # Test specific values that should produce exact results
        assert to_factor(0.25, "reduce") == 4.0  # 1/0.25 = 4
        assert to_factor(0.2, "reduce") == 5.0   # 1/0.2 = 5

        # Test values that remain unchanged in gain mode
        assert to_factor(2.5, "gain") == 2.5
        assert to_factor(1.001, "gain") == 1.001

class TestIntentResultCreation:
    """Test Intent and Result class creation for coverage."""

    def test_intent_creation(self):
        """Test Intent creation with various inputs."""
        from agents.intents import Intent

        # Normal creation
        intent = Intent("TEST", {"key": "value"})
        assert intent.kind == "TEST"
        assert intent.payload == {"key": "value"}

        # Creation with non-dict payload
        intent = Intent("TEST", "not_a_dict")
        assert intent.payload == {}

        # Creation with None payload
        intent = Intent("TEST", None)
        assert intent.payload == {}

    def test_result_creation(self):
        """Test Result creation with various inputs."""
        from agents.intents import Result

        # Normal creation
        result = Result("SUCCESS", 3.5)
        assert result.status == "SUCCESS"
        assert result.productivity_delta == 3.5
        assert result.metadata == {}

        # Creation with metadata
        result = Result("SUCCESS", 4.0, {"test": "value"})
        assert result.metadata == {"test": "value"}

        # Creation without metadata
        result = Result("ERROR", 1.0)
        assert result.metadata == {}

class TestAgentErrorHandling:
    """Test agent error handling for edge cases."""

    def test_agent_exception_handling(self):
        """Test that agents handle exceptions gracefully."""
        from agents.planner_agent import StrategicPlannerAgent
        from agents.intents import Intent

        class FailingPlannerAgent(StrategicPlannerAgent):
            def _execute_core(self, intent):
                raise ValueError("Simulated failure")

        agent = FailingPlannerAgent("test-failing", "agents/POLICY.md")
        intent = Intent("TEST", {})
        result = agent.execute(intent)

        assert result.status == "ERROR"
        assert result.productivity_delta == 1.0
        assert "error" in result.metadata
        assert "Simulated failure" in result.metadata["error"]

    def test_agent_with_missing_policy(self):
        """Test agent creation with non-existent policy file."""
        from agents.planner_agent import StrategicPlannerAgent
        from agents.intents import Intent

        # Agent should still work even if policy file doesn't exist
        agent = StrategicPlannerAgent("test-no-policy", "nonexistent/policy.md")
        intent = Intent("HORIZON_SHIFT", {"affects_strategy": True})
        result = agent.execute(intent)

        # Should still execute successfully
        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0

class TestAgentSpecificFunctionality:
    """Test specific agent functionalities for full coverage."""

    def test_planner_agent_portfolio_rebalance(self):
        """Test planner agent portfolio rebalancing."""
        from agents.planner_agent import StrategicPlannerAgent
        from agents.intents import Intent

        agent = StrategicPlannerAgent("test-portfolio", "agents/POLICY.md")
        intent = Intent("PORTFOLIO_REBALANCE", {"risk_adjustment": 1.2})
        result = agent.execute(intent)

        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0
        assert result.metadata["transformation"] == "portfolio_rebalance"

    def test_buyer_agent_procurement_rhythm(self):
        """Test buyer agent procurement rhythm changes."""
        from agents.buyer_agent import SupplyBuyerAgent
        from agents.intents import Intent

        agent = SupplyBuyerAgent("test-rhythm", "agents/POLICY.md")
        intent = Intent("PROCUREMENT_RHYTHM_CHANGE", {
            "rhythm_multiplier": 1.1,
            "make_vs_buy_ratio": 0.2
        })
        result = agent.execute(intent)

        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0
        assert result.metadata["transformation"] == "procurement_rhythm"

    def test_scheduler_agent_envelope_expansion(self):
        """Test scheduler agent envelope expansion."""
        from agents.scheduler_agent import ResourceSchedulerAgent
        from agents.intents import Intent

        agent = ResourceSchedulerAgent("test-expansion", "agents/POLICY.md")
        intent = Intent("RESOURCE_ENVELOPE_EXPANSION", {
            "expansion_factor": 1.2,
            "capacity_increase": 0.3
        })
        result = agent.execute(intent)

        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0
        assert result.metadata["transformation"] == "envelope_expansion"

    def test_ops_pilot_mission_optimization(self):
        """Test ops pilot mission parameter optimization."""
        from agents.ops_pilot_agent import OpsPilotAgent
        from agents.intents import Intent

        agent = OpsPilotAgent("test-mission", "agents/POLICY.md")
        intent = Intent("MISSION_PARAMETER_OPTIMIZATION", {
            "mission_efficiency": 1.1,
            "optimized_parameters": 3
        })
        result = agent.execute(intent)

        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0
        assert result.metadata["transformation"] == "mission_optimization"

    def test_buyer_agent_complex_metamorphosis(self):
        """Test buyer agent with complex supply chain metamorphosis."""
        from agents.buyer_agent import SupplyBuyerAgent
        from agents.intents import Intent

        agent = SupplyBuyerAgent("test-complex", "agents/POLICY.md")
        intent = Intent("SUPPLY_CHAIN_METAMORPHOSIS", {
            "affects_tempo": True,
            "lead_time_reduction": 0.4,
            "resilience_factor": 1.3
        })
        result = agent.execute(intent)

        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0
        assert "affects_tempo" in result.metadata

    def test_scheduler_agent_utilization_scenarios(self):
        """Test scheduler agent with different utilization scenarios."""
        from agents.scheduler_agent import ResourceSchedulerAgent
        from agents.intents import Intent

        agent = ResourceSchedulerAgent("test-util", "agents/POLICY.md")

        # High utilization scenario
        intent = Intent("ELASTIC_CAPACITY_TRANSFORM", {
            "expands_envelope": True,
            "scaling_factor": 1.2,
            "utilization_efficiency": 0.95
        })
        result = agent.execute(intent)
        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0

        # Low utilization scenario
        intent = Intent("ELASTIC_CAPACITY_TRANSFORM", {
            "expands_envelope": False,
            "scaling_factor": 1.0,
            "utilization_efficiency": 0.5
        })
        result = agent.execute(intent)
        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0

    def test_ops_pilot_safety_scenarios(self):
        """Test ops pilot with different safety margin scenarios."""
        from agents.ops_pilot_agent import OpsPilotAgent
        from agents.intents import Intent

        agent = OpsPilotAgent("test-safety", "agents/POLICY.md")

        # Conservative operation
        intent = Intent("OPERATIONAL_ENVELOPE_EXPANSION", {
            "expands_envelope": True,
            "safety_margin": 0.25,
            "performance_gain": 0.1
        })
        result = agent.execute(intent)
        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0

        # Optimized operation
        intent = Intent("OPERATIONAL_ENVELOPE_EXPANSION", {
            "expands_envelope": True,
            "safety_margin": 0.02,
            "performance_gain": 0.2
        })
        result = agent.execute(intent)
        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0
