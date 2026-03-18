"""
Student 2: Enrichment Layer - Context & Behavioral Analysis
Primary responsibility: Transform raw events into business-actionable intelligence
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import routers
from src.geo_engine import router as geo_router
from src.cti_pipelines import router as cti_router
from src.mitre_mapper import router as mitre_router
from src.trend_analysis import router as trend_router

# Lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Student 2: Enrichment Layer starting...")
    logger.info("Initializing GeoIP engine, CTI pipelines, MITRE mapper, and trend analysis...")
    yield
    # Shutdown
    logger.info("🛑 Student 2: Enrichment Layer shutting down...")

# Create app
app = FastAPI(
    title="Sentinel - Student 2: Enrichment Layer",
    description="Context enrichment & behavioral analysis service",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(geo_router.router, prefix="/api/v1/geo", tags=["GeoIP"])
app.include_router(cti_router.router, prefix="/api/v1/cti", tags=["CTI"])
app.include_router(mitre_router.router, prefix="/api/v1/mitre", tags=["MITRE ATT&CK"])
app.include_router(trend_router.router, prefix="/api/v1/trends", tags=["Trend Analysis"])

# Health check
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Student 2 - Enrichment Layer",
        "timestamp": datetime.utcnow().isoformat()
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Project Sentinel - Student 2 (Enrichment Layer)",
        "endpoints": {
            "health": "/health",
            "geo": "/api/v1/geo",
            "cti": "/api/v1/cti",
            "mitre": "/api/v1/mitre",
            "trends": "/api/v1/trends"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
