from backend.core.llm import get_llm
from backend.rag.retriever import retrieve_chunks
from backend.rag.context_builder import build_context

llm = get_llm()


def ask_rag(query: str, document_id: str = None):

    results = retrieve_chunks(
        query=query,
        top_k=5,
        document_id=document_id   # 🔥 PASS FILTER
    )

    context = build_context(results)

    if not context.strip():
        return {
            "answer": "I don't know based on the documents.",
            "context_used": ""
        }

    prompt = f"""
You are a research assistant.

Use ONLY the context below.

CONTEXT:
{context}

QUESTION:
{query}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "context_used": context
    }