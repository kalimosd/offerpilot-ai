# OfferPilot Web UI

Next.js frontend + FastAPI backend.

## Setup

```bash
# 1. Install backend dependencies (from project root)
pip install -e .
pip install fastapi uvicorn sse-starlette python-multipart

# 2. Install frontend dependencies
cd web/frontend
npm install

# 3. Configure .env (project root)
# Same as CLI agent — set OFFERPILOT_MODEL, API keys, etc.
```

## Run

```bash
# Terminal 1: Backend (from project root)
uvicorn web.api.main:app --reload --port 8000

# Terminal 2: Frontend
cd web/frontend
npm run dev
```

Open http://localhost:3000

## Pages

- **Chat** (`/`) — Conversational agent interface with file upload
- **Tracker** (`/tracker`) — Application status tracking with follow-up reminders
- **Outputs** (`/outputs`) — Browse and preview generated files
