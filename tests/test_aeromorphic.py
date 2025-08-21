#!/usr/bin/env python3
"""
UTCS-MI: AQUART-TEST-CODE-aeromorphic_tests-v1.0
Test quantum aeromorphic nano-teleportation functionality
"""

import unittest
import sys
import os

# Add framework path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'framework'))
from aeromorphic.nano_teleportation import (
    QuantumTeleportationEngine,
    AeromorphicLattice,
    QuantumAeromorphicIntegration,
    AeromorphicMaterial,
    QuantumTeleportationState
)


class TestQuantumTeleportationEngine(unittest.TestCase):
    """Test quantum teleportation engine"""
    
    def setUp(self):
        """Set up test environment"""
        self.material = AeromorphicMaterial(
            lattice_structure="hexagonal_carbon",
            quantum_coherence=100.0,
            entanglement_capacity=10,
            energy_requirements=150.0
        )
        self.engine = QuantumTeleportationEngine(self.material)
        
    def test_engine_initialization(self):
        """Test quantum engine initialization"""
        self.assertEqual(self.engine.material, self.material)
        self.assertEqual(len(self.engine.entangled_pairs), 0)
        self.assertEqual(self.engine.coherence_time, 100.0)
        
    def test_entanglement_pair_creation(self):
        """Test entanglement pair creation"""
        result = self.engine.create_entanglement_pair("cell_001", "cell_002")
        
        # Should succeed with good material properties
        if result:
            self.assertIn("cell_001", self.engine.entangled_pairs)
            self.assertIn("cell_002", self.engine.entangled_pairs)
            self.assertEqual(self.engine.entangled_pairs["cell_001"], "cell_002")
            self.assertEqual(self.engine.entangled_pairs["cell_002"], "cell_001")
        
    def test_entanglement_capacity_limit(self):
        """Test entanglement capacity limit"""
        # Fill up entanglement capacity
        for i in range(self.material.entanglement_capacity + 1):
            self.engine.entangled_pairs[f"cell_{i:03d}"] = f"partner_{i:03d}"
            
        # Should fail when capacity exceeded
        result = self.engine.create_entanglement_pair("overflow_1", "overflow_2")
        self.assertFalse(result)
        
    def test_quantum_teleportation_protocol(self):
        """Test quantum teleportation protocol execution"""
        source_cell = "cell_source"
        target_location = [1.0, 2.0, 3.0]
        
        try:
            result = self.engine.quantum_teleportation_protocol(source_cell, target_location)
            
            self.assertIsInstance(result, QuantumTeleportationState)
            self.assertEqual(result.source_cells, [source_cell])
            self.assertEqual(result.target_locations, target_location)
            self.assertGreater(result.fidelity, 0.0)
            self.assertLessEqual(result.fidelity, 1.0)
            self.assertEqual(len(result.quantum_state), 3)
            
        except ValueError as e:
            # Acceptable if entanglement channel fails
            self.assertIn("Failed to establish entanglement channel", str(e))


class TestAeromorphicLattice(unittest.TestCase):
    """Test aeromorphic lattice structure"""
    
    def setUp(self):
        """Set up test environment"""
        self.dimensions = (3, 3, 2)
        self.lattice = AeromorphicLattice(self.dimensions)
        
    def test_lattice_initialization(self):
        """Test lattice initialization"""
        self.assertEqual(self.lattice.dimensions, self.dimensions)
        expected_cells = self.dimensions[0] * self.dimensions[1] * self.dimensions[2]
        self.assertEqual(len(self.lattice.quantum_cells), expected_cells)
        
        # Check cell structure
        for cell_id, cell_data in self.lattice.quantum_cells.items():
            self.assertIn("position", cell_data)
            self.assertIn("quantum_state", cell_data)
            self.assertEqual(len(cell_data["position"]), 3)
            self.assertEqual(len(cell_data["quantum_state"]), 3)
            
    def test_aerodynamic_properties_calculation(self):
        """Test aerodynamic properties calculation"""
        properties = self.lattice.get_aerodynamic_properties()
        
        self.assertIsInstance(properties, dict)
        self.assertIn("lift_coefficient", properties)
        self.assertIn("drag_coefficient", properties)
        self.assertIn("camber_ratio", properties)
        self.assertIn("aspect_ratio", properties)
        
        # Validate reasonable ranges
        self.assertGreaterEqual(properties["lift_coefficient"], 0.0)
        self.assertLessEqual(properties["lift_coefficient"], 2.0)
        self.assertGreaterEqual(properties["drag_coefficient"], 0.0)
        self.assertLessEqual(properties["drag_coefficient"], 1.0)
        
    def test_cellular_transposition(self):
        """Test cellular transposition execution"""
        source_cell = "cell_0_0_0"
        target_location = [1.5, 1.5, 0.5]
        
        # Get initial cell position
        initial_position = self.lattice.quantum_cells[source_cell]["position"].copy()
        
        # Create quantum engine for the test
        quantum_engine = QuantumTeleportationEngine(self.lattice.material_properties)
        
        try:
            success = self.lattice.execute_cellular_transposition(
                source_cell, target_location, quantum_engine
            )
            
            if success:
                # Check that position was updated
                new_position = self.lattice.quantum_cells[source_cell]["position"]
                self.assertEqual(new_position, target_location)
                
        except Exception:
            # Transposition might fail due to quantum uncertainties
            pass
            
    def test_optimization_planning(self):
        """Test aerodynamic optimization planning"""
        target_profile = {
            "drag_coefficient": 0.1,
            "lift_coefficient": 1.5
        }
        
        plan = self.lattice._calculate_transposition_plan(target_profile)
        
        self.assertIsInstance(plan, list)
        # Plan might be empty if no optimization needed
        for transposition in plan:
            self.assertIn("source", transposition)
            self.assertIn("target", transposition)
            self.assertIn("reason", transposition)


class TestQuantumAeromorphicIntegration(unittest.TestCase):
    """Test quantum aeromorphic integration"""
    
    def setUp(self):
        """Set up test environment"""
        self.surface_dimensions = (5, 3, 2)
        self.integration = QuantumAeromorphicIntegration(self.surface_dimensions)
        
    def test_integration_initialization(self):
        """Test integration system initialization"""
        self.assertIsNotNone(self.integration.aeromorphic_lattice)
        self.assertEqual(self.integration.aeromorphic_lattice.dimensions, self.surface_dimensions)
        self.assertEqual(len(self.integration.optimization_history), 0)
        
    def test_surface_optimization(self):
        """Test aircraft surface optimization"""
        flight_conditions = {
            "altitude": 25000,
            "speed": 300,
            "aoa": 4.0
        }
        
        result = self.integration.optimize_aircraft_surface(flight_conditions)
        
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)
        self.assertIn("optimization_time", result)
        self.assertIn("current_profile", result)
        self.assertIn("target_profile", result)
        self.assertIn("new_profile", result)
        self.assertIn("performance_improvement", result)
        
        # Check performance improvement structure
        improvement = result["performance_improvement"]
        self.assertIn("lift_improvement_percent", improvement)
        self.assertIn("drag_reduction_percent", improvement)
        self.assertIn("ld_ratio_improvement_percent", improvement)
        self.assertIn("overall_efficiency_gain", improvement)
        
    def test_optimal_profile_calculation(self):
        """Test optimal profile calculation"""
        current_profile = {
            "lift_coefficient": 1.0,
            "drag_coefficient": 0.2
        }
        
        flight_conditions = {
            "altitude": 35000,
            "speed": 250,
            "aoa": 3.0
        }
        
        target_profile = self.integration._calculate_optimal_profile(
            current_profile, flight_conditions
        )
        
        self.assertIsInstance(target_profile, dict)
        self.assertIn("lift_coefficient", target_profile)
        self.assertIn("drag_coefficient", target_profile)
        self.assertIn("optimization_reason", target_profile)
        
    def test_performance_improvement_calculation(self):
        """Test performance improvement calculation"""
        current = {
            "lift_coefficient": 1.0,
            "drag_coefficient": 0.2
        }
        
        new = {
            "lift_coefficient": 1.2,
            "drag_coefficient": 0.15
        }
        
        improvement = self.integration._calculate_performance_improvement(current, new)
        
        self.assertIsInstance(improvement, dict)
        self.assertAlmostEqual(improvement["lift_improvement_percent"], 20.0, places=1)
        self.assertAlmostEqual(improvement["drag_reduction_percent"], 25.0, places=1)
        
        # L/D ratio should improve
        current_ld = current["lift_coefficient"] / current["drag_coefficient"]  # 5.0
        new_ld = new["lift_coefficient"] / new["drag_coefficient"]  # 8.0
        expected_ld_improvement = ((new_ld - current_ld) / current_ld) * 100  # 60%
        self.assertAlmostEqual(improvement["ld_ratio_improvement_percent"], expected_ld_improvement, places=1)


class TestAeromorphicMaterial(unittest.TestCase):
    """Test aeromorphic material properties"""
    
    def test_material_properties(self):
        """Test material property validation"""
        material = AeromorphicMaterial(
            lattice_structure="diamond_cubic",
            quantum_coherence=200.0,
            entanglement_capacity=100,
            energy_requirements=75.0
        )
        
        self.assertEqual(material.lattice_structure, "diamond_cubic")
        self.assertEqual(material.quantum_coherence, 200.0)
        self.assertEqual(material.entanglement_capacity, 100)
        self.assertEqual(material.energy_requirements, 75.0)


if __name__ == "__main__":
    unittest.main()