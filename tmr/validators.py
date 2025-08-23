"""
UTCS-MI: AQUART-TMR-VALIDATORS-tmr_validators-v1.0  
TMR Validators with S1000D/UTCS checks and schema validation
"""

import re
import json
from typing import Dict, Any, List
from pathlib import Path
import sys

# Import existing AMEDEO validation infrastructure  
sys.path.insert(0, str(Path(__file__).parent.parent))

from .core import ResponseSpec, ValidationReport


class TMRValidator:
    """Main TMR validator orchestrating all validation checks"""
    
    def __init__(self):
        self.schema_validator = SchemaValidator()
        self.utcs_validator = UTCSValidator()
        self.s1000d_validator = S1000DValidator()
        self.safety_validator = SafetyValidator()

    async def validate(self, response: ResponseSpec) -> ValidationReport:
        """Comprehensive validation of engine response"""
        errors = []
        warnings = []
        rules_passed = []
        
        # 1. Schema validation
        schema_result = self.schema_validator.validate(response)
        if not schema_result["valid"]:
            errors.extend(schema_result["errors"])
        else:
            rules_passed.append("schema_validation")
        
        # 2. UTCS-MI compliance
        utcs_result = self.utcs_validator.validate(response)
        if not utcs_result["valid"]:
            errors.extend(utcs_result["errors"])
        else:
            rules_passed.append("utcs_compliance")
        
        # 3. S1000D compliance (if applicable)
        s1000d_result = self.s1000d_validator.validate(response)
        if not s1000d_result["valid"]:
            warnings.extend(s1000d_result["warnings"])  # S1000D warnings, not errors
        else:
            rules_passed.append("s1000d_compliance")
        
        # 4. Safety validation
        safety_result = self.safety_validator.validate(response)
        if not safety_result["valid"]:
            errors.extend(safety_result["errors"])
        else:
            rules_passed.append("safety_validation")
        
        # Calculate overall score
        total_checks = 4
        passed_checks = len(rules_passed)
        score = (passed_checks / total_checks) * 100.0
        
        return ValidationReport(
            schema_ok=schema_result["valid"],
            rules=rules_passed,
            score=score,
            errors=errors,
            warnings=warnings
        )


class SchemaValidator:
    """JSON schema validation for response structure"""
    
    def __init__(self):
        self.response_schema = self._load_response_schema()
    
    def _load_response_schema(self) -> Dict[str, Any]:
        """Load or define response schema"""
        return {
            "type": "object",
            "required": ["response", "model"],
            "properties": {
                "response": {"type": "string", "minLength": 1},
                "model": {"type": "string"},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                "reasoning": {"type": "string"},
                "analysis": {"type": "string"}
            }
        }
    
    def validate(self, response: ResponseSpec) -> Dict[str, Any]:
        """Validate response against schema"""
        try:
            content = response.content
            
            # Check required fields
            if "response" not in content:
                return {"valid": False, "errors": ["Missing 'response' field"]}
            
            if not isinstance(content["response"], str) or len(content["response"]) == 0:
                return {"valid": False, "errors": ["Invalid 'response' field - must be non-empty string"]}
            
            if "model" not in content:
                return {"valid": False, "errors": ["Missing 'model' field"]}
            
            # Check confidence if present
            if "confidence" in content:
                conf = content["confidence"]
                if not isinstance(conf, (int, float)) or not (0 <= conf <= 1):
                    return {"valid": False, "errors": ["Invalid confidence value - must be between 0 and 1"]}
            
            return {"valid": True, "errors": []}
            
        except Exception as e:
            return {"valid": False, "errors": [f"Schema validation error: {e}"]}


class UTCSValidator:
    """UTCS-MI v5.0 compliance validator"""
    
    def __init__(self):
        # UTCS-MI identifier regex pattern
        self.utcs_pattern = re.compile(
            r'^AQUART-[A-Z]{3,4}-[A-Z0-9_-]+-[a-zA-Z0-9_-]+-v\d+\.\d+$'
        )
    
    def validate(self, response: ResponseSpec) -> Dict[str, Any]:
        """Validate UTCS-MI compliance"""
        errors = []
        
        try:
            content = response.content
            
            # Check for UTCS-MI metadata if present
            if "utcs_id" in content:
                utcs_id = content["utcs_id"]
                if not self.utcs_pattern.match(utcs_id):
                    errors.append(f"Invalid UTCS-MI ID format: {utcs_id}")
            
            # Check 13-field identifier semantic validation
            if "artifact_id" in content:
                artifact_id = content["artifact_id"]
                if not self._validate_artifact_semantics(artifact_id):
                    errors.append(f"Invalid UTCS artifact semantics: {artifact_id}")
            
            # Check determinism requirements
            if not self._check_determinism(response):
                errors.append("Response lacks deterministic characteristics")
            
            return {"valid": len(errors) == 0, "errors": errors}
            
        except Exception as e:
            return {"valid": False, "errors": [f"UTCS validation error: {e}"]}
    
    def _validate_artifact_semantics(self, artifact_id: str) -> bool:
        """Validate UTCS artifact semantic constraints"""
        # Basic semantic validation - in production would be more comprehensive
        parts = artifact_id.split('-')
        
        # Should have at least 4 parts: AQUART-TYPE-COMPONENT-VERSION
        if len(parts) < 4:
            return False
        
        # First part should be AQUART
        if parts[0] != "AQUART":
            return False
        
        # Version should match pattern
        version_part = parts[-1]
        version_pattern = re.compile(r'^v\d+\.\d+$')
        if not version_pattern.match(version_part):
            return False
        
        return True
    
    def _check_determinism(self, response: ResponseSpec) -> bool:
        """Check for deterministic characteristics"""
        content = response.content
        
        # Check for temperature <= 0.2 if controls are available
        # This is a proxy for deterministic generation
        if hasattr(response, 'controls'):
            temperature = getattr(response, 'controls', {}).get('temperature', 0.2)
            if temperature > 0.2:
                return False
        
        # Check for reproducible content structure
        required_fields = ["response", "model"]
        for field in required_fields:
            if field not in content:
                return False
        
        return True


class S1000DValidator:
    """S1000D compliance validator for aerospace documentation"""
    
    def __init__(self):
        # S1000D DM code pattern - simplified for basic validation
        self.dm_code_pattern = re.compile(
            r'^DMC-[A-Z0-9]+-[A-Z]+-\d{2}-\d{2}-\d{2}-\d{2}[A-Z]?-\d{3}[A-Z]?-[A-Z]$'
        )
        
        # Common S1000D elements
        self.s1000d_elements = [
            "dmodule", "dmTitle", "techName", "infoName", 
            "dmCode", "issueInfo", "dmAddressItems"
        ]
    
    def validate(self, response: ResponseSpec) -> Dict[str, Any]:
        """Validate S1000D compliance"""
        warnings = []
        
        try:
            content = response.content
            response_text = content.get("response", "")
            
            # Check for S1000D DM code if referenced
            if "DM" in response_text or "dmcode" in response_text.lower():
                dm_codes = re.findall(r'DMC-[A-Z0-9-]+', response_text)
                for dm_code in dm_codes:
                    if not self.dm_code_pattern.match(dm_code):
                        warnings.append(f"Invalid S1000D DM code format: {dm_code}")
            
            # Check for XML structure if claimed to be S1000D
            if "xml" in content.get("format", {}).get("ext", "").lower():
                if not self._validate_s1000d_xml_structure(response_text):
                    warnings.append("Invalid S1000D XML structure")
            
            # Check CSDB constraints
            if "csdb" in response_text.lower():
                if not self._validate_csdb_constraints(response_text):
                    warnings.append("CSDB constraint violations detected")
            
            return {"valid": len(warnings) == 0, "warnings": warnings}
            
        except Exception as e:
            return {"valid": False, "warnings": [f"S1000D validation error: {e}"]}
    
    def _validate_s1000d_xml_structure(self, content: str) -> bool:
        """Basic S1000D XML structure validation"""
        # Check for required S1000D elements
        required_patterns = [
            r'<dmodule.*?>',
            r'<dmTitle>',
            r'<dmCode.*?>'
        ]
        
        for pattern in required_patterns:
            if not re.search(pattern, content, re.IGNORECASE):
                return False
        
        return True
    
    def _validate_csdb_constraints(self, content: str) -> bool:
        """Validate Common Source Data Base constraints"""
        # Basic CSDB validation - in production would be more comprehensive
        
        # Check for proper naming conventions
        if "CSDB" in content:
            # Should reference proper CSDB objects
            csdb_pattern = re.compile(r'CSDB-[A-Z0-9-]+')
            matches = csdb_pattern.findall(content)
            
            for match in matches:
                # Basic format check
                if len(match.split('-')) < 3:
                    return False
        
        return True


class SafetyValidator:
    """Safety validation for TMR responses"""
    
    def __init__(self):
        self.forbidden_patterns = [
            r'\b(?:password|secret|key|token)\s*[:=]\s*\S+',
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # Credit card
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        ]
    
    def validate(self, response: ResponseSpec) -> Dict[str, Any]:
        """Validate safety and security of response"""
        errors = []
        
        try:
            content = response.content
            response_text = str(content)
            
            # Check for sensitive data patterns
            for pattern in self.forbidden_patterns:
                if re.search(pattern, response_text, re.IGNORECASE):
                    errors.append(f"Sensitive data pattern detected: {pattern}")
            
            # Check for injection attempts
            injection_patterns = [
                r'<script.*?>',
                r'javascript:',
                r'eval\s*\(',
                r'exec\s*\('
            ]
            
            for pattern in injection_patterns:
                if re.search(pattern, response_text, re.IGNORECASE):
                    errors.append(f"Potential injection detected: {pattern}")
            
            # Check response size limits
            if len(response_text) > 100000:  # 100KB limit
                errors.append("Response exceeds size limit")
            
            # Check for error indicators that might leak info
            error_indicators = ["traceback", "stack trace", "internal error", "debug info"]
            for indicator in error_indicators:
                if indicator.lower() in response_text.lower():
                    errors.append(f"Potential information leakage: {indicator}")
            
            return {"valid": len(errors) == 0, "errors": errors}
            
        except Exception as e:
            return {"valid": False, "errors": [f"Safety validation error: {e}"]}