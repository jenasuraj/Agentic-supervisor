from app.graph.State import State, AgentState
from app.graph.llm import llm
from langchain_core.messages import AIMessage
from langchain.agents import create_agent
from app.graph.tools.webSearch import web_search


prompt= """
You are a web search agent.

Your only job is to gather current or external information using the web_search tool and return a clean observation for the final agent.

Rules:
1 - Always call the web_search tool before answering.
2 - Use the user's exact topic, location, entity, or question as the search query.
3 - Do not answer from your own memory.
4 - After web_search returns, your final answer must be based on the tool result.
5 - Never say you cannot search or do not have access to a search tool after the tool has returned.
6 - Return only the useful search result in clear text. Do not mention internal tool calls.
7 - If the tool result is limited, say that the available search result is limited.
"""

tools = [web_search]

def webSearch(state: State):
    agent = create_agent(
        model = llm,
        system_prompt=prompt,
        tools=tools
    )
    response = agent.invoke({"messages":state["messages"]})
    agent_response = response["messages"][-1].content
    agentHouse = state["agents"][0]
    agentHouse["web_search"] = True
    return {"webSearch":[AIMessage(content=agent_response)]}