#!/usr/bin/env python3
"""
UTDC-GPS-MFF Generation Tool
UTCS-MI: EstándarUniversal:Herramienta-Desarrollo-UTDC-01.01-GeneratorTool-0001-v1.0-AerospaceAndQuantumUnitedAdvancedVenture-GeneracionHumana-CROSS-ReferenceImpl-generate1-RestoDeVidaUtil
"""

import sys
import json
import argparse
from pathlib import Path

# Add source path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utdc_gps_mff import MFFGenerator


def main():
    parser = argparse.ArgumentParser(description="Generate UTDC-GPS-MFF artifacts")
    parser.add_argument("template", help="Template name (e.g., s1000d/basic_document)")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument("--content", help="JSON file with content data")
    parser.add_argument("--regulation", default="UTDC", help="Primary regulation")
    parser.add_argument("--title", help="Document title")
    parser.add_argument("--description", help="Document description") 
    parser.add_argument("--author", default="AMEDEO Systems", help="Document author")
    parser.add_argument("--classification", default="CUI", help="Security classification")
    parser.add_argument("--method", default="GeneracionHibrida", help="Generation method")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    print("🚀 UTDC-GPS-MFF Generation")
    print("=" * 40)
    
    # Load content data
    content_data = {}
    
    if args.content:
        content_path = Path(args.content)
        if content_path.exists():
            with open(content_path) as f:
                content_data = json.load(f)
            print(f"📄 Loaded content from: {content_path}")
        else:
            print(f"❌ Content file not found: {content_path}")
            return 1
    
    # Override with command line arguments
    if args.title:
        content_data["title"] = args.title
    if args.description:
        content_data["description"] = args.description
    if args.author:
        content_data["author"] = args.author
    
    # Set defaults
    content_data.setdefault("title", "UTDC-GPS-MFF Generated Document")
    content_data.setdefault("description", "Document generated using UTDC-GPS-MFF standard")
    content_data.setdefault("author", args.author)
    content_data.setdefault("category", "GeneratedDocument")
    
    print(f"📋 Template: {args.template}")
    print(f"📋 Title: {content_data['title']}")
    print(f"📋 Regulation: {args.regulation}")
    print(f"📂 Output: {args.output}")
    
    try:
        # Create generator
        generator = MFFGenerator()
        
        # Generate artifact
        output_dir = Path(args.output)
        
        artifact_path, header_path = generator.generate_artifact(
            template_name=args.template,
            content_data=content_data,
            output_dir=output_dir,
            regulation=args.regulation,
            classification=args.classification,
            method=args.method
        )
        
        print(f"\n✅ Generation completed successfully!")
        print(f"📄 Artifact: {artifact_path}")
        print(f"📄 Header: {header_path}")
        
        if args.verbose:
            print(f"\n📊 Artifact size: {artifact_path.stat().st_size} bytes")
            print(f"📊 Header size: {header_path.stat().st_size} bytes")
            
            # Show header summary
            from utdc_gps_mff.core.header import MFFHeader
            header = MFFHeader.from_file(header_path)
            print(f"🏷️  UTCS-MI ID: {header.utcmi_id}")
            if header.artifact:
                print(f"🔒 SHA256: {header.artifact.sha256[:16]}...")
        
        return 0
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())