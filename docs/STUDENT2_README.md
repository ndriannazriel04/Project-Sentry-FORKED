# Student 2: Enrichment Layer - Implementation Guide

## Overview
**Goal:** Transform raw events into actionable intelligence through enrichment and correlation.

## Components

### 1. GeoIP Engine
**File:** `src/geo_engine/`

**Features:**
- MaxMind GeoLite2 database (self-hosted)
- Geolocation-based risk scoring
- Impossible travel detection
- VPN/Tor identification

**Endpoints:**
- `POST /api/v1/geo/check-location` - Check IP geolocation
- `POST /api/v1/geo/impossible-travel` - Detect travel anomalies
- `GET /api/v1/geo/vpn-tor-check/{ip}` - VPN/Tor check

### 2. CTI Pipelines
**File:** `src/cti_pipelines/`

**Features:**
- STIX/TAXII feed ingestion
- MyCERT threat indicator processing
- Local threat database maintenance
- Indicator checking (IPs, domains, hashes)

**Endpoints:**
- `POST /api/v1/cti/ingest-feed` - Ingest threat feed
- `GET /api/v1/cti/threats` - Get current threats
- `POST /api/v1/cti/check-indicator` - Check if indicator is malicious
- `GET /api/v1/cti/feeds` - List active feeds

### 3. MITRE ATT&CK Mapper
**File:** `src/mitre_mapper/`

**Features:**
- Automatic tactic/technique mapping
- Event sequence analysis
- Attack chain detection
- Confidence scoring

**Endpoints:**
- `POST /api/v1/mitre/map-event` - Map event to MITRE
- `GET /api/v1/mitre/techniques/{technique_id}` - Get technique details
- `POST /api/v1/mitre/campaign-mapping` - Map campaign

### 4. Trend Analysis
**File:** `src/trend_analysis/`

**Features:**
- Time-series pattern detection
- Recurring attack identification
- Anomaly detection
- Predictive forecasting

**Endpoints:**
- `GET /api/v1/trends/trends` - Get recent trends
- `POST /api/v1/trends/recurring-patterns` - Detect patterns
- `GET /api/v1/trends/anomaly-detection` - Find anomalies
- `GET /api/v1/trends/forecast` - Forecast attacks

## Database Schema

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed schemas.

## Data Integration

### From Student 1
- Raw events → Enrichment processing
- Asset list → Criticality scoring
- SBOM data → Vulnerability correlation

### To Student 3
- Enriched events with context
- Risk factors and scoring inputs
- MITRE technique mappings

## Development

### Install Dependencies
```bash
cd student-2-enrichment-layer
pip install -r requirements.txt
```

### Run Locally
```bash
python main.py
```

### API Documentation
- Swagger UI: http://localhost:8000/docs

## Testing
```bash
pytest tests/
```

## MVP Priorities
1. GeoIP engine with MaxMind database
2. Basic CTI feed ingestion (STIX)
3. Event-to-MITRE mapping (static rules)
4. Simple trend reporting

## Future Enhancements
- ML-based behavior anomaly detection
- Graph analytics for attack chains
- Real-time TAXII feed updates
- Custom MITRE mappings for industry-specific attacks
