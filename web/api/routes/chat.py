"""Chat route — SSE streaming agent conversation."""

from __future__ import annotations

import json

from fastapi import APIRouter
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage

from offerpilot.graph import build_graph, SYSTEM_PROMPT

router = APIRouter(prefix="/api/chat", tags=["chat"])

_graph = None


def _get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


@router.post("")
async def chat(req: ChatRequest):
    """Stream agent response via SSE."""

    def _to_lc_message(msg: dict):
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role == "user":
            return HumanMessage(content=content)
        if role == "assistant":
            return AIMessage(content=content)
        return HumanMessage(content=content)

    async def event_stream():
        graph = _get_graph()
        messages = [_to_lc_message(m) for m in req.history]
        messages.append(HumanMessage(content=req.message))

        result = graph.invoke({"messages": messages})

        for msg in result["messages"]:
            if isinstance(msg, SystemMessage):
                continue
            if isinstance(msg, HumanMessage):
                continue
            if isinstance(msg, AIMessage):
                if msg.tool_calls:
                    for tc in msg.tool_calls:
                        yield {"event": "tool_call", "data": json.dumps(
                            {"name": tc["name"], "args": {k: v for k, v in tc["args"].items() if k != "content"}},
                            ensure_ascii=False,
                        )}
                elif msg.content:
                    yield {"event": "token", "data": json.dumps(
                        {"content": msg.content}, ensure_ascii=False,
                    )}
            if isinstance(msg, ToolMessage):
                yield {"event": "tool_result", "data": json.dumps(
                    {"name": msg.name, "result": msg.content[:2000]}, ensure_ascii=False,
                )}

        yield {"event": "done", "data": "{}"}

    return EventSourceResponse(event_stream())
