import uuid
from datetime import datetime

from backend.database.mongo import db


def serialize_doc(doc):
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


def serialize_docs(docs):
    return [serialize_doc(doc) for doc in docs]


class ChatRepository:

    def __init__(self):
        self.sessions = db["sessions"]
        self.messages = db["messages"]

    def create_session(self):
        
        session_id = f"sess_{uuid.uuid4().hex}"

        session = {
            "_id": session_id,
            "session_id": session_id,
            "title": "New Chat",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        self.sessions.insert_one(session)

        return serialize_doc(session)

    def get_sessions(self):

        sessions = list(
            self.sessions.find().sort(
                "updated_at",
                -1
            )
        )

        return serialize_docs(sessions)

    def get_session(self, session_id):

        session = self.sessions.find_one(
            {"_id": session_id}
        )

        return serialize_doc(session)

    def delete_session(self, session_id):

        self.sessions.delete_one(
            {"_id": session_id}
        )

        self.messages.delete_many(
            {"session_id": session_id}
        )

    def add_message(
        self,
        session_id,
        role,
        content
    ):

        message = {
            "_id": f"msg_{uuid.uuid4().hex}",
            "session_id": session_id,
            "role": role,
            "content": content,
            "created_at": datetime.utcnow()
        }

        self.messages.insert_one(message)

        self.sessions.update_one(
            {"_id": session_id},
            {
                "$set": {
                    "updated_at": datetime.utcnow()
                }
            }
        )

        return serialize_doc(message)

    def get_messages(self, session_id):

        messages = list(
            self.messages.find(
                {"session_id": session_id}
            ).sort(
                "created_at",
                1
            )
        )

        return serialize_docs(messages)