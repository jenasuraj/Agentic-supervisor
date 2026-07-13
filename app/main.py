from fastapi import FastAPI
from app.routes.graph import router as graph_router


app = FastAPI(
    title="FastAPI Boilerplate",
    version="1.0.0",
)

app.include_router(graph_router, prefix="/graph")


@app.get("/")
def root():
    return {"message": "Server Running"}