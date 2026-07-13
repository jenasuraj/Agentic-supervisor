from langchain.tools import tool

@tool
def web_search(query:str):
    """use this tool to perform web search"""
    return "the current news is, protest is going in india by CJP in jantar mantar"