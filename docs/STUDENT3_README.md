# Student 3: Intelligence Layer - Implementation Guide

## Overview
**Goal:** Provide strategic intelligence and prescriptive remediation guidance.

## Components

### 1. Risk Engine
**File:** `src/risk_engine/`

**Features:**
- Dynamic 0-100 risk scoring
- Severity × Criticality algorithm
- Asset-aware risk assessment
- Threshold-based alerting

**Algorithm:**
```
Risk Score = (Event Severity × 0.6) + (Asset Criticality × 0.4)
Thresholds:
- Score ≥ 80: CRITICAL
- 60 ≤ Score < 80: HIGH
- 40 ≤ Score < 60: MEDIUM
- Score < 40: LOW
```

**Endpoints:**
- `POST /api/v1/risk/calculate` - Calculate risk score
- `GET /api/v1/risk/risk-profile/{asset_id}` - Get asset risk profile
- `POST /api/v1/risk/threshold-check` - Check against threshold

### 2. AI Advisor
**File:** `src/ai_advisor/`

**Features:**
- LLM integration (Gemini, GPT-4, Claude)
- RAG (Retrieval-Augmented Generation)
- Context-aware advisory
- Natural language queries

**Config:**
```
Supported models:
- gemini-pro (default)
- gpt-4
- claude-3-opus

Requires API key in .env
```

**Endpoints:**
- `POST /api/v1/advisor/advisory` - Get AI advisory
- `POST /api/v1/advisor/query` - Natural language query
- `GET /api/v1/advisor/context/{event_id}` - Get event context

### 3. Playbook Engine
**File:** `src/playbook_engine/`

**Features:**
- Automated playbook generation
- CLI command templating
- Approval workflow
- Execution audit trails

**Playbook Library:**
- Host isolation (firewall rules)
- Malicious IP blocking
- User account lockout
- Service restart/kill

**Endpoints:**
- `POST /api/v1/playbooks/generate` - Generate playbook
- `GET /api/v1/playbooks/{playbook_id}` - Get playbook details
- `POST /api/v1/playbooks/execute` - Execute (requires approval)
- `GET /api/v1/playbooks/library` - Get playbook library

## Integration with ChatOps

### Telegram Bot
```
Commands:
/alerts - Show current critical alerts
/risk [asset_id] - Get asset risk profile
/playbook [playbook_id] - Show playbook
/approve [playbook_id] - Approve playbook execution
```

### Discord Bot
- Embed-based alert display
- Reaction-based approval
- Thread-based discussion

## Database Schema

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed schemas.

## LLM Configuration

### Gemini Integration
```python
import google.generativeai as genai

genai.configure(api_key=os.getenv("LLM_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

response = model.generate_content(
    f"Provide security advice for: {event_summary}"
)
```

### RAG Setup
1. Store documents in ChromaDB
2. Embed using LLM or sentence-transformers
3. Retrieve top-k similar documents
4. Pass as context to LLM prompt

## Development

### Install Dependencies
```bash
cd student-3-intelligence-layer
pip install -r requirements.txt
```

### Run Locally
```bash
python main.py
```

### Environment Variables
```bash
LLM_API_KEY=your_key_here
LLM_MODEL=gemini-pro
```

### API Documentation
- Swagger UI: http://localhost:8000/docs

## Testing
```bash
pytest tests/
```

## MVP Priorities
1. Risk scoring engine (formula implementation)
2. Playbook library (3-5 core playbooks)
3. CLI command generation
4. Basic LLM integration (no RAG initially)

## Future Enhancements
- Full RAG implementation with document store
- ML-based playbook precision optimization
- Telegram/Discord bot with full ChatOps
- Approval workflow with RBAC
- Execution rollback capability
