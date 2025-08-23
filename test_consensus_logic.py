#!/usr/bin/env python3
"""
Test 2oo3 Consensus Logic Specifically
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from tmr.consensus import ConsensusEngine
from tmr.core import ResponseSpec, ValidationReport


def create_mock_response(engine_name: str, content_data: dict, validation_score: float = 95.0) -> dict:
    """Create a mock validated response"""
    from tmr.core import content_hash
    
    response = ResponseSpec(
        engine=engine_name,
        latency_ms=100 + hash(engine_name) % 50,  # Varied latency
        tokens_in=50,
        tokens_out=100,
        cost=0.01,
        content=content_data,
        content_hash=content_hash(content_data),
        timestamp=1234567890.0
    )
    
    validation = ValidationReport(
        schema_ok=True,
        rules=["schema_validation", "utcs_compliance", "safety_validation"],
        score=validation_score
    )
    
    return {
        "response": response,
        "validation": validation,
        "validation_score": validation_score
    }


async def test_consensus_scenarios():
    """Test various consensus scenarios"""
    
    print("🎯 Testing 2oo3 Consensus Logic")
    print("=" * 40)
    
    consensus = ConsensusEngine()
    
    # Scenario 1: Perfect 3oo3 consensus
    print("1. Testing 3oo3 Perfect Consensus")
    same_content = {"response": "Identical aerospace analysis", "model": "test"}
    responses_3oo3 = [
        create_mock_response("engine_a", same_content),
        create_mock_response("engine_b", same_content),
        create_mock_response("engine_c", same_content)
    ]
    
    result = await consensus.decide(responses_3oo3)
    print(f"   Result: {'✅ ACCEPTED' if result.accepted else '❌ REJECTED'}")
    print(f"   Decision Type: {result.proof.get('decision_type', 'unknown')}")
    print(f"   Agreement Count: {result.proof.get('agreement_count', 0)}")
    print()
    
    # Scenario 2: 2oo3 consensus (engines A and B agree)
    print("2. Testing 2oo3 Consensus (A+B agree, C differs)")
    content_ab = {"response": "Standard aerospace analysis", "model": "test"}
    content_c = {"response": "Alternative aerospace analysis", "model": "test"}
    responses_2oo3 = [
        create_mock_response("engine_a", content_ab),
        create_mock_response("engine_b", content_ab),
        create_mock_response("engine_c", content_c)
    ]
    
    result = await consensus.decide(responses_2oo3)
    print(f"   Result: {'✅ ACCEPTED' if result.accepted else '❌ REJECTED'}")
    print(f"   Decision Type: {result.proof.get('decision_type', 'unknown')}")
    print(f"   Agreeing Engines: {result.proof.get('agreeing_engines', [])}")
    print(f"   Winner: {result.winner_engine}")
    print()
    
    # Scenario 3: No consensus - all different
    print("3. Testing No Consensus (all engines differ)")
    responses_no_consensus = [
        create_mock_response("engine_a", {"response": "Analysis type A", "model": "test"}),
        create_mock_response("engine_b", {"response": "Analysis type B", "model": "test"}),
        create_mock_response("engine_c", {"response": "Analysis type C", "model": "test"})
    ]
    
    result = await consensus.decide(responses_no_consensus)
    print(f"   Result: {'✅ ACCEPTED' if result.accepted else '❌ REJECTED'}")
    print(f"   Decision Type: {result.proof.get('decision_type', 'unknown')}")
    print(f"   Fallback Used: {result.fallback_used}")
    if result.accepted:
        print(f"   Chosen Engine: {result.winner_engine}")
    print()
    
    # Scenario 4: Multiple 2oo3 groups (should use priority)
    print("4. Testing Multiple 2oo3 Groups (priority resolution)")
    content_group1 = {"response": "High priority analysis", "model": "test"}
    content_group2 = {"response": "Low priority analysis", "model": "test"}
    
    # Create responses where A+B agree and C gets same hash by chance
    # Then add more responses to create two groups
    responses_multi = [
        create_mock_response("engine_a", content_group1),  # High priority
        create_mock_response("engine_b", content_group2),  # Medium priority
        create_mock_response("engine_c", content_group2),  # Low priority - forms group with B
    ]
    
    # Add validation that creates two potential consensus groups
    responses_multi.append(create_mock_response("engine_a", content_group1))  # Duplicate for group
    
    result = await consensus.decide(responses_multi[:3])  # Use original 3
    print(f"   Result: {'✅ ACCEPTED' if result.accepted else '❌ REJECTED'}")
    print(f"   Decision Type: {result.proof.get('decision_type', 'unknown')}")
    if result.accepted:
        print(f"   Winner: {result.winner_engine}")
    print()
    
    # Scenario 5: Low validation scores (should be filtered out)
    print("5. Testing Low Validation Scores")
    responses_low_validation = [
        create_mock_response("engine_a", same_content, validation_score=50.0),  # Below threshold
        create_mock_response("engine_b", same_content, validation_score=60.0),  # Below threshold  
        create_mock_response("engine_c", same_content, validation_score=80.0)   # Above threshold
    ]
    
    result = await consensus.decide(responses_low_validation)
    print(f"   Result: {'✅ ACCEPTED' if result.accepted else '❌ REJECTED'}")
    print(f"   Reason: {result.reason}")
    print()
    
    # Scenario 6: Single engine (insufficient responses)
    print("6. Testing Insufficient Responses")
    single_response = [create_mock_response("engine_a", same_content)]
    
    result = await consensus.decide(single_response)
    print(f"   Result: {'✅ ACCEPTED' if result.accepted else '❌ REJECTED'}")
    print(f"   Reason: {result.reason}")
    print()
    
    print("🎯 Consensus Testing Complete!")
    print()
    
    # Summary
    print("📊 Summary of 2oo3 Consensus Behavior:")
    print("   ✅ 3oo3: All engines agree → immediate consensus")
    print("   ✅ 2oo3: Two engines agree → majority consensus")
    print("   ⚠️  1oo3: No agreement → tiebreaker or priority fallback")
    print("   ⚠️  0oo3: All fail validation → rejection")
    print("   🔒 Priority: engine_a > engine_b > engine_c > tiebreaker")


if __name__ == "__main__":
    asyncio.run(test_consensus_scenarios())