from app.graph.State import State, AgentState
from app.graph.llm import llm
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from app.graph.prompts import SUPERVISOR_SYSTEM_PROMPT as SYSTEM_PROMPT



def supervisor(state: State):
    print("🧠 Supervisor entered")
    response = llm.with_structured_output(AgentState).invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ])
    plans = []
    for planItem in response.plans:
        payload = {}
        payload["id"] = planItem.id
        payload["agent"] = planItem.agent
        payload["plan"] = planItem.plan
        payload["status"] = planItem.status
        plans.append(payload)
        
    print("📝 Supervisor plans created:", plans)
    if len(response.agents) == 0:  # if there is no agents, means there is no plans being created as well (but not strictly true...) 
        print("💬 Supervisor answering directly")
        return { 
                "planDescription": response.planDescription,
                "plans": plans,
                "agents": [{}],
                "messages":[AIMessage(content=response.normalResponse)],
                }
    else:
        agentHouse = {}
        for agent in response.agents:
            agentHouse[agent] = False
        print("✅ Supervisor handoff ready")
        return {
                "planDescription": response.planDescription,
                "plans": plans,
                "agents": [agentHouse],
                } 