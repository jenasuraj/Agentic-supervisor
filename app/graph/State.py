from typing import Annotated, TypedDict
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages


class AgentHouse(TypedDict):
    name:str
    status:bool


class State(TypedDict):
    messages: Annotated[list, add_messages]
    plan: str
    agents: list[AgentHouse]
    webSearch: Annotated[list, add_messages]
    weather: Annotated[list, add_messages]
    rag: Annotated[list, add_messages]
    

class AgentState(BaseModel):
    plan: str = Field( description="Overall plan for completing the user's request")
    agents: list[str] = Field( description="List of agents required to execute the plan")
    normalResponse: str = Field(description="normal response that llm has to generate")
