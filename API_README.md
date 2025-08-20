# AMEDEO API Framework

## Overview

The AMEDEO API Framework provides a standardized RESTful interface to the AMEDEO system components, including digital twins, flight operations, environmental monitoring, evidence management, and AI validation.

## JSON Schemas

The API uses JSON Schema (Draft 7) for data validation and documentation:

### Core Schemas

- **`system_status.schema.json`** - Overall system health and subsystem status
- **`digital_twin.schema.json`** - Digital twin state and telemetry
- **`flight_plan.schema.json`** - Flight plans and operational data
- **`environmental_metrics.schema.json`** - Environmental monitoring and compliance
- **`evidence_record.schema.json`** - DET evidence records with cryptographic integrity
- **`ai_spec_validation.schema.json`** - AI-SPEC validation results

## API Endpoints

### System Status
```
GET /amedeo/system/status
```
Returns overall system health including all subsystems (digital twin, environmental, flight operations, security, evidence store, compliance).

### Digital Twin Fleet
```
GET /amedeo/digital-twin/fleet
```
Returns digital twin fleet status with telemetry, predictions, and health scores.

### Environmental Metrics
```
GET /amedeo/environmental/metrics
```
Returns environmental monitoring data including emissions, noise, weather, and compliance status.

### Flight Operations
```
GET /amedeo/flight-ops/active
```
Returns active flight plans with routes, crew, environmental constraints, and status.

### Evidence Management
```
GET /amedeo/evidence/recent
```
Returns recent DET evidence records with cryptographic signatures and UTCS-MI compliance.

### Schema Access
```
GET /schemas/<schema_name>
```
Returns the JSON schema for validation and documentation.

## Usage

### Starting the API Server

```bash
# Install dependencies (optional for enhanced functionality)
pip install flask flask-cors

# Start server
python amedeo_api_server.py
```

The server will be available at `http://localhost:8080`

### Testing

```bash
# Run schema validation tests
python test_api_schemas.py
```

### Integration with AMEDEO Agents

The API server integrates with the existing AMEDEO agent system:

- **Strategic Planner Agent** - Provides strategic planning data
- **Supply Buyer Agent** - Manages supply chain and procurement data  
- **Resource Scheduler Agent** - Handles resource allocation and scheduling
- **Ops Pilot Agent** - Manages operational flight data

## Example Responses

### System Status
```json
{
  "timestamp": "2025-08-20T14:30:00Z",
  "version": "1.0.0",
  "uptime_seconds": 864000,
  "overall_status": "operational",
  "subsystems": {
    "digital_twin": {
      "status": "operational",
      "health_score": 0.98,
      "last_update": "2025-08-20T14:29:55Z",
      "alerts": []
    }
  }
}
```

### Digital Twin
```json
{
  "twin_id": "twin_BWB-Q100-001",
  "asset_id": "BWB-Q100-001",
  "registration": "AM-BWB-001",
  "last_sync": "2025-08-20T14:30:00Z",
  "telemetry": {
    "altitude_ft": 39000,
    "speed_knots": 485,
    "heading_deg": 270,
    "temperature_c": -56,
    "fuel_remaining_kg": 22500,
    "engine_status": ["nominal", "nominal", "nominal", "nominal"]
  },
  "health_score": 0.93
}
```

## Standards Compliance

- **JSON Schema Draft 7** for data validation
- **REST API** following OpenAPI principles
- **UTCS-MI v5.0** compliance for governance and traceability
- **Aerospace certification** standards (DO-178C, CS-25)
- **Post-quantum cryptography** (PQ-DILITHIUM) for evidence integrity

## Security Features

- Cryptographic signatures for evidence records
- UTCS-MI manifest validation
- Immutable evidence storage
- Multi-factor authentication support
- Geographic and data classification restrictions

## Architecture Integration

The AMEDEO API Framework integrates with:

- **AI-SPEC** - Policy validation and attestation
- **DET Evidence Twin** - Immutable evidence storage
- **QAL** - Quantum validation and computation
- **GAIA AIR-RTOS** - Real-time avionic systems
- **Agent Framework** - Strategic planning and operations

This API provides the standardized interface layer for the complete AMEDEO system-of-systems architecture.