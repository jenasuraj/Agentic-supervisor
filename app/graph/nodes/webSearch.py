from app.graph.State import State, AgentState
from app.graph.llm import llm
from langchain_core.messages import AIMessage
from langchain.agents import create_agent
from langchain.tools import tool
from app.graph.tools.webSearch import web_search
from app.graph.prompts import WEB_SEARCH_AGENT_SYSTEM_PROMPT as WEB_SEARCH_AGENT_SYSTEM_PROMPT
from langchain_core.prompts import PromptTemplate


def webSearch(state: State):
    print("Web search node entered")
    plans = state["plans"]

    @tool
    def read_plan():
        """Read only the web_search plans assigned by the supervisor."""
        print("Web search agent calling read_plan")
        web_search_plans = [
            plan for plan in plans
            if (plan["agent"] == "web_search")
        ]
        if len(web_search_plans) == 0:
            return "There are no todo plans as of now, please respond normally"
        return web_search_plans

    @tool
    def write_plan(id: int, status: str):
        """Update a web_search plan status by its structured plan id."""
        print(f"Web search agent calling write_plan: {id} -> {status}")
        if status not in ("pending", "completed"):
            return "Invalid status. Use only 'pending' or 'completed'."
        for plan in plans:
            if plan["id"] == id and plan["agent"] == "web_search":
                plan["status"] = status
                return f"plan {id} written successfully with status {status}"
        return f"No web_search plan found with id {id}"
    

    prompt_template = PromptTemplate.from_template(WEB_SEARCH_AGENT_SYSTEM_PROMPT)
    formatted_prompt = prompt_template.format(plans=state["plans"])

    agent = create_agent(
        model=llm,
        system_prompt=formatted_prompt,
        tools=[web_search, read_plan, write_plan],
    )

    response = agent.invoke({"messages": state["webSearch"]})
    # the react agent only takes messages as key and the value must be list of items.
    # str(message)  -> Human-readable output (good for displaying/logging content)
    # repr(message) -> Developer/debug representation (shows actual class like HumanMessage, AIMessage, ToolMessage and full object details)
    # you might get worried regarding context window as each item in messages has lot of mess, but they all dont go the the LLM .
    # whatever goes to llm context window is str(message).
    # for item in response["messages"]:
    #    print("\n\n", repr(item))

    agentHouse = state["agents"][0]
    agentHouse["web_search"] = True
    print("Web search node completed")
    return {
        "webSearch": response["messages"],
        "plans": plans,
        "agents": [agentHouse],
    }