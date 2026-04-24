"""Tracker route — application status CRUD."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/tracker", tags=["tracker"])


def _tools():
    from offerpilot.tools import tracker_add, tracker_update, tracker_query, check_followups
    return tracker_add, tracker_update, tracker_query, check_followups


class TrackerAddRequest(BaseModel):
    url: str
    company: str
    title: str
    status: str = "discovered"
    notes: str = ""


class TrackerUpdateRequest(BaseModel):
    url: str
    status: str
    notes: str = ""


@router.get("")
def query(status: str = "", company: str = "", days: int = 0):
    _, _, tracker_query, _ = _tools()
    result = tracker_query.invoke({"status": status, "company": company, "days": days})
    return {"result": result}


@router.post("")
def add(req: TrackerAddRequest):
    tracker_add, _, _, _ = _tools()
    result = tracker_add.invoke(req.model_dump())
    return {"result": result}


@router.patch("")
def update(req: TrackerUpdateRequest):
    _, tracker_update, _, _ = _tools()
    result = tracker_update.invoke(req.model_dump())
    return {"result": result}


@router.get("/followups")
def followups():
    _, _, _, check_followups = _tools()
    result = check_followups.invoke({})
    return {"result": result}
