#!/usr/bin/env python3
"""
UTCS-MI: AQUART-INTEGRATION-TEST-complete_amedeo_api-v1.0
Complete integration test for AMEDEO API system
"""

import json
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from amedeo_api_server import AMEDEOAPIServer
from test_api_schemas import validate_json_against_schema


def test_complete_integration():
    """Test complete AMEDEO API integration"""
    print("🚀 AMEDEO Complete Integration Test")
    print("=" * 60)
    
    # Initialize API
    api = AMEDEOAPIServer()
    
    # Test all endpoints
    endpoints = [
        ("System Status", api.get_system_status, "system_status"),
        ("Digital Twin", api.get_digital_twin_fleet, "digital_twin"),
        ("Flight Plan", api.get_active_flights, "flight_plan"),
        ("Environmental", api.get_environmental_metrics, "environmental_metrics"),
        ("Evidence", api.get_recent_evidence, "evidence_record"),
        ("Maintenance", lambda: api.get_maintenance_prediction(), None),
        ("Carbon Offset", lambda: api.get_carbon_offset(), None),
        ("AI Validation", lambda: api.get_ai_validation(), "ai_spec_validation")
    ]
    
    all_passed = True
    
    for name, endpoint_func, schema_name in endpoints:
        print(f"\n🔍 Testing {name}...")
        
        try:
            # Test endpoint response
            response = endpoint_func()
            print(f"   ✅ Endpoint response: {type(response).__name__}")
            
            # Validate against schema if available
            if schema_name and schema_name in api.schemas:
                schema = api.schemas[schema_name]
                is_valid, message = validate_json_against_schema(response, schema)
                
                if is_valid:
                    print(f"   ✅ Schema validation: {message}")
                else:
                    print(f"   ❌ Schema validation failed: {message}")
                    all_passed = False
            else:
                print(f"   ⚠️  Schema validation skipped")
                
            # Check response has required data
            if isinstance(response, dict) and response:
                print(f"   ✅ Response contains data")
            else:
                print(f"   ❌ Empty or invalid response")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ Endpoint failed: {str(e)}")
            all_passed = False
    
    return all_passed


def test_agent_integration():
    """Test AMEDEO agent integration"""
    print("\n🤖 Testing Agent Integration")
    print("=" * 40)
    
    try:
        api = AMEDEOAPIServer()
        status = api.get_system_status()
        
        # Check agents subsystem exists
        if "agents" not in status.get("subsystems", {}):
            print("   ❌ Agents subsystem not found in status")
            return False
        
        agents_info = status["subsystems"]["agents"]
        
        # Check agent counts
        total_agents = agents_info.get("total_agents", 0)
        operational_count = agents_info.get("operational_count", 0)
        
        print(f"   📊 Total agents: {total_agents}")
        print(f"   ✅ Operational agents: {operational_count}")
        
        if total_agents != 4:
            print(f"   ❌ Expected 4 agents, got {total_agents}")
            return False
        
        if operational_count != 4:
            print(f"   ⚠️  Only {operational_count}/4 agents operational")
        
        # Check individual agents
        agents = agents_info.get("agents", {})
        expected_agents = ["planner", "buyer", "scheduler", "pilot"]
        
        for agent_name in expected_agents:
            if agent_name in agents:
                agent_info = agents[agent_name]
                status = agent_info.get("status", "unknown")
                available = agent_info.get("available", False)
                print(f"   🤖 {agent_name}: {status} ({'✅' if available else '❌'})")
            else:
                print(f"   ❌ Agent {agent_name} not found")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Agent integration test failed: {str(e)}")
        return False


def test_example_validation():
    """Test example files validate against schemas"""
    print("\n📄 Testing Example File Validation")
    print("=" * 40)
    
    api = AMEDEOAPIServer()
    examples_dir = Path(__file__).parent / "examples"
    
    example_files = [
        ("system_status_response.json", "system_status"),
        ("flight_plan_response.json", "flight_plan"),
        ("digital_twin_response.json", "digital_twin")
    ]
    
    all_passed = True
    
    for filename, schema_name in example_files:
        file_path = examples_dir / filename
        
        if not file_path.exists():
            print(f"   ⚠️  Example file {filename} not found")
            continue
        
        try:
            with open(file_path) as f:
                data = json.load(f)
            
            schema = api.schemas.get(schema_name)
            if not schema:
                print(f"   ❌ Schema {schema_name} not found")
                all_passed = False
                continue
            
            is_valid, message = validate_json_against_schema(data, schema)
            
            if is_valid:
                print(f"   ✅ {filename}: {message}")
            else:
                print(f"   ❌ {filename}: {message}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ Error validating {filename}: {str(e)}")
            all_passed = False
    
    return all_passed


def test_cli_functionality():
    """Test CLI functionality"""
    print("\n💻 Testing CLI Functionality")
    print("=" * 30)
    
    import subprocess
    
    cli_tests = [
        ["python", "amedeo_cli.py", "list"],
        ["python", "amedeo_cli.py", "status", "--compact"],
        ["python", "amedeo_cli.py", "schema", "system_status"]
    ]
    
    all_passed = True
    
    for cmd in cli_tests:
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                cwd=Path(__file__).parent,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"   ✅ {' '.join(cmd[2:])}: Success")
            else:
                print(f"   ❌ {' '.join(cmd[2:])}: Failed (exit {result.returncode})")
                all_passed = False
                
        except subprocess.TimeoutExpired:
            print(f"   ❌ {' '.join(cmd[2:])}: Timeout")
            all_passed = False
        except Exception as e:
            print(f"   ❌ {' '.join(cmd[2:])}: {str(e)}")
            all_passed = False
    
    return all_passed


def main():
    """Run complete integration test suite"""
    print("🏗️  AMEDEO API Complete Integration Test Suite")
    print("=" * 80)
    
    tests = [
        ("Complete API Integration", test_complete_integration),
        ("Agent Integration", test_agent_integration),
        ("Example File Validation", test_example_validation),
        ("CLI Functionality", test_cli_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"   💥 Test error: {str(e)}")
            results.append((test_name, False))
    
    # Final summary
    print("\n" + "=" * 80)
    print("📊 Complete Integration Test Results:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} {test_name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("AMEDEO API system is fully operational and ready for deployment.")
        return True
    else:
        print("\n⚠️  Some integration tests failed.")
        print("Please review the output above and fix any issues.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)