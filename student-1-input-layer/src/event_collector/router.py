"""Event Collector Module - FastAPI based event ingestion"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok", "module": "event-collector"}

@router.post("/ingest")
async def ingest_event(event: dict):
    """
    Ingest a security event
    
    Event types: Auth, Access, Admin, System
    """
    return {"status": "received", "event": event}

@router.get("/")
async def list_events():
    """List all ingested events"""
    return {"events": [], "total": 0}
