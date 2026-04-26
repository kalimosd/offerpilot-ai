"""OfferPilot Agent — LangGraph-powered CLI agent for career workflows."""

from __future__ import annotations

import sys

from langchain_core.messages import HumanMessage

from .graph import build_graph


def run_agent(user_input: str) -> None:
    """Run the agent with a single user input."""
    graph = build_graph()
    result = graph.invoke({"messages": [HumanMessage(content=user_input)]}, {"recursion_limit": 30})
    last = result["messages"][-1]
    print(f"\n{last.content}")


def run_interactive() -> None:
    """Run the agent in multi-turn interactive mode."""
    print("🚀 OfferPilot Agent（输入 exit 退出）\n")
    graph = build_graph()
    messages = []

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 再见")
            break
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "q"):
            print("👋 再见")
            break

        messages.append(HumanMessage(content=user_input))
        result = graph.invoke({"messages": messages}, {"recursion_limit": 30})
        messages = result["messages"]
        last = messages[-1]
        print(f"\n{last.content}\n")


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) >= 2:
        user_input = " ".join(sys.argv[1:])
        print(f"🚀 OfferPilot Agent\n📝 任务: {user_input}\n")
        run_agent(user_input)
    else:
        run_interactive()


if __name__ == "__main__":
    main()
