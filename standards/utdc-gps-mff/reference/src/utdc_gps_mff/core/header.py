"""
UTDC-GPS-MFF Header Implementation
UTCS-MI: EstándarUniversal:Codigo-Desarrollo-UTDC-01.00-CoreHeader-0001-v1.0-AerospaceAndQuantumUnitedAdvancedVenture-GeneracionHumana-CROSS-ReferenceImpl-b2c3d4e5-RestoDeVidaUtil
"""

import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class ArtifactFormat:
    """Artifact format specification"""
    mime: str
    ext: str


@dataclass
class RegulationSchema:
    """Regulation schema specification"""
    name: str
    version: str


@dataclass
class ArtifactMetadata:
    """Core artifact metadata"""
    uri: str
    format: ArtifactFormat
    regulation_schema: RegulationSchema
    size_bytes: int
    sha256: str
    canonicalization: str


@dataclass
class TemplateReference:
    """Template reference specification"""
    uri: str
    version: str


@dataclass
class GenerationMetadata:
    """Generation process metadata"""
    method: str  # GeneracionHumana|GeneracionHibrida|GeneracionAuto
    model: str
    prompt_hash: str
    parameters: Dict[str, Any]


@dataclass
class ProvenanceEntry:
    """Provenance chain entry"""
    type: str
    id: str
    commit: str
    timestamp: Optional[str] = None


@dataclass
class Validator:
    """Validation rule specification"""
    name: str
    rule: str


@dataclass
class ComplianceMetadata:
    """Compliance validation metadata"""
    validators: List[Validator]
    result: str  # pending|passed|failed


@dataclass
class SecuritySignature:
    """Cryptographic signature specification"""
    alg: str  # Dilithium3|Ed25519
    sig: str


@dataclass
class SecurityMetadata:
    """Security classification and integrity"""
    classification: str  # CUI|PUBLIC|CONFIDENTIAL|SECRET
    integrity_signature: SecuritySignature


@dataclass
class Timestamps:
    """Creation and generation timestamps"""
    created_utc: str
    generated_utc: str


@dataclass
class Internationalization:
    """Language and locale specification"""
    lang: str  # BCP 47 language tag


class MFFHeader:
    """
    UTDC-GPS-MFF Header implementation
    
    Manages the complete MFF-Header structure with validation,
    serialization, and UTCS-MI compliance.
    """
    
    VALID_METHODS = {"GeneracionHumana", "GeneracionHibrida", "GeneracionAuto"}
    VALID_CLASSIFICATIONS = {"CUI", "PUBLIC", "CONFIDENTIAL", "SECRET"}
    VALID_DOMAINS = {"AIR", "SPACE", "DEFENSE", "GROUND", "CROSS"}
    
    def __init__(self, utcmi_id: str):
        """Initialize MFF Header with UTCS-MI identifier"""
        self.utcmi_id = utcmi_id
        self.validate_utcmi_id()
        
        # Initialize required fields
        self.repo_path: Optional[str] = None
        self.artifact: Optional[ArtifactMetadata] = None
        self.regulation_reference: List[str] = []
        self.template_ref: Optional[TemplateReference] = None
        self.generation: Optional[GenerationMetadata] = None
        self.provenance: List[ProvenanceEntry] = []
        self.compliance: Optional[ComplianceMetadata] = None
        self.security: Optional[SecurityMetadata] = None
        self.timestamps: Optional[Timestamps] = None
        self.license: str = "CC BY-SA 4.0"
        self.i18n: Optional[Internationalization] = None
    
    def validate_utcmi_id(self) -> bool:
        """Validate UTCS-MI v5.0+ identifier format"""
        if not self.utcmi_id.startswith("EstándarUniversal:"):
            raise ValueError("UTCS-MI ID must start with 'EstándarUniversal:'")
        
        parts = self.utcmi_id.split(":")[1].split("-")
        if len(parts) != 13:
            raise ValueError(f"UTCS-MI ID must have 13 fields, got {len(parts)}")
        
        # Validate version format (field 7)
        version = parts[6]
        if not version.startswith("v") or "." not in version[1:]:
            raise ValueError(f"Invalid version format: {version}")
        
        # Validate domain (field 10)
        domain = parts[9]
        if domain not in self.VALID_DOMAINS:
            raise ValueError(f"Invalid domain: {domain}")
        
        # Validate hash format (field 12)
        hash8 = parts[11]
        if len(hash8) != 8 or not all(c in "0123456789abcdef" for c in hash8):
            raise ValueError(f"Invalid hash8 format: {hash8}")
        
        return True
    
    def set_artifact(self, file_path: Path, regulation: str, version: str) -> None:
        """Set artifact metadata from file"""
        if not file_path.exists():
            raise FileNotFoundError(f"Artifact not found: {file_path}")
        
        with open(file_path, "rb") as f:
            content = f.read()
            sha256 = hashlib.sha256(content).hexdigest()
        
        mime_map = {
            ".xml": "application/xml",
            ".svg": "image/svg+xml",
            ".json": "application/json",
            ".mp4": "video/mp4",
            ".pdf": "application/pdf"
        }
        
        ext = file_path.suffix
        mime = mime_map.get(ext, "application/octet-stream")
        
        self.artifact = ArtifactMetadata(
            uri=str(file_path),
            format=ArtifactFormat(mime=mime, ext=ext[1:]),
            regulation_schema=RegulationSchema(name=regulation, version=version),
            size_bytes=len(content),
            sha256=sha256,
            canonicalization="utf8;lf;attr_order=asc;indent=2"
        )
    
    def set_generation(self, method: str, model: str, prompt: str, **params) -> None:
        """Set generation metadata"""
        if method not in self.VALID_METHODS:
            raise ValueError(f"Invalid generation method: {method}")
        
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:8]
        
        self.generation = GenerationMetadata(
            method=method,
            model=model,
            prompt_hash=prompt_hash,
            parameters=params
        )
    
    def add_provenance(self, prov_type: str, prov_id: str, commit: str) -> None:
        """Add provenance entry"""
        entry = ProvenanceEntry(
            type=prov_type,
            id=prov_id,
            commit=commit,
            timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        )
        self.provenance.append(entry)
    
    def set_compliance(self, validators: List[Dict], result: str = "pending") -> None:
        """Set compliance metadata"""
        validator_objs = [Validator(**v) for v in validators]
        self.compliance = ComplianceMetadata(validators=validator_objs, result=result)
    
    def set_security(self, classification: str, alg: str = "Dilithium3", sig: str = "") -> None:
        """Set security metadata"""
        if classification not in self.VALID_CLASSIFICATIONS:
            raise ValueError(f"Invalid classification: {classification}")
        
        self.security = SecurityMetadata(
            classification=classification,
            integrity_signature=SecuritySignature(alg=alg, sig=sig)
        )
    
    def set_timestamps(self, created: Optional[datetime] = None, generated: Optional[datetime] = None) -> None:
        """Set creation and generation timestamps"""
        now = datetime.now(timezone.utc)
        self.timestamps = Timestamps(
            created_utc=(created or now).isoformat().replace('+00:00', 'Z'),
            generated_utc=(generated or now).isoformat().replace('+00:00', 'Z')
        )
    
    def to_dict(self) -> Dict:
        """Convert header to dictionary"""
        result = {"utcmi_id": self.utcmi_id}
        
        if self.repo_path:
            result["repo_path"] = self.repo_path
        
        if self.artifact:
            result["artifact"] = {
                "uri": self.artifact.uri,
                "format": asdict(self.artifact.format),
                "regulation_schema": asdict(self.artifact.regulation_schema),
                "size_bytes": self.artifact.size_bytes,
                "sha256": self.artifact.sha256,
                "canonicalization": self.artifact.canonicalization
            }
        
        if self.regulation_reference:
            result["regulation_reference"] = self.regulation_reference
        
        if self.template_ref:
            result["template_ref"] = asdict(self.template_ref)
        
        if self.generation:
            result["generation"] = asdict(self.generation)
        
        if self.provenance:
            result["provenance"] = [asdict(p) for p in self.provenance]
        
        if self.compliance:
            result["compliance"] = {
                "validators": [asdict(v) for v in self.compliance.validators],
                "result": self.compliance.result
            }
        
        if self.security:
            result["security"] = {
                "classification": self.security.classification,
                "integrity_signature": asdict(self.security.integrity_signature)
            }
        
        if self.timestamps:
            result["timestamps"] = asdict(self.timestamps)
        
        result["license"] = self.license
        
        if self.i18n:
            result["i18n"] = asdict(self.i18n)
        
        return result
    
    def to_json(self, indent: int = 2) -> str:
        """Serialize header to canonical JSON"""
        return json.dumps(self.to_dict(), sort_keys=True, indent=indent, ensure_ascii=False)
    
    def save(self, path: Path) -> None:
        """Save header to file"""
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(self.to_json())
    
    @classmethod
    def from_dict(cls, data: Dict) -> "MFFHeader":
        """Create header from dictionary"""
        header = cls(data["utcmi_id"])
        
        # Populate fields from dictionary
        header.repo_path = data.get("repo_path")
        
        if "artifact" in data:
            a = data["artifact"]
            header.artifact = ArtifactMetadata(
                uri=a["uri"],
                format=ArtifactFormat(**a["format"]),
                regulation_schema=RegulationSchema(**a["regulation_schema"]),
                size_bytes=a["size_bytes"],
                sha256=a["sha256"],
                canonicalization=a["canonicalization"]
            )
        
        header.regulation_reference = data.get("regulation_reference", [])
        
        if "template_ref" in data:
            header.template_ref = TemplateReference(**data["template_ref"])
        
        if "generation" in data:
            header.generation = GenerationMetadata(**data["generation"])
        
        if "provenance" in data:
            header.provenance = [ProvenanceEntry(**p) for p in data["provenance"]]
        
        if "compliance" in data:
            c = data["compliance"]
            validators = [Validator(**v) for v in c["validators"]]
            header.compliance = ComplianceMetadata(validators=validators, result=c["result"])
        
        if "security" in data:
            s = data["security"]
            sig = SecuritySignature(**s["integrity_signature"])
            header.security = SecurityMetadata(
                classification=s["classification"],
                integrity_signature=sig
            )
        
        if "timestamps" in data:
            header.timestamps = Timestamps(**data["timestamps"])
        
        header.license = data.get("license", "CC BY-SA 4.0")
        
        if "i18n" in data:
            header.i18n = Internationalization(**data["i18n"])
        
        return header
    
    @classmethod
    def from_file(cls, path: Path) -> "MFFHeader":
        """Load header from file"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)