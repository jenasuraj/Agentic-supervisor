from app.graph.State import State, AgentState
from app.graph.llm import llm
from langchain.agents import create_agent
from langchain.tools import tool
from app.graph.tools.weather import weather_tool
from app.graph.prompts import WEATHER_AGENT_SYSTEM_PROMPT as WEATHER_AGENT_SYSTEM_PROMPT
from langchain_core.prompts import PromptTemplate



def weather(state: State):
    print("Weather node entered")
    plans = state["plans"]

    @tool
    def read_plan():
        """Read only the weather plans assigned by the supervisor."""
        print("Weather agent calling read_plan")
        weather_plans = [
            plan for plan in plans
            if (plan["agent"] == "weather")
        ]
        if len(weather_plans) == 0:
            return "There are no todo plans as of now, please respond normally"
        return weather_plans

    @tool
    def write_plan(id: int, status: str):
        """Update a weather plan status by its structured plan id."""
        print(f"Weather agent calling write_plan: {id} -> {status}")
        if status not in ("pending", "completed"):
            return "Invalid status. Use only 'pending' or 'completed'."
        for plan in plans:
            if plan["id"] == id and plan["agent"] == "weather":
               plan["status"] = status
               return f"plan {id} written successfully with status {status}"
        return f"Can't perform write operation, No weather plan found with id {id}"


    prompt_template = PromptTemplate.from_template(WEATHER_AGENT_SYSTEM_PROMPT)
    formatted_prompt = prompt_template.format(plans=state["plans"])

    agent = create_agent(
        model=llm,
        system_prompt=formatted_prompt,
        tools=[weather_tool, read_plan, write_plan],
    )

    response = agent.invoke({"messages": state["weather"]})
    agentHouse = state["agents"][0]
    agentHouse["weather"] = True
    print("Weather node completed")
    
    return {
        "weather": response["messages"],
        "plans": plans,
        "agents": [agentHouse],
    }