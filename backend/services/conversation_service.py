from backend.database.conversation_repository import (
    ConversationRepository
)

from backend.database.message_repository import (
    MessageRepository
)


class ConversationService:

    def __init__(self):

        self.conv_repo = (
            ConversationRepository()
        )

        self.msg_repo = (
            MessageRepository()
        )

    def create_chat(self):

        return self.conv_repo.create_conversation()

    def list_chats(self):

        return self.conv_repo.list_conversations()

    def get_chat_messages(
        self,
        conversation_id
    ):

        return self.msg_repo.get_messages(
            conversation_id
        )

    def delete_chat(
        self,
        conversation_id
    ):

        self.msg_repo.delete_messages(
            conversation_id
        )

        self.conv_repo.delete_conversation(
            conversation_id
        )