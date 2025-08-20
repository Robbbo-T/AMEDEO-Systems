#!/usr/bin/env python3
"""
UTCS-MI: AQUART-CLI-amedeo_client-v1.0
AMEDEO API Client - Command line interface for AMEDEO API
"""

import json
import sys
import argparse
from pathlib import Path

# Add current directory to path for API server import
sys.path.insert(0, str(Path(__file__).parent))

from amedeo_api_server import AMEDEOAPIServer


def format_json_output(data, compact=False):
    """Format JSON output for display"""
    if compact:
        return json.dumps(data, separators=(',', ':'))
    else:
        return json.dumps(data, indent=2)


def cmd_status(args):
    """Get system status"""
    api = AMEDEOAPIServer()
    status = api.get_system_status()
    print(format_json_output(status, args.compact))


def cmd_digital_twin(args):
    """Get digital twin fleet status"""
    api = AMEDEOAPIServer()
    twin_data = api.get_digital_twin_fleet()
    print(format_json_output(twin_data, args.compact))


def cmd_environmental(args):
    """Get environmental metrics"""
    api = AMEDEOAPIServer()
    env_data = api.get_environmental_metrics()
    print(format_json_output(env_data, args.compact))


def cmd_flights(args):
    """Get active flights"""
    api = AMEDEOAPIServer()
    flight_data = api.get_active_flights()
    print(format_json_output(flight_data, args.compact))


def cmd_evidence(args):
    """Get recent evidence"""
    api = AMEDEOAPIServer()
    evidence_data = api.get_recent_evidence()
    print(format_json_output(evidence_data, args.compact))


def cmd_schema(args):
    """Get schema definition"""
    api = AMEDEOAPIServer()
    
    if args.schema_name not in api.schemas:
        print(f"Error: Schema '{args.schema_name}' not found", file=sys.stderr)
        print(f"Available schemas: {', '.join(api.schemas.keys())}", file=sys.stderr)
        sys.exit(1)
    
    schema = api.schemas[args.schema_name]
    print(format_json_output(schema, args.compact))


def cmd_validate(args):
    """Validate a JSON file against a schema"""
    api = AMEDEOAPIServer()
    
    # Load JSON file
    try:
        with open(args.json_file) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{args.json_file}' not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{args.json_file}': {e}", file=sys.stderr)
        sys.exit(1)
    
    # Get schema
    if args.schema_name not in api.schemas:
        print(f"Error: Schema '{args.schema_name}' not found", file=sys.stderr)
        sys.exit(1)
    
    schema = api.schemas[args.schema_name]
    
    # Basic validation (simplified)
    try:
        required = schema.get("required", [])
        for field in required:
            if field not in data:
                print(f"❌ Validation failed: Missing required field '{field}'")
                sys.exit(1)
        
        print("✅ Validation passed")
        
    except Exception as e:
        print(f"❌ Validation error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_list(args):
    """List available endpoints and schemas"""
    api = AMEDEOAPIServer()
    
    print("📡 AMEDEO API Endpoints:")
    print("  status        - System status")
    print("  digital-twin  - Digital twin fleet")
    print("  environmental - Environmental metrics")
    print("  flights       - Active flights")
    print("  evidence      - Recent evidence")
    print()
    print("📋 Available Schemas:")
    for schema_name in sorted(api.schemas.keys()):
        print(f"  {schema_name}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AMEDEO API Client - Access AMEDEO system data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  amedeo-cli status                           # Get system status
  amedeo-cli digital-twin --compact          # Get digital twin data (compact)
  amedeo-cli schema system_status            # Get system_status schema
  amedeo-cli validate data.json flight_plan  # Validate data.json against flight_plan schema
  amedeo-cli list                            # List all endpoints and schemas
        """
    )
    
    parser.add_argument('--version', action='version', version='AMEDEO API Client v1.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Get system status')
    status_parser.add_argument('--compact', action='store_true', help='Output compact JSON')
    
    # Digital twin command
    digital_parser = subparsers.add_parser('digital-twin', help='Get digital twin fleet status')
    digital_parser.add_argument('--compact', action='store_true', help='Output compact JSON')
    
    # Environmental command
    env_parser = subparsers.add_parser('environmental', help='Get environmental metrics')
    env_parser.add_argument('--compact', action='store_true', help='Output compact JSON')
    
    # Flights command
    flights_parser = subparsers.add_parser('flights', help='Get active flights')
    flights_parser.add_argument('--compact', action='store_true', help='Output compact JSON')
    
    # Evidence command
    evidence_parser = subparsers.add_parser('evidence', help='Get recent evidence')
    evidence_parser.add_argument('--compact', action='store_true', help='Output compact JSON')
    
    # Schema command
    schema_parser = subparsers.add_parser('schema', help='Get schema definition')
    schema_parser.add_argument('schema_name', help='Name of schema to retrieve')
    schema_parser.add_argument('--compact', action='store_true', help='Output compact JSON')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate JSON against schema')
    validate_parser.add_argument('json_file', help='JSON file to validate')
    validate_parser.add_argument('schema_name', help='Schema to validate against')
    
    # List command
    subparsers.add_parser('list', help='List available endpoints and schemas')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Map commands to functions
    commands = {
        'status': cmd_status,
        'digital-twin': cmd_digital_twin,
        'environmental': cmd_environmental,
        'flights': cmd_flights,
        'evidence': cmd_evidence,
        'schema': cmd_schema,
        'validate': cmd_validate,
        'list': cmd_list
    }
    
    try:
        commands[args.command](args)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()