"""Tools an agent can call.

Each tool is a plain Python function wrapped with a name and
description so a language model can decide when to use it.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Tool:
    name: str
    description: str
    func: Callable[..., Any]


def add(a: float, b: float) -> float:
    return a + b


def get_word_length(word: str) -> int:
    return len(word)


DEFAULT_TOOLS = [
    Tool(name="add", description="Add two numbers together.", func=add),
    Tool(
        name="get_word_length",
        description="Return the number of characters in a word.",
        func=get_word_length,
    ),
]

_FACTS = {
    "python": "Python is a high-level, interpreted programming language created by Guido van Rossum in 1991.",
    "agent": (
        "In agentic AI, an agent perceives its environment, decides on an "
        "action (often via an LLM), and acts - repeating in a loop."
    ),
    "github": "GitHub is a platform for hosting and collaborating on Git repositories.",
    "openrouter": (
        "OpenRouter is a unified API that routes requests to many different "
        "LLM providers, including free-tier models."
    ),
}


def lookup_fact(topic: str) -> str:
    return _FACTS.get(topic.lower(), f"No fact found for '{topic}'.")


RESEARCH_TOOLS = [
    Tool(
        name="lookup_fact",
        description="Look up a short fact about a topic (e.g. python, agent, github, openrouter).",
        func=lookup_fact,
    ),
]
