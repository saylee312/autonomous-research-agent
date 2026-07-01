from backend.core.llm import get_llm
from backend.services.mode_detector import detect_mode
from backend.services.context_manager import build_chat_context
from backend.services.rag_router import handle_rag_query
from backend.database.chat_repository import ChatRepository


llm = get_llm()
repo = ChatRepository()


class UnifiedChatService:

    def chat(self, session_id: str, message: str):
        repo.add_message(session_id, "user", message)

        mode = detect_mode(message)
        chat_history = build_chat_context(session_id)

        response = ""

        if mode == "rag":
            rag_result = handle_rag_query(message)
            response = rag_result.get("answer", "No answer found.")
        else:
            messages = list(chat_history)
            messages.append({"role": "user", "content": message})
            response = llm.invoke(messages).content

        repo.add_message(session_id, "assistant", response)
        repo.add_message(session_id, "assistant", response)

        return response