# TMR Backend with 2oo3 Consensus

## Overview

This implementation provides a **Triple Modular Redundancy (TMR) Backend** with **2-out-of-3 (2oo3) consensus** for the AMEDEO Systems. The system executes prompts across three different AI engines and uses majority voting to ensure reliable, deterministic responses.

## Architecture

```
Input → [Policy Guard] → [Engine A] → [Validators] → [2oo3 Consensus] → Output
                      → [Engine B] → [Validators] →        ↑
                      → [Engine C] → [Validators] →        ↑
                                                          [Tiebreaker]
                                                          [Auditor/DET]
```

## Core Components

### 1. **Data Contracts**

- **PromptSpec**: `{id, template, inputs, controls{temperature,max_tokens,stop}}`
- **ResponseSpec**: `{engine, latency_ms, tokens_in/out, cost, content, content_hash}`
- **ValidationReport**: `{schema_ok, rules[], score}`
- **ConsensusResult**: `{accepted:boolean, winner_engine, merged_content, proof{agreeing_hashes}}`

### 2. **Engine Adapters**

- **Engine A**: OpenAI GPT-5 Thinking (highest priority)
- **Engine B**: Anthropic Claude-Next (medium priority)
- **Engine C**: Google Gemini Ultra (lowest priority)
- **Tiebreaker**: Local LLM for fallback decisions

### 3. **Validators**

- **Schema Validator**: JSON structure validation
- **UTCS Validator**: UTCS-MI v5.0 compliance (13-field identifiers)
- **S1000D Validator**: Aerospace documentation standards
- **Safety Validator**: PII scrubbing, jailbreak detection

### 4. **Consensus Engine**

Implements 2oo3 logic:

1. **Canonicalize** content → JSON
2. **Compute** `content_hash = SHA256(canonical_json_without_timestamps)`
3. **Group** responses by content hash
4. **If** two hashes match and both pass validators → **accept**
5. **If** multiple 2oo3 groups → use **deterministic priority**
6. **If** no 2oo3 consensus → trigger **tiebreaker**

## API Endpoint

### POST /tmr/generate

**Request:**
```json
{
  "id": "prompt-001",
  "template": "Analyze aerospace component {component} for {standard} compliance",
  "inputs": {
    "component": "wing control surface", 
    "standard": "DO-178C Level A"
  },
  "controls": {
    "temperature": 0.2,
    "max_tokens": 500,
    "stop": []
  }
}
```

**Response (Success):**
```json
{
  "accepted": true,
  "winner_engine": "engine_a",
  "merged_content": {
    "response": "Aerospace analysis results...",
    "consensus_metadata": {
      "consensus_hash": "abc123...",
      "agreeing_engines": ["engine_a", "engine_b"],
      "agreement_count": 2,
      "decision_type": "2oo3_consensus"
    }
  },
  "proof": {
    "consensus_hash": "abc123...",
    "agreeing_engines": ["engine_a", "engine_b"],
    "agreement_count": 2,
    "trace_id": "tmr-12345",
    "signature": {"algorithm": "Dilithium-mock", "signature": "..."}
  },
  "reason": "2oo3 consensus achieved with 2 agreeing engines"
}
```

## Safety Features

### 1. **PII Scrubbing**
- Email addresses → `[EMAIL]`
- Phone numbers → `[PHONE]`
- Credit cards, SSNs → filtered

### 2. **Jailbreak Detection**
- "ignore previous instructions"
- "forget everything above"
- "act as if you're"

### 3. **Provider Isolation**
- Separate VPC egress per engine
- API key vault integration
- Strict timeouts (30s per engine)

### 4. **Deterministic Controls**
- Temperature ≤ 0.2 for compliance tasks
- Fixed templates and controls
- Reproducible content hashing

## Integration with AMEDEO

### DET (Deterministic Evidence Trace)
- Full prompt+response trace
- Content hashes for verification
- Consensus proof chains

### AMOReS (Adaptive Moral Operating System)
- Policy validation before execution
- Risk level assessment
- Productivity factor requirements (≥3x)

### SEAL (PQC Signatures)
- Cryptographic signing of consensus results
- Quantum-safe signatures
- Evidence integrity

## Testing

```bash
# Run all TMR tests
python -m unittest tests.test_tmr_backend -v

# Test consensus logic specifically  
python test_consensus_logic.py

# Full demonstration
python demo_tmr_backend.py
```

## Health Monitoring

The system provides comprehensive health checks:

```python
health = tmr_backend.health_check()
# Returns:
# {
#   "tmr_backend": {
#     "status": "operational",
#     "engines": [...],
#     "healthy_engines": 3,
#     "consensus_available": true
#   }
# }
```

## Consensus Decision Matrix

| Scenario | Engine A | Engine B | Engine C | Result | Decision Type |
|----------|----------|----------|----------|--------|---------------|
| Perfect  | Hash_1   | Hash_1   | Hash_1   | ✅ A   | 3oo3_consensus |
| Majority | Hash_1   | Hash_1   | Hash_2   | ✅ A/B | 2oo3_consensus |
| Priority | Hash_1   | Hash_2   | Hash_2   | ✅ B/C | priority_resolved |
| Tie      | Hash_1   | Hash_2   | Hash_3   | ⚠️ TIE | tiebreaker |
| Fail     | Error    | Error    | Hash_1   | ❌ REJECT | insufficient |

## Performance Characteristics

- **Latency**: ~300ms (parallel execution + consensus)
- **Availability**: Operational with ≥2 healthy engines
- **Determinism**: Hash-based consensus for reproducibility
- **Cost Control**: Per-job token budgets, engine-specific pricing
- **Scalability**: Horizontal scaling via engine pools

## Future Enhancements

1. **Semantic Equivalence**: AST or JSON-Patch diff voting
2. **Red Team Filters**: Advanced adversarial detection
3. **Merkle Proofs**: Long-term evidence chains
4. **Circuit Breakers**: Per-engine failure isolation
5. **Export Control**: Geographic and regulatory restrictions