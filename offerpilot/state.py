"""LangGraph state definition."""

from __future__ import annotations

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    task_type: str                        # "pipeline" | "batch_evaluate" | "general"
    pipeline_config: str                  # portal config YAML path
    pipeline_days: int                    # scan time window (days)
    pipeline_top_n: int                   # number of recommendations
    pipeline_cn_focus: bool               # boost Chinese companies
    batch_jd_paths: list[str]             # JD file paths for batch evaluate
    batch_profile_path: str               # profile store path for batch evaluate
