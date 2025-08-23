#!/usr/bin/env python3
"""
UTCS-MI: EstándarUniversal:Codigo,Autogenesis,DO178C,00.00,HealingMechanismsController,0003,v1.0,Aerospace and Quantum United Agency,GeneracionHibrida,AIR,Amedeo Pelliccia,7f31a2b9,P0–P7
Test micro transistor self-healing functionality
"""

import unittest
import sys
import os

# Add framework path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'framework'))
from self_healing.micro_transistor import (
    MicroTransistorNode, 
    SelfHealingSurfaceController,
    HealingActuation,
    DamageAssessment
)


class TestMicroTransistorSelfHealing(unittest.TestCase):
    """Test micro transistor self-healing capabilities"""
    
    def setUp(self):
        """Set up test environment"""
        self.node = MicroTransistorNode("test_node_001", [1.0, 2.0, 3.0])
        
    def test_micro_transistor_initialization(self):
        """Test micro transistor node initialization"""
        self.assertEqual(self.node.node_id, "test_node_001")
        self.assertEqual(self.node.position, [1.0, 2.0, 3.0])
        self.assertEqual(self.node.healing_resources, 100.0)
        self.assertEqual(len(self.node.neighbors), 0)
        
    def test_damage_assessment_no_damage(self):
        """Test damage assessment with no damage detected"""
        sensor_readings = {
            "stress": 0.1,
            "temperature": 25.0,
            "vibration": 0.05
        }
        
        assessment = self.node.assess_damage(sensor_readings)
        
        self.assertIsInstance(assessment, DamageAssessment)
        self.assertEqual(assessment.damage_type, "none")
        self.assertEqual(assessment.severity, 0.0)
        self.assertEqual(assessment.node_id, "test_node_001")
        self.assertGreater(assessment.confidence, 0.7)
        
    def test_damage_assessment_stress_damage(self):
        """Test damage assessment with stress damage"""
        sensor_readings = {
            "stress": 0.9,
            "temperature": 25.0,
            "vibration": 0.05
        }
        
        assessment = self.node.assess_damage(sensor_readings)
        
        self.assertEqual(assessment.damage_type, "stress_crack")
        self.assertGreater(assessment.severity, 0.8)
        self.assertGreater(assessment.confidence, 0.9)
        
    def test_damage_assessment_thermal_damage(self):
        """Test damage assessment with thermal damage"""
        sensor_readings = {
            "stress": 0.1,
            "temperature": 180.0,
            "vibration": 0.05
        }
        
        assessment = self.node.assess_damage(sensor_readings)
        
        self.assertEqual(assessment.damage_type, "thermal_degradation")
        self.assertGreater(assessment.severity, 0.5)
        
    def test_healing_response_planning_no_damage(self):
        """Test healing response planning with no damage"""
        assessment = DamageAssessment(
            damage_type="none",
            severity=0.05,
            confidence=0.8,
            timestamp=1234567890.0,
            node_id="test_node_001",
            location=[1.0, 2.0, 3.0]
        )
        
        response = self.node.plan_healing_response(assessment)
        self.assertIsNone(response)
        
    def test_healing_response_planning_stress_damage(self):
        """Test healing response planning for stress damage"""
        assessment = DamageAssessment(
            damage_type="stress_crack",
            severity=0.6,
            confidence=0.95,
            timestamp=1234567890.0,
            node_id="test_node_001",
            location=[1.0, 2.0, 3.0]
        )
        
        response = self.node.plan_healing_response(assessment)
        
        self.assertIsInstance(response, HealingActuation)
        self.assertGreater(response.energy_required, 0)
        self.assertGreater(response.duration, 0)
        self.assertEqual(len(response.pattern), 3)
        self.assertGreater(response.success_probability, 0.5)
        
    def test_healing_execution_success(self):
        """Test successful healing execution"""
        actuation = HealingActuation(
            pattern=[1.0, 0.8, 0.6],
            energy_required=15.0,
            duration=5.0,
            success_probability=0.9
        )
        
        initial_resources = self.node.healing_resources
        result = self.node.execute_healing(actuation)
        
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)
        self.assertIn("resources_consumed", result)
        self.assertEqual(result["resources_consumed"], 15.0)
        self.assertEqual(self.node.healing_resources, initial_resources - 15.0)
        
    def test_healing_execution_insufficient_resources(self):
        """Test healing execution with insufficient resources"""
        self.node.healing_resources = 5.0  # Set low resources
        
        actuation = HealingActuation(
            pattern=[1.0, 0.8, 0.6],
            energy_required=15.0,
            duration=5.0,
            success_probability=0.9
        )
        
        result = self.node.execute_healing(actuation)
        
        self.assertFalse(result["success"])
        self.assertIn("Insufficient healing resources", result["reason"])
        self.assertEqual(result["resources_consumed"], 0.0)


class TestSelfHealingSurfaceController(unittest.TestCase):
    """Test self-healing surface controller"""
    
    def setUp(self):
        """Set up test environment"""
        self.nodes = [
            MicroTransistorNode(f"node_{i:03d}", [float(i), 0.0, 0.0])
            for i in range(5)
        ]
        self.controller = SelfHealingSurfaceController("test_surface", self.nodes)
        
    def test_controller_initialization(self):
        """Test controller initialization"""
        self.assertEqual(self.controller.surface_id, "test_surface")
        self.assertEqual(len(self.controller.nodes), 5)
        self.assertEqual(len(self.controller.healing_history), 0)
        
    def test_monitor_and_heal_no_damage(self):
        """Test monitoring and healing with no damage"""
        # Mock sensor readings to return low damage
        for node in self.nodes:
            node.get_sensor_readings = lambda: {
                "stress": 0.1,
                "temperature": 25.0,
                "vibration": 0.05,
                "pressure": 1.0
            }
            
        result = self.controller.monitor_and_heal()
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["nodes_assessed"], 5)
        self.assertEqual(result["healing_actions"], 0)
        self.assertFalse(result["critical_damage"])
        
    def test_monitor_and_heal_with_damage(self):
        """Test monitoring and healing with damage requiring healing"""
        # Mock sensor readings to return significant damage for first node
        def mock_readings_damaged():
            return {
                "stress": 0.9,  # Increased to ensure it triggers healing
                "temperature": 25.0,
                "vibration": 0.05,
                "pressure": 1.0
            }
            
        def mock_readings_normal():
            return {
                "stress": 0.1,
                "temperature": 25.0,
                "vibration": 0.05,
                "pressure": 1.0
            }
            
        self.nodes[0].get_sensor_readings = mock_readings_damaged
        for node in self.nodes[1:]:
            node.get_sensor_readings = mock_readings_normal
            
        result = self.controller.monitor_and_heal()
        
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["nodes_assessed"], 5)
        # The stress of 0.9 should trigger healing (above 0.8 threshold)
        self.assertGreaterEqual(result["healing_actions"], 1)
        
    def test_health_status_reporting(self):
        """Test health status reporting"""
        status = self.controller.get_health_status()
        
        self.assertIsInstance(status, dict)
        self.assertEqual(status["surface_id"], "test_surface")
        self.assertEqual(status["total_nodes"], 5)
        self.assertIn("health_percentage", status)
        self.assertIn("average_resources", status)
        self.assertGreaterEqual(status["health_percentage"], 0.0)
        self.assertLessEqual(status["health_percentage"], 100.0)


if __name__ == "__main__":
    unittest.main()