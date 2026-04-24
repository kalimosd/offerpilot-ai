"""Files route — upload, list, download, delete."""

from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/api/files", tags=["files"])

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUTS_DIR = REPO_ROOT / "outputs"
JDS_DIR = REPO_ROOT / "jds"
VALID_SUBDIRS = {"resumes", "research", "interview", "pipeline", "misc"}


@router.post("/upload")
async def upload(file: UploadFile = File(...), target: str = "root"):
    """Upload a file. target: 'root' saves to project root, 'jds' saves to jds/."""
    if target == "jds":
        dest_dir = JDS_DIR
    else:
        dest_dir = REPO_ROOT
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / file.filename
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"path": str(dest.relative_to(REPO_ROOT)), "size": dest.stat().st_size}


@router.get("/outputs")
def list_outputs(dir: str = ""):
    """List files in outputs/ or a subdirectory."""
    if dir and dir not in VALID_SUBDIRS:
        raise HTTPException(400, f"Invalid subdirectory: {dir}")
    target = OUTPUTS_DIR / dir if dir else OUTPUTS_DIR
    if not target.is_dir():
        return {"files": []}
    files = []
    for f in sorted(target.iterdir()):
        if f.name.startswith("."):
            continue
        if f.is_dir():
            count = sum(1 for x in f.iterdir() if not x.name.startswith("."))
            files.append({"name": f.name, "type": "dir", "count": count})
        else:
            files.append({
                "name": f.name,
                "type": f.suffix.lstrip("."),
                "size": f.stat().st_size,
                "modified": f.stat().st_mtime,
            })
    return {"files": files}


@router.get("/outputs/{subdir}/{filename}")
def get_file(subdir: str, filename: str):
    """Download or preview a file."""
    if subdir not in VALID_SUBDIRS:
        raise HTTPException(400, f"Invalid subdirectory: {subdir}")
    path = OUTPUTS_DIR / subdir / filename
    if not path.exists():
        raise HTTPException(404, "File not found")
    return FileResponse(path, filename=filename)


@router.delete("/outputs/{subdir}/{filename}")
def delete_file(subdir: str, filename: str):
    """Delete a file."""
    if subdir not in VALID_SUBDIRS:
        raise HTTPException(400, f"Invalid subdirectory: {subdir}")
    path = OUTPUTS_DIR / subdir / filename
    if not path.exists():
        raise HTTPException(404, "File not found")
    path.unlink()
    return {"deleted": f"{subdir}/{filename}"}
