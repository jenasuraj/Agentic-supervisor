from app.graph.State import State
from app.graph.llm import llm
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from app.graph.prompts import FINAL_AGENT_SYSTEM_PROMPT




def finalNode(state: State):
    print("🏁 Final node entered")
    if len(state["agents"][0].keys()) == 0:
        print("💬 Final node returning direct supervisor response")
        return {"messages": [AIMessage(content=state["messages"][-1].content)]}

    plans = state["plans"]
    final_context = f"""
    Original conversation:
    {state["messages"]}

    Supervisor plan description:
    {state["planDescription"]}

    Execution plans:
    {plans}

    """

    if any(plan["agent"] == "weather" for plan in plans):
        final_context += f"""
        Weather memory:
        {state["weather"]}

        """

    if any(plan["agent"] == "web_search" for plan in plans):
        final_context += f"""
        Web search memory:
        {state["webSearch"]}

        """

    if any(plan["agent"] == "rag" for plan in plans):
        final_context += f"""
        RAG memory:
        {state["rag"]}

        """

    response = llm.invoke([
        SystemMessage(content=FINAL_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=final_context),
    ])

    print("✅ Final node completed")
    return {"messages": [AIMessage(content=response.content)]}