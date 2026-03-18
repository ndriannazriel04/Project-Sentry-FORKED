"""Discovery Module - Hybrid asset discovery (Nmap + PCAP)"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok", "module": "discovery"}

@router.post("/scan")
async def start_scan(network: str):
    """
    Start a hybrid network discovery scan
    
    Active: Nmap scan | Passive: PCAP sniffing
    """
    return {"status": "scan_started", "network": network, "scan_id": "scan_123"}

@router.get("/scan/{scan_id}")
async def get_scan_status(scan_id: str):
    """Get scan results"""
    return {"scan_id": scan_id, "status": "in_progress", "assets": []}

@router.get("/assets")
async def list_assets():
    """List discovered assets"""
    return {"assets": [], "total": 0}
