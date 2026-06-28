from pydantic import BaseModel


class CreateSessionResponse(BaseModel):
    session_id: str
    title: str