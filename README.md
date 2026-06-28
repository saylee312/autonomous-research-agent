# Autonomous Research Agent — monorepo

This repository contains a FastAPI backend and a Vite-based frontend in a single monorepo and includes Docker configuration to build both together and serve the built frontend from the backend.

Quick start (Docker):

1. Build and run with Docker Compose:

```bash
docker compose build --pull --no-cache
docker compose up -d
```

2. Open the app at: http://localhost:8000 (API under `/api/*`, frontend served at `/`)

Developer (local) — backend only:

```bash
python -m venv .venv
source .venv/bin/activate    # or .\\.venv\\Scripts\\activate on Windows
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Developer (local) — frontend only:

```bash
cd frontend
npm install
npm run dev
```

Files added/changed
- `Dockerfile` — multi-stage build: builds frontend then installs Python dependencies and runs the backend.
- `docker-compose.yml` — builds and runs the combined image, exposing port 8000.
- `backend/main.py` — now mounts `frontend_dist/` when present so the built frontend is served by the backend.
- `requirements.txt` — appended `aiofiles` to support static file serving.
- `.dockerignore` and `.gitignore`

Notes and remaining work
- Native system dependencies: several Python packages used in the project (for example `pymupdf`, `camelot`, `easyocr`, and some PDF/image tools) require additional OS packages and runtime libraries. The Dockerfile installs a common set, but you may need to add distribution-specific packages for full feature parity.
- If you want a lighter production image, consider using `pip wheel` caching, multi-stage Python builds, or a specialized base image with required native libraries preinstalled.
- Secrets and environment configuration: Add a `.env` or use your orchestration system to provide environment variables (API keys, DB URIs, etc.). Do NOT commit secrets to Git.

If you'd like, I can:
- run a quick static check and mark the todo items complete,
- update `requirements.txt` to pin additional packages or add a `constraints.txt`, or
- produce a production-ready multi-stage Python image that installs all native libraries required by heavy packages.
