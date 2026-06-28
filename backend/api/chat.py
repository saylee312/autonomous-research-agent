from fastapi import APIRouter

from backend.schemas.chat import ChatRequest

from backend.services.chat_service import ChatService


router = APIRouter()

service = ChatService()


@router.post("")
async def chat(request: ChatRequest):

    response = service.chat(
        request.session_id,
        request.message,
        use_search=request.use_search
    )

    return {
        "response": response
    }