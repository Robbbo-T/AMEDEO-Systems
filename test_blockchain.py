#!/usr/bin/env python3
"""
Comprehensive test suite for GAIA AIR Blockchain Implementation
Tests all components including deterministic hashing, certificates, deployment configs, and security
"""

import sys
import json
import yaml
import os
import hashlib
from datetime import datetime, timezone

# Import blockchain components
sys.path.append('.')
from main import (
    GaiaBlockchainConfig, CertificateAuthority, BlockchainNode, 
    DeploymentGenerator, SecurityManager, SustainabilityManager,
    canonical_json
)

def test_deterministic_genesis():
    """Test deterministic genesis block generation"""
    print("🧪 Testing deterministic genesis block generation...")
    
    config = GaiaBlockchainConfig()
    
    # Generate multiple genesis blocks with same parameters
    genesis1 = config.generate_genesis_block(["val1", "val2", "val3"])
    genesis2 = config.generate_genesis_block(["val1", "val2", "val3"])
    
    # Remove timestamps and hashes for comparison
    genesis1_copy = genesis1.copy()
    genesis2_copy = genesis2.copy()
    
    # Set same timestamp for comparison
    test_timestamp = "2025-01-01T00:00:00+00:00"
    genesis1_copy["timestamp"] = test_timestamp
    genesis2_copy["timestamp"] = test_timestamp
    genesis1_copy["data"]["metadata"]["creation_date"] = test_timestamp
    genesis2_copy["data"]["metadata"]["creation_date"] = test_timestamp
    
    # Remove hashes
    del genesis1_copy["genesis_hash"]
    del genesis2_copy["genesis_hash"]
    
    # Should be identical
    canonical1 = canonical_json(genesis1_copy)
    canonical2 = canonical_json(genesis2_copy)
    
    if canonical1 == canonical2:
        print("✅ Deterministic genesis block generation works correctly")
        return True
    else:
        print("❌ Genesis blocks are not deterministic")
        return False

def test_certificate_authority():
    """Test certificate authority generation and node certificate issuance"""
    print("🧪 Testing certificate authority and X.509 certificates...")
    
    try:
        ca = CertificateAuthority()
        ca_key, ca_cert = ca.generate_ca()
        
        # Test CA certificate properties
        basic_constraints = None
        for ext in ca_cert.extensions:
            if ext.oid._name == 'basicConstraints':
                basic_constraints = ext.value
                break
        
        if basic_constraints is None or not basic_constraints.ca:
            print("❌ CA certificate is not marked as CA")
            return False
        
        # Generate node and certificate
        node = BlockchainNode("test-validator", "validator")
        node_key, node_pub = node.generate_keys()
        
        node_cert = ca.issue_node_certificate("test-validator", node_pub)
        
        # Verify certificate is signed by CA
        if node_cert.issuer != ca_cert.subject:
            print("❌ Node certificate not issued by CA")
            return False
        
        print("✅ Certificate authority and node certificates work correctly")
        return True
        
    except Exception as e:
        print(f"❌ Certificate test failed: {e}")
        return False

def test_ed25519_keys():
    """Test Ed25519 key generation for blockchain nodes"""
    print("🧪 Testing Ed25519 key generation...")
    
    try:
        node = BlockchainNode("test-node", "validator")
        private_key, public_key = node.generate_keys()
        
        # Verify keys are Ed25519
        from cryptography.hazmat.primitives.asymmetric import ed25519
        
        if not isinstance(private_key, ed25519.Ed25519PrivateKey):
            print("❌ Private key is not Ed25519")
            return False
            
        if not isinstance(public_key, ed25519.Ed25519PublicKey):
            print("❌ Public key is not Ed25519")
            return False
        
        print("✅ Ed25519 key generation works correctly")
        return True
        
    except Exception as e:
        print(f"❌ Ed25519 key test failed: {e}")
        return False

def test_deployment_configs():
    """Test deployment configuration generation"""
    print("🧪 Testing deployment configuration generation...")
    
    try:
        deployer = DeploymentGenerator()
        
        # Test Docker Compose
        docker_config = deployer.generate_docker_compose(3)
        
        # Check required services
        required_services = ["orderer1", "validator1", "validator2", "validator3", "api1"]
        for service in required_services:
            if service not in docker_config["services"]:
                print(f"❌ Missing service: {service}")
                return False
        
        # Check network configuration
        if "gaia_air_net" not in docker_config["networks"]:
            print("❌ Missing network configuration")
            return False
        
        # Test Kubernetes configs
        k8s_config = deployer.generate_kubernetes_config()
        network_policy = deployer.generate_network_policy()
        pdb = deployer.generate_pod_disruption_budget()
        
        if k8s_config["kind"] != "Namespace":
            print("❌ Invalid Kubernetes namespace config")
            return False
        
        if network_policy["kind"] != "NetworkPolicy":
            print("❌ Invalid NetworkPolicy config")
            return False
            
        if pdb["kind"] != "PodDisruptionBudget":
            print("❌ Invalid PodDisruptionBudget config")
            return False
        
        print("✅ Deployment configurations generated correctly")
        return True
        
    except Exception as e:
        print(f"❌ Deployment config test failed: {e}")
        return False

def test_security_manager():
    """Test security policy and compliance reporting"""
    print("🧪 Testing security manager and compliance...")
    
    try:
        security = SecurityManager()
        report = security.generate_security_report()
        
        # Check required policy areas
        required_policies = [
            "key_management", "access_control", "certificate_management", 
            "monitoring", "compliance"
        ]
        
        for policy in required_policies:
            if policy not in report["policies"]:
                print(f"❌ Missing security policy: {policy}")
                return False
        
        # Check compliance standards
        compliance = report["policies"]["compliance"]
        required_standards = ["s1000d", "utcs_mi", "nist_cybersecurity", "gdpr"]
        
        for standard in required_standards:
            if not compliance.get(standard):
                print(f"❌ Missing compliance standard: {standard}")
                return False
        
        print("✅ Security manager and compliance reporting work correctly")
        return True
        
    except Exception as e:
        print(f"❌ Security manager test failed: {e}")
        return False

def test_sustainability_manager():
    """Test sustainability KPI validation"""
    print("🧪 Testing sustainability KPI management...")
    
    try:
        sustainability = SustainabilityManager()
        
        # Test valid KPI data
        valid_data = {
            "co2e": 100.5,
            "energy": 500.0,
            "recycleRate": 85.5,
            "waterUsage": 1000.0,
            "wasteReduction": 50.0
        }
        
        if not sustainability.validate_kpi_schema(valid_data):
            print("❌ Valid KPI data rejected")
            return False
        
        # Test invalid KPI data (missing required field)
        invalid_data = {
            "energy": 500.0,
            "recycleRate": 85.5
            # Missing required "co2e"
        }
        
        if sustainability.validate_kpi_schema(invalid_data):
            print("❌ Invalid KPI data accepted")
            return False
        
        # Test IoT validation (mock)
        signature = hashlib.sha256(canonical_json(valid_data)).hexdigest()
        if not sustainability.validate_iot_data(valid_data, signature, "mock_key"):
            print("❌ IoT data validation failed")
            return False
        
        print("✅ Sustainability KPI management works correctly")
        return True
        
    except Exception as e:
        print(f"❌ Sustainability manager test failed: {e}")
        return False

def test_generated_files():
    """Test that all generated files are valid and can be loaded"""
    print("🧪 Testing generated configuration files...")
    
    try:
        output_dir = "gaia_air_blockchain_production"
        
        # Test JSON files
        json_files = [
            "genesis_block.json",
            "security_report.json",
            "s1000d_header.json"
        ]
        
        for file in json_files:
            path = os.path.join(output_dir, file)
            if not os.path.exists(path):
                print(f"❌ Missing file: {file}")
                return False
            
            with open(path, 'r') as f:
                json.load(f)  # Verify valid JSON
        
        # Test YAML files
        yaml_files = [
            "docker-compose.yml",
            "network-policy.yaml",
            "pdb.yaml"
        ]
        
        for file in yaml_files:
            path = os.path.join(output_dir, file)
            if not os.path.exists(path):
                print(f"❌ Missing file: {file}")
                return False
            
            with open(path, 'r') as f:
                yaml.safe_load(f)  # Verify valid YAML
        
        print("✅ All generated files are valid and loadable")
        return True
        
    except Exception as e:
        print(f"❌ File validation test failed: {e}")
        return False

def test_utcs_compliance():
    """Test UTCS-MI compliance and manifest integration"""
    print("🧪 Testing UTCS-MI compliance...")
    
    try:
        # Check manifest includes all blockchain artifacts
        with open("UTCS/manifest.json", 'r') as f:
            manifest = json.load(f)
        
        blockchain_files = [
            "main.py",
            "requirements.txt",
            "Dockerfile",
            "healthcheck.py",
            "security_audit.py",
            "gaia_air_blockchain_production/genesis_block.json",
            "gaia_air_blockchain_production/docker-compose.yml",
            "gaia_air_blockchain_production/security_report.json",
            "gaia_air_blockchain_production/network-policy.yaml",
            "gaia_air_blockchain_production/pdb.yaml",
            "gaia_air_blockchain_production/s1000d_header.json"
        ]
        
        for file in blockchain_files:
            if file not in manifest:
                print(f"❌ File not in UTCS manifest: {file}")
                return False
        
        # Verify UTCS identifier format
        for file, identifier in manifest.items():
            if "Blockchain" in identifier or "Gaia Air" in identifier:
                if not identifier.startswith("EstándarUniversal:"):
                    print(f"❌ Invalid UTCS identifier for {file}")
                    return False
        
        print("✅ UTCS-MI compliance verified")
        return True
        
    except Exception as e:
        print(f"❌ UTCS compliance test failed: {e}")
        return False

def main():
    """Run comprehensive test suite"""
    print("🚀 GAIA AIR Blockchain Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        test_deterministic_genesis,
        test_certificate_authority,
        test_ed25519_keys,
        test_deployment_configs,
        test_security_manager,
        test_sustainability_manager,
        test_generated_files,
        test_utcs_compliance
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! GAIA AIR Blockchain implementation is ready for production.")
        return True
    else:
        print("❌ Some tests failed. Please review the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)