from backend.rag.embeddings import embeddings
from backend.rag.vector_store import collection
from backend.core.logger import logger


def retrieve_chunks(query, top_k=5, document_id=None):
    """Retrieve semantically similar chunks from vector store.
    
    Args:
        query: Search query string
        top_k: Number of results to return
        document_id: Optional document filter
    
    Returns:
        Query results with documents and metadata
    """
    logger.debug(f"Retrieving {top_k} chunks for query: {query} (filter: {document_id})")
    
    # Embed query
    query_vector = embeddings.embed_query(query)
    
    # Build optional document filter
    where_filter = None
    if document_id:
        where_filter = {"document_id": document_id}
    
    # Query Chroma with optional filtering
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        where=where_filter
    )
    
    docs = results.get("documents", [[]])[0]
    logger.debug(f"Retrieved {len(docs)} documents")
    
    return results