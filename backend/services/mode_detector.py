def detect_mode(message: str):

    msg = message.lower()

    # RAG indicators
    rag_keywords = [
        "document",
        "file",
        "pdf",
        "report",
        "upload",
        "data from",
        "in the file"
    ]

    # Tool indicators
    tool_keywords = [
        "+",
        "-",
        "*",
        "/",
        "calculate",
        "solve"
    ]

    if any(k in msg for k in rag_keywords):

        return "rag"

    if any(k in msg for k in tool_keywords):

        return "tool"

    return "chat"