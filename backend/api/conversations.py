from fastapi import APIRouter

from backend.services.conversation_service import (
    ConversationService
)


router = APIRouter()

service = ConversationService()


@router.post("")
async def create_chat():

    return service.create_chat()


@router.get("")
async def list_chats():

    return service.list_chats()


@router.get("/{conversation_id}")

async def get_messages(
    conversation_id: str
):

    return service.get_chat_messages(
        conversation_id
    )


@router.delete(
    "/{conversation_id}"
)
async def delete_chat(
    conversation_id: str
):

    service.delete_chat(
        conversation_id
    )

    return {
        "message":
        "deleted"
    }