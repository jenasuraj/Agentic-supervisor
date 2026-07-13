from app.graph.State import State, AgentState
from app.graph.llm import llm
from langchain_core.messages import AIMessage
from langchain.agents import create_agent
from app.graph.tools.weather import weather_tool


prompt= """
You are a weather agent.

Your only job is to gather weather information using the weather_tool and return a clean observation for the final agent.

Rules:
1 - Always call the weather_tool before answering.
2 - Pass the user's requested place, city, state, country, or full weather question to the tool.
3 - Do not answer weather questions from your own memory.
4 - After weather_tool returns, your final answer must be based on the tool result.
5 - Never say you cannot provide weather or do not have weather tools after the tool has returned.
6 - Return only the useful weather result in clear text. Do not mention internal tool calls.
7 - If the user did not provide a location, say that the location is missing.
"""
tools = [weather_tool]

def weather(state: State):
    agent = create_agent(
        model=llm,
        system_prompt=prompt,
        tools=tools
    )
    response = agent.invoke({"messages":state["messages"]})
    agent_response = response["messages"][-1].content
    agentHouse = state["agents"][0]
    agentHouse["weather"] = True
    return {"weather":[AIMessage(content=agent_response)]}
