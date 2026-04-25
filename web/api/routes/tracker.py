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


class TrackerEditRequest(BaseModel):
    """Edit any field of a tracker row, identified by original URL."""
    original_url: str
    url: str | None = None
    company: str | None = None
    title: str | None = None
    status: str | None = None
    notes: str | None = None


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


@router.put("")
def edit(req: TrackerEditRequest):
    """Edit any field of a tracker row."""
    import csv
    from datetime import datetime
    from pathlib import Path
    tracker_file = Path(__file__).resolve().parents[3] / "data" / "tracker.tsv"
    if not tracker_file.exists():
        return {"result": "错误：tracker 文件不存在"}
    fields = ["url", "company", "title", "status", "applied_date", "last_update", "notes"]
    rows = []
    updated = False
    with open(tracker_file, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if row["url"].strip() == req.original_url.strip():
                if req.url is not None:
                    row["url"] = req.url
                if req.company is not None:
                    row["company"] = req.company
                if req.title is not None:
                    row["title"] = req.title
                if req.status is not None:
                    row["status"] = req.status
                if req.notes is not None:
                    row["notes"] = req.notes
                row["last_update"] = datetime.now().strftime("%Y-%m-%d")
                updated = True
            rows.append(row)
    if not updated:
        return {"result": f"错误：未找到 URL {req.original_url}"}
    with open(tracker_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    return {"result": "已更新"}
