#!/usr/bin/env python3
"""
AQUA-OS / ADT Final Requirements Validation
Validates all DoD (Definition of Done) criteria from the problem statement
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd="/home/runner/work/AMEDEO-Systems/AMEDEO-Systems")
        if result.returncode == 0:
            print(f"   ✅ PASSED")
            return True
        else:
            print(f"   ❌ FAILED: {result.stderr.strip() if result.stderr else result.stdout.strip()}")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def validate_requirements():
    """Validate all AQUA-OS/ADT requirements"""
    
    print("🚀 AQUA-OS / ADT (Aerospace Digital Transponder) Validation")
    print("=" * 65)
    print("Priority: P0–P2 • Path: /kernel, /framework/cqea, /integration/system-of-systems")
    print("IF: ARINC 653 partitions, QAL, AEIC, SEAL, DET, UTCS-MI")
    print()
    
    requirements = []
    
    # Requirement 1: Boots on HAL_Sim; passes ATA-27 host test @1 kHz/1000 steps with 2oo3 consensus = 100%
    print("📋 Requirement 1: ATA-27 host test @1kHz/1000 steps with 2oo3 consensus")
    success1 = run_command("./out/tests_ata27_flight_ctrl_host", "Running ATA-27 test")
    requirements.append(("ATA-27 test @1kHz/1000 steps", success1))
    
    # Requirement 2: ARINC 653-like scheduling demo; worst-case jitter ≤ 50 µs
    print("\n📋 Requirement 2: ARINC 653-like scheduling demo; worst-case jitter ≤ 50 µs")
    success2 = run_command("./out/integration_demo", "ARINC 653 scheduling demo")
    requirements.append(("ARINC 653 scheduling ≤ 50µs jitter", success2))
    
    # Requirement 3: UTCS-MI coverage = 100% of P0–P1 binaries/configs
    print("\n📋 Requirement 3: UTCS-MI coverage = 100% of P0–P1 binaries/configs")
    success3a = run_command("python3 tools/utcs_agent_validator.py", "UTCS-MI agent validation")
    success3b = run_command("python3 tools/utcs_p0_p1_coverage.py", "UTCS-MI P0-P1 coverage")
    success3 = success3a and success3b
    requirements.append(("UTCS-MI coverage 100%", success3))
    
    # Requirement 4: SAST (-Wall -Wextra -Werror, cppcheck) no high findings
    print("\n📋 Requirement 4: SAST (-Wall -Wextra -Werror, cppcheck) no high findings")
    success4a = run_command("cd build && make clean && make", "Compile with -Wall -Wextra -Werror")
    success4b = run_command("cppcheck -I include/ -I kernel/ -I framework/cqea/ --enable=warning --error-exitcode=1 src/ tests/ kernel/ framework/ integration/", "Static analysis with cppcheck")
    success4 = success4a and success4b
    requirements.append(("SAST compliance", success4))
    
    # Check directory structure
    print("\n📋 Path Requirements: Directory structure validation")
    paths = ["/kernel", "/framework/cqea", "/integration/system-of-systems"]
    path_success = True
    for path in paths:
        full_path = Path("/home/runner/work/AMEDEO-Systems/AMEDEO-Systems" + path)
        if full_path.exists():
            print(f"   ✅ {path} exists")
        else:
            print(f"   ❌ {path} missing")
            path_success = False
    requirements.append(("Required directory structure", path_success))
    
    # Summary
    print("\n" + "=" * 65)
    print("📊 REQUIREMENTS SUMMARY")
    print("=" * 65)
    
    all_passed = True
    for req_name, status in requirements:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {req_name}")
        if not status:
            all_passed = False
    
    print("\n" + "=" * 65)
    if all_passed:
        print("🎉 ALL AQUA-OS/ADT REQUIREMENTS: PASSED")
        print("   • Boots on HAL_Sim; passes ATA-27 host test @1 kHz/1000 steps with 2oo3 consensus = 100%")
        print("   • ARINC 653-like scheduling demo; worst-case jitter ≤ 50 µs (host profile)")
        print("   • UTCS-MI coverage = 100% of P0–P1 binaries/configs")
        print("   • SAST (-Wall -Wextra -Werror, cppcheck) no high findings")
    else:
        print("💥 AQUA-OS/ADT REQUIREMENTS: FAILED")
        print("   Some requirements were not met. See details above.")
    
    return all_passed

if __name__ == "__main__":
    success = validate_requirements()
    sys.exit(0 if success else 1)