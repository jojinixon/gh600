"""LLM client abstraction.

`LLMClient` is the interface the agent talks to. `FakeLLM` is a
deterministic, offline stand-in used in tests and while learning the
agent loop. Swap in a real provider (GitHub Models, Azure OpenAI,
OpenAI, ...) once a lesson introduces one, by writing a class that
implements `decide` the same way.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any, Protocol

import requests

from .tools import Tool


@dataclass
class ToolCall:
    name: str
    arguments: dict[str, Any]


@dataclass
class LLMResponse:
    content: str
    tool_call: ToolCall | None = None


DEFAULT_PERSONA = "You are a helpful agent that solves the user's goal, using tools when useful."


class LLMClient(Protocol):
    def decide(
        self,
        goal: str,
        history: list[tuple[str, str]],
        tools: list[Tool],
        persona: str = DEFAULT_PERSONA,
    ) -> LLMResponse: ...


class FakeLLM:
    """A scripted LLM for tests and offline experimentation.

    Give it a list of responses up front; it returns them in order,
    one per `decide` call, so agent behavior is fully predictable.
    """

    def __init__(self, script: list[LLMResponse]):
        self._script = list(script)

    def decide(
        self,
        goal: str,
        history: list[tuple[str, str]],
        tools: list[Tool],
        persona: str = DEFAULT_PERSONA,
    ) -> LLMResponse:
        if not self._script:
            raise RuntimeError("FakeLLM script exhausted")
        return self._script.pop(0)


class OpenRouterLLM:
    """Calls a real model through OpenRouter's chat completions API.

    Needs `OPENROUTER_API_KEY` (see `.env.example`). Defaults to a free
    model so you can run this without spending anything; override with
    `OPENROUTER_MODEL` or the constructor argument.

    Since OpenRouter's free models don't support OpenAI-style tool
    calling, the agent's tool menu is described in the system prompt
    and the model is asked to reply with one JSON object -- either a
    tool call or a final answer -- which is parsed back into an
    `LLMResponse`.
    """

    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    DEFAULT_MODEL = "nex-agi/nex-n2.5-mini:free"

    SYSTEM_PROMPT = (
        "{persona}\n\n"
        "You can either call one tool or give a final answer.\n\n"
        "Available tools:\n{tool_list}\n\n"
        "Respond with EXACTLY one JSON object and nothing else:\n"
        '- To call a tool: {{"tool": "<name>", "arguments": {{...}}}}\n'
        '- To give a final answer: {{"answer": "<your answer>"}}'
    )

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY is not set (copy .env.example to .env and fill it in)"
            )
        self.model = model or os.environ.get("OPENROUTER_MODEL", self.DEFAULT_MODEL)

    def decide(
        self,
        goal: str,
        history: list[tuple[str, str]],
        tools: list[Tool],
        persona: str = DEFAULT_PERSONA,
    ) -> LLMResponse:
        tool_list = "\n".join(f"- {t.name}: {t.description}" for t in tools) or "(none)"
        messages = [
            {
                "role": "system",
                "content": self.SYSTEM_PROMPT.format(persona=persona, tool_list=tool_list),
            }
        ]
        for role, content in history:
            messages.append(
                {"role": "user" if role == "user" else "assistant", "content": content}
            )

        response = requests.post(
            self.API_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={"model": self.model, "messages": messages},
            timeout=30,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return self._parse(content)

    # Small free models sometimes leak a raw stop/end token (e.g.
    # "<CPA_DONE>", "<|endoftext|>") into the visible text instead of
    # having it swallowed by the API, so it has to be stripped here.
    _SPECIAL_TOKEN_RE = re.compile(r"\s*<[^<>\s]{1,40}>\s*")

    @classmethod
    def _strip_special_tokens(cls, text: str) -> str:
        return cls._SPECIAL_TOKEN_RE.sub(" ", text).strip()

    @classmethod
    def _parse(cls, content: str) -> LLMResponse:
        content = cls._strip_special_tokens(content)
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            return LLMResponse(content=content)

        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return LLMResponse(content=content)

        if "tool" in data:
            return LLMResponse(
                content="",
                tool_call=ToolCall(name=data["tool"], arguments=data.get("arguments", {})),
            )
        return LLMResponse(content=cls._strip_special_tokens(data.get("answer", content)))
