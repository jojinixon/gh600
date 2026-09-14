"""A minimal think -> act -> observe agent loop."""
from __future__ import annotations

from dataclasses import dataclass, field

from .llm import DEFAULT_PERSONA, LLMClient, LLMResponse
from .memory import Memory
from .tools import Tool


@dataclass
class Agent:
    llm: LLMClient
    tools: list[Tool]
    memory: Memory = field(default_factory=Memory)
    max_steps: int = 5
    persona: str = DEFAULT_PERSONA

    def _tool_by_name(self, name: str) -> Tool | None:
        return next((t for t in self.tools if t.name == name), None)

    def run(self, goal: str) -> str:
        self.memory.add("user", goal)

        for _ in range(self.max_steps):
            response: LLMResponse = self.llm.decide(
                goal=goal,
                history=self.memory.history(),
                tools=self.tools,
                persona=self.persona,
            )

            if response.tool_call is None:
                self.memory.add("assistant", response.content)
                return response.content

            tool = self._tool_by_name(response.tool_call.name)
            if tool is None:
                raise ValueError(f"Unknown tool requested: {response.tool_call.name}")

            result = tool.func(**response.tool_call.arguments)
            self.memory.add(
                "tool",
                f"{tool.name}({response.tool_call.arguments}) -> {result}",
            )

        raise RuntimeError(
            f"Agent did not reach a final answer within {self.max_steps} steps"
        )
