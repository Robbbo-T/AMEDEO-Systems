#!/usr/bin/env python3
"""Security audit script for GAIA AIR blockchain"""

import json
import hashlib
from datetime import datetime, timezone

def audit_genesis_block(genesis_file: str) -> bool:
    """Audit genesis block for deterministic hashing"""
    with open(genesis_file, 'r') as f:
        genesis = json.load(f)
    
    # Remove the hash for recalculation
    original_hash = genesis.get('genesis_hash')
    if 'genesis_hash' in genesis:
        del genesis['genesis_hash']
    
    # Calculate canonical hash
    canonical_data = json.dumps(genesis, sort_keys=True, separators=(",", ":")).encode()
    calculated_hash = hashlib.sha256(canonical_data).hexdigest()
    
    # Restore original hash
    genesis['genesis_hash'] = original_hash
    
    return original_hash == calculated_hash

def main():
    """Main audit function"""
    print("🔍 GAIA AIR Blockchain Security Audit")
    print("=" * 40)
    
    # Audit genesis block
    genesis_ok = audit_genesis_block('gaia_air_blockchain_production/genesis_block.json')
    print(f"Genesis block integrity: {'✅ PASS' if genesis_ok else '❌ FAIL'}")
    
    # Check current timestamp
    current_time = datetime.now(timezone.utc)
    print(f"Audit timestamp: {current_time.isoformat()}")
    
    # Load security report
    with open('gaia_air_blockchain_production/security_report.json', 'r') as f:
        security_report = json.load(f)
    
    # Check compliance status
    all_compliant = all(
        status in ["compliant", "active"] 
        for status in security_report['status'].values()
    )
    
    print(f"Overall compliance: {'✅ PASS' if all_compliant else '❌ FAIL'}")
    
    # Output recommendations
    print("\n📋 Recommendations:")
    for recommendation in security_report['recommendations']:
        print(f"   • {recommendation}")
    
    return genesis_ok and all_compliant

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)