from langchain.tools import tool

@tool
def weather_tool(query:str):
    """use this tool to fetch current weather of a place"""
    return "the current weather is cold and temperature is 20 degree celcius"