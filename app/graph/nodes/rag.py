from app.graph.State import State, AgentState
from app.graph.llm import llm
from langchain.agents import create_agent
from langchain.tools import tool
from app.graph.prompts import RAG_PROMPT as prompt
from langchain_core.prompts import PromptTemplate


def rag(state: State):
    from app.graph.tools.rag import rag_fetcher
    print("RAG node entered")
    plans = state["plans"]

    @tool
    def read_plan():
        """Read only the RAG plans assigned by the supervisor."""
        print("RAG agent calling read_plan")
        rag_plans = [
            plan for plan in plans
            if (plan["agent"] == "rag")
        ]
        if len(rag_plans) == 0:
            return "There are no todo plans as of now, please respond normally"
        return rag_plans

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

    prompt_template = PromptTemplate.from_template(prompt)
    formatted_prompt = prompt_template.format(plans=state["plans"])

    agent = create_agent(
        model=llm,
        system_prompt=formatted_prompt,
        tools=[rag_fetcher, read_plan, write_plan],
    )

    response = agent.invoke({"messages": state["rag"]})
    agentHouse = state["agents"][0]
    agentHouse["rag"] = True
    print("RAG node completed")
    return {
        "rag": response["messages"],
        "plans": plans,
        "agents": [agentHouse],
    }
