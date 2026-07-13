from app.graph.State import State
from app.graph.llm import llm
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from app.graph.prompts import FINAL_AGENT_SYSTEM_PROMPT
from textwrap import dedent


def _message_text(message):
    if isinstance(message, dict):
        content = message.get("content", "")
    else:
        content = getattr(message, "content", "")

    if isinstance(content, str):
        return content
    return str(content)


def _format_messages(messages):
    if not messages:
        return "None"

    formatted = []
    for index, message in enumerate(messages, start=1):
        role = getattr(message, "type", None)
        if role is None and isinstance(message, dict):
            role = message.get("role")
        formatted.append(f"{index}. {role or 'message'}: {_message_text(message)}")
    return "\n".join(formatted)


def _has_requested_agents(state: State):
    agents = state.get("agents") or []
    if not agents:
        return False

    agent_house = agents[0] or {}
    return any(agent_house.keys())


def _agent_observations(state: State):
    observations = []
    agent_house = (state.get("agents") or [{}])[0] or {}

    for agent_name, completed in agent_house.items():
        if agent_name == "web_search":
            messages = state.get("webSearch") or []
        elif agent_name == "weather":
            messages = state.get("weather") or []
            if not messages:
                messages = state.get("webSearch") or []
        elif agent_name == "rag":
            messages = state.get("rag") or []
        else:
            messages = []

        observations.append(
            f"Agent: {agent_name}\n"
            f"Completed: {completed}\n"
            f"Observation:\n{_format_messages(messages)}"
        )

    return "\n\n".join(observations) if observations else "None"


def finalNode(state: State):
    if not _has_requested_agents(state):
        return {"messages": [AIMessage(content=_message_text(state["messages"][-1]))]}

    final_context = dedent(f"""
    Supervisor plan:
    {state.get("plan") or "None"}

    Original conversation:
    {_format_messages(state.get("messages"))}

    Specialist observations:
    {_agent_observations(state)}

    Write the final answer for the user now.
    """).strip()

    response = llm.invoke([
        SystemMessage(content=FINAL_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=final_context),
    ])

    return {"messages": [AIMessage(content=_message_text(response))]}
