from app.graph.State import State, AgentState
from app.graph.llm import llm
from langchain_core.messages import AIMessage
from langchain.agents import create_agent
from langchain.tools import tool
from app.graph.tools.weather import weather_tool
from app.graph.prompts import WEATHER_AGENT_SYSTEM_PROMPT as WEATHER_AGENT_SYSTEM_PROMPT



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
        for plan in plans:
            if plan["id"] == id:
               plan["status"] = status
               return f"plan {id} written successfully with status {status}"
        return f"No weather plan found with id {id}"


    agent = create_agent(
        model=llm,
        system_prompt=WEATHER_AGENT_SYSTEM_PROMPT,
        tools=[weather_tool, read_plan, write_plan],
    )
    response = agent.invoke({"messages": state["messages"]})
    agent_response = response["messages"][-1].content
    agentHouse = state["agents"][0]
    agentHouse["weather"] = True
    print("Weather node completed")
    
    return {
        "weather": [AIMessage(content=agent_response)],
        "plans": plans,
        "agents": [agentHouse],
    }