from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()


llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="openai/gpt-4o-mini",
)
