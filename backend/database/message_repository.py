import uuid

from datetime import datetime

from backend.database.mongo import db


class MessageRepository:

    def __init__(self):

        self.collection = db["messages"]

    def add_message(

        self,

        conversation_id,

        role,

        content

    ):

        message = {

            "_id":
            f"msg_{uuid.uuid4().hex}",

            "conversation_id":
            conversation_id,

            "role":
            role,

            "content":
            content,

            "created_at":
            datetime.utcnow()
        }

        self.collection.insert_one(
            message
        )

        return message

    def get_messages(
        self,
        conversation_id
    ):

        return list(
            self.collection.find(
                {
                    "conversation_id":
                    conversation_id
                }
            ).sort(
                "created_at",
                1
            )
        )

    def delete_messages(
        self,
        conversation_id
    ):

        self.collection.delete_many(
            {
                "conversation_id":
                conversation_id
            }
        )