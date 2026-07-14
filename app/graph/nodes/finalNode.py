from app.graph.State import State
from app.graph.llm import llm
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from app.graph.prompts import FINAL_AGENT_SYSTEM_PROMPT
from textwrap import dedent




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
            f"Observation:\n{(messages)}"
        )

    return "\n\n".join(observations) if observations else "None"




def finalNode(state: State):
    print("🏁 Final node entered")
    if len(state["agents"][0].keys()) == 0:
        print("💬 Final node returning direct supervisor response")
        return {"messages": [AIMessage(content=state["messages"][-1].content)]}

    final_context = dedent(f"""
    Supervisor plan description:
    {state.get("planDescription") or "None"}

    Execution plans:
    {state.get("plans") or "None"}

    Original conversation:
    {state.get("messages")}

    Specialist observations:
    {_agent_observations(state)}

    Write the final answer for the user now.
    """).strip()

    response = llm.invoke([
        SystemMessage(content=FINAL_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=final_context),
    ])

    print("✅ Final node completed")
    return {"messages": [AIMessage(content=response.content)]}
