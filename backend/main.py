"""
FastAPI application entry point for Autonomous Research Agent.

Provides:
- REST API endpoints for chat, RAG, reports, and sessions
- CORS middleware
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.chat import router as chat_router
from backend.api.rag import router as rag_router
from backend.api.reports import router as reports_router
from backend.api.sessions import router as sessions_router
from backend.core.logger import logger

app = FastAPI(
    title="Autonomous Research Agent",
    description="AI-powered research platform with multi-source integration",
)

# ============================================================================
# CORS
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# API Routes
# ============================================================================

app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])
app.include_router(rag_router, prefix="/api/rag", tags=["RAG"])
app.include_router(reports_router, prefix="/api/reports", tags=["Reports"])
app.include_router(sessions_router, prefix="/api/sessions", tags=["Sessions"])

# ============================================================================
# Health Check
# ============================================================================

@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "ok",
        "message": "Research Agent Running",
    }

# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Research Agent Running",
        "docs": "/docs",
        "health": "/health",
    }