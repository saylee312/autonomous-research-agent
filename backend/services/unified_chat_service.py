from backend.core.llm import get_llm
from backend.services.mode_detector import detect_mode
from backend.services.context_manager import build_chat_context
from backend.services.rag_router import handle_rag_query
from backend.database.chat_repository import ChatRepository


llm = get_llm()
repo = ChatRepository()


class UnifiedChatService:

    def chat(self, session_id: str, message: str):

        # 1. Save user message
        repo.add_message(session_id, "user", message)

        # 2. Detect mode (rag vs normal chat)
        mode = detect_mode(message)

        # 3. Build chat history
        chat_history = build_chat_context(session_id)

        response = ""

        # -------------------------
        # RAG MODE
        # -------------------------
        if mode == "rag":

            rag_result = handle_rag_query(message)

            response = rag_result.get("answer", "No answer found.")

        # -------------------------
        # NORMAL CHAT MODE
        # -------------------------
        else:

            messages = list(chat_history)

            messages.append({
                "role": "user",
                "content": message
            })

            result = llm.invoke(messages)
            response = result.content

        # 4. Save assistant response
        repo.add_message(session_id, "assistant", response)

        return response