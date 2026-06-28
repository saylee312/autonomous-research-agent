import uuid

from backend.rag.embeddings import embeddings
from backend.rag.vector_store import collection


def ingest_chunks(chunks):

    print(f"\nReceived chunks: {len(chunks)}")

    if not chunks:
        raise ValueError(
            "No chunks generated from document"
        )

    texts = []
    metadatas = []
    ids = []

    for chunk in chunks:

        content = chunk.get(
            "content",
            ""
        )

        if not content or not content.strip():
            continue

        ids.append(
            str(uuid.uuid4())
        )

        texts.append(
            content
        )

        metadatas.append(
            chunk.get(
                "metadata",
                {}
            )
        )

    print(
        f"Valid texts: {len(texts)}"
    )

    if texts:
        print(
            "First text preview:",
            texts[0][:300]
        )

    if not texts:
        raise ValueError(
            "All generated chunks are empty"
        )

    try:

        vectors = embeddings.embed_documents(
            texts
        )

    except Exception as e:

        print(
            "Embedding error:",
            str(e)
        )

        raise

    print(
        f"Embeddings generated: {len(vectors)}"
    )

    if not vectors:
        raise ValueError(
            "Embedding model returned empty list"
        )

    collection.upsert(
        ids=ids,
        embeddings=vectors,
        documents=texts,
        metadatas=metadatas
    )

    print(
        f"Inserted {len(ids)} chunks into Chroma"
    )

    return len(ids)