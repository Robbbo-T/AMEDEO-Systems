#!/usr/bin/env python3
"""
UTCS-MI: AQUART-MTR-CODE-micro_transistor_controller-v1.0
Micro Transistor Implementation for Self-Healing Aerodynamic Surfaces
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import time
import json
import hashlib


@dataclass
class HealingActuation:
    """Healing actuation parameters for micro transistor control"""
    pattern: List[float]  # 3D activation pattern
    energy_required: float  # Joules
    duration: float  # Seconds
    success_probability: float  # 0.0-1.0


@dataclass
class DamageAssessment:
    """Damage assessment result from micro transistor sensors"""
    damage_type: str
    severity: float  # 0.0-1.0
    confidence: float  # 0.0-1.0
    timestamp: float
    node_id: str
    location: List[float]  # 3D coordinates


class MicroTransistorNode:
    """Autonomous self-healing control node for aerodynamic surfaces"""
    
    def __init__(self, node_id: str, position: List[float]):
        self.node_id = node_id
        self.position = position
        self.neighbors = []  # Other nodes in mesh
        self.sensor_data = {}
        self.healing_resources = 100.0  # Available healing agent percentage
        self.last_assessment = None
        
    def assess_damage(self, sensor_readings: Dict[str, float]) -> DamageAssessment:
        """Assess local damage using embedded ML model"""
        # Simplified damage assessment based on sensor thresholds
        stress_level = sensor_readings.get('stress', 0.0)
        temperature = sensor_readings.get('temperature', 20.0)
        vibration = sensor_readings.get('vibration', 0.0)
        
        # Basic damage classification
        if stress_level > 0.8:
            damage_type = "stress_crack"
            severity = min(1.0, stress_level)
        elif temperature > 150.0:
            damage_type = "thermal_degradation" 
            severity = min(1.0, (temperature - 100.0) / 100.0)
        elif vibration > 0.7:
            damage_type = "fatigue_damage"
            severity = min(1.0, vibration)
        else:
            damage_type = "none"
            severity = 0.0
            
        confidence = 0.95 if severity > 0.1 else 0.8
        
        assessment = DamageAssessment(
            damage_type=damage_type,
            severity=severity,
            confidence=confidence,
            timestamp=time.time(),
            node_id=self.node_id,
            location=self.position.copy()
        )
        
        self.last_assessment = assessment
        return assessment
    
    def plan_healing_response(self, damage_assessment: DamageAssessment) -> Optional[HealingActuation]:
        """Determine optimal healing response for detected damage"""
        if damage_assessment.severity < 0.1:
            return None  # No healing needed
            
        # Calculate energy requirements based on damage severity
        base_energy = 10.0  # Base Joules
        energy_req = base_energy * damage_assessment.severity * 2.0
        
        # Check resource availability
        if energy_req > self.healing_resources:
            # Request resources from neighbors (simplified)
            energy_req = min(energy_req, self.healing_resources)
            
        # Generate activation pattern based on damage type
        if damage_assessment.damage_type == "stress_crack":
            pattern = [1.0, 0.8, 0.6]  # High intensity healing
            duration = 5.0
        elif damage_assessment.damage_type == "thermal_degradation":
            pattern = [0.6, 0.8, 0.4]  # Moderate healing with cooling
            duration = 8.0
        elif damage_assessment.damage_type == "fatigue_damage":
            pattern = [0.8, 0.6, 0.8]  # Oscillating repair pattern
            duration = 6.0
        else:
            pattern = [0.5, 0.5, 0.5]  # Default pattern
            duration = 3.0
            
        success_prob = min(0.98, 0.9 - damage_assessment.severity * 0.2)
        
        return HealingActuation(
            pattern=pattern,
            energy_required=energy_req,
            duration=duration,
            success_probability=success_prob
        )
    
    def execute_healing(self, actuation: HealingActuation) -> Dict:
        """Execute healing sequence with evidence recording"""
        if actuation.energy_required > self.healing_resources:
            return {
                "success": False,
                "reason": "Insufficient healing resources",
                "resources_consumed": 0.0,
                "timestamp": time.time()
            }
            
        # Simulate healing execution
        start_time = time.time()
        
        # Consume resources
        self.healing_resources -= actuation.energy_required
        
        # Simulate success/failure based on probability
        success = random.random() < actuation.success_probability
        
        evidence = {
            "success": success,
            "actuation": {
                "pattern": actuation.pattern,
                "energy_required": actuation.energy_required,
                "duration": actuation.duration
            },
            "resources_consumed": actuation.energy_required,
            "execution_time": time.time() - start_time,
            "timestamp": time.time(),
            "node_id": self.node_id
        }
        
        return evidence
    
    def get_sensor_readings(self) -> Dict[str, float]:
        """Get current sensor readings (simulated)"""
        import random
        return {
            "stress": random.uniform(0.0, 1.0),
            "temperature": random.uniform(15.0, 200.0),
            "vibration": random.uniform(0.0, 1.0),
            "pressure": random.uniform(0.8, 1.2)
        }


class SelfHealingSurfaceController:
    """Integration layer between micro transistors and AQUA-OS"""
    
    def __init__(self, surface_id: str, transistor_nodes: List[MicroTransistorNode]):
        self.surface_id = surface_id
        self.nodes = {node.node_id: node for node in transistor_nodes}
        self.healing_history = []
        
    def monitor_and_heal(self) -> Dict:
        """Main healing control loop"""
        # Collect damage assessments from all nodes
        damage_reports = []
        for node_id, node in self.nodes.items():
            sensor_readings = node.get_sensor_readings()
            report = node.assess_damage(sensor_readings)
            damage_reports.append(report)
        
        # Determine which nodes need healing
        healing_actions = []
        critical_damage = False
        
        for report in damage_reports:
            if report.severity > 0.1:
                node = self.nodes[report.node_id]
                actuation = node.plan_healing_response(report)
                if actuation:
                    healing_actions.append({
                        "node_id": report.node_id,
                        "assessment": report,
                        "actuation": actuation
                    })
                    if report.severity > 0.7:
                        critical_damage = True
        
        # Execute healing actions
        results = []
        for action in healing_actions:
            node = self.nodes[action["node_id"]]
            result = node.execute_healing(action["actuation"])
            results.append({
                "node_id": action["node_id"],
                "assessment": action["assessment"],
                "execution_result": result
            })
        
        # Create summary
        healing_summary = {
            "surface_id": self.surface_id,
            "timestamp": time.time(),
            "nodes_assessed": len(damage_reports),
            "healing_actions": len(healing_actions),
            "critical_damage": critical_damage,
            "results": results,
            "status": "completed"
        }
        
        self.healing_history.append(healing_summary)
        return healing_summary
    
    def get_health_status(self) -> Dict:
        """Get overall health status of the surface"""
        total_nodes = len(self.nodes)
        healthy_nodes = 0
        total_resources = 0.0
        
        for node in self.nodes.values():
            # Consider new nodes (no assessment yet) as healthy, or nodes with low severity
            if node.last_assessment is None or node.last_assessment.severity < 0.1:
                healthy_nodes += 1
            total_resources += node.healing_resources
            
        avg_resources = total_resources / total_nodes if total_nodes > 0 else 0.0
        health_percentage = (healthy_nodes / total_nodes * 100) if total_nodes > 0 else 0.0
        
        return {
            "surface_id": self.surface_id,
            "health_percentage": health_percentage,
            "average_resources": avg_resources,
            "total_nodes": total_nodes,
            "healthy_nodes": healthy_nodes,
            "timestamp": time.time()
        }