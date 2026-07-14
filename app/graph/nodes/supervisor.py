from app.graph.State import State, AgentState
from app.graph.llm import llm
from langchain_core.messages import SystemMessage, AIMessage
from app.graph.prompts import SUPERVISOR_SYSTEM_PROMPT as SYSTEM_PROMPT



def supervisor(state: State):
    print("🧠 Supervisor entered")
    response = llm.with_structured_output(AgentState).invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ])
    plans = {}
    for planItem in response.plans:
        plans[planItem] = "pending"
    print(f"📋 Supervisor created {len(plans)} plan(s): {list(plans.keys())}")
    print(f"👥 Supervisor selected agent(s): {response.agents or ['finalNode']}")

    if len(response.agents) == 0:
       print("💬 Supervisor answering directly")
       return { "planDescription": response.planDescription,
                "plans": plans,
                "agents": [{}],
                "messages":[AIMessage(content=response.normalResponse)]
            }
    else:
        agentHouse = {}
        for agent in response.agents:
            agentHouse[agent] = False
        print("✅ Supervisor handoff ready")
        return { "planDescription": response.planDescription,
                 "plans": plans,
                 "agents": [agentHouse]} 
