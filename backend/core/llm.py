from functools import lru_cache

from langchain_groq import ChatGroq

from backend.core.config import settings


@lru_cache(maxsize=None)
def get_llm():

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=settings.GROQ_API_KEY,
        temperature=0
    )