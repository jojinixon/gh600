"""Run the agent against a real model through OpenRouter.

Usage:
    python examples/run_agent.py "What is 12 + 30?"

Requires OPENROUTER_API_KEY in a .env file (copy .env.example to .env
and fill it in). Uses a free model by default.
"""
from __future__ import annotations

import sys

from dotenv import load_dotenv

from gh600.agent import Agent
from gh600.llm import OpenRouterLLM
from gh600.tools import DEFAULT_TOOLS


def main() -> None:
    load_dotenv()

    goal = " ".join(sys.argv[1:]) or "What is 12 + 30?"
    agent = Agent(llm=OpenRouterLLM(), tools=DEFAULT_TOOLS)

    result = agent.run(goal)

    print(f"Goal: {goal}")
    print(f"Answer: {result}")
    print("\n--- steps ---")
    for role, content in agent.memory.history():
        print(f"[{role}] {content}")


if __name__ == "__main__":
    main()
