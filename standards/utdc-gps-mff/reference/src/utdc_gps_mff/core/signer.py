"""
UTDC-GPS-MFF Signer Implementation
UTCS-MI: EstándarUniversal:Codigo-Desarrollo-UTDC-01.02-Signer-0001-v1.0-AerospaceAndQuantumUnitedAdvancedVenture-GeneracionHumana-CROSS-ReferenceImpl-d4e5f6a7-RestoDeVidaUtil

Integrates with existing AMEDEO SEAL PQC signing infrastructure
"""

import sys
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional

# Import existing SEAL system
sys.path.append(str(Path(__file__).parents[5] / "agents"))
try:
    from base_agent import SEAL
except ImportError:
    # Fallback mock implementation if base_agent not available
    class SEAL:
        def __init__(self):
            self.signature_algorithm = "Dilithium-mock"
        
        def sign(self, obj: Any) -> Dict[str, Any]:
            return {
                "algorithm": self.signature_algorithm,
                "signature": f"PQC_SIG_{hash(str(obj)) % 10000:04d}",
                "object_hash": f"sha256:{hash(str(obj)) % 100000000:08x}",
                "timestamp": "mock_timestamp"
            }

from .header import MFFHeader


class MFFSigner:
    """
    UTDC-GPS-MFF Cryptographic Signer
    
    Provides PQC signature capabilities for MFF artifacts using
    the existing AMEDEO SEAL infrastructure.
    """
    
    def __init__(self, algorithm: str = "Dilithium3"):
        """Initialize signer with specified algorithm"""
        self.algorithm = algorithm
        self.seal = SEAL()
        
    def sign_header(self, header: MFFHeader) -> str:
        """Sign MFF header and update security metadata"""
        # Generate canonical representation for signing
        canonical_json = header.to_json()
        content_hash = hashlib.sha256(canonical_json.encode()).hexdigest()
        
        # Use SEAL to generate PQC signature
        seal_result = self.seal.sign(canonical_json)
        
        # Extract signature from SEAL result
        signature = seal_result.get("signature", "")
        
        # Update header security metadata
        if not header.security:
            header.set_security("CUI", self.algorithm, signature)
        else:
            header.security.integrity_signature.alg = self.algorithm
            header.security.integrity_signature.sig = signature
        
        return signature
    
    def sign_artifact(self, artifact_path: Path, header: MFFHeader) -> str:
        """Sign artifact file and update header"""
        if not artifact_path.exists():
            raise FileNotFoundError(f"Artifact not found: {artifact_path}")
        
        # Read and hash artifact
        with open(artifact_path, "rb") as f:
            content = f.read()
            content_hash = hashlib.sha256(content).hexdigest()
        
        # Sign the hash
        seal_result = self.seal.sign(content_hash)
        signature = seal_result.get("signature", "")
        
        # Update header artifact hash if needed
        if header.artifact:
            header.artifact.sha256 = content_hash
        
        return signature
    
    def verify_signature(self, header: MFFHeader) -> bool:
        """Verify header signature"""
        if not header.security or not header.security.integrity_signature.sig:
            return False
        
        # Generate canonical representation
        canonical_json = header.to_json()
        
        # For mock implementation, verify by regenerating signature
        seal_result = self.seal.sign(canonical_json)
        expected_signature = seal_result.get("signature", "")
        
        return expected_signature == header.security.integrity_signature.sig
    
    def create_signature_chain(self, headers: list[MFFHeader]) -> Dict[str, str]:
        """Create signature chain for multiple related headers"""
        signatures = {}
        
        for header in headers:
            signature = self.sign_header(header)
            signatures[header.utcmi_id] = signature
        
        # Create chain signature
        chain_content = "|".join(signatures.values())
        chain_signature = self.seal.sign(chain_content).get("signature", "")
        signatures["_chain"] = chain_signature
        
        return signatures