from langchain.tools import tool
import os
import requests


@tool
def weather_tool(query: str):
    """use this tool to fetch current weather of a place"""
    print(f"🌦️ Weather tool called: {query}")
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": query,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric",
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        desc = weather_data["weather"][0]["description"]
        print(f"✅ Weather tool result: {temp}°C, {humidity}% humidity, {desc}")
        return f"temperature is {temp}°C, Humidity: {humidity}% Condition: {desc.capitalize()}"

    except requests.exceptions.HTTPError:
        print("❌ Weather tool failed: city not found or invalid API key")
    except Exception as e:
        print(f"❌ Weather tool error: {e}")
