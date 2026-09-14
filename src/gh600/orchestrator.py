"""A minimal multi-agent orchestrator.

Chains two specialized agents together: a Researcher that gathers
facts with tools, and a Writer that turns those facts into a final
answer. This is the simplest possible multi-agent pattern -- a fixed
sequential handoff -- as a starting point for more elaborate
orchestration (routing, parallel agents, debate, ...) later in the
course.
"""
from __future__ import annotations

from dataclasses import dataclass

from .agent import Agent


@dataclass
class Orchestrator:
    researcher: Agent
    writer: Agent

    def run(self, goal: str) -> str:
        notes = self.researcher.run(goal)
        return self.writer.run(
            f"Question: {goal}\n\nResearch notes:\n{notes}\n\n"
            "Write a clear final answer using only these notes."
        )
