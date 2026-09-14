from gh600.agent import Agent
from gh600.llm import FakeLLM, LLMResponse, ToolCall
from gh600.orchestrator import Orchestrator
from gh600.tools import RESEARCH_TOOLS


def test_orchestrator_chains_researcher_into_writer():
    researcher_llm = FakeLLM(
        [
            LLMResponse(
                content="",
                tool_call=ToolCall(name="lookup_fact", arguments={"topic": "python"}),
            ),
            LLMResponse(content="Python is a programming language."),
        ]
    )
    writer_llm = FakeLLM([LLMResponse(content="Python is a popular programming language.")])

    researcher = Agent(llm=researcher_llm, tools=RESEARCH_TOOLS)
    writer = Agent(llm=writer_llm, tools=[])
    orchestrator = Orchestrator(researcher=researcher, writer=writer)

    result = orchestrator.run("What is Python?")

    assert result == "Python is a popular programming language."
    assert "Python is a programming language." in writer.memory.history()[0][1]
