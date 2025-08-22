#!/usr/bin/env python3
"""
UTCS-MI: EstándarUniversal:Codigo,Autogenesis,DO178C,00.00,HealingSafetyMonitor,0004,v1.0,Aerospace and Quantum United Agency,GeneracionHibrida,AIR,Amedeo Pelliccia,51de0c77,P0–P7
RTA (Run-Time Assurance) Supervisor for Self-Healing Systems
DAL-A safety monitor with partitioning from DAL-B healing control
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import time
import math

# Safety limits per AMEDEO Systems cert requirements
MAX_SKIN_TEMP_DELTA_C = 25.0     # ≤+25°C over 5s
MAX_CURRENT_PER_TILE_A = 1.0     # ≤1A per tile
MAX_SURFACE_DUTY_CYCLE = 0.10    # ≤10% per minute
THERMAL_GUARD_TIMEOUT_MS = 500   # <500ms macro recovery thermal guard

@dataclass
class SafetyEnvelope:
    """Safety envelope for RTA monitoring"""
    max_temperature_delta: float  # °C
    max_current: float           # Amperes
    max_duty_cycle: float        # 0.0-1.0
    thermal_timeout: float       # seconds


@dataclass
class RTADecision:
    """RTA supervisor decision result"""
    approved: bool
    reasoning: str
    safety_constraints: Dict[str, float]
    timestamp: float
    envelope_reduction: Optional[float] = None  # For airborne macro operations


class RTASupervisor:
    """Run-Time Assurance supervisor (DAL-A) with safety interlocks"""
    
    def __init__(self, safety_envelope: SafetyEnvelope):
        self.safety_envelope = safety_envelope
        self.temperature_history = []
        self.current_history = []
        self.duty_cycle_tracker = {}
        self.thermal_guard_active = False
        self.airborne_mode = False
        
    def approve(self, pattern: List[float], energy: float, duration: float) -> bool:
        """RTA approval API for healing patterns"""
        decision = self._evaluate_safety_constraints(pattern, energy, duration)
        
        if decision.approved:
            self._update_safety_tracking(pattern, energy, duration)
            
        return decision.approved
    
    def approve_with_details(self, pattern: List[float], energy: float, duration: float) -> RTADecision:
        """RTA approval with detailed decision reasoning"""
        return self._evaluate_safety_constraints(pattern, energy, duration)
    
    def _evaluate_safety_constraints(self, pattern: List[float], energy: float, duration: float) -> RTADecision:
        """Evaluate healing action against safety constraints"""
        timestamp = time.time()
        
        # Calculate thermal impact
        thermal_delta = self._estimate_thermal_impact(pattern, energy, duration)
        
        # Check temperature safety limit
        if thermal_delta > self.safety_envelope.max_temperature_delta:
            return RTADecision(
                approved=False,
                reasoning=f"Thermal delta {thermal_delta:.1f}°C exceeds limit {self.safety_envelope.max_temperature_delta}°C",
                safety_constraints={"thermal_delta": thermal_delta},
                timestamp=timestamp
            )
        
        # Calculate current requirements
        current_required = self._estimate_current_draw(pattern, energy, duration)
        
        # Check current safety limit
        if current_required > self.safety_envelope.max_current:
            return RTADecision(
                approved=False,
                reasoning=f"Current {current_required:.2f}A exceeds limit {self.safety_envelope.max_current}A",
                safety_constraints={"current": current_required},
                timestamp=timestamp
            )
        
        # Check duty cycle limits
        duty_cycle = self._calculate_duty_cycle(duration)
        if duty_cycle > self.safety_envelope.max_duty_cycle:
            return RTADecision(
                approved=False,
                reasoning=f"Duty cycle {duty_cycle:.1%} exceeds limit {self.safety_envelope.max_duty_cycle:.1%}",
                safety_constraints={"duty_cycle": duty_cycle},
                timestamp=timestamp
            )
        
        # Check airborne constraints
        if self.airborne_mode and self._is_macro_operation(pattern, energy, duration):
            return RTADecision(
                approved=False,
                reasoning="Macro shape recovery prohibited while airborne",
                safety_constraints={"airborne_macro": True},
                timestamp=timestamp,
                envelope_reduction=0.5  # Reduce envelope for safety
            )
        
        # All constraints satisfied
        return RTADecision(
            approved=True,
            reasoning="All safety constraints satisfied",
            safety_constraints={
                "thermal_delta": thermal_delta,
                "current": current_required,
                "duty_cycle": duty_cycle
            },
            timestamp=timestamp
        )
    
    def _estimate_thermal_impact(self, pattern: List[float], energy: float, duration: float) -> float:
        """Estimate thermal delta from heating pattern"""
        # Simplified thermal model - real implementation would use FEA
        pattern_intensity = sum(pattern) / len(pattern) if pattern else 0.0
        
        # Thermal delta ∝ energy × intensity × time / thermal mass
        thermal_mass_factor = 10.0  # Simplified thermal mass
        thermal_delta = (energy * pattern_intensity * math.sqrt(duration)) / thermal_mass_factor
        
        return thermal_delta
    
    def _estimate_current_draw(self, pattern: List[float], energy: float, duration: float) -> float:
        """Estimate current draw from energy and duration"""
        if duration <= 0:
            return float('inf')  # Infinite current for zero time
            
        # P = I × V, assuming nominal voltage
        nominal_voltage = 12.0  # V
        power = energy / duration  # Watts
        current = power / nominal_voltage  # Amperes
        
        return current
    
    def _calculate_duty_cycle(self, duration: float) -> float:
        """Calculate duty cycle over last minute"""
        current_time = time.time()
        minute_ago = current_time - 60.0
        
        # Clean old entries
        self.duty_cycle_tracker = {
            t: d for t, d in self.duty_cycle_tracker.items() 
            if t > minute_ago
        }
        
        # Add current operation
        self.duty_cycle_tracker[current_time] = duration
        
        # Calculate total on-time in last minute
        total_on_time = sum(self.duty_cycle_tracker.values())
        duty_cycle = total_on_time / 60.0  # Duty cycle over 60 seconds
        
        return duty_cycle
    
    def _is_macro_operation(self, pattern: List[float], energy: float, duration: float) -> bool:
        """Determine if this is a macro shape recovery operation"""
        # Macro operations: longer duration (1-10s), higher energy
        return duration > MACRO_OPERATION_MIN_DURATION_S or energy > MACRO_OPERATION_MIN_ENERGY_J  # >1s or >100mJ
    
    def _update_safety_tracking(self, pattern: List[float], energy: float, duration: float):
        """Update safety tracking after approved action"""
        current_time = time.time()
        
        # Track temperature impact
        thermal_delta = self._estimate_thermal_impact(pattern, energy, duration)
        self.temperature_history.append({
            "timestamp": current_time,
            "thermal_delta": thermal_delta,
            "duration": duration
        })
        
        # Track current usage
        current_draw = self._estimate_current_draw(pattern, energy, duration)
        self.current_history.append({
            "timestamp": current_time,
            "current": current_draw,
            "duration": duration
        })
        
        # Activate thermal guard if needed
        if thermal_delta > 15.0:  # Significant heating
            self.thermal_guard_active = True
            
    def set_airborne_mode(self, airborne: bool):
        """Set airborne mode (restricts macro operations)"""
        self.airborne_mode = airborne
        
    def get_safety_status(self) -> Dict:
        """Get current safety status"""
        current_time = time.time()
        
        # Recent temperature tracking
        recent_temp_deltas = [
            entry["thermal_delta"] for entry in self.temperature_history
            if current_time - entry["timestamp"] < 300  # Last 5 minutes
        ]
        
        max_recent_temp = max(recent_temp_deltas) if recent_temp_deltas else 0.0
        
        # Recent current tracking
        recent_currents = [
            entry["current"] for entry in self.current_history
            if current_time - entry["timestamp"] < 60  # Last minute
        ]
        
        max_recent_current = max(recent_currents) if recent_currents else 0.0
        
        return {
            "safety_envelope_active": True,
            "airborne_mode": self.airborne_mode,
            "thermal_guard_active": self.thermal_guard_active,
            "max_recent_temp_delta": max_recent_temp,
            "max_recent_current": max_recent_current,
            "current_duty_cycle": self._calculate_duty_cycle(0),
            "timestamp": current_time
        }


class DALPartitionManager:
    """Partition manager for DAL-A/DAL-B separation"""
    
    def __init__(self):
        self.dal_a_functions = ["rta_supervisor", "safety_monitor", "thermal_guard"]
        self.dal_b_functions = ["heal_sense", "heal_exec", "pattern_synth"]
        self.dal_c_functions = ["maintenance", "det_logging", "analytics"]
        
    def validate_partition_boundary(self, function_name: str, target_dal: str) -> bool:
        """Validate DAL partition boundary access"""
        if target_dal == "DAL-A":
            return function_name in self.dal_a_functions
        elif target_dal == "DAL-B":
            return function_name in self.dal_b_functions
        elif target_dal == "DAL-C":
            return function_name in self.dal_c_functions
        return False
    
    def get_partition_info(self) -> Dict:
        """Get partition information"""
        return {
            "DAL-A": {
                "functions": self.dal_a_functions,
                "description": "Safety Monitor - RTA supervisor, interlocks, temp/energy guards"
            },
            "DAL-B": {
                "functions": self.dal_b_functions,
                "description": "Heal-Sense/Exec - feature extraction, pattern synth, arbitration"
            },
            "DAL-C": {
                "functions": self.dal_c_functions,
                "description": "Maintenance - DET logging, PQC signing, analytics"
            }
        }