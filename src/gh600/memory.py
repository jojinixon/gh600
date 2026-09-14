"""Short-term conversational memory for an agent."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Memory:
    _entries: list[tuple[str, str]] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self._entries.append((role, content))

    def history(self) -> list[tuple[str, str]]:
        return list(self._entries)

    def clear(self) -> None:
        self._entries.clear()
