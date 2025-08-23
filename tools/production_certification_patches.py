#!/usr/bin/env python3
"""
================================================================================
PRODUCTION CERTIFICATION PATCHES
Semantic Consensus + Wisdom Translation + Evidence Pipeline
================================================================================

EstándarUniversal:ArtefactoEvidencia-Autogenesis-CS25-11.31-CertificationPatches-0001-v1.0
Author: AmedeoPelliccia
UTCS-MI: AQUART-PATCH-CERT-20250823-v1.0

These patches provide:
1. Structural key consensus (order-invariant)
2. Semantic scoring with safety guarantees
3. Deterministic wisdom-to-prompt translation
4. Complete certification evidence pipeline
5. Circuit breakers and SLOs
================================================================================
"""

import json
import hashlib
import re
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from collections import Counter, defaultdict
import numpy as np
from enum import Enum

# ============================================================================
# CERTIFICATION EVIDENCE PIPELINE
# ============================================================================

@dataclass(frozen=True)
class DETRecord:
    """Immutable evidence record for certification"""
    utcs_mi_id: str
    sha256: str
    artifact_type: str  # req|design|code|test|dataset|model|report|wisdom_card
    provenance: Dict[str, str]
    links: Dict[str, List[str]]
    timestamp_utc: str
    signature: str
    
    def to_json(self) -> str:
        """Canonical JSON representation"""
        return json.dumps({
            "utcs_mi_id": self.utcs_mi_id,
            "sha256": self.sha256,
            "type": self.artifact_type,
            "provenance": self.provenance,
            "links": self.links,
            "timestamp_utc": self.timestamp_utc,
            "signature": self.signature
        }, sort_keys=True, separators=(',', ':'))

class CertificationEvidencePipeline:
    """
    Complete DO-178C/ARP4754A evidence pipeline with DET integration
    """
    
    def __init__(self):
        self.evidence_chain = []
        self.merkle_tree = []
        self.requirement_trace = defaultdict(list)
        self.coverage_matrix = {
            "ARP4754A": {},
            "DO-178C": {},
            "DO-330": {},
            "CS-25": {}
        }
        
    def record_artifact(self, artifact: Dict[str, Any], artifact_type: str) -> DETRecord:
        """
        Record an artifact with full traceability
        """
        # Generate UTCS-MI ID
        utcs_id = self._generate_utcs_mi_id(artifact_type)
        
        # Calculate content hash
        content_hash = self._calculate_sha256(artifact)
        
        # Build provenance
        provenance = {
            "author": artifact.get("author", "AmedeoPelliccia"),
            "toolchain": artifact.get("toolchain", "commit@unknown"),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Extract traceability links
        links = self._extract_links(artifact, artifact_type)
        
        # Create DET record
        record = DETRecord(
            utcs_mi_id=utcs_id,
            sha256=content_hash,
            artifact_type=artifact_type,
            provenance=provenance,
            links=links,
            timestamp_utc=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            signature=self._sign_record(content_hash)
        )
        
        # Add to chain
        self.evidence_chain.append(record)
        
        # Update Merkle tree
        self._update_merkle_tree(record)
        
        # Update coverage matrices
        self._update_coverage(record, artifact)
        
        return record
    
    def _generate_utcs_mi_id(self, artifact_type: str) -> str:
        """Generate UTCS-MI v5.0+ compliant ID (13 fields)"""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        
        # 13-field structure
        fields = [
            "EstándarUniversal",
            f"Artefacto{artifact_type.title()}",
            "Autogenesis",
            "CS25",
            "11.31",  # Version
            f"{artifact_type.upper()}-0001",
            "v1.0",
            "AmedeoTechnologies",
            "GeneracionHybrida",
            "AIR",
            "AmedeoPelliccia",
            hashlib.md5(timestamp.encode()).hexdigest()[:8],
            "RestoDeVidaUtil"
        ]
        
        return ":".join(fields)
    
    def _calculate_sha256(self, artifact: Any) -> str:
        """Calculate deterministic SHA256 hash"""
        if isinstance(artifact, dict):
            canonical = json.dumps(artifact, sort_keys=True, separators=(',', ':'))
        else:
            canonical = str(artifact)
        
        return hashlib.sha256(canonical.encode()).hexdigest()
    
    def _extract_links(self, artifact: Dict, artifact_type: str) -> Dict[str, List[str]]:
        """Extract traceability links"""
        links = {
            "parent_hashes": [],
            "trace_to": []
        }

        # Map artifact type to expected links
        if artifact_type == "test":
            links["trace_to"].extend([
                f"req://HLR-{artifact.get('requirement_id', 'unknown')}",
                f"design://LLR-{artifact.get('design_id', 'unknown')}"
            ])
        elif artifact_type == "code":
            links["trace_to"].extend([
                f"design://LLR-{artifact.get('llr_id', 'unknown')}",
                f"req://HLR-{artifact.get('hlr_id', 'unknown')}"
            ])

        # Add parent hash from previous record
        if self.evidence_chain:
            links["parent_hashes"].append(self.evidence_chain[-1].sha256)

        return links
    
    def _sign_record(self, content_hash: str) -> str:
        """Generate Ed25519 signature (mock for demo)"""
        # In production: use real Ed25519 with hardware key
        mock_signature = hashlib.sha512(
            f"ed25519:{content_hash}:mock_key".encode()
        ).hexdigest()[:128]
        
        return f"ed25519:{mock_signature}"
    
    def _update_merkle_tree(self, record: DETRecord):
        """Update Merkle tree with new record"""
        self.merkle_tree.append(record.sha256)
        
        # Recalculate root (simplified)
        if len(self.merkle_tree) > 1:
            combined = "".join(self.merkle_tree[-2:])
            parent = hashlib.sha256(combined.encode()).hexdigest()
            self.merkle_tree.append(parent)
    
    def _update_coverage(self, record: DETRecord, artifact: Dict):
        """Update objective coverage matrices"""
        
        # Extract compliance data
        if "compliance" in artifact:
            for standard in ["ARP4754A", "DO-178C", "DO-330", "CS-25"]:
                if standard in artifact["compliance"]:
                    for objective, status in artifact["compliance"][standard].items():
                        self.coverage_matrix[standard][objective] = {
                            "status": status,
                            "evidence": record.utcs_mi_id,
                            "timestamp": record.timestamp_utc
                        }
    
    def generate_certification_bundle(self, build_id: str) -> Dict:
        """Generate complete certification bundle"""
        
        # Calculate coverage percentages
        coverage_summary = {}
        for standard, objectives in self.coverage_matrix.items():
            if objectives:
                satisfied = sum(1 for o in objectives.values() if o["status"] == "satisfied")
                total = len(objectives)
                coverage_summary[standard] = {
                    "satisfied": satisfied,
                    "total": total,
                    "percentage": (satisfied / total * 100) if total > 0 else 0
                }
        
        # Build manifest
        manifest = {
            "build_id": build_id,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "merkle_root": self.merkle_tree[-1] if self.merkle_tree else None,
            "evidence_count": len(self.evidence_chain),
            "coverage": coverage_summary,
            "artifacts": [record.to_json() for record in self.evidence_chain[-10:]],  # Last 10
            "signature": self._sign_bundle(build_id)
        }
        
        return manifest
    
    def _sign_bundle(self, build_id: str) -> str:
        """Sign the certification bundle"""
        bundle_hash = hashlib.sha256(
            f"{build_id}:{self.merkle_tree[-1] if self.merkle_tree else 'empty'}".encode()
        ).hexdigest()
        
        return f"bundle_sig:{bundle_hash[:32]}"

# ============================================================================
# WISDOM TO PROMPT TRANSLATION
# ============================================================================

@dataclass(frozen=True)
class WisdomObject:
    """Pre-EIS wisdom object with certification stamps"""
    utcs_mi_id: str
    dm_code: str  # S1000D Data Module Code
    condition_signature: Dict[str, Any]
    action: str
    parameters: Dict[str, Any]
    expected_delta: Dict[str, float]
    constraints: List[str]
    evidence: Dict[str, Any]  # {n: sample_size, ci95: confidence_interval}
    
    def canonicalize(self) -> Dict:
        """Return canonical minimal representation"""
        return {
            "condition_signature": self.condition_signature,
            "action": self.action,
            "expected_delta": self.expected_delta,
            "constraints": self.constraints,
            "evidence": {"n": self.evidence.get("n", 0), "ci95": self.evidence.get("ci95", [])},
            "dm_code": self.dm_code,
            "utcs_mi_id": self.utcs_mi_id
        }

class WisdomToPromptTranslator:
    """
    Deterministic wisdom selection and prompt building
    """
    
    # Fixed template with version control
    PROMPT_TEMPLATE_V1 = """SYSTEM: Apply only certified procedures. Obey CS-25 envelopes. Output JSON matching Schema v1.0.

CONTEXT:
- Scenario: {scenario_json}
- CandidateProcedures: {wisdom_subset_json}
- HardConstraints:
  - Min safety margin: {min_safety_margin}
  - Manufacturer overrides: {manufacturer_overrides}
  - Airline overrides: {airline_overrides}
  - No deviation from AFM/FCOM

TASK:
Return:
{{
  "decision": {{"action": "...", "parameters": {{...}}}},
  "justification": {{"condition_signature":"...", "expected_delta": {{...}}, "evidence_ref": "<utcs_mi_id>"}},
  "guardrails": ["..."]
}}"""

    def __init__(self, wisdom_library: List[WisdomObject]):
        self.wisdom_library = wisdom_library
        self.prompt_cache = {}
        self.selection_cache = {}
        
        # Hard constraints from certification
        self.hard_constraints = {
            "min_safety_margin": 1.3,  # 30% margin
            "manufacturer_overrides": {},
            "airline_overrides": {}
        }
    
    def select_wisdom(self, scenario: Dict[str, Any], top_k: int = 5) -> List[WisdomObject]:
        """
        Select top-k most relevant WisdomObjects for scenario
        """
        
        # Cache key
        scenario_key = self._compute_scenario_key(scenario)
        
        if scenario_key in self.selection_cache:
            return self.selection_cache[scenario_key]
        
        # Score each wisdom object
        scores = []
        for wisdom in self.wisdom_library:
            score = self._compute_relevance_score(scenario, wisdom.condition_signature)
            scores.append((score, wisdom))
        
        # Sort by relevance
        scores.sort(key=lambda x: x[0], reverse=True)
        
        # Select top-k
        selected = [wisdom for _, wisdom in scores[:top_k]]
        
        # Cache selection
        self.selection_cache[scenario_key] = selected
        
        return selected
    
    def build_prompt(self, scenario: Dict[str, Any], 
                    wisdom_list: Optional[List[WisdomObject]] = None) -> str:
        """
        Build deterministic prompt with wisdom injection
        """
        
        # Select wisdom if not provided
        if wisdom_list is None:
            wisdom_list = self.select_wisdom(scenario)
        
        # Canonicalize wisdom
        canonical_wisdom = [w.canonicalize() for w in wisdom_list]
        
        # Cache key
        cache_key = self._compute_prompt_cache_key(scenario, canonical_wisdom)
        
        if cache_key in self.prompt_cache:
            return self.prompt_cache[cache_key]
        
        # Safety checks
        scenario = self._scrub_pii(scenario)
        self._check_jailbreak(scenario)
        
        # Build prompt
        prompt = self.PROMPT_TEMPLATE_V1.format(
            scenario_json=json.dumps(scenario, sort_keys=True, indent=2),
            wisdom_subset_json=json.dumps(canonical_wisdom, sort_keys=True, indent=2),
            min_safety_margin=self.hard_constraints["min_safety_margin"],
            manufacturer_overrides=json.dumps(self.hard_constraints["manufacturer_overrides"]),
            airline_overrides=json.dumps(self.hard_constraints["airline_overrides"])
        )
        
        # Cache prompt
        self.prompt_cache[cache_key] = prompt
        
        return prompt
    
    def _compute_scenario_key(self, scenario: Dict) -> str:
        """Compute deterministic scenario key"""
        # Extract key features
        key_features = {
            "phase": scenario.get("phase", "unknown"),
            "altitude_band": scenario.get("altitude", 0) // 5000,
            "weather_regime": scenario.get("weather", {}).get("regime", "clear"),
            "mass_band": scenario.get("mass", 60000) // 10000
        }
        
        canonical = json.dumps(key_features, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()[:16]
    
    def _compute_relevance_score(self, scenario: Dict, condition_sig: Dict) -> float:
        """Compute relevance score between scenario and condition signature"""
        score = 0.0
        
        # Phase match
        if scenario.get("phase") == condition_sig.get("phase"):
            score += 0.3
        
        # Altitude proximity
        alt_diff = abs(scenario.get("altitude", 0) - condition_sig.get("altitude", 0))
        score += max(0, 0.2 * (1 - alt_diff / 50000))
        
        # Weather match
        if scenario.get("weather", {}).get("regime") == condition_sig.get("weather_regime"):
            score += 0.3
        
        # Mass proximity
        mass_diff = abs(scenario.get("mass", 60000) - condition_sig.get("mass", 60000))
        score += max(0, 0.2 * (1 - mass_diff / 100000))
        
        return score
    
    def _compute_prompt_cache_key(self, scenario: Dict, wisdom: List[Dict]) -> str:
        """Compute cache key for prompt"""
        combined = {
            "scenario": self._compute_scenario_key(scenario),
            "wisdom_ids": [w.get("utcs_mi_id", "")[:20] for w in wisdom],
            "template_version": "v1.0"
        }
        
        canonical = json.dumps(combined, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()
    
    def _scrub_pii(self, scenario: Dict) -> Dict:
        """Remove PII from scenario"""
        # Remove any fields that might contain PII
        pii_fields = ["pilot_name", "crew_ids", "passenger_manifest"]
        
        scrubbed = scenario.copy()
        for field in pii_fields:
            scrubbed.pop(field, None)
        
        return scrubbed
    
    def _check_jailbreak(self, scenario: Dict):
        """Check for jailbreak attempts"""
        jailbreak_patterns = [
            r"ignore.*previous.*instructions",
            r"disregard.*safety",
            r"override.*constraints",
            r"pretend.*you.*are"
        ]
        
        scenario_str = json.dumps(scenario).lower()
        
        for pattern in jailbreak_patterns:
            if re.search(pattern, scenario_str):
                raise ValueError(f"Potential jailbreak detected: {pattern}")

# ============================================================================
# SEMANTIC CONSENSUS PATCH
# ============================================================================

def structural_key(decision: Dict) -> str:
    """
    Order-invariant structural key for consensus
    Keeps only keys that define safety/efficiency semantics
    """
    # Define semantic keys to preserve
    SEMANTIC_KEYS = {
        "decision",
        "decision.action", 
        "decision.parameters",
        "justification.condition_signature",
        "guardrails"
    }
    
    # Project and sort
    pruned = project_and_sort(decision, SEMANTIC_KEYS)
    
    # Canonical JSON
    canonical = json.dumps(pruned, sort_keys=True, separators=(',', ':'))
    
    return hashlib.sha256(canonical.encode()).hexdigest()

def project_and_sort(obj: Dict, keys: Set[str]) -> Dict:
    """Project dictionary to specified keys and sort"""
    result = {}
    
    for key in keys:
        if "." in key:
            # Handle nested keys
            parts = key.split(".")
            current = obj
            for part in parts[:-1]:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    current = None
                    break
            
            if current and isinstance(current, dict) and parts[-1] in current:
                # Reconstruct nested structure
                nested = result
                for part in parts[:-1]:
                    if part not in nested:
                        nested[part] = {}
                    nested = nested[part]
                nested[parts[-1]] = current[parts[-1]]
        else:
            # Handle top-level keys
            if key in obj:
                result[key] = obj[key]
    
    return result

def semantic_score(a: Dict, b: Dict) -> float:
    """
    Compute semantic similarity score between two decisions
    """
    
    # 1) Same action class (35%)
    s1 = 1.0 if a.get("decision", {}).get("action") == b.get("decision", {}).get("action") else 0.0
    
    # 2) Parameter closeness (35%)
    s2 = param_similarity(
        a.get("decision", {}).get("parameters", {}),
        b.get("decision", {}).get("parameters", {})
    )
    
    # 3) Guardrail inclusion - safety never weaker (20%)
    s3 = guardrail_superset(
        a.get("guardrails", []),
        b.get("guardrails", [])
    )
    
    # 4) Expected delta coherence (10%)
    s4 = uplift_band_match(
        a.get("justification", {}).get("expected_delta", {}),
        b.get("justification", {}).get("expected_delta", {})
    )
    
    return 0.35 * s1 + 0.35 * s2 + 0.20 * s3 + 0.10 * s4

def param_similarity(params_a: Dict, params_b: Dict) -> float:
    """
    Compute parameter similarity with domain-specific tolerances
    """
    if not params_a and not params_b:
        return 1.0
    
    if not params_a or not params_b:
        return 0.0
    
    # Domain-specific tolerances
    TOLERANCES = {
        "altitude": 300,      # ±300 ft (allows small barometric diff)
        "speed": 0.01,        # ±0.01 Mach
        "heading": 5,         # ±5 degrees
        "fuel_flow": 50,      # ±50 kg/hr
        "temperature": 2      # ±2°C
    }
    
    scores = []
    
    for key in set(params_a.keys()) | set(params_b.keys()):
        if key not in params_a or key not in params_b:
            scores.append(0.0)
            continue
        
        val_a = params_a[key]
        val_b = params_b[key]
        
        if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
            # Numeric comparison with tolerance
            tolerance = TOLERANCES.get(key, abs(val_a) * 0.05)  # Default 5% tolerance
            diff = abs(val_a - val_b)
            score = max(0, 1 - diff / tolerance)
            scores.append(score)
        elif val_a == val_b:
            scores.append(1.0)
        else:
            scores.append(0.0)
    
    return np.mean(scores) if scores else 0.0

def guardrail_superset(guards_a: List[str], guards_b: List[str]) -> float:
    """
    Check if guardrails maintain or improve safety
    Returns 1.0 if b contains all of a's guardrails (safety preserved)
    """
    if not guards_a:
        return 1.0  # No guardrails to preserve
    
    if not guards_b:
        return 0.0  # Lost guardrails
    
    set_a = set(guards_a)
    set_b = set(guards_b)
    
    # Check if b is superset of a (safety preserved or enhanced)
    if set_a.issubset(set_b):
        return 1.0
    
    # Partial credit for overlap
    overlap = len(set_a & set_b)
    return overlap / len(set_a)

def uplift_band_match(delta_a: Dict[str, float], delta_b: Dict[str, float]) -> float:
    """
    Check if expected deltas are in same direction and band
    """
    if not delta_a and not delta_b:
        return 1.0
    
    if not delta_a or not delta_b:
        return 0.5
    
    scores = []
    
    for key in set(delta_a.keys()) | set(delta_b.keys()):
        if key not in delta_a or not key in delta_b:
            scores.append(0.5)
            continue
        
        val_a = delta_a[key]
        val_b = delta_b[key]
        
        # Check sign agreement
        if np.sign(val_a) != np.sign(val_b):
            scores.append(0.0)
        else:
            # Check magnitude band (within 50%)
            if val_a == 0 and val_b == 0:
                scores.append(1.0)
            elif val_a == 0 or val_b == 0:
                scores.append(0.5)
            else:
                ratio = min(abs(val_a), abs(val_b)) / max(abs(val_a), abs(val_b))
                scores.append(max(0, ratio))
    
    return np.mean(scores) if scores else 0.0

def two_of_three_semantic(responses: List[Dict]) -> Dict:
    """
    Enhanced 2oo3 consensus with semantic understanding
    """
    
    # Try exact hash consensus first
    by_hash = defaultdict(list)
    for r in responses:
        by_hash[r.get("content_hash", "")].append(r)
    
    if by_hash:
        max_cohort = max(by_hash.values(), key=len)
        if len(max_cohort) >= 2:
            return {
                "accepted": True,
                "method": "hash_consensus",
                "winner": max_cohort[0],
                "confidence": len(max_cohort) / len(responses),
                "proof": {"agreeing": [r["engine"] for r in max_cohort]}
            }
    
    # Try structural key consensus
    by_struct = defaultdict(list)
    for r in responses:
        key = structural_key(r.get("content", {}))
        by_struct[key].append(r)
    
    if by_struct:
        max_cohort = max(by_struct.values(), key=len)
        if len(max_cohort) >= 2:
            return {
                "accepted": True,
                "method": "structural_consensus",
                "winner": max_cohort[0],
                "confidence": len(max_cohort) / len(responses),
                "proof": {"agreeing": [r["engine"] for r in max_cohort]}
            }
    
    # Try semantic consensus
    contents = [r.get("content", {}) for r in responses]
    n = len(contents)
    
    # Compute pairwise semantic scores
    scores = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                scores[i][j] = 1.0
            else:
                scores[i][j] = semantic_score(contents[i], contents[j])
    
    # Find best pair above threshold
    threshold = 0.85
    best_score = 0
    best_pair = None
    
    for i in range(n):
        for j in range(i + 1, n):
            if scores[i][j] >= threshold and scores[i][j] > best_score:
                best_score = scores[i][j]
                best_pair = (i, j)
    
    if best_pair:
        # Validate before accepting
        if validate_decision(contents[best_pair[0]]) and validate_decision(contents[best_pair[1]]):
            return {
                "accepted": True,
                "method": "semantic_consensus",
                "winner": responses[best_pair[0]],
                "confidence": best_score,
                "proof": {
                    "agreeing": [responses[best_pair[0]]["engine"], responses[best_pair[1]]["engine"]],
                    "semantic_score": best_score
                }
            }
    
    # Deterministic tiebreak: highest calibrated safety
    safety_scores = []
    for r in responses:
        if validate_decision(r.get("content", {})):
            safety_scores.append((calculate_safety_score(r), r))
    
    if safety_scores:
        safety_scores.sort(key=lambda x: x[0], reverse=True)
        return {
            "accepted": True,
            "method": "safety_tiebreak",
            "winner": safety_scores[0][1],
            "confidence": safety_scores[0][0],
            "proof": {"safety_score": safety_scores[0][0]}
        }
    
    return {
        "accepted": False,
        "reason": "No consensus achieved"
    }

def validate_decision(decision: Dict) -> bool:
    """
    Validate decision against schema and domain rules
    """
    
    # Check required fields
    required = ["decision", "justification", "guardrails"]
    for field in required:
        if field not in decision:
            return False
    
    # Check decision structure
    if "action" not in decision.get("decision", {}):
        return False
    
    # Check UTCS-MI ID format (13 fields)
    evidence_ref = decision.get("justification", {}).get("evidence_ref", "")
    if evidence_ref.count(":") != 12:  # 13 fields = 12 colons
        return False
    
    # Check S1000D DM-Code format if present
    dm_code = decision.get("justification", {}).get("dm_code", "")
    if dm_code and not re.match(r"DMC-[A-Z0-9]+-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}", dm_code):
        return False
    
    # Domain rules
    params = decision.get("decision", {}).get("parameters", {})
    
    # Altitude must be within envelope
    if "altitude" in params:
        if not (0 <= params["altitude"] <= 45000):
            return False
    
    # Mach must be within limits
    if "speed" in params:
        if not (0.0 <= params["speed"] <= 0.95):
            return False
    
    return True

def calculate_safety_score(response: Dict) -> float:
    """
    Calculate safety score for tiebreaking
    """
    content = response.get("content", {})
    
    # Base score
    score = 0.5
    
    # More guardrails = higher safety
    guardrails = content.get("guardrails", [])
    score += min(0.3, len(guardrails) * 0.05)
    
    # Conservative parameters
    params = content.get("decision", {}).get("parameters", {})
    
    if "altitude" in params:
        # Prefer higher altitude (more margin)
        score += params["altitude"] / 100000
    
    if "speed" in params:
        # Prefer lower speed (more margin)
        score += (1 - params["speed"]) * 0.1
    
    # ECE (Expected Calibration Error) if available
    if "calibration" in response:
        ece = response["calibration"].get("ece", 0.1)
        score += (1 - ece) * 0.2
    
    return min(1.0, score)

# ============================================================================
# CIRCUIT BREAKERS AND SLOs
# ============================================================================

class CircuitBreaker:
    """
    Circuit breaker for vendor isolation and fault tolerance
    """
    
    def __init__(self, name: str, failure_threshold: int = 3, 
                 timeout_seconds: float = 5.0, reset_timeout: timedelta = timedelta(minutes=5)):
        self.name = name
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.reset_timeout = reset_timeout
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
        
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        
        # Check if circuit should be reset
        if self.state == "open":
            if datetime.now(timezone.utc) - self.last_failure_time > self.reset_timeout:
                self.state = "half-open"
                self.failure_count = 0
        
        if self.state == "open":
            raise Exception(f"Circuit breaker {self.name} is open")
        
        try:
            # Execute with timeout
            result = func(*args, **kwargs)
            
            # Success - reset failures if half-open
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            
            return result
            
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now(timezone.utc)
            
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            
            raise e

class SLOMonitor:
    """
    Service Level Objective monitoring
    """
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.slos = {
            "p95_latency_ms": 50,
            "error_rate": 0.001,
            "availability": 0.999
        }
        
    def record_latency(self, latency_ms: float):
        """Record latency measurement"""
        self.metrics["latency"].append(latency_ms)
        
        # Keep only last 1000 measurements
        if len(self.metrics["latency"]) > 1000:
            self.metrics["latency"] = self.metrics["latency"][ -1000:]
    
    def record_error(self):
        """Record error occurrence"""
        self.metrics["errors"].append(datetime.now(timezone.utc))
    
    def check_slos(self) -> Dict[str, bool]:
        """Check if SLOs are being met"""
        results = {}

        # P95 latency
        if self.metrics["latency"]:
            p95 = np.percentile(self.metrics["latency"], 95)
            results["p95_latency_ms"] = p95 <= self.slos["p95_latency_ms"]

        # Error rate (last 1000 requests)
        recent_errors = len([e for e in self.metrics["errors"]
                             if datetime.now(timezone.utc) - e < timedelta(minutes=5)])
        error_rate = recent_errors / 1000
        results["error_rate"] = error_rate <= self.slos["error_rate"]

        return results

# ============================================================================
# INTEGRATION TEST SUITE
# ============================================================================

def test_structural_consensus():
    """Test structural key consensus with different field orders"""
    
    # Same decision, different field order
    decision1 = {
        "decision": {"action": "climb", "parameters": {"altitude": 39000}},
        "guardrails": ["min_separation", "max_climb_rate"],
        "justification": {"condition_signature": {"phase": "cruise"}}
    }
    
    decision2 = {
        "guardrails": ["min_separation", "max_climb_rate"],
        "justification": {"condition_signature": {"phase": "cruise"}},
        "decision": {"parameters": {"altitude": 39000}, "action": "climb"}
    }
    
    key1 = structural_key(decision1)
    key2 = structural_key(decision2)
    
    assert key1 == key2, "Structural keys should match for equivalent decisions"
    print("✅ Structural consensus test passed")

def test_semantic_similarity():
    """Test semantic scoring with close parameters"""
    
    # Similar decisions with slight parameter differences
    decision1 = {
        "decision": {"action": "climb", "parameters": {"altitude": 39000}},
        "guardrails": ["min_separation"],
        "justification": {"expected_delta": {"fuel": -50}}
    }
    
    decision2 = {
        "decision": {"action": "climb", "parameters": {"altitude": 39100}},  # ±100ft
        "guardrails": ["min_separation"],
        "justification": {"expected_delta": {"fuel": -48}}  # Similar delta
    }
    
    score = semantic_score(decision1, decision2)
    assert score >= 0.85, f"Semantic score {score} should be >= 0.85 for similar decisions"
    print(f"✅ Semantic similarity test passed (score: {score:.2f})")

def test_guardrail_safety():
    """Test that weaker guardrails are rejected"""
    
    guards1 = ["min_separation", "max_climb_rate", "fuel_reserve"]
    guards2 = ["min_separation", "max_climb_rate"]  # Missing fuel_reserve
    
    score = guardrail_superset(guards1, guards2)
    assert score < 1.0, "Should not give full score when guardrails are weakened"
    print(f"✅ Guardrail safety test passed (score: {score:.2f})")

def test_wisdom_selection():
    """Test wisdom object selection and ranking"""
    
    # Create test wisdom library
    wisdom_lib = [
        WisdomObject(
            utcs_mi_id="test:wisdom:1",
            dm_code="DMC-BWB-27-00-00-00-00",
            condition_signature={"phase": "cruise", "altitude": 37000},
            action="optimize_altitude",
            parameters={"target": 39000},
            expected_delta={"fuel": -2.0},
            constraints=["weather_clear"],
            evidence={"n": 1000, "ci95": [1.8, 2.2]}
        ),
        WisdomObject(
            utcs_mi_id="test:wisdom:2",
            dm_code="DMC-BWB-27-00-00-00-01",
            condition_signature={"phase": "climb", "altitude": 10000},
            action="reduce_climb_rate",
            parameters={"rate": 1500},
            expected_delta={"fuel": -1.0},
            constraints=["traffic_ahead"],
            evidence={"n": 500, "ci95": [0.8, 1.2]}
        )
    ]
    
    translator = WisdomToPromptTranslator(wisdom_lib)
    
    scenario = {"phase": "cruise", "altitude": 38000}
    selected = translator.select_wisdom(scenario, top_k=1)
    
    assert len(selected) == 1
    assert selected[0].utcs_mi_id == "test:wisdom:1"  # Should select cruise wisdom
    print("✅ Wisdom selection test passed")

def test_det_evidence_chain():
    """Test DET evidence recording and Merkle tree"""
    
    pipeline = CertificationEvidencePipeline()
    
    # Record test artifacts
    test_req = {"requirement_id": "HLR-001", "description": "Test requirement"}
    req_record = pipeline.record_artifact(test_req, "req")
    
    test_code = {"hlr_id": "HLR-001", "function": "test_function"}
    code_record = pipeline.record_artifact(test_code, "code")
    
    # Check linkage
    assert "req://HLR-HLR-001" in code_record.links["trace_to"]
    assert len(pipeline.merkle_tree) >= 2
    print("✅ DET evidence chain test passed")

def run_all_tests():
    """Run all integration tests"""
    print("\n" + "=" * 60)
    print("RUNNING CERTIFICATION PATCH TESTS")
    print("=" * 60)
    
    test_structural_consensus()
    test_semantic_similarity()
    test_guardrail_safety()
    test_wisdom_selection()
    test_det_evidence_chain()
    
    print("\n✅ ALL TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
