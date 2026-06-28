from pydantic import BaseModel


class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    status: str