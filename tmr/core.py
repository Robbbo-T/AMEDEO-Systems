"""
UTCS-MI: AQUART-TMR-CORE-tmr_core-v1.0
TMR Core Backend with Data Contracts and Main Orchestration
"""

import asyncio
import json
import hashlib
import time
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import sys

# Import existing AMEDEO infrastructure
sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))
from base_agent import DET, AMOReS, SEAL

@dataclass
class PromptSpec:
    """Prompt specification with controls"""
    id: str
    template: str
    inputs: Dict[str, Any]
    controls: Dict[str, Any]  # temperature, max_tokens, stop sequences

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass 
class ResponseSpec:
    """Engine response specification"""
    engine: str
    latency_ms: int
    tokens_in: int
    tokens_out: int
    cost: float
    content: Dict[str, Any]
    content_hash: str
    timestamp: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ValidationReport:
    """Validation report for responses"""
    schema_ok: bool
    rules: List[str]
    score: float
    errors: List[str] = None
    warnings: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ConsensusResult:
    """2oo3 consensus result"""
    accepted: bool
    winner_engine: Optional[str]
    merged_content: Optional[Dict[str, Any]]
    proof: Dict[str, Any]  # agreeing_hashes, trace_ids, etc.
    reason: str = ""
    fallback_used: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def canonicalize(obj: Dict[str, Any]) -> str:
    """Canonicalize object for consistent hashing"""
    # Remove timestamps and other volatile fields
    clean_obj = {k: v for k, v in obj.items() if k not in ['timestamp', 'latency_ms']}
    return json.dumps(clean_obj, separators=(",", ":"), sort_keys=True)


def content_hash(obj: Dict[str, Any]) -> str:
    """Compute SHA256 hash of canonicalized content"""
    return hashlib.sha256(canonicalize(obj).encode()).hexdigest()


class TMRBackend:
    """Triple Modular Redundancy Backend with 2oo3 Consensus"""
    
    def __init__(self, agent_id: str = "tmr-backend"):
        self.agent_id = agent_id
        self.det = DET(agent_id)
        self.amores = AMOReS()
        self.seal = SEAL()
        
        # Initialize mock engines (will be replaced with real adapters)
        from .engines import OpenAIAdapter, AnthropicAdapter, GoogleAdapter
        self.engines = [
            OpenAIAdapter("engine_a"),
            AnthropicAdapter("engine_b"), 
            GoogleAdapter("engine_c")
        ]
        
        # Initialize validators
        from .validators import TMRValidator
        self.validator = TMRValidator()
        
        # Initialize consensus engine
        from .consensus import ConsensusEngine
        self.consensus = ConsensusEngine()

    async def generate(self, prompt_spec: PromptSpec) -> ConsensusResult:
        """
        Main TMR generation with 2oo3 consensus
        
        Flow:
        1. Normalize prompt and validate policy
        2. Fan out to all 3 engines in parallel 
        3. Validate each response
        4. Apply 2oo3 consensus on content hashes
        5. Return result with audit trail
        """
        
        # 1. Input normalization and policy validation
        if not self._validate_prompt_policy(prompt_spec):
            return ConsensusResult(
                accepted=False,
                winner_engine=None,
                merged_content=None,
                proof={"reason": "policy_violation"},
                reason="Prompt failed policy validation"
            )
        
        # 2. Begin DET trace
        trace_id = self.det.begin_trace(self._prompt_to_intent(prompt_spec))
        
        try:
            # 3. Parallel execution with timeout
            responses = await self._execute_parallel(prompt_spec)
            
            # 4. Validate responses
            validated_responses = await self._validate_responses(responses)
            
            # 5. Apply 2oo3 consensus
            consensus_result = await self._apply_consensus(validated_responses)
            
            # 6. Add audit evidence 
            consensus_result.proof["trace_id"] = trace_id
            consensus_result.proof["engines_used"] = [r.engine for r in responses]
            consensus_result.proof["validation_scores"] = [
                r.get("validation_score", 0.0) for r in validated_responses
            ]
            
            # 7. Sign with SEAL and commit trace
            evidence = self.seal.sign(consensus_result)
            consensus_result.proof["signature"] = evidence
            self.det.commit_trace(trace_id, evidence)
            
            return consensus_result
            
        except Exception as e:
            self.det.log_failure(trace_id, e)
            return ConsensusResult(
                accepted=False,
                winner_engine=None,
                merged_content=None,
                proof={"error": str(e), "trace_id": trace_id},
                reason=f"TMR execution failed: {e}"
            )

    def _validate_prompt_policy(self, prompt_spec: PromptSpec) -> bool:
        """Validate prompt against AMEDEO policy using AMOReS"""
        # Convert PromptSpec to Intent for AMOReS validation
        intent = self._prompt_to_intent(prompt_spec)
        return self.amores.validate(intent)

    def _prompt_to_intent(self, prompt_spec: PromptSpec):
        """Convert PromptSpec to Intent for AMEDEO compatibility"""
        from base_agent import Intent
        
        return Intent(
            kind="TMR_GENERATE",
            payload={
                "prompt_id": prompt_spec.id,
                "template": prompt_spec.template,
                "risk_level": 0.1,  # Low risk for standard generation
                "expected_gain": 3.0  # Minimum productivity factor
            }
        )

    async def _execute_parallel(self, prompt_spec: PromptSpec) -> List[ResponseSpec]:
        """Execute prompt on all engines in parallel with timeout"""
        
        async def call_engine_with_timeout(engine, prompt_spec):
            try:
                # 30 second timeout per engine
                return await asyncio.wait_for(
                    engine.generate(prompt_spec), 
                    timeout=30.0
                )
            except asyncio.TimeoutError:
                return ResponseSpec(
                    engine=engine.name,
                    latency_ms=30000,
                    tokens_in=0,
                    tokens_out=0, 
                    cost=0.0,
                    content={"error": "timeout"},
                    content_hash="timeout",
                    timestamp=time.time()
                )
            except Exception as e:
                return ResponseSpec(
                    engine=engine.name,
                    latency_ms=0,
                    tokens_in=0,
                    tokens_out=0,
                    cost=0.0, 
                    content={"error": str(e)},
                    content_hash="error",
                    timestamp=time.time()
                )
        
        # Execute all engines in parallel
        tasks = [call_engine_with_timeout(engine, prompt_spec) for engine in self.engines]
        responses = await asyncio.gather(*tasks, return_exceptions=False)
        
        return responses

    async def _validate_responses(self, responses: List[ResponseSpec]) -> List[Dict[str, Any]]:
        """Validate each response using TMR validators"""
        validated = []
        
        for response in responses:
            # Skip error responses
            if "error" in response.content:
                continue
                
            validation_report = await self.validator.validate(response)
            
            validated.append({
                "response": response,
                "validation": validation_report,
                "validation_score": validation_report.score
            })
        
        return validated

    async def _apply_consensus(self, validated_responses: List[Dict[str, Any]]) -> ConsensusResult:
        """Apply 2oo3 consensus logic"""
        return await self.consensus.decide(validated_responses)

    def health_check(self) -> Dict[str, Any]:
        """Health check for TMR backend"""
        engine_health = []
        for engine in self.engines:
            try:
                health = engine.health_check()
                engine_health.append({
                    "name": engine.name,
                    "status": "healthy" if health else "unhealthy",
                    "last_check": time.time()
                })
            except Exception as e:
                engine_health.append({
                    "name": engine.name, 
                    "status": "error",
                    "error": str(e),
                    "last_check": time.time()
                })
        
        healthy_count = sum(1 for e in engine_health if e["status"] == "healthy")
        
        return {
            "tmr_backend": {
                "status": "operational" if healthy_count >= 2 else "degraded",
                "engines": engine_health,
                "healthy_engines": healthy_count,
                "consensus_available": healthy_count >= 2,
                "agent_id": self.agent_id
            }
        }