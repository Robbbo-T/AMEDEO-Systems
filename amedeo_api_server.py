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
        # Get agent status
        agent_status = self._get_agent_status()
        
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
                },
                "agents": agent_status
            }
        }
    
    def _get_agent_status(self) -> Dict[str, Any]:
        """Get status from AMEDEO agents"""
        try:
            # Test basic agent functionality
            from agents.base_agent import Intent
            
            test_intent = Intent(
                kind="STATUS_CHECK",
                payload={"affects_strategy": True, "expected_gain": 3.5}
            )
            
            agent_results = {}
            for name, agent in self.agents.items():
                try:
                    # Access correct agent ID attribute  
                    agent_id = getattr(agent, 'id', f"api-{name}")
                    agent_results[name] = {
                        "status": "operational",
                        "last_check": datetime.now(timezone.utc).isoformat(),
                        "agent_id": agent_id,
                        "available": True
                    }
                except Exception as e:
                    agent_results[name] = {
                        "status": "degraded", 
                        "last_check": datetime.now(timezone.utc).isoformat(),
                        "error": str(e),
                        "available": False
                    }
            
            return {
                "status": "operational",
                "agents": agent_results,
                "total_agents": len(self.agents),
                "operational_count": sum(1 for a in agent_results.values() if a["available"])
            }
            
        except Exception as e:
            return {
                "status": "degraded",
                "error": f"Agent system error: {str(e)}",
                "total_agents": len(self.agents),
                "operational_count": 0
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
    
    def get_maintenance_prediction(self, asset_id: str = "BWB-Q100-001") -> Dict[str, Any]:
        """Get maintenance prediction for an asset"""
        return {
            "asset_id": asset_id,
            "prediction_date": datetime.now(timezone.utc).isoformat(),
            "time_horizon_days": 60,
            "current_health_score": 0.93,
            "predicted_health_score": 0.85,
            "risk_assessment": {
                "overall_risk": "low",
                "risk_score": 0.23,
                "confidence": 0.89
            },
            "recommendations": [
                {
                    "component": "engine_1_turbine",
                    "maintenance_type": "borescope_inspection",
                    "urgency": "medium",
                    "predicted_date": "2025-09-15",
                    "confidence": 0.87,
                    "estimated_hours": 4,
                    "parts_required": [],
                    "cost_estimate_usd": 2500
                },
                {
                    "component": "landing_gear_main",
                    "maintenance_type": "lubrication",
                    "urgency": "low",
                    "predicted_date": "2025-09-20",
                    "confidence": 0.92,
                    "estimated_hours": 2,
                    "parts_required": ["hydraulic_fluid_5606"],
                    "cost_estimate_usd": 800
                }
            ],
            "maintenance_schedule": {
                "next_a_check": "2025-09-01",
                "next_b_check": "2025-11-15",
                "next_c_check": "2026-03-01",
                "next_d_check": "2027-08-15"
            }
        }
    
    def get_carbon_offset(self, flight_id: str = "FL8A3C9F2B") -> Dict[str, Any]:
        """Get carbon offset information for a flight"""
        return {
            "flight_id": flight_id,
            "emissions_kg": 42500,
            "offset_calculation": {
                "base_emissions_kg": 42500,
                "reduction_achieved_kg": 2125,
                "net_emissions_kg": 40375,
                "offset_required_kg": 40375
            },
            "offset_options": [
                {
                    "provider": "CarbonNeutral Airways",
                    "type": "verified",
                    "rate_per_kg": 0.045,
                    "total_cost_usd": 1816.88,
                    "certificate_available": True,
                    "project": "Amazon Rainforest Conservation",
                    "rating": 4.8
                },
                {
                    "provider": "ClimateCare",
                    "type": "premium",
                    "rate_per_kg": 0.025,
                    "total_cost_usd": 1009.38,
                    "certificate_available": True,
                    "project": "Wind Farm Development India",
                    "rating": 4.5
                }
            ],
            "selected_option": {
                "provider": "CarbonNeutral Airways",
                "certificate_id": "CN-2025-8A3C9F2B",
                "transaction_id": "TXN-445566778899",
                "validation_date": "2025-08-20T14:35:00Z",
                "expiry_date": "2026-08-20T14:35:00Z"
            },
            "compliance": {
                "corsia_compliant": True,
                "eu_ets_compliant": True,
                "voluntary_offset": False
            }
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
    
    def get_ai_validation(self, pipeline_id: str = "PIPE-8A3C9F2B") -> Dict[str, Any]:
        """Get AI-SPEC validation results"""
        return {
            "validation_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pipeline_id": pipeline_id,
            "validation_level": 4,
            "policy_version": "AI-SPEC-v2.1",
            "results": {
                "overall_status": "approved",
                "policy_checks": [
                    {
                        "policy": "data_governance",
                        "result": "pass",
                        "message": "Data lineage properly documented",
                        "severity": "info"
                    },
                    {
                        "policy": "model_explainability",
                        "result": "pass",
                        "message": "Model decisions are interpretable",
                        "severity": "info"
                    },
                    {
                        "policy": "bias_assessment",
                        "result": "pass",
                        "message": "No significant bias detected",
                        "severity": "info"
                    }
                ],
                "security": {
                    "encryption": "PQ",
                    "signed": True,
                    "attestation": "SGX-enabled",
                    "mfa_verified": True
                },
                "constraints": {
                    "time_limit_minutes": 60,
                    "rate_limit": "100/hour",
                    "data_classification": "confidential",
                    "geographic_restrictions": ["EU", "US"]
                }
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
            
            @self.app.route('/amedeo/maintenance/prediction/<asset_id>', methods=['GET'])
            def maintenance_prediction(asset_id):
                return jsonify(self.api.get_maintenance_prediction(asset_id))
            
            @self.app.route('/amedeo/environmental/carbon-offset/<flight_id>', methods=['GET'])
            def carbon_offset(flight_id):
                return jsonify(self.api.get_carbon_offset(flight_id))
            
            @self.app.route('/amedeo/ai-spec/validation/<pipeline_id>', methods=['GET'])
            def ai_validation(pipeline_id):
                return jsonify(self.api.get_ai_validation(pipeline_id))
            
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
        print("   GET /amedeo/maintenance/prediction/<asset_id>")
        print("   GET /amedeo/environmental/carbon-offset/<flight_id>")
        print("   GET /amedeo/ai-spec/validation/<pipeline_id>")
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