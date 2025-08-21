#!/usr/bin/env python3
"""
UTDC-GPS-MFF Validation Tool
UTCS-MI: EstándarUniversal:Herramienta-Desarrollo-UTDC-01.00-ValidatorTool-0001-v1.0-AerospaceAndQuantumUnitedAdvancedVenture-GeneracionHumana-CROSS-ReferenceImpl-validate1-RestoDeVidaUtil
"""

import sys
import argparse
from pathlib import Path

# Add source path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utdc_gps_mff import MFFValidator


def main():
    parser = argparse.ArgumentParser(description="Validate UTDC-GPS-MFF artifacts")
    parser.add_argument("files", nargs="+", help="MFF header files to validate")
    parser.add_argument("--regulation", help="Specific regulation to validate against")
    parser.add_argument("--cascade", action="store_true", help="Validate as cascade chain")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    validator = MFFValidator()
    all_valid = True
    headers = []
    
    print("🔍 UTDC-GPS-MFF Validation")
    print("=" * 40)
    
    for file_path in args.files:
        path = Path(file_path)
        print(f"\n📄 Validating: {path.name}")
        
        if not path.exists():
            print(f"❌ File not found: {path}")
            all_valid = False
            continue
        
        try:
            # Basic validation
            result = validator.validate_file(path)
            
            if result.is_valid:
                print(f"✅ Basic validation: PASSED")
                print(f"   Coverage: {result.coverage:.1f}%")
            else:
                print(f"❌ Basic validation: FAILED")
                all_valid = False
                
                for error in result.errors:
                    print(f"   Error: {error}")
            
            if result.warnings and args.verbose:
                for warning in result.warnings:
                    print(f"   Warning: {warning}")
            
            # Regulation-specific validation
            if args.regulation:
                from utdc_gps_mff.core.header import MFFHeader
                header = MFFHeader.from_file(path)
                reg_result = validator.validate_regulatory_compliance(header, args.regulation)
                
                if reg_result.is_valid:
                    print(f"✅ {args.regulation} compliance: PASSED")
                else:
                    print(f"❌ {args.regulation} compliance: FAILED")
                    all_valid = False
                    
                    for error in reg_result.errors:
                        print(f"   Error: {error}")
                
                headers.append(header)
            
        except Exception as e:
            print(f"❌ Validation error: {e}")
            all_valid = False
    
    # Cascade validation
    if args.cascade and headers:
        print(f"\n🔗 Cascade Validation ({len(headers)} headers)")
        cascade_result = validator.validate_cascade_requirements(headers)
        
        if cascade_result.is_valid:
            print("✅ Cascade requirements: PASSED")
        else:
            print("❌ Cascade requirements: FAILED")
            all_valid = False
            
            for error in cascade_result.errors:
                print(f"   Error: {error}")
    
    # Summary
    print("\n" + "=" * 40)
    if all_valid:
        print("🎉 All validations PASSED")
        return 0
    else:
        print("💥 Some validations FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())