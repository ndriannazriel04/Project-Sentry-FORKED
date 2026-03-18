# Architecture & Design

## Project Sentinel - Deep Dive

### Overview
**Sentinel** is built on a **3-Student Model** where each component specializes in a specific phase of the security intelligence pipeline.

### Student 1: Input Layer - The Senses

**Objective:** Capture raw security events and asset inventory without losing signal in the noise.

#### Components:

1. **Hybrid Discovery Engine**
   - Active scanning: Nmap, Zmap for network enumeration
   - Passive collection: PCAP sniffing with Scapy
   - Outputs: Asset inventory with OS, services, open ports
   - Frequency: Daily/weekly baseline + on-demand

2. **Event Collector API (FastAPI)**
   - Four core event types:
     - **Auth**: Login events (successful, failed, multi-factor)
     - **Access**: File access, database queries, API calls
     - **Admin**: Privilege changes, user creation/deletion, sudo usage
     - **System**: Process execution, service starts, kernel modules loaded
   - RESTful endpoints for ingestion
   - Batching for performance

3. **Custom SBOM Generator**
   - Parses: package managers (pip, npm, apt), Docker images, binary analysis
   - Format: CycloneDX (SBOM standard)
   - NVD/CVE integration for vulnerability detection
   - Supply chain risk assessment

4. **Golden Image / Drift Logic**
   - Establish baseline ("known-good" state) for assets
   - Continuous comparison with current state
   - Detects: file modifications, permission changes, config drift
   - Alerts on unauthorized changes

#### Database Schema (PostgreSQL):
```sql
-- Assets table
CREATE TABLE assets (
    id UUID PRIMARY KEY,
    name VARCHAR,
    ip_address INET,
    hostname VARCHAR,
    os_type VARCHAR,
    asset_criticality INT (1-10),
    created_at TIMESTAMP,
    last_scanned TIMESTAMP
);

-- Events table
CREATE TABLE events (
    id UUID PRIMARY KEY,
    asset_id UUID REFERENCES assets(id),
    event_type VARCHAR (Auth|Access|Admin|System),
    source_ip INET,
    user_id VARCHAR,
    action VARCHAR,
    status VARCHAR (success|failure),
    timestamp TIMESTAMP,
    raw_data JSONB
);

-- SBOM table
CREATE TABLE sbom_records (
    id UUID PRIMARY KEY,
    asset_id UUID REFERENCES assets(id),
    component_name VARCHAR,
    version VARCHAR,
    vulnerability_count INT,
    generated_at TIMESTAMP
);

-- Golden baseline
CREATE TABLE golden_baseline (
    id UUID PRIMARY KEY,
    asset_id UUID REFERENCES assets(id),
    file_hash VARCHAR,
    config_hash VARCHAR,
    baseline_time TIMESTAMP
);
```

---

### Student 2: Enrichment Layer - The Detective

**Objective:** Add context to raw events, enabling threat correlation and pattern recognition.

#### Components:

1. **Local Geo-Network Engine**
   - MaxMind GeoLite2 database (self-hosted, no external calls)
   - Detects:
     - Geographically impossible login (e.g., NYC → Singapore in 5 minutes)
     - VPN/Tor routing
     - High-risk countries (configurable)
   - Scores each login by geo-risk

2. **Local CTI Ingestion Pipeline (STIX/TAXII)**
   - Ingests: MyCERT threat feeds, OSINT sources, custom TAXII servers
   - All processing local (no data exfil)
   - Maintains local copies of threat databases
   - Checks indicators (IPs, domains, file hashes) against known-bad

3. **MITRE ATT&CK Mapper**
   - Maps events to MITRE tactics/techniques
   - Event sequence analysis: detects multi-step attack chains
   - Example: (nmap scan → SSH brute-force → privilege escalation) → Tactic: Initial Access > Persistence
   - Confidence scoring (0.0-1.0)

4. **Historical Trend Analysis**
   - Time-series data on attack patterns
   - Identifies recurring adversaries
   - Seasonal trends (more attacks during business hours?)
   - Forecasting (predictive analytics)

#### Database Schema (PostgreSQL + Time-Series):
```sql
CREATE TABLE enriched_events (
    id UUID PRIMARY KEY,
    event_id UUID REFERENCES events(id),
    
    -- GeoIP
    country_iso VARCHAR,
    is_vpn BOOLEAN,
    is_tor BOOLEAN,
    geo_risk_score FLOAT,
    
    -- CTI
    known_malicious BOOLEAN,
    cti_sources TEXT[],
    
    -- MITRE
    mitre_tactic VARCHAR,
    mitre_technique VARCHAR,
    mitre_confidence FLOAT,
    
    -- Timestamps
    created_at TIMESTAMP
);

-- For trend analysis (time-series optimized)
CREATE TABLE attack_trends (
    time TIMESTAMP,
    tactic VARCHAR,
    technique VARCHAR,
    event_count INT,
    severity_avg FLOAT
) USING (time TIMESTAMP WITH TIME ZONE, tactic, technique);
CREATE INDEX ON attack_trends (time DESC);
```

---

### Student 3: Intelligence Layer - The Commander

**Objective:** Translate technical alerts into business-ready intelligence and prescriptive guidance.

#### Components:

1. **Real-time Risk Scoring Engine**
   - Algorithm: `Risk Score = (Event Severity × 0.6) + (Asset Criticality × 0.4)`
   - Range: 0-100
   - Dynamic thresholds:
     - 80+: CRITICAL (immediate action)
     - 60-79: HIGH
     - 40-59: MEDIUM
     - <40: LOW
   - Context: asset type, user role, time of day

2. **AI Advisory Brain (LLM + RAG)**
   - Models: Gemini Pro, GPT-4, Claude 3 Opus (configurable)
   - Retrieval: Pull similar historical incidents, remediation playbooks, threat reports
   - Generation: LLM produces natural language advisory
   - Examples:
     - "Brute-force SSH attack detected (3 failed logins from known malicious IP 203.xyz). Recommend: Block IP at ingress firewall, force password reset for user."
     - "Configuration drift detected on DB server. SBOM shows outdated PostgreSQL. Recommend: Apply security patches, restart service."

3. **Automated Playbook Generator**
   - Input: enriched event + asset type + current context
   - Output: Executable CLI commands (IPTables, user management, service restarts)
   - Requires approval before execution (for safety)
   - Examples:
     ```bash
     # Isolate compromised host
     sudo iptables -I INPUT -s <malicious_ip> -j DROP
     
     # Lock compromised user
     sudo usermod -L <username>
     
     # Block at firewall
     sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="<malicious_ip>" drop'
     ```

4. **Interactive ChatOps**
   - Telegram/Discord bot integration
   - Natural language queries: "Show me critical alerts from today"
   - One-click action approval
   - Audit trail of all actions

#### Database Schema (PostgreSQL):
```sql
CREATE TABLE risk_assessments (
    id UUID PRIMARY KEY,
    event_id UUID REFERENCES events(id),
    asset_id UUID REFERENCES assets(id),
    
    event_severity INT (1-10),
    asset_criticality INT (1-10),
    risk_score FLOAT (0-100),
    
    advisory_text TEXT,
    ai_confidence FLOAT,
    
    created_at TIMESTAMP
);

CREATE TABLE playbooks (
    id UUID PRIMARY KEY,
    event_id UUID,
    automation_type VARCHAR,
    
    commands TEXT[],
    execution_status VARCHAR (draft|pending|approved|executed|failed),
    approver_id VARCHAR,
    approved_at TIMESTAMP,
    
    executed_by VARCHAR,
    executed_at TIMESTAMP,
    audit_log JSONB
);

CREATE TABLE chatops_interactions (
    id UUID PRIMARY KEY,
    user_id VARCHAR,
    channel VARCHAR (telegram|discord),
    query TEXT,
    response TEXT,
    action_taken VARCHAR,
    timestamp TIMESTAMP
);
```

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ SENSORS (Student 1)                                              │
│ ├─ Network scanning (Nmap/PCAP) → Assets                        │
│ ├─ Event ingestion (Auth, Access, Admin, System)                │
│ ├─ SBOM generation (CycloneDX)                                  │
│ └─ Golden baseline comparison                                    │
└─────────────────────┬───────────────────────────────────────────┘
                      │ Raw Events & Assets
                      ▼
        ┌──────────────────────────────────────┐
        │ PostgreSQL Database (Primary Store)  │
        │ - Events, Assets, SBOM, Baseline    │
        │ - Redis for caching & real-time     │
        └──────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ ENRICHMENT (Student 2)                                           │
│ ├─ GeoIP analysis (MaxMind) → geo_risk_score                    │
│ ├─ CTI checking (MyCERT, OSINT) → known_malicious              │
│ ├─ MITRE mapping (ATT&CK) → tactic + technique                │
│ └─ Trend analysis (time-series) → patterns                      │
└─────────────────────┬───────────────────────────────────────────┘
                      │ Enriched Events with Context
                      ▼
        ┌──────────────────────────────────────┐
        │ PostgreSQL (Enrichment Tables)       │
        │ - enriched_events, attack_trends     │
        │ - Vector embeddings (Chromadb)       │
        └──────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ INTELLIGENCE (Student 3)                                         │
│ ├─ Risk scoring (0-100 algorithm)                               │
│ ├─ AI advisory (LLM + RAG retrieval)                            │
│ ├─ Playbook generation (CLI commands)                           │
│ └─ ChatOps (Telegram/Discord)                                   │
└─────────────────────┬───────────────────────────────────────────┘
                      │ Risk Scores, Advisories, Actions
                      ▼
        ┌──────────────────────────────────────┐
        │ React Dashboard + WebSocket Streaming│
        │ - Real-time alerts                   │
        │ - ChatOps interface                  │
        │ - Playbook approval/execution        │
        └──────────────────────────────────────┘
```

---

## Privacy & Security

✅ **Self-Hosted:** All processing happens on-premises
✅ **No Exfiltration:** GeoIP, CTI, MITRE databases stored locally
✅ **Encryption:** PostgreSQL column encryption, TLS for inter-service comms
✅ **RBAC:** Admin (full access) vs. Analyst (read-only)
✅ **Audit Logs:** Every action logged with user, timestamp, changes

---

## Deployment Notes

### Docker Compose Services
1. PostgreSQL (database)
2. Redis (caching, real-time)
3. Student 1 (port 8001)
4. Student 2 (port 8002)
5. Student 3 (port 8003)
6. React Frontend (port 3000)

### Scaling Strategy
- **Horizontal:** Add more Student instances behind load balancer
- **Vertical:** Increase DB connections, Redis cache size
- **Archival:** Move old events to cold storage (S3/NAS)

---

## Next Steps
1. Implement database connection pooling
2. Build time-series query optimization
3. Deploy initial ML models for trend detection
4. Set up LLM integration (Gemini/GPT)
5. Create ChatOps bot framework
