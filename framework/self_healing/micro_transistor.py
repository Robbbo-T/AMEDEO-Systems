#!/usr/bin/env python3
"""
UTCS-MI: EstándarUniversal:Codigo,Autogenesis,DO178C,00.00,MicroTransistorController,0001,v1.0,Aerospace and Quantum United Agency,GeneracionHibrida,AIR,Amedeo Pelliccia,c8a9e3f1,P0–P7
Micro Transistor Implementation for Self-Healing Aerodynamic Surfaces
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import time
import json
import hashlib
import random

# Add safety framework
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'safety'))
from rta_supervisor import RTASupervisor, SafetyEnvelope, DALPartitionManager

# Physical constants for cert-ready implementation
SEVERITY_THRESHOLD = 0.1  # Minimum damage severity requiring action
CONFIDENCE_HIGH = 0.8     # High confidence threshold
CONFIDENCE_LOW = 0.3      # Low confidence threshold

# Energy limits per AMEDEO Systems cert requirements
MAX_ENERGY_PER_NODE_MJ = 50.0e-3  # 50 mJ per node maximum
MAX_ENERGY_PER_TILE_J = 2.0       # 2 J per tile maximum
BASE_ENERGY_MJ = 5.0e-3           # 5 mJ base energy (was 10 J - major reduction)

# Tile leader consensus parameters (0.01-0.1 m² patches)
TILE_SIZE_M2 = 0.05               # 0.05 m² per tile
NODES_PER_TILE = 10              # ~10 nodes per tile
CONSENSUS_TIMEOUT_MS = 100        # 100ms consensus timeout


@dataclass
class HealingActuation:
    """Healing actuation parameters for micro transistor control"""
    pattern: List[float]  # 3D activation pattern
    energy_required: float  # Joules (≤50mJ per node limit)
    duration: float  # Seconds (0.1-1s for local healing, 1-10s for macro)
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


@dataclass
class TileConsensusVote:
    """2oo3 consensus vote for tile healing decisions"""
    voter_id: str
    vote: str  # "approve", "reject", "abstain"
    reasoning: str
    energy_budget: float
    timestamp: float


class TileLeader:
    """Tile leader for consensus-based healing decisions (2oo3 voting)"""
    
    def __init__(self, tile_id: str, leader_node_id: str, backup_nodes: List[str]):
        self.tile_id = tile_id
        self.leader_node_id = leader_node_id
        self.backup_nodes = backup_nodes  # 2 backup nodes for 2oo3
        self.energy_budget = MAX_ENERGY_PER_TILE_J
        self.healing_queue = []
        
    def propose_healing_action(self, action: Dict) -> bool:
        """Propose healing action to tile consensus (2oo3)"""
        # Leader proposes, backups vote
        votes = []
        
        # Leader always votes (primary decision maker)
        leader_vote = self._evaluate_healing_proposal(action)
        votes.append(TileConsensusVote(
            voter_id=self.leader_node_id,
            vote=leader_vote,
            reasoning="Leader evaluation",
            energy_budget=self.energy_budget,
            timestamp=time.time()
        ))
        
        # Get votes from backup nodes
        for backup_id in self.backup_nodes:
            backup_vote = self._get_backup_vote(backup_id, action)
            votes.append(backup_vote)
        
        # 2oo3 consensus: need at least 2 approvals
        approve_count = sum(1 for vote in votes if vote.vote == "approve")
        
        if approve_count >= 2:
            # Consensus reached - execute action
            self._execute_consensed_action(action, votes)
            return True
        else:
            # Consensus failed
            return False
    
    def _evaluate_healing_proposal(self, action: Dict) -> str:
        """Leader evaluates healing proposal"""
        actuation = action.get("actuation")
        if actuation is None:
            return "reject"
            
        energy_required = actuation.energy_required if hasattr(actuation, 'energy_required') else 0.0
        
        # Check energy budget
        if energy_required > self.energy_budget:
            return "reject"
        
        # Check severity threshold
        assessment = action.get("assessment")
        if assessment is None:
            return "reject"
            
        severity = assessment.severity if hasattr(assessment, 'severity') else 0.0
        if severity < SEVERITY_THRESHOLD:
            return "reject"
            
        return "approve"
    
    def _get_backup_vote(self, backup_id: str, action: Dict) -> TileConsensusVote:
        """Get vote from backup node (simplified)"""
        # In real implementation, this would communicate with actual backup nodes
        actuation = action.get("actuation")
        assessment = action.get("assessment")
        
        energy_required = actuation.energy_required if (actuation and hasattr(actuation, 'energy_required')) else 0.0
        severity = assessment.severity if (assessment and hasattr(assessment, 'severity')) else 0.0
        
        # Backup logic: conservative voting
        if energy_required > MAX_ENERGY_PER_NODE_MJ * 5:  # Multiple nodes worth
            vote = "reject"
            reasoning = "Energy budget exceeded"
        elif severity > 0.8:
            vote = "approve"  
            reasoning = "Critical damage requires immediate action"
        elif severity > SEVERITY_THRESHOLD:
            vote = "approve"
            reasoning = "Standard healing threshold met"
        else:
            vote = "reject"
            reasoning = "Below healing threshold"
            
        return TileConsensusVote(
            voter_id=backup_id,
            vote=vote,
            reasoning=reasoning,
            energy_budget=self.energy_budget,
            timestamp=time.time()
        )
    
    def _execute_consensed_action(self, action: Dict, votes: List[TileConsensusVote]):
        """Execute action approved by 2oo3 consensus"""
        actuation = action.get("actuation")
        energy_cost = actuation.energy_required if (actuation and hasattr(actuation, 'energy_required')) else 0.0
        self.energy_budget -= energy_cost
        
        # Record consensus decision
        consensus_record = {
            "action": action,
            "votes": [{"voter": v.voter_id, "vote": v.vote, "reasoning": v.reasoning} for v in votes],
            "energy_consumed": energy_cost,
            "remaining_budget": self.energy_budget,
            "timestamp": time.time()
        }
        self.healing_queue.append(consensus_record)


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
            
        # Confidence based on severity and detection clarity
        if damage_type == "none":
            confidence = 0.95  # High confidence in no damage
        elif severity > 0.8:
            confidence = 0.95  # High confidence in severe damage
        elif severity > SEVERITY_THRESHOLD:
            confidence = CONFIDENCE_HIGH
        else:
            confidence = CONFIDENCE_LOW
        
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
            
        # Calculate energy requirements based on damage severity (cert-ready limits)
        energy_req = BASE_ENERGY_MJ * damage_assessment.severity * 2.0
        
        # Enforce per-node energy ceiling
        energy_req = min(energy_req, MAX_ENERGY_PER_NODE_MJ)
        
        # Check resource availability
        if energy_req > self.healing_resources:
            # Request resources from neighbors (simplified)
            energy_req = min(energy_req, self.healing_resources)
            
        # Generate activation pattern based on damage type with thermal timing constraints
        if damage_assessment.damage_type == "stress_crack":
            pattern = [1.0, 0.8, 0.6]  # High intensity healing
            duration = 0.5  # Local crack sealing: 0.1-1s
        elif damage_assessment.damage_type == "thermal_degradation":
            pattern = [0.6, 0.8, 0.4]  # Moderate healing with cooling
            duration = 0.8  # Local thermal repair: 0.1-1s  
        elif damage_assessment.damage_type == "fatigue_damage":
            pattern = [0.8, 0.6, 0.8]  # Oscillating repair pattern
            duration = 0.3  # Fast local fatigue repair: 0.1-1s
        elif damage_assessment.damage_type == "macro_reshape":
            pattern = [0.5, 0.5, 0.5]  # Macro shape recovery (ground only)
            duration = 5.0  # Macro shape recovery: 1-10s
        else:
            pattern = [0.5, 0.5, 0.5]  # Default local healing
            duration = 0.2  # Conservative local healing timing
            
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
    """Integration layer between micro transistors and AQUA-OS with tile leader consensus"""
    
    def __init__(self, surface_id: str, transistor_nodes: List[MicroTransistorNode]):
        self.surface_id = surface_id
        self.nodes = {node.node_id: node for node in transistor_nodes}
        self.healing_history = []
        
        # Create tile leaders for consensus (0.01-0.1 m² patches)
        self.tile_leaders = self._create_tile_leaders(transistor_nodes)
        
        # Initialize RTA supervisor (DAL-A safety monitor)
        safety_envelope = SafetyEnvelope(
            max_temperature_delta=25.0,  # ≤+25°C over 5s
            max_current=1.0,             # ≤1A per tile
            max_duty_cycle=0.10,         # ≤10% per minute
            thermal_timeout=0.5          # <500ms thermal guard
        )
        self.rta_supervisor = RTASupervisor(safety_envelope)
        self.dal_partition_manager = DALPartitionManager()
        
    def _create_tile_leaders(self, nodes: List[MicroTransistorNode]) -> Dict[str, TileLeader]:
        """Create tile leaders for 2oo3 consensus"""
        tile_leaders = {}
        
        # Group nodes into tiles (simplified - by proximity)
        for i in range(0, len(nodes), NODES_PER_TILE):
            tile_nodes = nodes[i:i+NODES_PER_TILE]
            if len(tile_nodes) >= 3:  # Need at least 3 for 2oo3
                tile_id = f"tile_{i//NODES_PER_TILE}"
                leader_node = tile_nodes[0]
                backup_nodes = [tile_nodes[1].node_id, tile_nodes[2].node_id]
                
                tile_leader = TileLeader(
                    tile_id=tile_id,
                    leader_node_id=leader_node.node_id,
                    backup_nodes=backup_nodes
                )
                tile_leaders[tile_id] = tile_leader
                
        return tile_leaders
        
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
        
        # Execute healing actions via tile leader consensus (2oo3)
        results = []
        consensus_failures = 0
        
        for action in healing_actions:
            # Find which tile this node belongs to
            tile_leader = self._find_tile_leader_for_node(action["node_id"])
            
            if tile_leader:
                # Use 2oo3 consensus before executing
                consensus_approved = tile_leader.propose_healing_action(action)
                
                if consensus_approved:
                    # RTA supervisor approval (DAL-A safety gate)
                    actuation = action["actuation"]
                    rta_approved = self.rta_supervisor.approve(
                        pattern=actuation.pattern,
                        energy=actuation.energy_required,
                        duration=actuation.duration
                    )
                    
                    if rta_approved:
                        # Execute healing action
                        node = self.nodes[action["node_id"]]
                        result = node.execute_healing(action["actuation"])
                        results.append({
                            "node_id": action["node_id"],
                            "assessment": action["assessment"],
                            "execution_result": result,
                            "consensus": "approved",
                            "rta_approval": "approved"
                        })
                    else:
                        # RTA rejected for safety reasons
                        results.append({
                            "node_id": action["node_id"],
                            "assessment": action["assessment"],
                            "execution_result": {"success": False, "reason": "RTA safety rejection"},
                            "consensus": "approved",
                            "rta_approval": "rejected"
                        })
                        consensus_failures += 1
                else:
                    # Consensus rejected the action
                    results.append({
                        "node_id": action["node_id"],
                        "assessment": action["assessment"],
                        "execution_result": {"success": False, "reason": "Consensus rejected"},
                        "consensus": "rejected"
                    })
                    consensus_failures += 1
            else:
                # No tile leader - emergency fallback (should not happen)
                node = self.nodes[action["node_id"]]
                result = node.execute_healing(action["actuation"])
                results.append({
                    "node_id": action["node_id"],
                    "assessment": action["assessment"],
                    "execution_result": result,
                    "consensus": "fallback"
                })
        
        # Create summary with consensus metrics
        healing_summary = {
            "surface_id": self.surface_id,
            "timestamp": time.time(),
            "nodes_assessed": len(damage_reports),
            "healing_actions": len(healing_actions),
            "consensus_failures": consensus_failures,
            "critical_damage": critical_damage,
            "results": results,
            "status": "completed"
        }
        
        self.healing_history.append(healing_summary)
        return healing_summary
        
    def _find_tile_leader_for_node(self, node_id: str) -> Optional[TileLeader]:
        """Find tile leader responsible for given node"""
        for tile_leader in self.tile_leaders.values():
            if (node_id == tile_leader.leader_node_id or 
                node_id in tile_leader.backup_nodes):
                return tile_leader
        return None
    
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
    
    def set_airborne_mode(self, airborne: bool):
        """Set airborne mode (restricts macro healing operations)"""
        self.rta_supervisor.set_airborne_mode(airborne)
        
    def get_safety_status(self) -> Dict:
        """Get RTA supervisor safety status"""
        return self.rta_supervisor.get_safety_status()
    
    def get_dal_partition_info(self) -> Dict:
        """Get DAL partition information"""
        return self.dal_partition_manager.get_partition_info()