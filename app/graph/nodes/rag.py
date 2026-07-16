from app.graph.State import State, AgentState
from app.graph.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.agents import create_agent
from langchain.tools import tool
from app.graph.prompts import RAG_PROMPT as prompt


def rag(state: State):
    from app.graph.tools.rag import rag_fetcher
    print("RAG node entered")
    plans = state["plans"]
    pending_rag_plans = [
        plan for plan in plans
        if plan["agent"] == "rag" and plan["status"] == "pending"
    ]

    @tool
    def read_plan():
        """Read only the RAG plans assigned by the supervisor."""
        print("RAG agent calling read_plan")
        if len(pending_rag_plans) == 0:
            return "There are no todo plans as of now, please respond normally"
        return pending_rag_plans

    @tool
    def write_plan(id: int, status: str):
        """Update a RAG plan status by its structured plan id."""
        print(f"RAG agent calling write_plan: {id} -> {status}")
        if status not in ("pending", "completed"):
            return "Invalid status. Use only 'pending' or 'completed'."
        for plan in plans:
            if plan["id"] == id and plan["agent"] == "rag":
                plan["status"] = status
                return f"plan {id} written successfully with status {status}"
        return f"No RAG plan found with id {id}"

    agent = create_agent(
        model=llm,
        system_prompt=prompt,
        tools=[rag_fetcher, read_plan, write_plan],
    )

    agent_messages = [
        SystemMessage(content=f"""
        Past RAG memory / context:
        {state["rag"]}

        Current pending RAG plans:
        {pending_rag_plans}

        Important:
        - Use past memory only as context.
        - Do not assume a current plan is completed just because a similar old task was completed.
        - You must complete the current pending RAG plans or explain why you cannot.
        """),
                HumanMessage(content="Execute the current pending RAG plans now."),
            ]
    response = agent.invoke({"messages": agent_messages})
    new_messages = response["messages"][len(agent_messages):]
    agentHouse = state["agents"][0]
    agentHouse["rag"] = True
    print("RAG node completed")
    return {
        "rag": new_messages,
        "plans": plans,
        "agents": [agentHouse],
    }
