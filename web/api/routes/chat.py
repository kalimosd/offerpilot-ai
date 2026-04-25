"""Chat route — SSE streaming agent conversation."""

from __future__ import annotations

import json

from fastapi import APIRouter
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

router = APIRouter(prefix="/api/chat", tags=["chat"])

_graph = None


def _get_graph():
    global _graph
    if _graph is None:
        from offerpilot.graph import build_graph
        _graph = build_graph()
    return _graph


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


@router.post("")
async def chat(req: ChatRequest):
    """Stream agent response via SSE using graph.stream()."""

    def _to_lc_message(msg: dict):
        from langchain_core.messages import HumanMessage, AIMessage
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role == "user":
            return HumanMessage(content=content)
        if role == "assistant":
            return AIMessage(content=content)
        return HumanMessage(content=content)

    async def event_stream():
        from langchain_core.messages import AIMessage, ToolMessage
        graph = _get_graph()
        messages = [_to_lc_message(m) for m in req.history]
        from langchain_core.messages import HumanMessage
        messages.append(HumanMessage(content=req.message))

        for event in graph.stream({"messages": messages}, stream_mode="updates"):
            for node_name, node_output in event.items():
                for msg in node_output.get("messages", []):
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
                    elif isinstance(msg, ToolMessage):
                        yield {"event": "tool_result", "data": json.dumps(
                            {"name": msg.name, "result": msg.content[:2000]}, ensure_ascii=False,
                        )}

        yield {"event": "done", "data": "{}"}

    return EventSourceResponse(event_stream())
