![Prod Agentic Hero](public/img.png)

Prod Agentic is a FastAPI + LangGraph backend that experiments with a supervisor-led multi-agent workflow. A supervisor node reads the user request, creates execution plans, routes work to specialist agents, and then a final node combines the results into one response.

The current graph includes:

- Supervisor agent for planning and routing
- Weather agent for live weather queries
- Web search agent using Tavily
- RAG agent using PGVector and HuggingFace embeddings
- Final response agent for answer synthesis
- Emoji terminal logs for easier graph debugging

## Tech Stack

- Python
- FastAPI
- Uvicorn
- LangGraph
- LangChain
- OpenRouter / OpenAI-compatible chat model
- Tavily search
- OpenWeather API
- PostgreSQL + PGVector
- HuggingFace sentence-transformer embeddings

## Install `uv`

`uv` is a fast Python package and virtual environment manager.

### Windows PowerShell

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart your terminal, then check:

```powershell
uv --version
```

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then check:

```bash
uv --version
```

## Setup Project

Clone the repo and enter the project folder:

```bash
git clone <your-repo-url>
cd prod-agentic
```

Create a virtual environment:

```bash
uv venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

On macOS / Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
uv pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root folder:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/database_name
```

Make sure PostgreSQL and PGVector are available before using the RAG flow.

## Run The Server

Start the FastAPI app:

```bash
uvicorn app.main:app --reload
```

Server will run at:

```text
http://127.0.0.1:8000
```

Health check:

```text
GET /
```

Graph endpoint:

```text
POST /graph/invoke
```

Example request:

```json
{
  "message": "prepare a deep research on what the future is going to look like in 2050, and if delhi's weather is like now is it gonna affect the future, also what is the education of suraj jena"
}
```

## Project Structure

```text
app/
  main.py                  FastAPI app entrypoint
  routes/
    graph.py               API route for graph invocation
  graph/
    FlowPath.py            LangGraph workflow and routing
    State.py               Shared graph state types
    llm.py                 Chat model setup
    prompts.py             Supervisor and final node prompts
    VectorStore.py         PGVector RAG setup
    nodes/
      supervisor.py        Creates plans and selects agents
      weather.py           Weather specialist node
      webSearch.py         Web search specialist node
      rag.py               RAG specialist node
      finalNode.py         Final response composer
    tools/
      weather.py           OpenWeather tool
      webSearch.py         Tavily search tool
      rag.py               Vector search tool
public/
  img.png                  README hero image
```

## Development Notes

- Use `uvicorn app.main:app --reload` during development.
- Keep secrets inside `.env`.
- The terminal logs show the graph flow with emojis, so it is easier to see which node or tool is running.
- If the RAG node loads slowly, it may be initializing embeddings or writing documents to PGVector.

