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
