from app.graph.State import State, AgentState
from app.graph.llm import llm
from langchain_core.messages import SystemMessage, AIMessage
from app.graph.prompts import SUPERVISOR_SYSTEM_PROMPT as SYSTEM_PROMPT




def supervisor(state: State):
    response = llm.with_structured_output(AgentState).invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ])
    if len(response.agents) == 0:
       return { "plan": response.plan,
                "agents": [{}],
                "messages":[AIMessage(content=response.normalResponse)]
            }
    else:
        agentHouse = {}
        for agent in response.agents:
            agentHouse[agent] = False
        return { "plan": response.plan,"agents": [agentHouse]} 
