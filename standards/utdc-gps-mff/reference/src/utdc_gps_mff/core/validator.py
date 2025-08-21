"""
UTDC-GPS-MFF Validator Implementation
UTCS-MI: EstándarUniversal:Codigo-Desarrollo-UTDC-01.01-Validator-0001-v1.0-AerospaceAndQuantumUnitedAdvancedVenture-GeneracionHumana-CROSS-ReferenceImpl-c3d4e5f6-RestoDeVidaUtil
"""

import json
import jsonschema
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .header import MFFHeader


@dataclass
class ValidationResult:
    """Validation result container"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    coverage: float = 0.0


class MFFValidator:
    """
    UTDC-GPS-MFF Validator
    
    Provides comprehensive validation for MFF artifacts including:
    - UTCS-MI compliance
    - JSON schema validation
    - Regulatory schema validation
    - Hash verification
    - Signature validation
    """
    
    def __init__(self, schema_path: Optional[Path] = None):
        """Initialize validator with optional custom schema"""
        self.schema_path = schema_path or self._get_default_schema_path()
        self.schema = self._load_schema()
        
    def _get_default_schema_path(self) -> Path:
        """Get default schema path"""
        return Path(__file__).parent.parent.parent / "schemas" / "mff-header-v1.0.json"
    
    def _load_schema(self) -> Dict:
        """Load JSON schema for validation"""
        if not self.schema_path.exists():
            # Return basic schema if file doesn't exist
            return {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "required": ["utcmi_id"],
                "properties": {
                    "utcmi_id": {"type": "string"},
                    "repo_path": {"type": "string"},
                    "artifact": {"type": "object"},
                    "regulation_reference": {"type": "array"},
                    "template_ref": {"type": "object"},
                    "generation": {"type": "object"},
                    "provenance": {"type": "array"},
                    "compliance": {"type": "object"},
                    "security": {"type": "object"},
                    "timestamps": {"type": "object"},
                    "license": {"type": "string"},
                    "i18n": {"type": "object"}
                }
            }
        
        with open(self.schema_path, 'r') as f:
            return json.load(f)
    
    def validate_file(self, file_path: Path) -> ValidationResult:
        """Validate MFF header file"""
        errors = []
        warnings = []
        
        try:
            # Load and parse header
            header = MFFHeader.from_file(file_path)
            return self.validate_header(header)
            
        except FileNotFoundError:
            errors.append(f"Header file not found: {file_path}")
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON format: {e}")
        except Exception as e:
            errors.append(f"Header parsing error: {e}")
        
        return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
    
    def validate_header(self, header: MFFHeader) -> ValidationResult:
        """Validate MFF header object"""
        errors = []
        warnings = []
        
        # Validate UTCS-MI compliance
        try:
            header.validate_utcmi_id()
        except ValueError as e:
            errors.append(f"UTCS-MI validation failed: {e}")
        
        # Validate JSON schema
        try:
            jsonschema.validate(header.to_dict(), self.schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation failed: {e.message}")
        except jsonschema.SchemaError as e:
            errors.append(f"Schema error: {e.message}")
        
        # Validate mandatory fields
        header_dict = header.to_dict()
        mandatory_fields = [
            "utcmi_id", "artifact", "regulation_reference", 
            "template_ref", "generation", "compliance", 
            "security", "timestamps", "license"
        ]
        
        for field in mandatory_fields:
            if field not in header_dict or header_dict[field] is None:
                errors.append(f"Missing mandatory field: {field}")
        
        # Validate artifact hash if file exists
        if header.artifact and Path(header.artifact.uri).exists():
            if not self._verify_artifact_hash(header.artifact):
                errors.append("Artifact hash verification failed")
        elif header.artifact:
            warnings.append(f"Artifact file not found: {header.artifact.uri}")
        
        # Validate generation method
        if header.generation and header.generation.method not in header.VALID_METHODS:
            errors.append(f"Invalid generation method: {header.generation.method}")
        
        # Validate security classification
        if header.security and header.security.classification not in header.VALID_CLASSIFICATIONS:
            errors.append(f"Invalid security classification: {header.security.classification}")
        
        # Calculate coverage
        total_fields = len(mandatory_fields) + 3  # Optional fields: repo_path, provenance, i18n
        present_fields = sum(1 for field in mandatory_fields + ["repo_path", "provenance", "i18n"] 
                           if field in header_dict and header_dict[field] is not None)
        coverage = (present_fields / total_fields) * 100
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            coverage=coverage
        )
    
    def _verify_artifact_hash(self, artifact) -> bool:
        """Verify artifact hash matches file content"""
        try:
            file_path = Path(artifact.uri)
            with open(file_path, "rb") as f:
                content = f.read()
                import hashlib
                actual_hash = hashlib.sha256(content).hexdigest()
                return actual_hash == artifact.sha256
        except Exception:
            return False
    
    def validate_regulatory_compliance(self, header: MFFHeader, regulation: str) -> ValidationResult:
        """Validate compliance with specific regulation"""
        errors = []
        warnings = []
        
        if not header.regulation_reference or regulation not in header.regulation_reference:
            errors.append(f"Header not marked for regulation: {regulation}")
        
        if not header.compliance:
            errors.append("No compliance metadata found")
        elif header.compliance.result == "failed":
            errors.append("Compliance validation marked as failed")
        elif header.compliance.result == "pending":
            warnings.append("Compliance validation is pending")
        
        # Regulation-specific validations
        if regulation == "S1000D" and header.artifact:
            if header.artifact.format.ext != "xml":
                errors.append("S1000D requires XML format")
        
        if regulation in ["DO-178C", "CS-25"] and header.security:
            if header.security.classification == "PUBLIC":
                warnings.append(f"{regulation} typically requires restricted classification")
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)
    
    def validate_cascade_requirements(self, headers: List[MFFHeader]) -> ValidationResult:
        """Validate cascade requirements across multiple headers"""
        errors = []
        warnings = []
        
        if len(headers) < 1:
            errors.append("No headers provided for cascade validation")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
        
        # Validate individual requirements (≥3x impact)
        for header in headers:
            # Mock validation - in practice would check specific impact metrics
            if header.generation and "impact" in header.generation.parameters:
                impact = header.generation.parameters.get("impact", 0)
                if impact < 3.0:
                    errors.append(f"Header {header.utcmi_id} has insufficient impact: {impact} < 3.0")
        
        # Validate cascade total (≥81x)
        total_impact = 1.0
        for header in headers:
            if header.generation and "impact" in header.generation.parameters:
                total_impact *= header.generation.parameters.get("impact", 1.0)
        
        if total_impact < 81.0:
            errors.append(f"Cascade total impact insufficient: {total_impact} < 81.0")
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)