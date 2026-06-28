import uuid
from datetime import datetime

from backend.database.mongo import db


def serialize_doc(doc):

    if not doc:
        return None

    for key, value in doc.items():
        doc[key] = str(value)

    return doc


def serialize_docs(docs):

    return [serialize_doc(doc) for doc in docs]


class DocumentRepository:

    def __init__(self):

        self.collection = db["documents"]

    def create_document(
        self,
        filename: str,
        file_path: str
    ):

        document = {
            "_id": f"doc_{uuid.uuid4().hex}",
            "filename": filename,
            "file_path": file_path,
            "status": "uploaded",
            "created_at": datetime.utcnow()
        }

        self.collection.insert_one(document)

        return serialize_doc(document)

    def get_document(
        self,
        document_id: str
    ):

        document = self.collection.find_one(
            {"_id": document_id}
        )

        return serialize_doc(document)

    def list_documents(self):

        documents = list(
            self.collection.find()
            .sort("created_at", -1)
        )

        return serialize_docs(documents)

    def update_status(
        self,
        document_id: str,
        status: str
    ):

        self.collection.update_one(
            {"_id": document_id},
            {
                "$set": {
                    "status": status
                }
            }
        )

    def delete_document(
        self,
        document_id: str
    ):

        self.collection.delete_one(
            {"_id": document_id}
        )