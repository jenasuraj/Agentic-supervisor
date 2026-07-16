from app.graph.State import State
from langgraph.graph import StateGraph, START, END
from app.graph.nodes.supervisor import supervisor
from app.graph.nodes.finalNode import finalNode
from app.graph.nodes.webSearch import webSearch
from app.graph.nodes.weather import weather
from app.graph.nodes.rag import rag
from langgraph.checkpoint.memory import InMemorySaver


def router(state:State):
    print("🧭 Router checking next agent")
    if(len(state["agents"]) == 0):
        print("🏁 Router -> finalNode")
        return "finalNode"
    else:
        agentHouse = state["agents"][0]
        for agent in agentHouse:
            if(agentHouse[agent] == False):
                print(f"➡️ Router -> {agent}")
                return agent
        
        for plan in state["plans"]:
            if(plan["status"] == "pending"):
                print("Few plans were not completed, so loop again ->")
                agent = plan["agent"]
                if agent in state["agents"][0]:
                    state["agents"][0][agent] = False
                    print(f"➡️ Router -> {agent}")
                    return agent
        
        print("🏁 Router -> finalNode")
        return "finalNode"
    

graph_builder = StateGraph(State)
graph_builder.add_node("supervisor", supervisor)
graph_builder.add_node("finalNode", finalNode)
graph_builder.add_node("web_search", webSearch)
graph_builder.add_node("weather", weather)
graph_builder.add_node("rag", rag)

graph_builder.add_edge(START, "supervisor")
for agent_node in ["supervisor","web_search","weather","rag"]:
    graph_builder.add_conditional_edges(agent_node,router,["web_search","weather","rag","finalNode"])
graph_builder.add_edge("finalNode",END)

memory = InMemorySaver() # Use memory for local/dev, or PostgresSaver/RedisSaver for production
graph = graph_builder.compile(checkpointer=memory)