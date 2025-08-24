#!/usr/bin/env python3
"""
Additional test cases for CI-AD010 AutopilotComputer structure validation
Ensures compliance with the problem statement requirements
"""

import os
import pytest
from pathlib import Path

# Use existing base directory from main test file
BASE_DIR = "/home/runner/work/AMEDEO-Systems/AMEDEO-Systems/UTCS/AIR"

class TestCIAD010Structure:
    """Test cases specifically for CI-AD010 AutopilotComputer structure"""

    def test_ci_ad010_main_directories(self):
        """Test that CI-AD010 has all 10 main directories as specified"""
        ci_ad010_path = f"{BASE_DIR}/Digital/Software/AvionicaSoftwareCertificable/AutopilotFlightDirector/CI-AD010"
        assert os.path.exists(ci_ad010_path), "CI-AD010 directory does not exist"
        
        expected_main_dirs = [
            "01-Requirements",
            "02-Design", 
            "03-SourceCode",
            "04-Executables",
            "05-Tests",
            "06-Documentation",
            "07-Tools",
            "08-ThirdParty",
            "09-Ops-Maintenance", 
            "10-Sustainment-Engineering"
        ]
        
        for dir_name in expected_main_dirs:
            dir_path = f"{ci_ad010_path}/{dir_name}"
            assert os.path.exists(dir_path), f"Directory {dir_name} missing in CI-AD010"
            assert os.path.isdir(dir_path), f"{dir_name} is not a directory"

    def test_ci_ad010_requirements_structure(self):
        """Test 01-Requirements directory structure"""
        req_path = f"{BASE_DIR}/Digital/Software/AvionicaSoftwareCertificable/AutopilotFlightDirector/CI-AD010/01-Requirements"
        
        # Test subdirectories
        expected_subdirs = [
            "System-Interface-Requirements",
            "High-Level-Requirements", 
            "Low-Level-Requirements",
            "Requirements-Traceability"
        ]
        
        for subdir in expected_subdirs:
            subdir_path = f"{req_path}/{subdir}"
            assert os.path.exists(subdir_path), f"Requirements subdirectory {subdir} missing"
        
        # Test specific files mentioned in problem statement
        expected_files = [
            "System-Interface-Requirements/ICD-APC-FMS-001.pdf",
            "System-Interface-Requirements/ICD-APC-Actuator-001.pdf",
            "High-Level-Requirements/SRS-APC-FlightModes.docx",
            "High-Level-Requirements/SRS-APC-ControlLaws.docx",
            "Low-Level-Requirements/LLR-APC-PitchControl.docx",
            "Low-Level-Requirements/LLR-APC-RollControl.docx",
            "Requirements-Traceability/RTM-SystemToHighLevel.xlsx",
            "Requirements-Traceability/RTM-HighToLowLevel.xlsx"
        ]
        
        for file_path in expected_files:
            full_path = f"{req_path}/{file_path}"
            assert os.path.exists(full_path), f"Requirements file {file_path} missing"

    def test_ci_ad010_source_code_structure(self):
        """Test 03-SourceCode directory structure"""
        src_path = f"{BASE_DIR}/Digital/Software/AvionicaSoftwareCertificable/AutopilotFlightDirector/CI-AD010/03-SourceCode"
        
        # Test main source directories
        expected_dirs = [
            "src/modules/ControlLaws",
            "src/modules/ModeLogic", 
            "src/core",
            "inc/ControlLaws",
            "build_scripts"
        ]
        
        for dir_path in expected_dirs:
            full_path = f"{src_path}/{dir_path}"
            assert os.path.exists(full_path), f"Source directory {dir_path} missing"
        
        # Test specific source files mentioned in problem statement
        expected_files = [
            "src/modules/ControlLaws/pitch_damper.c",
            "src/modules/ModeLogic/altitude_hold.c", 
            "src/core/apc_main.c",
            "inc/ControlLaws/pitch_damper.h",
            "inc/apc_common.h",
            "build_scripts/Makefile_APC",
            "build_scripts/build_toolchain_env.sh"
        ]
        
        for file_path in expected_files:
            full_path = f"{src_path}/{file_path}"
            assert os.path.exists(full_path), f"Source file {file_path} missing"

    def test_ci_ad010_executables_structure(self):
        """Test 04-Executables directory structure"""
        exec_path = f"{BASE_DIR}/Digital/Software/AvionicaSoftwareCertificable/AutopilotFlightDirector/CI-AD010/04-Executables"
        
        # Test releases directory
        releases_path = f"{exec_path}/Releases/v1.0"
        assert os.path.exists(releases_path), "Releases/v1.0 directory missing"
        
        # Test specific files mentioned in problem statement
        expected_files = [
            "apc_app_v1.0.bin",
            "apc_app_v1.0.sha256",
            "ReleaseNotes_v1.0.txt"
        ]
        
        for file_name in expected_files:
            file_path = f"{releases_path}/{file_name}"
            assert os.path.exists(file_path), f"Executable file {file_name} missing"

    def test_ci_ad010_tests_structure(self):
        """Test 05-Tests directory structure for DAL-C focus"""
        tests_path = f"{BASE_DIR}/Digital/Software/AvionicaSoftwareCertificable/AutopilotFlightDirector/CI-AD010/05-Tests"
        
        # Test test categories
        expected_dirs = [
            "UnitTests/Test_Cases",
            "UnitTests/Test_Results",
            "IntegrationTests/Test_Procedures",
            "IntegrationTests/Test_Results", 
            "SystemTests/Test_Cases",
            "SystemTests/Test_Results",
            "Coverage_Reports"
        ]
        
        for dir_path in expected_dirs:
            full_path = f"{tests_path}/{dir_path}"
            assert os.path.exists(full_path), f"Test directory {dir_path} missing"
        
        # Test specific files mentioned in problem statement
        expected_files = [
            "UnitTests/Test_Cases/UTC-APC-PitchControl.xlsx",
            "UnitTests/Test_Results/UnitTestReport_PitchControl.xml",
            "IntegrationTests/Test_Procedures/ITP_Procedure_ModeTransitions.pdf",
            "IntegrationTests/Test_Results/IntegrationTestReport_20240110.pdf",
            "SystemTests/Test_Cases/STC-APC-AutolandSequence.xlsx", 
            "SystemTests/Test_Results/SystemTestReport_Run_20240215.pdf",
            "Coverage_Reports/Statement_Decision_Coverage_Report_v1.0.html"
        ]
        
        for file_path in expected_files:
            full_path = f"{tests_path}/{file_path}"
            assert os.path.exists(full_path), f"Test file {file_path} missing"

    def test_ci_ad010_documentation_structure(self):
        """Test 06-Documentation directory for DO-178C lifecycle data"""
        doc_path = f"{BASE_DIR}/Digital/Software/AvionicaSoftwareCertificable/AutopilotFlightDirector/CI-AD010/06-Documentation"
        
        # Test documentation categories
        expected_dirs = [
            "Plans",
            "Reports",
            "Certification-Logs"
        ]
        
        for dir_name in expected_dirs:
            dir_path = f"{doc_path}/{dir_name}"
            assert os.path.exists(dir_path), f"Documentation directory {dir_name} missing"
        
        # Test specific files mentioned in problem statement
        expected_files = [
            "Plans/PSAC-APC.pdf",
            "Plans/SCMP-APC.pdf", 
            "Plans/SQAP-APC.pdf",
            "Plans/SVVP-APC.pdf",
            "Reports/VerificationSummaryReport_v1.0.pdf",
            "Certification-Logs/RACM-APC.xlsx",
            "Certification-Logs/ProblemReport_Log.xlsx"
        ]
        
        for file_path in expected_files:
            full_path = f"{doc_path}/{file_path}"
            assert os.path.exists(full_path), f"Documentation file {file_path} missing"

    def test_ci_ad010_sustainment_engineering(self):
        """Test 10-Sustainment-Engineering directory for RestoDeVidaUtil lifecycle"""
        sust_path = f"{BASE_DIR}/Digital/Software/AvionicaSoftwareCertificable/AutopilotFlightDirector/CI-AD010/10-Sustainment-Engineering"
        
        # Test sustainment categories
        expected_dirs = [
            "Change-Control/Change-Requests",
            "Change-Control/Impact-Analysis", 
            "Change-Control/Change-Control-Board",
            "Recertification-Data/v1.1_Update_Package",
            "Obsolescence-Management"
        ]
        
        for dir_path in expected_dirs:
            full_path = f"{sust_path}/{dir_path}"
            assert os.path.exists(full_path), f"Sustainment directory {dir_path} missing"
        
        # Test specific files mentioned in problem statement
        expected_files = [
            "Change-Control/Change-Requests/ECR-APC-2024-005.pdf",
            "Change-Control/Impact-Analysis/ImpactAnalysis_ECR-2024-005.pdf",
            "Change-Control/Change-Control-Board/CCB_Minutes_20240315.pdf",
            "Recertification-Data/v1.1_Update_Package/SummaryOfChanges_v1.1.pdf",
            "Recertification-Data/v1.1_Update_Package/RegressionTest_Results_v1.1.pdf",
            "Obsolescence-Management/Hardware-Obsolescence-Report.xlsx",
            "Obsolescence-Management/ThirdParty-SOUP-Watchlist.md"
        ]
        
        for file_path in expected_files:
            full_path = f"{sust_path}/{file_path}"
            assert os.path.exists(full_path), f"Sustainment file {file_path} missing"

    def test_ci_ad010_manifest_preserved(self):
        """Test that the original manifest.json is preserved"""
        manifest_path = f"{BASE_DIR}/Digital/Software/AvionicaSoftwareCertificable/AutopilotFlightDirector/CI-AD010/manifest.json"
        assert os.path.exists(manifest_path), "Original manifest.json missing"
        
        # Test that it contains expected CI-AD010 content
        with open(manifest_path, 'r') as f:
            content = f.read()
            assert "CI-AD010" in content, "Manifest does not contain CI-AD010 reference"
            assert "AutopilotComputer" in content, "Manifest does not contain AutopilotComputer reference"
            assert "DAL-C" in content, "Manifest does not contain DAL-C reference"