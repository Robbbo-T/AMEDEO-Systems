#!/usr/bin/env python3
"""
Test suite to validate the UTCS/SPACE space systems directory structure
Ensures compliance with UTCS-MI standards and proper file organization
"""

import os
import json
import yaml
import pytest
from pathlib import Path

BASE_DIR = "/home/runner/work/AMEDEO-Systems/AMEDEO-Systems/UTCS/SPACE"

class TestUTCSSpaceStructure:
    """Test cases for UTCS/SPACE directory structure validation"""

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
        """Test Digital/Software space systems structure"""
        base_path = f"{BASE_DIR}/Digital/Software"
        assert os.path.exists(base_path), "Digital software base path does not exist"
        
        # Check for SatelliteBusManagement components
        sbm_path = f"{base_path}/SatelliteBusManagement"
        assert os.path.exists(sbm_path), "SatelliteBusManagement directory missing"
        
        # Verify CI-SD001 has the correct structure
        ci_sd001_path = f"{sbm_path}/CI-SD001/Source/AttitudeDeterminationControlSystem/v1.0"
        assert os.path.exists(ci_sd001_path), "CI-SD001 structure incorrect"
        
        # Check manifest and system files exist
        manifest_path = f"{ci_sd001_path}/manifest.json"
        system_path = f"{ci_sd001_path}/Sistema_DO178C_CI-SD001_v1.0.json"
        
        assert os.path.exists(manifest_path), "CI-SD001 manifest.json missing"
        assert os.path.exists(system_path), "CI-SD001 system definition missing"

    def test_environmental_space_structure(self):
        """Test Environmental space systems structure matches problem statement"""
        base_path = f"{BASE_DIR}/Environmental/Sistema"
        assert os.path.exists(base_path), "Environmental sistema base path does not exist"
        
        # Test CI-SE001 structure as specified in problem statement
        ci_se001_path = f"{base_path}/ThermalManagement/PassiveThermalControl/CI-SE001/Source/MultiLayerInsulation/v1.0"
        assert os.path.exists(ci_se001_path), "CI-SE001 structure does not match specification"
        
        manifest_path = f"{ci_se001_path}/manifest.json"
        system_path = f"{ci_se001_path}/Sistema_CS25_CI-SE001_v1.0.json"
        
        assert os.path.exists(manifest_path), "CI-SE001 manifest.json missing"
        assert os.path.exists(system_path), "CI-SE001 system definition missing"
        
        # Test CI-SE030 PowerGeneration structure
        ci_se030_path = f"{base_path}/PowerGeneration/SolarPowerSystems/CI-SE030/Source/DeployableSolarArrays/v1.0"
        assert os.path.exists(ci_se030_path), "CI-SE030 structure missing"
        
        se030_manifest = f"{ci_se030_path}/manifest.json"
        se030_system = f"{ci_se030_path}/Sistema_CS25_CI-SE030_v1.0.json"
        assert os.path.exists(se030_manifest), "CI-SE030 manifest.json missing"
        assert os.path.exists(se030_system), "CI-SE030 system definition missing"

    def test_operating_space_structure(self):
        """Test Operating space systems structure matches problem statement"""
        base_path = f"{BASE_DIR}/Operating/Sistema"
        assert os.path.exists(base_path), "Operating sistema base path does not exist"
        
        # Test CI-SO005 structure as specified in problem statement
        ci_so005_path = f"{base_path}/PropulsionSystems/ElectricPropulsion/CI-SO005/Source/IonThruster/v1.0"
        assert os.path.exists(ci_so005_path), "CI-SO005 structure does not match specification"
        
        manifest_path = f"{ci_so005_path}/manifest.json"
        system_path = f"{ci_so005_path}/Sistema_ARP4754A_CI-SO005_v1.0.json"
        
        assert os.path.exists(manifest_path), "CI-SO005 manifest.json missing"
        assert os.path.exists(system_path), "CI-SO005 system definition missing"

    def test_manifest_utcs_compliance(self):
        """Test that manifest files comply with UTCS-MI standards"""
        # Test CI-SE001 manifest
        manifest_path = f"{BASE_DIR}/Environmental/Sistema/ThermalManagement/PassiveThermalControl/CI-SE001/Source/MultiLayerInsulation/v1.0/manifest.json"
        
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
        assert "AerospaceSpaceEnvironmental" in utcs_id, "Category not properly reflected in UTCS-MI ID"
        assert "CI-SE001" in manifest["component_id"], "Component ID mismatch"
        assert manifest["domain"] == "SPACE", "Domain should be SPACE"

    def test_system_definition_structure(self):
        """Test that system definition files have proper structure"""
        system_path = f"{BASE_DIR}/Operating/Sistema/PropulsionSystems/ElectricPropulsion/CI-SO005/Source/IonThruster/v1.0/Sistema_ARP4754A_CI-SO005_v1.0.json"
        
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

    def test_component_count_sampling(self):
        """Test that we have representative samples of space components"""
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
        
        # We should have representative samples from the 150 space components
        assert len(digital_manifests) >= 3, f"Expected at least 3 Digital space components, got {len(digital_manifests)}"
        assert len(env_manifests) >= 2, f"Expected at least 2 Environmental space components, got {len(env_manifests)}"
        assert len(operating_manifests) >= 2, f"Expected at least 2 Operating space components, got {len(operating_manifests)}"

    def test_file_naming_conventions(self):
        """Test that files follow correct naming conventions for space systems"""
        # Test that system definition files follow the regulation-specific naming pattern
        
        # Environmental space system should use CS25
        cs25_file = f"{BASE_DIR}/Environmental/Sistema/ThermalManagement/PassiveThermalControl/CI-SE001/Source/MultiLayerInsulation/v1.0/Sistema_CS25_CI-SE001_v1.0.json"
        assert os.path.exists(cs25_file), "CS25 naming convention not followed for environmental space system"
        
        # Operating space system should use ARP4754A  
        arp_file = f"{BASE_DIR}/Operating/Sistema/PropulsionSystems/ElectricPropulsion/CI-SO005/Source/IonThruster/v1.0/Sistema_ARP4754A_CI-SO005_v1.0.json"
        assert os.path.exists(arp_file), "ARP4754A naming convention not followed for operating space system"
        
        # Digital space system should use DO178C
        do178c_file = f"{BASE_DIR}/Digital/Software/SatelliteBusManagement/CI-SD001/Source/AttitudeDeterminationControlSystem/v1.0/Sistema_DO178C_CI-SD001_v1.0.json"
        assert os.path.exists(do178c_file), "DO178C naming convention not followed for digital space system"

    def test_space_specific_systems(self):
        """Test that space-specific systems are properly implemented"""
        # Verify space-specific digital systems exist
        quantum_system = f"{BASE_DIR}/Digital/Software/QuantumSpaceSystems/CI-SD022/Source/QuantumCommunicationSatellite/v1.0"
        assert os.path.exists(quantum_system), "Quantum space system missing"
        
        # Verify space-specific environmental systems exist
        radiation_shield = f"{BASE_DIR}/Environmental/Sistema/RadiationEnvironment/RadiationShielding/CI-SE013/Source/AluminumShielding/v1.0"
        assert os.path.exists(radiation_shield), "Radiation shielding system missing"
        
        # Verify space-specific operating systems exist
        formation_flying = f"{BASE_DIR}/Operating/Sistema/FormationFlying/RelativeNavigation/CI-SO047/Source/GPSRelativeNavigation/v1.0"
        assert os.path.exists(formation_flying), "Formation flying system missing"

    def test_space_domain_consistency(self):
        """Test that all manifests have SPACE domain"""
        manifest_files = []
        
        for root, dirs, files in os.walk(BASE_DIR):
            if "manifest.json" in files:
                manifest_files.append(os.path.join(root, "manifest.json"))
        
        for manifest_file in manifest_files:
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
            
            assert manifest["domain"] == "SPACE", f"Manifest {manifest_file} does not have SPACE domain"
            assert "SPACE" in manifest["utcs_mi_id"], f"UTCS-MI ID in {manifest_file} does not contain SPACE"


if __name__ == "__main__":
    # Run tests
    test_suite = TestUTCSSpaceStructure()
    
    tests = [
        test_suite.test_main_directories_exist,
        test_suite.test_digital_software_structure,
        test_suite.test_environmental_space_structure,
        test_suite.test_operating_space_structure,
        test_suite.test_manifest_utcs_compliance,
        test_suite.test_system_definition_structure,
        test_suite.test_component_count_sampling,
        test_suite.test_file_naming_conventions,
        test_suite.test_space_specific_systems,
        test_suite.test_space_domain_consistency
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
        print("🎉 All tests passed! UTCS/SPACE structure is compliant.")
    else:
        print("❌ Some tests failed. Please review the implementation.")