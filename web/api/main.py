"""OfferPilot Web API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import chat, tracker, files

app = FastAPI(title="OfferPilot API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(tracker.router)
app.include_router(files.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
