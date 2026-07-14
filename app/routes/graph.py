from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.graph.FlowPath import graph
router = APIRouter()


class GraphRequest(BaseModel):
    message: str = Field(..., min_length=1)


class GraphResponse(BaseModel):
    response: str
    planDescription: str | None = None
    plans: dict[str, str] | None = None


@router.post("/invoke", response_model=GraphResponse)
def invoke_graph(payload: GraphRequest):
    result = graph.invoke({"messages": [{"role": "user", "content": payload.message}]})
    answer = result["messages"][-1].content
    return {
        "response": answer,
    }