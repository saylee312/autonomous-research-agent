from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message: str
    use_search: Optional[bool] = None  # Optional: enable web search for current query (None lets service decide)


class ChatMessage(BaseModel):
    role: str
    content: str