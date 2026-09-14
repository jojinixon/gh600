import pytest

from gh600.agent import Agent
from gh600.llm import FakeLLM, LLMResponse, ToolCall
from gh600.memory import Memory
from gh600.tools import DEFAULT_TOOLS


def test_agent_answers_directly_when_no_tool_needed():
    llm = FakeLLM([LLMResponse(content="42")])
    agent = Agent(llm=llm, tools=DEFAULT_TOOLS, memory=Memory())

    result = agent.run("What is the answer to everything?")

    assert result == "42"


def test_agent_uses_a_tool_before_answering():
    llm = FakeLLM(
        [
            LLMResponse(
                content="",
                tool_call=ToolCall(name="add", arguments={"a": 2, "b": 3}),
            ),
            LLMResponse(content="The answer is 5"),
        ]
    )
    agent = Agent(llm=llm, tools=DEFAULT_TOOLS, memory=Memory())

    result = agent.run("What is 2 + 3?")

    assert result == "The answer is 5"
    assert any(
        role == "tool" and "add(" in content for role, content in agent.memory.history()
    )


def test_agent_raises_if_it_never_reaches_an_answer():
    tool_call = LLMResponse(
        content="", tool_call=ToolCall(name="add", arguments={"a": 1, "b": 1})
    )
    llm = FakeLLM([tool_call] * 5)
    agent = Agent(llm=llm, tools=DEFAULT_TOOLS, memory=Memory(), max_steps=2)

    with pytest.raises(RuntimeError):
        agent.run("loop forever")
