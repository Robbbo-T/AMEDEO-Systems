#!/usr/bin/env python3
"""
UTCS-MI: AQUART-API-TEST-schema_validation-v1.0
Test AMEDEO API schemas and server functionality
"""

import json
import sys
from pathlib import Path

# Add agents to path
sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from amedeo_api_server import AMEDEOAPIServer


def validate_json_against_schema(data, schema):
    """Basic JSON schema validation (simplified)"""
    try:
        # Basic validation - check required fields exist
        required = schema.get("required", [])
        for field in required:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Check properties match schema types
        properties = schema.get("properties", {})
        for field, value in data.items():
            if field in properties:
                field_schema = properties[field]
                expected_type = field_schema.get("type")
                
                if expected_type == "string" and not isinstance(value, str):
                    return False, f"Field {field} should be string, got {type(value)}"
                elif expected_type == "number" and not isinstance(value, (int, float)):
                    return False, f"Field {field} should be number, got {type(value)}"
                elif expected_type == "boolean" and not isinstance(value, bool):
                    return False, f"Field {field} should be boolean, got {type(value)}"
                elif expected_type == "object" and not isinstance(value, dict):
                    return False, f"Field {field} should be object, got {type(value)}"
                elif expected_type == "array" and not isinstance(value, list):
                    return False, f"Field {field} should be array, got {type(value)}"
        
        return True, "Valid"
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def test_api_schemas():
    """Test that API responses validate against schemas"""
    print("🧪 Testing AMEDEO API Schemas")
    print("=" * 50)
    
    # Initialize API server
    api = AMEDEOAPIServer()
    
    # Test cases: (endpoint_method, schema_name)
    test_cases = [
        (api.get_system_status, "system_status"),
        (api.get_digital_twin_fleet, "digital_twin"),
        (api.get_active_flights, "flight_plan"),
        (api.get_environmental_metrics, "environmental_metrics"),
        (api.get_recent_evidence, "evidence_record")
    ]
    
    all_passed = True
    
    for endpoint_method, schema_name in test_cases:
        print(f"\n🔍 Testing {schema_name}...")
        
        # Get API response
        try:
            response_data = endpoint_method()
            print(f"   ✅ API response generated")
        except Exception as e:
            print(f"   ❌ API response failed: {str(e)}")
            all_passed = False
            continue
        
        # Get schema
        if schema_name not in api.schemas:
            print(f"   ❌ Schema {schema_name} not found")
            all_passed = False
            continue
        
        schema = api.schemas[schema_name]
        print(f"   ✅ Schema loaded")
        
        # Validate response against schema
        is_valid, message = validate_json_against_schema(response_data, schema)
        
        if is_valid:
            print(f"   ✅ Validation passed: {message}")
        else:
            print(f"   ❌ Validation failed: {message}")
            all_passed = False
    
    return all_passed


def test_schema_loading():
    """Test that all schemas load correctly"""
    print("\n📋 Testing Schema Loading")
    print("=" * 30)
    
    api = AMEDEOAPIServer()
    
    expected_schemas = [
        "system_status",
        "digital_twin", 
        "flight_plan",
        "environmental_metrics",
        "evidence_record",
        "ai_spec_validation"
    ]
    
    all_passed = True
    
    for schema_name in expected_schemas:
        if schema_name in api.schemas:
            schema = api.schemas[schema_name]
            if "$schema" in schema and "properties" in schema:
                print(f"   ✅ {schema_name}: Valid JSON Schema")
            else:
                print(f"   ❌ {schema_name}: Invalid schema structure")
                all_passed = False
        else:
            print(f"   ❌ {schema_name}: Schema not found")
            all_passed = False
    
    return all_passed


def test_example_response():
    """Test example response from problem statement"""
    print("\n📄 Testing Example Response")
    print("=" * 30)
    
    # Load example system status
    example_path = Path(__file__).parent / "examples" / "system_status_response.json"
    
    if not example_path.exists():
        print("   ⚠️  Example file not found, skipping")
        return True
    
    try:
        with open(example_path) as f:
            example_data = json.load(f)
        
        api = AMEDEOAPIServer()
        schema = api.schemas.get("system_status")
        
        if not schema:
            print("   ❌ System status schema not found")
            return False
        
        is_valid, message = validate_json_against_schema(example_data, schema)
        
        if is_valid:
            print(f"   ✅ Example validates against schema: {message}")
            return True
        else:
            print(f"   ❌ Example validation failed: {message}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing example: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("🚀 AMEDEO API Schema Test Suite")
    print("=" * 60)
    
    tests = [
        ("Schema Loading", test_schema_loading),
        ("API Schema Validation", test_api_schemas),
        ("Example Response", test_example_response)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} tests...")
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"   💥 Test suite error: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} {test_name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! AMEDEO API schemas are valid.")
        return True
    else:
        print("\n⚠️  Some tests failed. Check output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)