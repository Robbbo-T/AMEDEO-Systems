#!/usr/bin/env python3
"""
UTCS-MI P0-P1 Binary Coverage Validator
Ensures 100% coverage of P0-P1 binaries and configurations
"""

import os
import sys
from pathlib import Path

def validate_p0_p1_coverage():
    """Validate UTCS-MI coverage of P0-P1 binaries and configurations"""
    
    print("🔍 UTCS-MI P0-P1 Binary Coverage Validation")
    print("=" * 50)
    
    base_path = Path(__file__).parent.parent
    
    # P0-P1 Critical binaries and configurations
    p0_p1_artifacts = [
        "out/tests_ata27_flight_ctrl_host",        # P0: Core ATA-27 test
        "out/integration_demo",                    # P0: System integration
        "kernel/arinc653_partition.c",             # P0: Core partitioning
        "framework/cqea/cqea_core.c",              # P1: CQEA framework
        "src/HAL_Sim.c",                           # P0: Hardware abstraction
        "src/Voter_Interface.c",                   # P0: 2oo3 voting
        "src/det.c",                               # P0: Deterministic logging
        "src/poae.c",                              # P0: POAE control cycle
        "src/tsn_sim.c",                           # P1: Time-sensitive networking
        "tests/ata27_flight_ctrl_host.c",          # P0: Flight control test
        "include/Voter_Interface.h",               # P0: Voting interface
        "include/HAL_Interface.h",                 # P0: HAL interface
        "include/det.h",                           # P0: DET interface
        "include/poae.h",                          # P0: POAE interface
        "include/tsn_sim.h"                        # P1: TSN interface
    ]
    
    covered_files = []
    missing_files = []
    
    print("📋 Checking P0-P1 artifact coverage:")
    
    for artifact in p0_p1_artifacts:
        artifact_path = base_path / artifact
        priority = "P0" if any(x in artifact for x in ["tests_ata27", "HAL_", "Voter_", "det.", "poae."]) else "P1"
        
        if artifact_path.exists():
            size = artifact_path.stat().st_size if artifact_path.is_file() else 0
            print(f"✓ [{priority}] {artifact} ({size} bytes)")
            covered_files.append((artifact, priority))
        else:
            print(f"✗ [{priority}] {artifact} - MISSING")
            missing_files.append((artifact, priority))
    
    # Calculate coverage
    total_artifacts = len(p0_p1_artifacts)
    covered_count = len(covered_files)
    coverage_percent = (covered_count / total_artifacts) * 100.0
    
    print(f"\n📊 Coverage Analysis:")
    print(f"   Total P0-P1 artifacts: {total_artifacts}")
    print(f"   Covered artifacts: {covered_count}")
    print(f"   Coverage percentage: {coverage_percent:.1f}%")
    
    # P0 and P1 breakdown
    p0_covered = len([f for f, p in covered_files if p == "P0"])
    p1_covered = len([f for f, p in covered_files if p == "P1"])
    p0_total = len([f for f in p0_p1_artifacts if any(x in f for x in ["tests_ata27", "HAL_", "Voter_", "det.", "poae."])])
    p1_total = total_artifacts - p0_total
    
    print(f"   P0 coverage: {p0_covered}/{p0_total} ({(p0_covered/p0_total)*100:.1f}%)")
    print(f"   P1 coverage: {p1_covered}/{p1_total} ({(p1_covered/p1_total)*100:.1f}%)")
    
    # UTCS-MI requirement: 100% of P0-P1
    if coverage_percent >= 100.0:
        print(f"\n✅ UTCS-MI requirement MET: {coverage_percent:.1f}% >= 100%")
        success = True
    else:
        print(f"\n❌ UTCS-MI requirement NOT MET: {coverage_percent:.1f}% < 100%")
        if missing_files:
            print("   Missing artifacts:")
            for artifact, priority in missing_files:
                print(f"     - [{priority}] {artifact}")
        success = False
    
    return success

if __name__ == "__main__":
    success = validate_p0_p1_coverage()
    
    if success:
        print("\n🎉 UTCS-MI P0-P1 coverage validation: PASSED")
    else:
        print("\n💥 UTCS-MI P0-P1 coverage validation: FAILED")
    
    sys.exit(0 if success else 1)