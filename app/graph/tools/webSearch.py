from langchain.tools import tool
from tavily import TavilyClient
import os


@tool
def web_search(query:str):
    """use this tool to perform web search, provide your query as input"""
    print(f"🔎 Web search tool called: {query}")
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query)
    print("✅ Web search tool completed")
    return response
