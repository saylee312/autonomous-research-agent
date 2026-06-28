from fastapi import APIRouter

from backend.database.chat_repository import ChatRepository

router = APIRouter()

repo = ChatRepository()


@router.post("/")
async def create_session():
    return repo.create_session()


@router.get("/")
async def get_sessions():
    return repo.get_sessions()


@router.get("/{session_id}")
async def get_session(session_id: str):
    return repo.get_messages(session_id)


@router.delete("/{session_id}")
async def delete_session(session_id: str):

    repo.delete_session(session_id)

    return {
        "message": "deleted"
    }