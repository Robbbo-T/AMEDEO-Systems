#!/usr/bin/env python3
"""
UTCS-MI: AQUART-API-SERVER-amedeo_api-v1.0
AMEDEO API Server - RESTful API for AMEDEO system components
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional
import sys

# Add agents to path for integration
sys.path.insert(0, str(Path(__file__).parent / "agents"))

try:
    # Try to import Flask for a full REST server
    from flask import Flask, jsonify, request, Response
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    # Fallback to basic HTTP server
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import urllib.parse
    FLASK_AVAILABLE = False

from agents import StrategicPlannerAgent, SupplyBuyerAgent, ResourceSchedulerAgent, OpsPilotAgent


class AMEDEOAPIServer:
    """AMEDEO API Server providing standardized access to system components"""
    
    def __init__(self, schemas_dir: str = "schemas"):
        self.schemas_dir = Path(schemas_dir)
        self.schemas = self._load_schemas()
        self.agents = self._initialize_agents()
        
    def _load_schemas(self) -> Dict[str, Dict]:
        """Load all JSON schemas"""
        schemas = {}
        schema_files = [
            "system_status.schema.json",
            "digital_twin.schema.json", 
            "flight_plan.schema.json",
            "environmental_metrics.schema.json",
            "evidence_record.schema.json",
            "ai_spec_validation.schema.json"
        ]
        
        for schema_file in schema_files:
            schema_path = self.schemas_dir / schema_file
            if schema_path.exists():
                with open(schema_path) as f:
                    schema_name = schema_file.replace('.schema.json', '')
                    schemas[schema_name] = json.load(f)
                    
        return schemas
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize AMEDEO agents for integration"""
        return {
            "planner": StrategicPlannerAgent("api-planner", "agents/POLICY.md"),
            "buyer": SupplyBuyerAgent("api-buyer", "agents/POLICY.md"),
            "scheduler": ResourceSchedulerAgent("api-scheduler", "agents/POLICY.md"),
            "pilot": OpsPilotAgent("api-pilot", "agents/POLICY.md")
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
            "uptime_seconds": 864000,
            "overall_status": "operational",
            "subsystems": {
                "digital_twin": {
                    "status": "operational",
                    "health_score": 0.98,
                    "last_update": datetime.now(timezone.utc).isoformat(),
                    "alerts": []
                },
                "environmental": {
                    "status": "operational", 
                    "health_score": 0.96,
                    "last_update": datetime.now(timezone.utc).isoformat(),
                    "alerts": []
                },
                "flight_operations": {
                    "status": "operational",
                    "health_score": 0.94,
                    "last_update": datetime.now(timezone.utc).isoformat(),
                    "alerts": []
                },
                "security": {
                    "status": "operational",
                    "health_score": 0.99,
                    "last_update": datetime.now(timezone.utc).isoformat(),
                    "alerts": []
                },
                "evidence_store": {
                    "status": "operational",
                    "health_score": 1.0,
                    "last_update": datetime.now(timezone.utc).isoformat(),
                    "alerts": []
                },
                "compliance": {
                    "status": "operational",
                    "health_score": 0.97,
                    "last_update": datetime.now(timezone.utc).isoformat(),
                    "alerts": []
                }
            }
        }
    
    def get_digital_twin_fleet(self) -> Dict[str, Any]:
        """Get digital twin fleet status"""
        return {
            "twin_id": "twin_BWB-Q100-001",
            "asset_id": "BWB-Q100-001", 
            "registration": "AM-BWB-001",
            "last_sync": datetime.now(timezone.utc).isoformat(),
            "telemetry": {
                "altitude_ft": 39000,
                "speed_knots": 485,
                "heading_deg": 270,
                "temperature_c": -56,
                "pressure_psi": 14.7,
                "fuel_remaining_kg": 22500,
                "engine_status": ["nominal", "nominal", "nominal", "nominal"]
            },
            "predictions": {
                "fuel_efficiency": 0.82,
                "eta": "2025-08-20T17:45:00Z",
                "maintenance_score": 0.91,
                "remaining_cycles": 4250
            },
            "health_score": 0.93,
            "maintenance_due": "2025-09-15T08:00:00Z"
        }
    
    def get_environmental_metrics(self) -> Dict[str, Any]:
        """Get environmental metrics"""
        return {
            "metric_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "location": {
                "airport_code": "LHR",
                "lat": 51.4775,
                "lon": -0.4614,
                "altitude_m": 25
            },
            "emissions": {
                "co2_kg": 42500,
                "nox_kg": 125,
                "pm_kg": 12.5,
                "so2_kg": 8.2
            },
            "noise": {
                "level_db": 82.5,
                "frequency_hz": 1000,
                "duration_seconds": 45
            },
            "weather": {
                "temperature_c": 15,
                "pressure_hpa": 1013.25,
                "humidity_percent": 65,
                "wind_speed_knots": 12,
                "wind_direction_deg": 270,
                "visibility_meters": 10000
            },
            "compliance": {
                "status": "compliant",
                "violations": []
            }
        }
    
    def get_active_flights(self) -> Dict[str, Any]:
        """Get active flight operations"""
        return {
            "flight_id": "FL8A3C9F2B",
            "flight_number": "AM100",
            "aircraft_id": "BWB-Q100-001",
            "departure": "LHR",
            "arrival": "JFK",
            "departure_time": "2025-08-21T10:00:00Z",
            "arrival_time": "2025-08-21T17:45:00Z",
            "route": [
                {
                    "waypoint": "LHR",
                    "altitude": 0,
                    "estimated_time": "2025-08-21T10:00:00Z",
                    "coordinates": {"lat": 51.4775, "lon": -0.4614}
                },
                {
                    "waypoint": "DVR", 
                    "altitude": 35000,
                    "estimated_time": "2025-08-21T10:25:00Z",
                    "coordinates": {"lat": 51.1257, "lon": 1.3134}
                },
                {
                    "waypoint": "JFK",
                    "altitude": 0,
                    "estimated_time": "2025-08-21T17:45:00Z",
                    "coordinates": {"lat": 40.6413, "lon": -73.7781}
                }
            ],
            "fuel_plan_kg": 45000,
            "environmental_constraints": {
                "max_altitude_ft": 41000,
                "noise_abatement_zones": ["LHR", "JFK"],
                "emission_reduction_mode": True,
                "carbon_offset_required": True
            },
            "crew": [
                {
                    "id": "CREW001",
                    "name": "Captain Smith",
                    "role": "captain",
                    "license": "ATPL-12345"
                }
            ],
            "status": "scheduled"
        }
    
    def get_recent_evidence(self) -> Dict[str, Any]:
        """Get recent evidence records"""
        return {
            "evidence_id": str(uuid.uuid4()),
            "execution_id": "FL8A3C9F2B",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": "operational",
            "data": {
                "action": "flight_plan_created",
                "flight_number": "AM100",
                "departure": "LHR",
                "arrival": "JFK",
                "compliance_checks": {
                    "emissions": "pass",
                    "noise": "pass",
                    "security": "pass"
                }
            },
            "hash": "3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c",
            "signatures": [
                {
                    "signer": "amedeo-api-server",
                    "signature": "sig_8a3c9f2b4d5e6f7a",
                    "algorithm": "ECDSA-SHA256",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            ],
            "utcs_mi": {
                "compliant": True,
                "version": "5.0",
                "manifest": {
                    "schema": "flight_operation",
                    "validated": True
                }
            },
            "immutable": True,
            "retention": {
                "years": 7,
                "classification": "operational"
            }
        }


if FLASK_AVAILABLE:
    # Flask-based REST API server
    class FlaskAMEDEOServer:
        def __init__(self):
            self.app = Flask(__name__)
            CORS(self.app)
            self.api = AMEDEOAPIServer()
            self._setup_routes()
        
        def _setup_routes(self):
            """Setup REST API routes"""
            
            @self.app.route('/amedeo/system/status', methods=['GET'])
            def system_status():
                return jsonify(self.api.get_system_status())
            
            @self.app.route('/amedeo/digital-twin/fleet', methods=['GET'])
            def digital_twin_fleet():
                return jsonify(self.api.get_digital_twin_fleet())
            
            @self.app.route('/amedeo/environmental/metrics', methods=['GET'])
            def environmental_metrics():
                return jsonify(self.api.get_environmental_metrics())
            
            @self.app.route('/amedeo/flight-ops/active', methods=['GET'])
            def active_flights():
                return jsonify(self.api.get_active_flights())
            
            @self.app.route('/amedeo/evidence/recent', methods=['GET'])
            def recent_evidence():
                return jsonify(self.api.get_recent_evidence())
            
            @self.app.route('/schemas/<schema_name>', methods=['GET'])
            def get_schema(schema_name):
                if schema_name in self.api.schemas:
                    return jsonify(self.api.schemas[schema_name])
                return jsonify({"error": "Schema not found"}), 404
            
            @self.app.route('/health', methods=['GET'])
            def health_check():
                return jsonify({"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()})
        
        def run(self, host='0.0.0.0', port=8080, debug=False):
            """Run the Flask server"""
            self.app.run(host=host, port=port, debug=debug)


def main():
    """Main entry point"""
    if FLASK_AVAILABLE:
        print("🚀 Starting AMEDEO API Server (Flask)")
        server = FlaskAMEDEOServer()
        print("📡 Server running on http://localhost:8080")
        print("📋 Available endpoints:")
        print("   GET /amedeo/system/status")
        print("   GET /amedeo/digital-twin/fleet") 
        print("   GET /amedeo/environmental/metrics")
        print("   GET /amedeo/flight-ops/active")
        print("   GET /amedeo/evidence/recent")
        print("   GET /schemas/<schema_name>")
        print("   GET /health")
        server.run(debug=True)
    else:
        print("⚠️  Flask not available, install with: pip install flask flask-cors")
        print("🔧 Basic API functions available in AMEDEOAPIServer class")
        
        # Demo the API functions
        api = AMEDEOAPIServer()
        print("\n📊 Demo API Responses:")
        print("System Status:", json.dumps(api.get_system_status(), indent=2)[:200] + "...")
        print("Digital Twin:", json.dumps(api.get_digital_twin_fleet(), indent=2)[:200] + "...")


if __name__ == "__main__":
    main()