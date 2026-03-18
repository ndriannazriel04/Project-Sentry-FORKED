# Student 1: Input Layer - Implementation Guide

## Overview
**Goal:** Provide raw visibility into network and system security events.

## Components

### 1. Event Collector API
**File:** `src/event_collector/`

**Endpoints:**
- `POST /api/v1/events/ingest` - Ingest security events
- `GET /api/v1/events/` - List all events
- `GET /api/v1/events/{event_id}` - Get specific event details

**Event Schema:**
```json
{
  "event_type": "Auth|Access|Admin|System",
  "asset_id": "uuid",
  "source_ip": "192.168.1.1",
  "user_id": "john.doe",
  "action": "login|file_access|privilege_change|process_start",
  "status": "success|failure",
  "timestamp": "2026-03-18T10:30:00Z",
  "raw_data": {}
}
```

### 2. Discovery Engine
**File:** `src/discovery/`

**Features:**
- Nmap active scanning for network mapping
- PCAP sniffing for passive asset discovery
- Service fingerprinting
- OS detection

**Endpoints:**
- `POST /api/v1/discovery/scan` - Start network scan
- `GET /api/v1/discovery/scan/{scan_id}` - Get scan results
- `GET /api/v1/discovery/assets` - List discovered assets

### 3. SBOM Generator
**File:** `src/sbom_generator/`

**Features:**
- CycloneDX format compliance
- Package manager parsing (pip, npm, apt, docker)
- NVD/CVE correlation
- Component versioning

**Endpoints:**
- `POST /api/v1/sbom/generate` - Generate SBOM for asset
- `GET /api/v1/sbom/{sbom_id}` - Get SBOM details
- `GET /api/v1/sbom/vulnerabilities/{asset_id}` - List vulnerabilities

### 4. Drift Detection
**File:** `src/drift_detection/`

**Features:**
- Golden image baseline creation
- Real-time drift detection
- File hash comparison
- Configuration change tracking

**Endpoints:**
- `POST /api/v1/drift/baseline/{asset_id}` - Create baseline
- `POST /api/v1/drift/check/{asset_id}` - Check for drift
- `GET /api/v1/drift/drift-report/{asset_id}` - Get detailed report

## Database Schema

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed schemas.

## Development

### Install Dependencies
```bash
cd student-1-input-layer
pip install -r requirements.txt
```

### Run Locally
```bash
python main.py
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing
```bash
pytest tests/
```

## MVP Priorities
1. Event ingestion API (POST /api/v1/events/ingest)
2. Asset tracking (basic inventory)
3. SBOM generation from Docker images
4. Golden baseline for 1-2 asset types

## Future Enhancements
- Live PCAP sniffing with Scapy
- Kubernetes secrets detection
- Cloud asset discovery (AWS/Azure/GCP)
- Mobile device onboarding
