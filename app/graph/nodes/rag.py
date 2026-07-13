from app.graph.State import State, AgentState
from app.graph.llm import llm
from langchain_core.messages import AIMessage
from langchain.agents import create_agent


prompt= """
You are a RAG agent.

Your only job is to fetch relevant personal/project knowledge using the rag_fetcher tool and return a clean observation for the final agent.

Rules:
1 - Always call the rag_fetcher tool before answering.
2 - Use the user's exact question as the retrieval query.
3 - Do not answer from your own memory.
4 - After rag_fetcher returns, your final answer must be based on the retrieved context.
5 - Never say you cannot access RAG or personal data after the tool has returned.
6 - Return only the useful retrieved information in clear text. Do not mention internal tool calls.
7 - If the retrieved context is not enough, say that the available RAG context is limited.
"""

def rag(state: State):
    from app.graph.tools.rag import rag_fetcher

    agent = create_agent(
        model=llm,
        system_prompt=prompt,
        tools=[rag_fetcher]
    )
    response = agent.invoke({"messages":state["messages"]})
    agent_response = response["messages"][-1].content
    agentHouse = state["agents"][0]
    agentHouse["rag"] = True
    return {"rag":[AIMessage(content=agent_response)]}
