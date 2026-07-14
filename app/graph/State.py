from typing import Annotated, TypedDict
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages


class AgentHouse(TypedDict):
    name:str
    status:bool


class State(TypedDict):
    messages: Annotated[list, add_messages]
    planDescription: str
    plans: dict[str, str]
    agents: list[AgentHouse]
    webSearch: Annotated[list, add_messages]
    weather: Annotated[list, add_messages]
    rag: Annotated[list, add_messages]
    

class AgentState(BaseModel):
    planDescription: str = Field( description="Overall plan description for completing the user's request")
    plans: list[str] = Field(description="List of individual execution plans or steps required for the user's request")
    agents: list[str] = Field( description="List of agents required to execute the plans")
    normalResponse: str = Field(description="normal response that llm has to generate")
