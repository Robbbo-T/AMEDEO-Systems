"""
UTCS-MI: AQUART-TMR-CONSENSUS-consensus_engine-v1.0
2oo3 Consensus Engine with Tiebreaking and Deterministic Priority
"""

import asyncio
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict
from .core import ConsensusResult, ResponseSpec
from .engines import LocalLLMAdapter


class ConsensusEngine:
    """2oo3 Consensus Engine with deterministic tiebreaking"""
    
    def __init__(self):
        self.tiebreaker = LocalLLMAdapter("tiebreaker")
        self.engine_priorities = {
            "engine_a": 1,  # OpenAI - highest priority
            "engine_b": 2,  # Anthropic - medium priority  
            "engine_c": 3,  # Google - lowest priority
            "tiebreaker": 4  # Local model - fallback only
        }
    
    async def decide(self, validated_responses: List[Dict[str, Any]]) -> ConsensusResult:
        """
        Apply 2oo3 consensus logic:
        1. Group responses by content hash
        2. Find groups with 2+ agreeing responses
        3. If multiple groups have 2+ agreements, use deterministic priority
        4. If no 2+ agreement, trigger tiebreaker
        """
        
        if len(validated_responses) < 2:
            return ConsensusResult(
                accepted=False,
                winner_engine=None,
                merged_content=None,
                proof={"reason": "insufficient_responses"},
                reason="Less than 2 valid responses available"
            )
        
        # 1. Group by content hash
        hash_groups = defaultdict(list)
        for validated_resp in validated_responses:
            response = validated_resp["response"]
            validation = validated_resp["validation"]
            
            # Only consider responses that pass validation
            if validation.score >= 70.0:  # 70% validation threshold
                hash_groups[response.content_hash].append(validated_resp)
        
        # 2. Find groups with 2+ agreements (2oo3)
        consensus_groups = {
            hash_val: group for hash_val, group in hash_groups.items() 
            if len(group) >= 2
        }
        
        if len(consensus_groups) == 1:
            # Single consensus group - clear winner
            winner_hash, winner_group = next(iter(consensus_groups.items()))
            return self._create_consensus_result(winner_group, winner_hash, "2oo3_consensus")
        
        elif len(consensus_groups) > 1:
            # Multiple consensus groups - use deterministic priority
            return await self._resolve_multiple_consensus(consensus_groups)
        
        else:
            # No 2oo3 consensus - trigger tiebreaker
            return await self._trigger_tiebreaker(validated_responses)
    
    def _create_consensus_result(
        self, 
        winning_group: List[Dict[str, Any]], 
        consensus_hash: str,
        decision_type: str
    ) -> ConsensusResult:
        """Create consensus result from winning group"""
        
        # Select best response from group (lowest latency as tiebreaker)
        best_response = min(
            winning_group, 
            key=lambda x: x["response"].latency_ms
        )["response"]
        
        # Merge content from agreeing responses
        merged_content = best_response.content.copy()
        merged_content["consensus_metadata"] = {
            "consensus_hash": consensus_hash,
            "agreeing_engines": [resp["response"].engine for resp in winning_group],
            "agreement_count": len(winning_group),
            "decision_type": decision_type,
            "selected_engine": best_response.engine,
            "selection_reason": "lowest_latency"
        }
        
        # Build proof
        proof = {
            "consensus_hash": consensus_hash,
            "agreeing_engines": [resp["response"].engine for resp in winning_group],
            "agreeing_hashes": [resp["response"].content_hash for resp in winning_group],
            "agreement_count": len(winning_group),
            "decision_type": decision_type,
            "winner_selection": {
                "engine": best_response.engine,
                "latency_ms": best_response.latency_ms,
                "cost": best_response.cost,
                "validation_score": next(
                    resp["validation"].score for resp in winning_group 
                    if resp["response"].engine == best_response.engine
                )
            }
        }
        
        return ConsensusResult(
            accepted=True,
            winner_engine=best_response.engine,
            merged_content=merged_content,
            proof=proof,
            reason=f"2oo3 consensus achieved with {len(winning_group)} agreeing engines"
        )
    
    async def _resolve_multiple_consensus(
        self, 
        consensus_groups: Dict[str, List[Dict[str, Any]]]
    ) -> ConsensusResult:
        """Resolve multiple consensus groups using deterministic priority"""
        
        # Find the group with the highest priority engine
        best_group = None
        best_hash = None
        best_priority = float('inf')
        
        for hash_val, group in consensus_groups.items():
            # Find highest priority engine in this group
            group_priority = min(
                self.engine_priorities.get(resp["response"].engine, 999)
                for resp in group
            )
            
            if group_priority < best_priority:
                best_priority = group_priority
                best_group = group
                best_hash = hash_val
        
        if best_group:
            result = self._create_consensus_result(
                best_group, 
                best_hash, 
                "priority_resolved_consensus"
            )
            result.reason = f"Multiple consensus groups resolved by engine priority (priority {best_priority})"
            return result
        
        # Fallback - shouldn't happen but handle gracefully
        return ConsensusResult(
            accepted=False,
            winner_engine=None,
            merged_content=None,
            proof={"reason": "priority_resolution_failed"},
            reason="Failed to resolve multiple consensus groups"
        )
    
    async def _trigger_tiebreaker(
        self, 
        validated_responses: List[Dict[str, Any]]
    ) -> ConsensusResult:
        """Trigger tiebreaker when no 2oo3 consensus is reached"""
        
        try:
            # Prepare tiebreaker prompt
            from .core import PromptSpec
            
            # Summarize the disagreeing responses
            response_summaries = []
            for i, validated_resp in enumerate(validated_responses):
                response = validated_resp["response"]
                validation = validated_resp["validation"]
                
                summary = {
                    "engine": response.engine,
                    "content_preview": str(response.content)[:200] + "...",
                    "validation_score": validation.score,
                    "latency_ms": response.latency_ms,
                    "cost": response.cost
                }
                response_summaries.append(summary)
            
            tiebreaker_prompt = PromptSpec(
                id="tiebreaker_decision",
                template="Select the best response from the following options based on quality, validation score, and coherence: {summaries}",
                inputs={"summaries": response_summaries},
                controls={"temperature": 0.0, "max_tokens": 100}  # Deterministic
            )
            
            # Get tiebreaker decision
            tiebreaker_response = await self.tiebreaker.generate(tiebreaker_prompt)
            
            # Parse tiebreaker decision (mock implementation)
            decision = self._parse_tiebreaker_decision(tiebreaker_response, validated_responses)
            
            if decision:
                chosen_response, chosen_validation = decision
                
                merged_content = chosen_response.content.copy()
                merged_content["tiebreaker_metadata"] = {
                    "tiebreaker_used": True,
                    "tiebreaker_engine": self.tiebreaker.name,
                    "original_disagreement": len(validated_responses),
                    "chosen_engine": chosen_response.engine,
                    "tiebreaker_reasoning": tiebreaker_response.content.get("decision", "")
                }
                
                proof = {
                    "decision_type": "tiebreaker",
                    "tiebreaker_engine": self.tiebreaker.name,
                    "disagreeing_engines": [resp["response"].engine for resp in validated_responses],
                    "disagreeing_hashes": [resp["response"].content_hash for resp in validated_responses],
                    "chosen_engine": chosen_response.engine,
                    "chosen_hash": chosen_response.content_hash,
                    "tiebreaker_trace_id": getattr(tiebreaker_response, 'trace_id', None)
                }
                
                return ConsensusResult(
                    accepted=True,
                    winner_engine=chosen_response.engine,
                    merged_content=merged_content,
                    proof=proof,
                    reason="Tiebreaker resolved disagreement between engines",
                    fallback_used=True
                )
            
            else:
                # Fallback to deterministic priority if tiebreaker fails
                return self._fallback_to_priority(validated_responses)
                
        except Exception as e:
            # Final fallback
            return self._fallback_to_priority(validated_responses, error=str(e))
    
    def _parse_tiebreaker_decision(
        self, 
        tiebreaker_response: ResponseSpec, 
        validated_responses: List[Dict[str, Any]]
    ) -> Optional[Tuple[ResponseSpec, Any]]:
        """Parse tiebreaker decision and return chosen response"""
        
        try:
            # Mock parsing - in production would be more sophisticated
            decision_content = tiebreaker_response.content.get("decision", "")
            
            # Look for engine names in the decision
            for validated_resp in validated_responses:
                engine_name = validated_resp["response"].engine
                if engine_name in decision_content:
                    return validated_resp["response"], validated_resp["validation"]
            
            # If no clear decision, return highest validation score
            best_resp = max(
                validated_responses,
                key=lambda x: x["validation"].score
            )
            return best_resp["response"], best_resp["validation"]
            
        except Exception:
            return None
    
    def _fallback_to_priority(
        self, 
        validated_responses: List[Dict[str, Any]], 
        error: Optional[str] = None
    ) -> ConsensusResult:
        """Final fallback using engine priority"""
        
        # Select response from highest priority engine
        best_response = None
        best_validation = None
        best_priority = float('inf')
        
        for validated_resp in validated_responses:
            response = validated_resp["response"]
            validation = validated_resp["validation"]
            
            engine_priority = self.engine_priorities.get(response.engine, 999)
            if engine_priority < best_priority:
                best_priority = engine_priority
                best_response = response
                best_validation = validation
        
        if best_response:
            merged_content = best_response.content.copy()
            merged_content["fallback_metadata"] = {
                "fallback_reason": error or "no_consensus_achieved",
                "selected_by": "engine_priority",
                "priority_rank": best_priority,
                "validation_score": best_validation.score
            }
            
            proof = {
                "decision_type": "priority_fallback",
                "fallback_reason": error or "no_consensus_achieved",
                "chosen_engine": best_response.engine,
                "chosen_hash": best_response.content_hash,
                "engine_priority": best_priority,
                "available_engines": [resp["response"].engine for resp in validated_responses]
            }
            
            return ConsensusResult(
                accepted=True,
                winner_engine=best_response.engine,
                merged_content=merged_content,
                proof=proof,
                reason=f"Priority fallback selected {best_response.engine} (priority {best_priority})",
                fallback_used=True
            )
        
        # Ultimate fallback
        return ConsensusResult(
            accepted=False,
            winner_engine=None,
            merged_content=None,
            proof={"reason": "total_failure", "error": error},
            reason="All consensus mechanisms failed"
        )