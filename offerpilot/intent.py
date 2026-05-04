"""Intent parsing for OfferPilot agent routing."""

from __future__ import annotations

import re
from typing import Any

PIPELINE_KEYWORDS = (
    "pipeline",
    "auto-pipeline",
    "扫描并推荐",
    "扫描→排序",
    "扫描->排序",
    "全自动",
)
BATCH_EVAL_KEYWORDS = (
    "batch evaluate",
    "batch-evaluate",
    "批量评估",
    "evaluate all",
    "评估所有",
    "全部评估",
)

DEFAULT_PIPELINE_CONFIG = "portals_cn.yml"
DEFAULT_PIPELINE_DAYS = 7
DEFAULT_PIPELINE_TOP_N = 10
DEFAULT_PROFILE_PATH = "profile_store.yaml"


def classify_user_intent(content: str) -> dict[str, Any]:
    """Classify a user request into graph routing fields."""
    normalized = content.lower()

    if _is_pipeline_request(normalized):
        return {
            "task_type": "pipeline",
            "pipeline_config": DEFAULT_PIPELINE_CONFIG,
            "pipeline_days": _parse_days(normalized),
            "pipeline_top_n": _parse_top_n(normalized),
            "pipeline_cn_focus": _has_cn_focus(normalized),
        }
    if any(keyword in normalized for keyword in BATCH_EVAL_KEYWORDS):
        return {"task_type": "batch_evaluate", "batch_profile_path": DEFAULT_PROFILE_PATH}

    return {"task_type": "general"}


def _is_pipeline_request(content: str) -> bool:
    if any(keyword in content for keyword in PIPELINE_KEYWORDS):
        return True

    has_scan = "扫描" in content or "scan" in content
    has_rank_or_recommend = any(word in content for word in ("推荐", "排序", "rank", "recommend"))
    return has_scan and has_rank_or_recommend


def _parse_days(content: str) -> int:
    patterns = (
        r"(?:最近|近|last)\s*(\d{1,3})\s*(?:天|day|days)",
        r"(\d{1,3})\s*(?:天|day|days)",
    )
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return max(1, int(match.group(1)))
    return DEFAULT_PIPELINE_DAYS


def _parse_top_n(content: str) -> int:
    patterns = (
        r"(?:前|top)\s*(\d{1,3})\s*(?:个|条|岗位|jobs?)?",
        r"推荐\s*(\d{1,3})\s*(?:个|条|岗位|jobs?)",
    )
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return max(1, int(match.group(1)))
    return DEFAULT_PIPELINE_TOP_N


def _has_cn_focus(content: str) -> bool:
    return any(word in content for word in ("国内", "中国", "cn", "china", "中文"))
