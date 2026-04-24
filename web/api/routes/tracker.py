"""Tracker route — application status CRUD."""

from __future__ import annotations

from fastapi import APIRouter, Query
from pydantic import BaseModel

from offerpilot.tools import tracker_add, tracker_update, tracker_query, check_followups

router = APIRouter(prefix="/api/tracker", tags=["tracker"])


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
    result = tracker_query.invoke({"status": status, "company": company, "days": days})
    return {"result": result}


@router.post("")
def add(req: TrackerAddRequest):
    result = tracker_add.invoke(req.model_dump())
    return {"result": result}


@router.patch("")
def update(req: TrackerUpdateRequest):
    result = tracker_update.invoke(req.model_dump())
    return {"result": result}


@router.get("/followups")
def followups():
    result = check_followups.invoke({})
    return {"result": result}
