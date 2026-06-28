import uuid

from datetime import datetime

from backend.database.mongo import db


class ConversationRepository:

    def __init__(self):

        self.collection = db["conversations"]

    def create_conversation(
        self,
        title="New Chat"
    ):

        conversation = {

            "_id":
            f"conv_{uuid.uuid4().hex}",

            "title":
            title,

            "created_at":
            datetime.utcnow(),

            "updated_at":
            datetime.utcnow()
        }

        self.collection.insert_one(
            conversation
        )

        return conversation

    def list_conversations(self):

        return list(
            self.collection.find()
            .sort(
                "updated_at",
                -1
            )
        )

    def get_conversation(
        self,
        conversation_id
    ):

        return self.collection.find_one(
            {
                "_id":
                conversation_id
            }
        )

    def delete_conversation(
        self,
        conversation_id
    ):

        self.collection.delete_one(
            {
                "_id":
                conversation_id
            }
        )