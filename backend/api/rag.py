from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from pydantic import BaseModel

from backend.rag.rag_service import RagService
from backend.rag.multimodal import load_document
from backend.rag.processors.chunk_builder import build_chunks
from backend.rag.ingestion import ingest_chunks
from backend.database.document_repository import DocumentRepository
from backend.rag.processors.image_understanding import understand_image


router = APIRouter()

service = RagService()
repo = DocumentRepository()


# -------------------------
# REQUEST MODEL (UPDATED)
# -------------------------
class QueryRequest(BaseModel):
    query: str
    document_id: str | None = None   # 🔥 IMPORTANT FIX


# -------------------------
# QUERY DOCUMENT (FIXED)
# -------------------------
@router.post("/query")
async def query_rag(payload: QueryRequest):

    try:
        result = service.query_document(
            payload.query,
            payload.document_id   # 🔥 PASS DOCUMENT CONTEXT
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# UPLOAD DOCUMENT (UNCHANGED LOGIC)
# -------------------------
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    try:
        file_path = f"backend/storage/uploads/{file.filename}"

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        document = repo.create_document(
            filename=file.filename,
            file_path=file_path
        )

        document_id = document["_id"]

        parsed = load_document(file_path)
        parsed["image_descriptions"] = []

        for image_path in parsed.get("images", []):

            try:
                description = understand_image(image_path)
                parsed["image_descriptions"].append(description)

            except Exception as e:
                print("Image processing failed:", str(e))

        chunks = build_chunks(
            document_id=document_id,
            filename=file.filename,
            parsed_data=parsed
        )

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Document contains no extractable content."
            )

        ingest_chunks(chunks)

        repo.update_status(document_id, "processed")

        return {
            "document_id": document_id,
            "status": "processed",
            "chunks": len(chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# LIST DOCUMENTS
# -------------------------
@router.get("/documents")
async def list_documents():
    return repo.list_documents()


# -------------------------
# DELETE DOCUMENT
# -------------------------
@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):

    repo.delete_document(document_id)

    return {"message": "deleted"}