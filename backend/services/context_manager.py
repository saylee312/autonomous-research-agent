from backend.database.chat_repository import ChatRepository

repo = ChatRepository()


def build_chat_context(session_id: str):

    messages = repo.get_messages(session_id)

    context = []

    for msg in messages[-10:]:  # last 10 messages

        context.append(
            {
                "role": msg["role"],
                "content": msg["content"]
            }
        )

    return context