import uuid

from backend.rag.embeddings import embeddings
from backend.rag.vector_store import collection
from backend.core.logger import logger


def ingest_chunks(chunks):
    """Ingest and embed text chunks into vector store.
    
    Args:
        chunks: List of text chunks with metadata
    
    Returns:
        List of chunk IDs in vector store
    """
    logger.debug(f"Ingesting {len(chunks)} chunks")

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

    logger.debug(f"Valid texts: {len(texts)}")

    if texts:
        logger.debug(f"First text preview (300 chars): {texts[0][:300]}")

    if not texts:
        raise ValueError(
            "All generated chunks are empty"
        )

    try:

        vectors = embeddings.embed_documents(
            texts
        )

    except Exception as e:

        logger.error(f"Embedding error: {str(e)}")
        raise

    logger.debug(f"Embeddings generated: {len(vectors)}")

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

    logger.info(f"Inserted {len(ids)} chunks into vector store")

    return len(ids)