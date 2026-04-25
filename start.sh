#!/bin/bash
# OfferPilot Web UI — one command to start both backend and frontend

DIR="$(cd "$(dirname "$0")" && pwd)"

cleanup() {
  kill $API_PID $WEB_PID 2>/dev/null
  exit 0
}
trap cleanup INT TERM

echo "🚀 Starting OfferPilot Web UI..."

# Backend
cd "$DIR"
.venv/bin/uvicorn web.api.main:app --port 8000 &
API_PID=$!

# Frontend
cd "$DIR/web/frontend"
npm run dev -- --port 3000 &
WEB_PID=$!

echo ""
echo "✅ Backend:  http://localhost:8000"
echo "✅ Frontend: http://localhost:3000"
echo "   Press Ctrl+C to stop both"
echo ""

wait
