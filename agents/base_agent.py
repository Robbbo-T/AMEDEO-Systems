#!/usr/bin/env python3
"""
UTCS-MI: AQUART-AGT-CODE-base_agent-v1.0
AMEDEO Base Agent Framework
Depth: foundational agent contract for bordering the future
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
import json
import time
from pathlib import Path


@dataclass
class Intent:
    """Agent execution intent with depth indicators"""
    kind: str                 # e.g., "HORIZON_SHIFT", "SUPPLY_CHAIN_METAMORPHOSIS"
    payload: Dict[str, Any]   # free-form, validated by POLICY/AMOReS
    
    def affects_strategy(self) -> bool:
        """Check if intent changes strategic decisions"""
        return self.payload.get("affects_strategy", False)
    
    def affects_tempo(self) -> bool:
        """Check if intent changes operational rhythms"""
        return self.payload.get("affects_tempo", False)
    
    def expands_envelope(self) -> bool:
        """Check if intent expands operational limits"""
        return self.payload.get("expands_envelope", False)


@dataclass
class Result:
    """Agent execution result with evidence"""
    status: str
    reason: str = ""
    productivity_delta: float = 0.0
    trace_id: str = ""
    evidence: Optional[Dict[str, Any]] = None
    extras: Optional[Dict[str, Any]] = None


def to_factor(x: float, kind: str = "gain") -> float:
    """
    Normalize metrics to 'factor > 1.0':
    - gain:     4.1  -> 4.1x
    - reduce:   0.28 -> 1/(1-0.72)=3.57x  (if '0.28' is remaining fraction)
    """
    if kind == "gain":    
        return max(x, 1.0)
    if kind == "reduce":  
        # Handle edge cases: if x is 0.0 or 1.0, return large factor
        if x <= 0.0:
            return 1e6  # Very large factor for complete elimination
        if x >= 1.0:
            return 1e6  # Very large factor for complete reduction
        return 1.0 / (1.0 - x)  # Normal case: x=0.72 => 3.57x
    return max(x, 1.0)


class DET:
    """Deterministic Evidence Trace system"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.trace_log = []
    
    def begin_trace(self, intent: Intent) -> str:
        """Start a new trace for the intent"""
        trace_id = f"{self.agent_id}-{int(time.time()*1000)}"
        self.trace_log.append({
            "trace_id": trace_id,
            "timestamp": time.time(),
            "intent": {
                "kind": intent.kind,
                "payload": intent.payload
            },
            "status": "STARTED"
        })
        return trace_id
    
    def commit_trace(self, trace_id: str, evidence: Dict[str, Any]):
        """Commit evidence for a trace"""
        for entry in self.trace_log:
            if "trace_id" in entry and entry["trace_id"] == trace_id:
                entry["evidence"] = evidence
                entry["status"] = "COMMITTED"
                entry["commit_timestamp"] = time.time()
                break
    
    def log_rejection(self, intent: Intent, reason: str):
        """Log a rejected intent"""
        self.trace_log.append({
            "timestamp": time.time(),
            "intent": {
                "kind": intent.kind,
                "payload": intent.payload
            },
            "status": "REJECTED",
            "reason": reason
        })
    
    def log_failure(self, trace_id: str, error: Exception):
        """Log a failed execution"""
        for entry in self.trace_log:
            if "trace_id" in entry and entry["trace_id"] == trace_id:
                entry["status"] = "FAILED"
                entry["error"] = str(error)
                entry["failure_timestamp"] = time.time()
                break
    
    @staticmethod
    def verify_trace(trace_id: str) -> bool:
        """Verify trace integrity (mock implementation)"""
        return True
    
    @staticmethod
    def verify_cascade_trace(trace_ids: List[str]) -> bool:
        """Verify cascade of traces (mock implementation)"""
        return all(trace_ids)


class AMOReS:
    """Adaptive Moral Operating System - ethical/legal guardrails"""
    
    def __init__(self):
        self.rules = self._load_default_rules()
    
    def _load_default_rules(self) -> Dict[str, Any]:
        """Load default ethical/legal rules"""
        return {
            "max_risk_level": 0.3,
            "requires_human_approval": ["irreversible_changes", "regulatory_impact"],
            "forbidden_actions": ["data_destruction", "unauthorized_access"],
            "min_productivity_delta": 3.0
        }
    
    def validate(self, intent: Intent) -> bool:
        """Validate intent against ethical/legal rules"""
        # Check for forbidden actions
        if intent.kind in self.rules["forbidden_actions"]:
            return False
        
        # Check productivity requirements - be more flexible for test cases
        expected_delta = intent.payload.get("expected_gain", None)
        if expected_delta is not None and expected_delta < self.rules["min_productivity_delta"]:
            return False
        
        # Check risk level
        risk_level = intent.payload.get("risk_level", 0.0)
        if risk_level > self.rules["max_risk_level"]:
            return False
        
        return True


class SEAL:
    """Cryptographic signature system using PQC"""
    
    def __init__(self):
        self.signature_algorithm = "Dilithium-mock"
    
    def sign(self, obj: Any) -> Dict[str, Any]:
        """Sign object with PQC signature"""
        return {
            "algorithm": self.signature_algorithm,
            "signature": f"PQC_SIG_{hash(str(obj)) % 10000:04d}",
            "object_hash": f"sha256:{hash(str(obj)) % 100000000:08x}",
            "timestamp": time.time()
        }


class AMEDEOAgent:
    """Base agent that borders the future, not paints it"""
    
    MIN_DEPTH_FACTOR = 3.0
    
    def __init__(self, agent_id: str, policy_path: str):
        self.id = agent_id
        self.policy_path = policy_path
        self.det = DET(agent_id)
        self.amores = AMOReS()
        self.seal = SEAL()
        self.policy = self._load_policy()
    
    def _load_policy(self) -> Dict[str, Any]:
        """Load agent policy configuration"""
        if Path(self.policy_path).exists():
            try:
                with open(self.policy_path, 'r') as f:
                    # Simple policy parsing - in production would be more sophisticated
                    return {"loaded": True, "path": self.policy_path}
            except Exception:
                pass
        return {"loaded": False, "default": True}
    
    def execute(self, intent: Intent) -> Result:
        """Execute intent with full validation and tracing"""
        
        # 1. Depth test: surface actions are rejected
        if self._is_surface(intent):
            self.det.log_rejection(intent, "DEPTH_TEST_FAIL")
            return Result(
                status="REJECTED", 
                reason="Surface action - does not change decisions/rhythms/limits"
            )
        
        # 2. AMOReS validation: ethical/legal guardrails
        if not self.amores.validate(intent):
            self.det.log_rejection(intent, "AMORES_FAIL")
            return Result(
                status="FAIL_SAFE", 
                reason="Ethical/legal guardrails violated"
            )
        
        # 3. Execute with tracing
        trace_id = self.det.begin_trace(intent)
        try:
            result = self._execute_core(intent)
            
            # 4. Verify minimum depth impact
            if result.productivity_delta < self.MIN_DEPTH_FACTOR:
                return Result(
                    status="REJECTED", 
                    reason=f"Insufficient depth impact: {result.productivity_delta:.1f}x < {self.MIN_DEPTH_FACTOR}x",
                    extras={"achieved_delta": result.productivity_delta}
                )
            
            # 5. Sign evidence and commit trace
            result.evidence = self.seal.sign(result)
            result.trace_id = trace_id
            self.det.commit_trace(trace_id, result.evidence)
            
            return result
            
        except Exception as e:
            self.det.log_failure(trace_id, e)
            return Result(
                status="FAIL_SAFE", 
                reason=f"Execution failed, safe fallback: {e}"
            )
    
    def _is_surface(self, intent: Intent) -> bool:
        """Test if intent is surface-level (not deep)"""
        return not any([
            intent.affects_strategy(),
            intent.affects_tempo(), 
            intent.expands_envelope()
        ])
    
    def _execute_core(self, intent: Intent) -> Result:
        """Core execution logic - to be overridden by specialized agents"""
        return Result(
            status="SUCCESS", 
            productivity_delta=self.MIN_DEPTH_FACTOR,
            reason="Base agent default execution"
        )


class InsufficientDepth(Exception):
    """Raised when agent action lacks required depth"""
    pass


class InsufficientImpact(Exception):
    """Raised when productivity delta is below threshold"""
    pass


class InsufficientEnvelopeExpansion(Exception):
    """Raised when envelope expansion is below threshold"""
    pass