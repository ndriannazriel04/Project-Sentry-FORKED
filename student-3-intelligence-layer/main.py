"""
Student 3: Intelligence Layer - Risk Scoring & AI Advisory
Primary responsibility: Provide strategic risk assessment and prescriptive guidance
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
from src.risk_engine import router as risk_router
from src.ai_advisor import router as advisor_router
from src.playbook_engine import router as playbook_router

# Lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Student 3: Intelligence Layer starting...")
    logger.info("Initializing risk engine, AI advisor, and playbook generator...")
    yield
    # Shutdown
    logger.info("🛑 Student 3: Intelligence Layer shutting down...")

# Create app
app = FastAPI(
    title="Sentinel - Student 3: Intelligence Layer",
    description="Risk scoring and AI-powered advisory service",
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
app.include_router(risk_router.router, prefix="/api/v1/risk", tags=["Risk Engine"])
app.include_router(advisor_router.router, prefix="/api/v1/advisor", tags=["AI Advisor"])
app.include_router(playbook_router.router, prefix="/api/v1/playbooks", tags=["Playbooks"])

# Health check
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Student 3 - Intelligence Layer",
        "timestamp": datetime.utcnow().isoformat()
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Project Sentinel - Student 3 (Intelligence Layer)",
        "endpoints": {
            "health": "/health",
            "risk": "/api/v1/risk",
            "advisor": "/api/v1/advisor",
            "playbooks": "/api/v1/playbooks"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
