# Deployment Guide

## Quick Start

### Prerequisites
- Docker & Docker Compose (v2.0+)
- 4GB RAM minimum
- 20GB disk space (for databases and threat intel)
- Internet connection (for initial downloads)

### Step 1: Clone & Configure
```bash
git clone <repo> && cd project-sentinel
cp .env.example .env

# Edit .env with your settings
nano .env
```

**Key configurations:**
- `POSTGRES_PASSWORD` - Set secure password!
- `LLM_API_KEY` - Your Gemini/GPT-4 API key
- `LLM_MODEL` - Preferred LLM (gemini-pro, gpt-4, claude-3-opus)

### Step 2: Start the Stack
```bash
docker-compose up -d
```

Watch logs:
```bash
docker-compose logs -f
```

### Step 3: Verify Health
```bash
curl http://localhost:8001/health  # Student 1
curl http://localhost:8002/health  # Student 2
curl http://localhost:8003/health  # Student 3
curl http://localhost:3000          # Frontend
```

**Expected responses:**
```json
{
  "status": "healthy",
  "service": "Student X - ...",
  "timestamp": "2026-03-18T..."
}
```

### Step 4: Access Dashboard
- Frontend: **http://localhost:3000**
- Student 1 API Docs: http://localhost:8001/docs
- Student 2 API Docs: http://localhost:8002/docs
- Student 3 API Docs: http://localhost:8003/docs

---

## Database Setup

### Initial Schema Creation
PostgreSQL automatically runs init scripts from `infra/postgres/init-scripts/`:

1. Create tables for events, assets, SBOM
2. Create views for dashboard queries
3. Create indexes for performance

Run migrations:
```bash
docker-compose exec postgres psql -U sentinel_user -d sentinel -c "\dt"
```

### Backup & Restore
```bash
# Backup
docker-compose exec postgres pg_dump -U sentinel_user sentinel > backup.sql

# Restore
docker-compose exec postgres psql -U sentinel_user sentinel < backup.sql
```

---

## GeoIP Data Setup

### Download MaxMind
1. Register at https://www.maxmind.com (free GeoLite2)
2. Download `GeoLite2-City.mmdb`
3. Place in `infra/geoip-db/GeoLite2-City.mmdb`

### Alternative: Use Free IP2Location
See `infra/geoip-db/README.md`

---

## Threat Intelligence Setup

### MyCERT STIX Feed
1. Register at https://cti.mycert.org.my/
2. Get STIX/TAXII feed URL
3. Update `.env`:
   ```
   CTI_STIX_FEED_URL=https://cti.mycert.org.my/stix/feed
   ```

### Other OSINT Sources
- AlienVault OTX: https://otx.alienvault.com/
- MISP: https://www.misp-project.org/
- Custom feeds via TAXII

---

## Production Deployment

### Prerequisites
- Kubernetes cluster (EKS, AKS, GKE, on-prem)
- Persistent storage (EBS, Azure Disk, NFS)
- Load balancer
- Monitoring (Prometheus, Grafana)

### Helm Chart (Coming Soon)
```bash
helm install sentinel ./helm-sentinel \
  --namespace security \
  --values values.yaml
```

### Environment Scaling
```yaml
# Increase resources
POSTGRES_MAX_CONNECTIONS=200
STUDENT1_WORKERS=4  # FastAPI workers
STUDENT2_WORKERS=4
STUDENT3_WORKERS=4
REDIS_MAXMEMORY=2gb
```

### Backup Strategy
- Daily PostgreSQL backups to S3
- Weekly full system snapshots
- Keep 30-day retention

### Security Hardening
```bash
# Use secrets management
kubectl create secret generic sentinel-secrets \
  --from-literal=db_password=xxx \
  --from-literal=llm_api_key=xxx

# Network policies
kubectl apply -f network-policies.yaml

# RBAC roles
kubectl apply -f rbac-roles.yaml
```

---

## Monitoring & Alerts

### Prometheus Metrics
Student services expose `/metrics` endpoint:
```bash
curl http://localhost:8001/metrics
```

**Key metrics:**
- `sentinel_events_total` - Total events ingested
- `sentinel_risk_score_current` - Current risk scores
- `sentinel_api_request_duration_ms` - API latency
- `sentinel_db_connection_pool` - DB connection usage

### Grafana Dashboards
1. Add Prometheus data source
2. Import dashboards from `infra/grafana/dashboards/`
3. View: http://localhost:3001

### Alert Rules
Edit `infra/prometheus/rules.yml`:
```yaml
- alert: HighRiskScore
  expr: sentinel_risk_score_current > 80
  for: 5m
  annotations:
    summary: "Critical risk detected: {{ $value }}"
```

---

## Troubleshooting

### Services Won't Start
```bash
# Check logs
docker-compose logs student-1-event-collector

# Verify network
docker network ls
docker network inspect sentinel

# Rebuild images
docker-compose build --no-cache
```

### Database Connection Issues
```bash
# Check PostgreSQL
docker-compose exec postgres psql -U sentinel_user -c "SELECT 1"

# Reset DB (careful!)
docker-compose down -v
docker-compose up -d
```

### Out of Disk Space
```bash
# Clean up Docker storage
docker system prune -a

# Migrate to larger volume
docker-compose down
# Manually copy postgres_data volume
docker-compose up -d
```

### LLM API Errors
```bash
# Test API key
curl -H "Authorization: Bearer $LLM_API_KEY" \
  https://generativelanguage.googleapis.com/v1/models/gemini-pro

# Update .env with correct key
```

---

## Maintenance

### Regular Tasks
- **Daily**: Check logs, verify health checks
- **Weekly**: Review alerts, update threat feeds
- **Monthly**: Analyze metrics, capacity planning
- **Quarterly**: Security patches, dependency updates

### Getting Help
- 📧 Email: sentinel@yourdomain.my
- 🐛 GitHub Issues: [Report a bug](#)
- 💬 Discord: [Join community](#)

---

## Next Steps
1. Initialize first assets in Student 1
2. Configure threat feeds in Student 2
3. Test LLM integration in Student 3
4. Create custom playbooks for your environment
5. Set up ChatOps bot
