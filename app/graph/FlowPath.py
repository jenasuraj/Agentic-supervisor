from app.graph.State import State
from langgraph.graph import StateGraph, START, END
from app.graph.nodes.supervisor import supervisor
from app.graph.nodes.finalNode import finalNode
from app.graph.nodes.webSearch import webSearch
from app.graph.nodes.weather import weather
from app.graph.nodes.rag import rag


def router(state:State):
    if(len(state["agents"]) == 0):
        return "finalNode"
    else:
        agentHouse = state["agents"][0]
        for agent in agentHouse:
            if(agentHouse[agent] == False):
                return agent
        return "finalNode"
    

graph_builder = StateGraph(State)
graph_builder.add_node("supervisor", supervisor)
graph_builder.add_node("finalNode", finalNode)
graph_builder.add_node("web_search", webSearch)
graph_builder.add_node("weather", weather)
graph_builder.add_node("rag", rag)

graph_builder.add_edge(START, "supervisor")
graph_builder.add_conditional_edges("supervisor",router,["web_search","weather","rag","finalNode"])
graph_builder.add_conditional_edges("web_search",router,["web_search","weather","rag","finalNode"])
graph_builder.add_conditional_edges("weather",router,["web_search","weather","rag","finalNode"])
graph_builder.add_conditional_edges("rag",router,["web_search","weather","rag","finalNode"])
graph_builder.add_edge("finalNode",END)
graph = graph_builder.compile()