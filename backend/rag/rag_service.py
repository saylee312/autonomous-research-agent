import os

from backend.database.document_repository import DocumentRepository
from backend.rag.query_engine import ask_rag


UPLOAD_DIR = "backend/storage/uploads"


class RagService:
    """Service for saving, querying, listing, and deleting RAG documents."""

    def __init__(self):
        self.repo = DocumentRepository()
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    def save_document(self, file):
        filepath = os.path.join(UPLOAD_DIR, file.filename)
        with open(filepath, "wb") as buffer:
            buffer.write(file.file.read())

        return self.repo.create_document(
            filename=file.filename,
            file_path=filepath
        )

    def query_document(self, query: str, document_id: str = None):
        return ask_rag(query, document_id=document_id)

    def get_documents(self):
        return self.repo.list_documents()

    def delete_document(self, document_id):
        document = self.repo.get_document(document_id)

        if not document:
            return False

        filepath = document["file_path"]

        if os.path.exists(filepath):
            os.remove(filepath)

        self.repo.delete_document(document_id)

        return True