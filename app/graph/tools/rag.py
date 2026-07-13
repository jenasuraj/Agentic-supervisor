from langchain.tools import tool
from app.graph.VectorStore import vector_store


@tool
def rag_fetcher(query:str):
    """use this tool to fetch important personal data from RAG db regarding mr suraj jena"""

    results = vector_store.similarity_search(
        query,
        k=3,
    )
    context = "\n\n".join(
        f"Source: {doc.metadata}\nContent: {doc.page_content}"
        for doc in results
    )
    return context
