from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles

from backend.api.chat import router as chat_router
from backend.api.rag import router as rag_router
from backend.api.reports import router as reports_router
from backend.api.sessions import router as sessions_router


app = FastAPI(
    title="Autonomous Research Agent"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://app:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    chat_router,
    prefix="/api/chat",
    tags=["Chat"]
)

app.include_router(
    rag_router,
    prefix="/api/rag",
    tags=["RAG"]
)

app.include_router(
    reports_router,
    prefix="/api/reports",
    tags=["Reports"]
)

app.include_router(
    sessions_router,
    prefix="/api/sessions",
    tags=["Sessions"]
)


@app.get("/")
async def root():
    return {
        "message": "Research Agent Running"
    }


# Serve frontend static files when present (built by Dockerfile)
frontend_dir = os.path.join(os.getcwd(), "frontend_dist")
if os.path.isdir(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")