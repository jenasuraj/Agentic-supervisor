from app.graph.State import State, AgentState
from app.graph.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.agents import create_agent
from langchain.tools import tool
from app.graph.tools.weather import weather_tool
from app.graph.prompts import WEATHER_AGENT_SYSTEM_PROMPT as WEATHER_AGENT_SYSTEM_PROMPT



def weather(state: State):
    print("Weather node entered")
    plans = state["plans"]
    pending_weather_plans = [
        plan for plan in plans
        if plan["agent"] == "weather" and plan["status"] == "pending"
    ]

    @tool
    def read_plan():
        """Read only the weather plans assigned by the supervisor."""
        print("Weather agent calling read_plan")
        if len(pending_weather_plans) == 0:
            return "There are no todo plans as of now, please respond normally"
        return pending_weather_plans

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


    agent = create_agent(
        model=llm,
        system_prompt=WEATHER_AGENT_SYSTEM_PROMPT,
        tools=[weather_tool, read_plan, write_plan],
    )

    agent_messages = [
        SystemMessage(content=f"""
        Past weather memory / context:
        {state["weather"]}

        Current pending weather plans:
        {pending_weather_plans}

        Important:
        - Use past memory only as context.
        - Do not assume a current plan is completed just because a similar old task was completed.
        - You must complete the current pending weather plans or explain why you cannot.
        """),
        HumanMessage(content="Execute the current pending weather plans now."),
    ]
    response = agent.invoke({"messages": agent_messages})
    new_messages = response["messages"][len(agent_messages):]
    agentHouse = state["agents"][0]
    agentHouse["weather"] = True
    print("Weather node completed")
    
    return {
        "weather": new_messages,
        "plans": plans,
        "agents": [agentHouse],
    }
