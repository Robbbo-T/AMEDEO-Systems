#!/usr/bin/env python3
"""
UTCS-MI: AQUART-AGT-TEST-depth_validation-v1.0
Comprehensive depth validation tests for AMEDEO agent system
"""

import pytest
import sys
from pathlib import Path

# Add agents directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from base_agent import AMEDEOAgent, Intent, Result, DET
from planner_agent import StrategicPlannerAgent
from buyer_agent import SupplyBuyerAgent
from scheduler_agent import ResourceSchedulerAgent  
from ops_pilot_agent import OpsPilotAgent


class TestDepthValidation:
    """Test depth validation for surface vs. profound actions"""
    
    def test_base_agent_rejects_surface_actions(self):
        """Base agent should reject actions that don't change decisions/rhythms/limits"""
        agent = AMEDEOAgent("test-surface", "agents/POLICY.md")
        
        # Surface intent: no deep impact indicators
        surface_intent = Intent(
            kind="reschedule_meeting",
            payload={
                "affects_strategy": False,
                "affects_tempo": False,
                "expands_envelope": False,
                "expected_gain": 1.1  # Below threshold anyway
            }
        )
        
        result = agent.execute(surface_intent)
        assert result.status == "REJECTED"
        assert "Surface action" in result.reason
        assert "decisions/rhythms/limits" in result.reason
    
    def test_base_agent_accepts_depth_actions(self):
        """Base agent should accept actions with depth indicators"""
        agent = AMEDEOAgent("test-depth", "agents/POLICY.md")
        
        # Deep intent: affects strategy
        depth_intent = Intent(
            kind="strategic_transformation",
            payload={
                "affects_strategy": True,
                "affects_tempo": False,
                "expands_envelope": False,
                "expected_gain": 3.5  # Above threshold
            }
        )
        
        result = agent.execute(depth_intent)
        assert result.status == "SUCCESS"
        assert result.productivity_delta >= 3.0
        assert result.evidence is not None
        assert result.trace_id != ""
    
    def test_insufficient_impact_rejection(self):
        """Agent should reject actions with insufficient productivity delta"""
        agent = AMEDEOAgent("test-impact", "agents/POLICY.md")
        
        # Deep intent but insufficient impact
        low_impact_intent = Intent(
            kind="minor_optimization",
            payload={
                "affects_strategy": True,
                "expected_gain": 3.5  # Set to pass AMOReS but will be overridden by mock
            }
        )
        
        # Mock the _execute_core to return low impact
        def mock_execute_core(intent):
            return Result(status="SUCCESS", productivity_delta=2.0)
        
        agent._execute_core = mock_execute_core
        
        result = agent.execute(low_impact_intent)
        assert result.status == "REJECTED"
        assert "Insufficient depth impact" in result.reason
        assert "2.0x < 3.0x" in result.reason


class TestStrategicPlannerDepth:
    """Test Strategic Planner depth validation"""
    
    def test_horizon_shift_depth(self):
        """Strategic Planner should achieve depth through horizon transformation"""
        agent = StrategicPlannerAgent("planner-test", "agents/POLICY.md")
        
        intent = Intent(
            kind="HORIZON_SHIFT",
            payload={
                "affects_strategy": True,
                "current_model": "waterfall_sequential",
                "quantum_readiness_threshold": 0.95,
                "expected_gain": 4.2
            }
        )
        
        result = agent.execute(intent)
        assert result.status == "HORIZON_TRANSFORMED"
        assert result.productivity_delta >= 3.0
        assert "new_architecture" in result.extras
        assert result.extras["new_architecture"]["model"] == "quantum_superposition_planning"
    
    def test_portfolio_collapse_depth(self):
        """Portfolio collapse should demonstrate quantum advantage"""
        agent = StrategicPlannerAgent("planner-collapse", "agents/POLICY.md")
        
        intent = Intent(
            kind="PORTFOLIO_QUANTUM_COLLAPSE",
            payload={
                "affects_strategy": True,
                "superposed_initiatives": ["proj_a", "proj_b", "proj_c"],
                "measurement_criteria": {"roi": 0.8, "risk": 0.2},
                "collapse_threshold": 0.8,
                "expected_gain": 4.0
            }
        )
        
        result = agent.execute(intent)
        assert result.status == "PORTFOLIO_COLLAPSED"
        assert result.productivity_delta >= 3.0
        assert "collapsed_state" in result.extras


class TestSupplyBuyerDepth:
    """Test Supply Buyer depth validation"""
    
    def test_supply_chain_metamorphosis(self):
        """Supply chain metamorphosis should achieve network transformation"""
        agent = SupplyBuyerAgent("buyer-test", "agents/POLICY.md")
        
        intent = Intent(
            kind="SUPPLY_CHAIN_METAMORPHOSIS",
            payload={
                "affects_tempo": True,
                "current_topology": "linear_chain",
                "carbon_limit": 1000,
                "redundancy_factor": 3,
                "supplier_count": 25,
                "expected_gain": 5.0
            }
        )
        
        result = agent.execute(intent)
        assert result.status == "SUPPLY_CHAIN_METAMORPHOSED"
        assert result.productivity_delta >= 3.0
        assert "adaptive_network" in result.extras
        assert result.extras["adaptive_network"]["self_healing"] is True
    
    def test_procurement_rhythm_shift(self):
        """Procurement rhythm shift should achieve quantum flow"""
        agent = SupplyBuyerAgent("buyer-rhythm", "agents/POLICY.md")
        
        intent = Intent(
            kind="PROCUREMENT_RHYTHM_SHIFT",
            payload={
                "affects_tempo": True,
                "current_rhythm": "batch_weekly",
                "supplier_entanglements": 8,
                "flow_quantum_size": 0.1,
                "expected_gain": 4.0
            }
        )
        
        result = agent.execute(intent)
        assert result.status == "PROCUREMENT_RHYTHM_SHIFTED"
        assert result.productivity_delta >= 3.0
        assert "quantum_flow" in result.extras


class TestResourceSchedulerDepth:
    """Test Resource Scheduler depth validation"""
    
    def test_elastic_capacity_transform(self):
        """Elastic capacity should transcend fixed limits"""
        agent = ResourceSchedulerAgent("scheduler-test", "agents/POLICY.md")
        
        intent = Intent(
            kind="ELASTIC_CAPACITY_TRANSFORM",
            payload={
                "expands_envelope": True,
                "base_capacity": 100,
                "qubit_pool_size": 64,
                "elasticity_params": {
                    "min_scale": 0.2,
                    "max_scale": 5.0,
                    "response_time_ms": 50
                },
                "expected_gain": 4.0
            }
        )
        
        result = agent.execute(intent)
        assert result.status == "CAPACITY_LIMITS_TRANSCENDED"
        assert result.productivity_delta >= 3.0
        assert "elastic_model" in result.extras
        assert result.extras["paradigm_shift"]["after"] == "quantum_elastic_field"
    
    def test_maintenance_paradigm_shift(self):
        """Maintenance shift should enable self-healing"""
        agent = ResourceSchedulerAgent("scheduler-maintenance", "agents/POLICY.md")
        
        intent = Intent(
            kind="MAINTENANCE_PARADIGM_SHIFT",
            payload={
                "expands_envelope": True,
                "current_maintenance": "scheduled_windows",
                "nano_threshold": 0.01,
                "self_healing_level": "molecular",
                "expected_gain": 4.0
            }
        )
        
        result = agent.execute(intent)
        assert result.status == "MAINTENANCE_PARADIGM_TRANSFORMED"
        assert result.productivity_delta >= 3.0
        assert "self_healing_system" in result.extras


class TestOpsPilotDepth:
    """Test Ops Pilot depth validation"""
    
    def test_operational_envelope_expansion(self):
        """Envelope expansion should achieve quantum-classical hybrid"""
        agent = OpsPilotAgent("pilot-test", "agents/POLICY.md")
        
        intent = Intent(
            kind="OPERATIONAL_ENVELOPE_EXPANSION",
            payload={
                "expands_envelope": True,
                "current_envelope": "classical_deterministic",
                "entanglement_layers": 3,
                "bloch_competency_threshold": 0.98,
                "expected_gain": 4.0
            }
        )
        
        result = agent.execute(intent)
        assert result.status == "OPERATIONAL_ENVELOPE_EXPANDED"
        assert result.productivity_delta >= 3.0
        assert "hybrid_envelope" in result.extras
        assert result.extras["hybrid_envelope"]["envelope_type"] == "quantum_classical_hybrid"
    
    def test_mission_capability_quantum_leap(self):
        """Mission capability leap should enable new mission classes"""
        agent = OpsPilotAgent("pilot-mission", "agents/POLICY.md")
        
        intent = Intent(
            kind="MISSION_CAPABILITY_QUANTUM_LEAP",
            payload={
                "expands_envelope": True,
                "current_capabilities": ["transport", "surveillance"],
                "quantum_resources": 32,
                "target_mission_classes": ["quantum_sensing", "temporal_navigation"],
                "expected_gain": 5.0
            }
        )
        
        result = agent.execute(intent)
        assert result.status == "MISSION_CAPABILITY_QUANTUM_LEAP"
        assert result.productivity_delta >= 3.0
        assert "emergent_capabilities" in result.extras


class TestCascadeDepth:
    """Test cascade effects across all agents"""
    
    def test_full_agent_cascade_depth(self):
        """All 4 agents in cascade should create exponential systemic change"""
        
        # Initialize all agents
        planner = StrategicPlannerAgent("cascade-planner", "agents/POLICY.md")
        buyer = SupplyBuyerAgent("cascade-buyer", "agents/POLICY.md")
        scheduler = ResourceSchedulerAgent("cascade-scheduler", "agents/POLICY.md")
        pilot = OpsPilotAgent("cascade-pilot", "agents/POLICY.md")
        
        # Execute cascade
        results = []
        
        # 1. Planner changes horizon
        horizon_intent = Intent(
            kind="HORIZON_SHIFT",
            payload={"affects_strategy": True, "expected_gain": 4.2}
        )
        result1 = planner.execute(horizon_intent)
        results.append(result1)
        assert result1.productivity_delta >= 3.0
        
        # 2. Buyer adapts supply chain
        supply_intent = Intent(
            kind="SUPPLY_CHAIN_METAMORPHOSIS",
            payload={"affects_tempo": True, "carbon_limit": 1000, "expected_gain": 4.0}
        )
        result2 = buyer.execute(supply_intent)
        results.append(result2)
        assert result2.productivity_delta >= 3.0
        
        # 3. Scheduler makes capacity elastic
        capacity_intent = Intent(
            kind="ELASTIC_CAPACITY_TRANSFORM",
            payload={"expands_envelope": True, "qubit_pool_size": 64, "expected_gain": 4.0}
        )
        result3 = scheduler.execute(capacity_intent)
        results.append(result3)
        assert result3.productivity_delta >= 3.0
        
        # 4. Pilot expands operational envelope
        envelope_intent = Intent(
            kind="OPERATIONAL_ENVELOPE_EXPANSION",
            payload={"expands_envelope": True, "entanglement_layers": 3, "expected_gain": 4.0}
        )
        result4 = pilot.execute(envelope_intent)
        results.append(result4)
        assert result4.productivity_delta >= 3.0
        
        # Verify cascade impact
        total_impact = 1.0
        for result in results:
            total_impact *= result.productivity_delta
        
        assert total_impact >= 81.0  # 3^4 minimum
        
        # Verify all traces are valid
        trace_ids = [result.trace_id for result in results]
        assert DET.verify_cascade_trace(trace_ids)
        
        # Verify systemic change
        assert all(result.status.endswith(("TRANSFORMED", "TRANSCENDED", "EXPANDED", "METAMORPHOSED")) 
                  for result in results)


class TestMetricNormalization:
    """Test metric normalization functions"""
    
    def test_to_factor_gain(self):
        """Test gain factor normalization"""
        from base_agent import to_factor
        
        assert to_factor(4.2, "gain") == 4.2
        assert to_factor(0.5, "gain") == 1.0  # Floor at 1.0
        assert to_factor(-1.0, "gain") == 1.0  # Floor at 1.0
    
    def test_to_factor_reduce(self):
        """Test reduction factor normalization"""
        from base_agent import to_factor
        
        assert abs(to_factor(0.72, "reduce") - 3.571) < 0.01
        assert to_factor(0.0, "reduce") >= 1e6  # Avoid div by zero
        assert to_factor(1.0, "reduce") >= 1e6  # Complete reduction


if __name__ == "__main__":
    pytest.main([__file__, "-v"])