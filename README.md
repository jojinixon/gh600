# gh600

Hands On: Github - Agentic AI Developer (Certification)

A small, dependency-light codebase for learning core agentic AI
concepts by building them from scratch:

- **Tools** ([src/gh600/tools.py](src/gh600/tools.py)) — plain functions an agent can call.
- **Memory** ([src/gh600/memory.py](src/gh600/memory.py)) — short-term conversation history.
- **LLM client** ([src/gh600/llm.py](src/gh600/llm.py)) — the interface between the agent
  and a language model.
  - `FakeLLM` is a scripted, offline stand-in used in tests.
  - `OpenRouterLLM` calls a real model (free tier, via
    [openrouter.ai](https://openrouter.ai)) so you can see the agent
    reason for real. It asks the model to reply with one JSON object
    (a tool call or a final answer) since free OpenRouter models don't
    support native tool calling.
- **Agent** ([src/gh600/agent.py](src/gh600/agent.py)) — a minimal think → act → observe
  loop tying the above together. Each `Agent` has its own `persona`
  (a short instruction string) and `tools`, so two agents built from
  the same class can behave completely differently.
- **Orchestrator** ([src/gh600/orchestrator.py](src/gh600/orchestrator.py)) — the simplest
  multi-agent pattern: a fixed handoff between a `Researcher` agent
  (gathers facts with the `lookup_fact` tool) and a `Writer` agent
  (turns those facts into a final answer, no tools).

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

Copy `.env.example` to `.env` and add an OpenRouter API key (free,
from https://openrouter.ai/keys) if you want to run the live example.
`.env` is gitignored — never commit real credentials.

## Run tests

```powershell
pytest
```

Tests use `FakeLLM` only, so they run offline with no API key.

## Run the agent against a real model

```powershell
python examples\run_agent.py "What is 12 + 30?"
```

## Run the two-agent (Researcher -> Writer) pipeline

```powershell
python examples\run_multi_agent.py "What is Python?"
```

## Suggested path through the course

1. Read [tests/test_agent.py](tests/test_agent.py) to see the agent loop in action with
   `FakeLLM` — no API key required.
2. Run [examples/run_agent.py](examples/run_agent.py) to see the same loop driven by a real
   model through `OpenRouterLLM`.
3. Add a tool in `tools.py` and a test for it.
4. Read [tests/test_orchestrator.py](tests/test_orchestrator.py) and run
   [examples/run_multi_agent.py](examples/run_multi_agent.py) to see two agents with
   different personas hand work off to each other.
5. Implement another `LLMClient` (e.g. `GitHubModelsClient` or
   `AzureOpenAIClient`) in `llm.py` once a lesson introduces that
   provider — same pattern as `OpenRouterLLM`.
6. Extend `Orchestrator` toward richer patterns — routing between more
   than two agents, parallel agents, or a debate/critique loop — as
   later lessons cover them.
