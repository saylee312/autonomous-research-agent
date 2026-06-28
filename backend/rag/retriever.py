from backend.rag.embeddings import embeddings
from backend.rag.vector_store import collection


def retrieve_chunks(query, top_k=5, document_id=None):

    print("\n========== RETRIEVER ==========")
    print("Query:", query)
    print("Document filter:", document_id)

    # 1. Embed query
    query_vector = embeddings.embed_query(query)

    print("Embedding dimension:", len(query_vector))

    # 2. Build filter (THIS IS THE FIX)
    where_filter = None

    if document_id:
        where_filter = {
            "document_id": document_id
        }

    # 3. Query Chroma with optional filtering
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        where=where_filter  # 🔥 KEY FIX
    )

    # 4. Debug logs
    print("Results keys:", results.keys())

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    print("Documents found:", len(docs))

    # 5. Return structured results
    return results