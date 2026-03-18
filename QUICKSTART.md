# Project Sentinel - Quick Start Guide

## 🚀 Welcome to Project Sentinel!

This guide will get you up and running in 5 minutes.

---

## Step 1: Clone & Navigate
```bash
cd c:\Users\User\Desktop\Sentry\project-sentinel
```

## Step 2: Create Environment File
```bash
cp .env.example .env
```

**Edit `.env` with:**
- `POSTGRES_PASSWORD`: Choose a secure password
- `LLM_API_KEY`: Your Google Gemini or OpenAI API key (optional for MVP)
- `LLM_MODEL`: `gemini-pro` (default)

## Step 3: Start All Services
```bash
docker-compose up -d
```

**What's starting:**
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- Student 1: Input Layer (port 8001)
- Student 2: Enrichment Layer (port 8002)
- Student 3: Intelligence Layer (port 8003)
- React Frontend (port 3000)

## Step 4: Wait for Health Checks
```bash
# Monitor startup progress
docker-compose logs -f
```

**All services healthy?** Check:
```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "Student X - ...",
  "timestamp": "2026-03-18T..."
}
```

## Step 5: Access Dashboard
**Open your browser:**
- **Frontend Dashboard**: http://localhost:3000
- **Student 1 API Docs**: http://localhost:8001/docs
- **Student 2 API Docs**: http://localhost:8002/docs
- **Student 3 API Docs**: http://localhost:8003/docs

---

## First Steps: Testing the Platform

### 1. Add an Asset (Student 1)
```bash
curl -X POST http://localhost:8001/api/v1/discovery/assets \
  -H "Content-Type: application/json" \
  -d '{
    "name": "web-server-01",
    "ip_address": "192.168.1.100",
    "hostname": "web-server-01.local",
    "os_type": "Ubuntu Linux",
    "asset_criticality": 8
  }'
```

### 2. Ingest a Test Event (Student 1)
```bash
curl -X POST http://localhost:8001/api/v1/events/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": "<asset_id_from_step_1>",
    "event_type": "Auth",
    "source_ip": "203.0.113.5",
    "user_id": "admin",
    "action": "login",
    "status": "success"
  }'
```

### 3. Check Geolocation (Student 2)
```bash
curl -X POST http://localhost:8002/api/v1/geo/check-location \
  -H "Content-Type: application/json" \
  -d '{"ip": "203.0.113.5"}'
```

### 4. Map to MITRE ATT&CK (Student 2)
```bash
curl -X POST http://localhost:8002/api/v1/mitre/map-event \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "Auth",
    "action": "bruteforce",
    "count": 50
  }'
```

### 5. Calculate Risk Score (Student 3)
```bash
curl -X POST http://localhost:8003/api/v1/risk/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "Auth",
    "event_severity": 7,
    "asset_criticality": 8
  }'
```

---

## 📊 Database Access

### Connect to PostgreSQL
```bash
docker-compose exec postgres psql -U sentinel_user -d sentinel
```

**Useful queries:**
```sql
-- List all assets
SELECT name, ip_address, asset_criticality FROM assets;

-- Recent events
SELECT event_type, action, status, created_at FROM events ORDER BY created_at DESC LIMIT 10;

-- Risk assessment summary
SELECT risk_level, COUNT(*) FROM risk_assessments GROUP BY risk_level;
```

---

## 📝 File Structure Cheat Sheet

```
project-sentinel/
├── docker-compose.yml          ← Start everything here
├── .env.example                ← Copy to .env
├── docker/                     ← Dockerfiles for each service
├── student-1-input-layer/      ← Raw event collection
├── student-2-enrichment-layer/ ← Context & correlation
├── student-3-intelligence-layer/← Risk scoring & AI
├── frontend/                   ← React dashboard
├── infra/                      ← Databases, configs, data
└── docs/                       ← Full documentation
```

---

## 🛠️ Useful Commands

### View Logs
```bash
docker-compose logs -f student-1-event-collector
docker-compose logs -f student-2-enrichment
docker-compose logs -f student-3-intelligence
```

### Restart a Service
```bash
docker-compose restart student-1-event-collector
```

### Stop Everything
```bash
docker-compose down
```

### Full Reset (careful!)
```bash
docker-compose down -v  # -v removes volumes (database)
docker-compose up -d
```

### Check Resource Usage
```bash
docker stats
```

---

## 🐛 Troubleshooting

### Service Won't Start?
1. Check logs: `docker-compose logs <service_name>`
2. Verify disk space: `docker system df`
3. Rebuild: `docker-compose build --no-cache <service_name>`

### Database Connection Error?
```bash
# Verify PostgreSQL is healthy
docker-compose exec postgres pg_isready

# Reset database
docker-compose down -v && docker-compose up -d postgres
```

### Port Already in Use?
Change ports in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Change first number to 8011:8000
```

### LLM API Errors?
- Verify API key in `.env`
- Test with curl: `curl https://generativelanguage.googleapis.com/v1/models/gemini-pro`

---

## 📚 Next: Read Full Documentation

- [Architecture](./docs/ARCHITECTURE.md) - System design & data flow
- [Student 1 Guide](./docs/STUDENT1_README.md) - Input layer details
- [Student 2 Guide](./docs/STUDENT2_README.md) - Enrichment layer details
- [Student 3 Guide](./docs/STUDENT3_README.md) - Intelligence layer details
- [Deployment](./docs/DEPLOYMENT.md) - Production setup

---

## 🎯 MVP Goals (First Sprint)

- [ ] Events ingestion API working
- [ ] Asset inventory populated
- [ ] SBOM generation from sample asset
- [ ] GeoIP enrichment enabled
- [ ] Basic risk scoring functioning
- [ ] Dashboard displaying alerts

---

## 💡 Pro Tips

1. **Use API docs**: Swagger is your friend (http://localhost:8000/docs)
2. **Monitor database**: `SELECT * FROM events ORDER BY created_at DESC;`
3. **Check performance**: View Docker metrics with `docker stats`
4. **Backup early**: `docker-compose exec postgres pg_dump ...` before changes
5. **Test incrementally**: Add one asset, ingest events, check enrichment

---

## 🆘 Need Help?

- Check the relevant `STUDENT*_README.md`
- Review `docs/DEPLOYMENT.md` for production setup
- Check GitHub Issues for similar problems
- Review logs: `docker-compose logs`

---

**Happy Sentrying! 🛡️**

Next step: Read [ARCHITECTURE.md](./docs/ARCHITECTURE.md) to understand how everything works.
