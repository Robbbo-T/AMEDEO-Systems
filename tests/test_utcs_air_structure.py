#!/usr/bin/env python3
"""
Test suite to validate the UTCS/AIR airborne systems directory structure
Ensures compliance with UTCS-MI standards and proper file organization
"""

import os
import json
import yaml
import pytest
from pathlib import Path

BASE_DIR = "/home/runner/work/AMEDEO-Systems/AMEDEO-Systems/UTCS/AIR"

class TestUTCSAIRStructure:
    """Test cases for UTCS/AIR directory structure validation"""

    def test_main_directories_exist(self):
        """Test that main category directories exist"""
        expected_dirs = [
            f"{BASE_DIR}/Digital",
            f"{BASE_DIR}/Environmental", 
            f"{BASE_DIR}/Operating"
        ]
        
        for dir_path in expected_dirs:
            assert os.path.exists(dir_path), f"Directory {dir_path} does not exist"
            assert os.path.isdir(dir_path), f"{dir_path} is not a directory"

    def test_digital_software_structure(self):
        """Test Digital/Software/AvionicaSoftwareCertificable structure"""
        base_path = f"{BASE_DIR}/Digital/Software/AvionicaSoftwareCertificable"
        assert os.path.exists(base_path), f"Digital software base path does not exist"
        
        # Check for FlightManagementSystem components
        fms_path = f"{base_path}/FlightManagementSystem"
        assert os.path.exists(fms_path), "FlightManagementSystem directory missing"
        
        # Verify CI-AD001 has the correct structure
        ci_ad001_path = f"{fms_path}/CI-AD001/Source/PrimaryFlightManagementComputer/v1.0"
        assert os.path.exists(ci_ad001_path), "CI-AD001 structure incorrect"
        
        # Check manifest and system files exist
        manifest_path = f"{ci_ad001_path}/manifest.json"
        system_path = f"{ci_ad001_path}/Sistema_DO178C_CI-AD001_v1.0.json"
        
        assert os.path.exists(manifest_path), "CI-AD001 manifest.json missing"
        assert os.path.exists(system_path), "CI-AD001 system definition missing"

    def test_environmental_control_structure(self):
        """Test Environmental control system structure matches problem statement"""
        base_path = f"{BASE_DIR}/Environmental/Sistema/ControlAmbiental"
        assert os.path.exists(base_path), "Environmental control base path does not exist"
        
        # Test CI-AE001 structure as specified in problem statement
        ci_ae001_path = f"{base_path}/EnvironmentalControlSystem/CI-AE001/Source/EcsCore/v1.0"
        assert os.path.exists(ci_ae001_path), "CI-AE001 structure does not match specification"
        
        manifest_path = f"{ci_ae001_path}/manifest.json"
        system_path = f"{ci_ae001_path}/Sistema_CS25_CI-AE001_v1.0.json"
        
        assert os.path.exists(manifest_path), "CI-AE001 manifest.json missing"
        assert os.path.exists(system_path), "CI-AE001 system definition missing"
        
        # Test CI-AE002 Config structure
        ci_ae002_path = f"{base_path}/EnvironmentalControlSystem/CI-AE002/Config/EcsConfiguration/v1.0"
        assert os.path.exists(ci_ae002_path), "CI-AE002 config structure missing"
        
        config_file = f"{ci_ae002_path}/Sistema_CS25_CI-AE002_Config_v1.0.yaml"
        assert os.path.exists(config_file), "CI-AE002 config YAML missing"
        
        # Test CI-AE003 TestReport structure
        ci_ae003_path = f"{base_path}/EnvironmentalControlSystem/CI-AE003/TestReport/EcsVerification/v1.0"
        assert os.path.exists(ci_ae003_path), "CI-AE003 test report structure missing"
        
        evidence_file = f"{ci_ae003_path}/Evidencia_CS25_CI-AE003_v1.0.pdf"
        assert os.path.exists(evidence_file), "CI-AE003 evidence file missing"

    def test_operating_fbw_structure(self):
        """Test Operating/FlyByWire structure matches problem statement"""
        base_path = f"{BASE_DIR}/Operating/Sistema/ControlVuelo"
        assert os.path.exists(base_path), "Operating control flight base path does not exist"
        
        # Test CI-AO001 structure as specified in problem statement
        ci_ao001_path = f"{base_path}/FlyByWireControlSystem/CI-AO001/Source/FbwCore/v1.0"
        assert os.path.exists(ci_ao001_path), "CI-AO001 structure does not match specification"
        
        manifest_path = f"{ci_ao001_path}/manifest.json"
        system_path = f"{ci_ao001_path}/Sistema_ARP4754A_CI-AO001_v1.0.json"
        
        assert os.path.exists(manifest_path), "CI-AO001 manifest.json missing"
        assert os.path.exists(system_path), "CI-AO001 system definition missing"

    def test_manifest_utcs_compliance(self):
        """Test that manifest files comply with UTCS-MI standards"""
        # Test CI-AE001 manifest
        manifest_path = f"{BASE_DIR}/Environmental/Sistema/ControlAmbiental/EnvironmentalControlSystem/CI-AE001/Source/EcsCore/v1.0/manifest.json"
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        # Verify required UTCS-MI fields
        required_fields = [
            "utcs_mi_id", "component_id", "component_name", "version",
            "category", "certification_level", "design_assurance_level",
            "created_by", "program", "domain", "lifecycle"
        ]
        
        for field in required_fields:
            assert field in manifest, f"Required field {field} missing from manifest"
        
        # Verify UTCS-MI ID format
        utcs_id = manifest["utcs_mi_id"]
        assert utcs_id.startswith("EstándarUniversal:"), "UTCS-MI ID does not start with EstándarUniversal:"
        assert "AerospaceEnvironmental" in utcs_id, "Category not properly reflected in UTCS-MI ID"
        assert "CI-AE001" in manifest["component_id"], "Component ID mismatch"

    def test_system_definition_structure(self):
        """Test that system definition files have proper structure"""
        system_path = f"{BASE_DIR}/Operating/Sistema/ControlVuelo/FlyByWireControlSystem/CI-AO001/Source/FbwCore/v1.0/Sistema_ARP4754A_CI-AO001_v1.0.json"
        
        with open(system_path, 'r') as f:
            system_def = json.load(f)
        
        # Verify required system definition fields
        required_fields = [
            "system_id", "system_name", "regulation", "version", "description",
            "interfaces", "requirements", "test_cases", "certification_evidence",
            "safety_assessment", "dependencies", "configuration"
        ]
        
        for field in required_fields:
            assert field in system_def, f"Required field {field} missing from system definition"
        
        # Verify safety assessment structure
        safety_assessment = system_def["safety_assessment"]
        assert "failure_conditions" in safety_assessment
        assert "safety_objectives" in safety_assessment
        assert "dal_classification" in safety_assessment
        assert safety_assessment["dal_classification"] == "DAL-C"

    def test_config_yaml_structure(self):
        """Test that configuration YAML files have proper structure"""
        config_path = f"{BASE_DIR}/Environmental/Sistema/ControlAmbiental/EnvironmentalControlSystem/CI-AE002/Config/EcsConfiguration/v1.0/Sistema_CS25_CI-AE002_Config_v1.0.yaml"
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Verify required configuration sections
        assert "component" in config, "Component section missing from config"
        assert "configuration" in config, "Configuration section missing"
        assert "validation" in config, "Validation section missing"
        
        # Verify component section
        component = config["component"]
        assert "id" in component and component["id"] == "CI-AE002"
        assert "name" in component
        assert "version" in component and component["version"] == "v1.0"

    def test_component_count_sampling(self):
        """Test that we have representative samples of components"""
        # Count manifests in each category
        digital_manifests = []
        env_manifests = []
        operating_manifests = []
        
        for root, dirs, files in os.walk(f"{BASE_DIR}/Digital"):
            if "manifest.json" in files:
                digital_manifests.append(root)
        
        for root, dirs, files in os.walk(f"{BASE_DIR}/Environmental"):
            if "manifest.json" in files:
                env_manifests.append(root)
                
        for root, dirs, files in os.walk(f"{BASE_DIR}/Operating"):
            if "manifest.json" in files:
                operating_manifests.append(root)
        
        # We should have representative samples (not necessarily all 330 components)
        assert len(digital_manifests) >= 10, f"Expected at least 10 Digital components, got {len(digital_manifests)}"
        assert len(env_manifests) >= 7, f"Expected at least 7 Environmental components, got {len(env_manifests)}"
        assert len(operating_manifests) >= 7, f"Expected at least 7 Operating components, got {len(operating_manifests)}"

    def test_file_naming_conventions(self):
        """Test that files follow correct naming conventions"""
        # Test that system definition files follow the regulation-specific naming pattern
        
        # Environmental system should use CS25
        cs25_file = f"{BASE_DIR}/Environmental/Sistema/ControlAmbiental/EnvironmentalControlSystem/CI-AE001/Source/EcsCore/v1.0/Sistema_CS25_CI-AE001_v1.0.json"
        assert os.path.exists(cs25_file), "CS25 naming convention not followed for environmental system"
        
        # Operating system should use ARP4754A  
        arp_file = f"{BASE_DIR}/Operating/Sistema/ControlVuelo/FlyByWireControlSystem/CI-AO001/Source/FbwCore/v1.0/Sistema_ARP4754A_CI-AO001_v1.0.json"
        assert os.path.exists(arp_file), "ARP4754A naming convention not followed for operating system"
        
        # Digital system should use DO178C
        do178c_file = f"{BASE_DIR}/Digital/Software/AvionicaSoftwareCertificable/FlightManagementSystem/CI-AD001/Source/PrimaryFlightManagementComputer/v1.0/Sistema_DO178C_CI-AD001_v1.0.json"
        assert os.path.exists(do178c_file), "DO178C naming convention not followed for digital system"

if __name__ == "__main__":
    # Run tests
    test_suite = TestUTCSAIRStructure()
    
    tests = [
        test_suite.test_main_directories_exist,
        test_suite.test_digital_software_structure,
        test_suite.test_environmental_control_structure,
        test_suite.test_operating_fbw_structure,
        test_suite.test_manifest_utcs_compliance,
        test_suite.test_system_definition_structure,
        test_suite.test_config_yaml_structure,
        test_suite.test_component_count_sampling,
        test_suite.test_file_naming_conventions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__} - PASSED")
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} - FAILED: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! UTCS/AIR structure is compliant.")
    else:
        print("❌ Some tests failed. Please review the implementation.")