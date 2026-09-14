"""Run a two-agent pipeline (Researcher -> Writer) against a real model.

Usage:
    python examples/run_multi_agent.py "What is Python?"

Requires OPENROUTER_API_KEY in a .env file (copy .env.example to .env
and fill it in). Uses a free model by default.
"""
from __future__ import annotations

import sys

from dotenv import load_dotenv

from gh600.agent import Agent
from gh600.llm import OpenRouterLLM
from gh600.orchestrator import Orchestrator
from gh600.tools import RESEARCH_TOOLS


def main() -> None:
    load_dotenv()

    goal = " ".join(sys.argv[1:]) or "What is Python?"

    researcher = Agent(
        llm=OpenRouterLLM(),
        tools=RESEARCH_TOOLS,
        persona=(
            "You are a Researcher agent. Use the lookup_fact tool to gather "
            "relevant facts, then give a final answer that is just the raw "
            "facts you found, one per line."
        ),
    )
    writer = Agent(
        llm=OpenRouterLLM(),
        tools=[],
        persona=(
            "You are a Writer agent. You never call tools - you only write. "
            "Turn the research notes you're given into one clear, "
            "well-written final answer."
        ),
    )
    orchestrator = Orchestrator(researcher=researcher, writer=writer)

    result = orchestrator.run(goal)

    print(f"Goal: {goal}\n")
    print("--- researcher steps ---")
    for role, content in researcher.memory.history():
        print(f"[{role}] {content}")
    print("\n--- writer steps ---")
    for role, content in writer.memory.history():
        print(f"[{role}] {content}")
    print(f"\nFinal answer: {result}")


if __name__ == "__main__":
    main()
