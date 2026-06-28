import chromadb

from backend.core.config import settings


client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_PATH
)

collection = client.get_or_create_collection(
    name="multimodal_rag"
)