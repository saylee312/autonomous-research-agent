import arxiv
import time
from backend.core.logger import logger
from typing import List, Dict


# Rate limiting: 3 requests per 10 seconds
ARXIV_MIN_INTERVAL = 3.33
last_request_time = 0


def _rate_limit():
    """Enforce rate limiting between arxiv requests"""
    global last_request_time
    
    elapsed = time.time() - last_request_time
    if elapsed < ARXIV_MIN_INTERVAL:
        time.sleep(ARXIV_MIN_INTERVAL - elapsed)
    
    last_request_time = time.time()


def search_arxiv(query: str, max_results: int = 3) -> str:
    """
    Search arxiv with retry logic and rate limiting using Client API.
    
    Args:
        query: Search query string
        max_results: Maximum number of results (default: 3)
    
    Returns:
        String representation of results
    """
    
    max_retries = 3
    retry_delay = 2
    client = arxiv.Client()
    
    for attempt in range(max_retries):
        try:
            # Enforce rate limiting
            _rate_limit()
            
            start = time.time()
            
            search = arxiv.Search(
                query=query,
                max_results=max_results
            )

            results: List[Dict] = []

            # Use new Client.results() API instead of deprecated Search.results()
            for paper in client.results(search):
                results.append(
                    {
                        "title": paper.title,
                        "summary": paper.summary,
                        "url": paper.entry_id
                    }
                )
            
            elapsed = time.time() - start
            logger.debug(f"ArXiv search completed in {elapsed:.2f}s ({len(results)} papers)")

            return str(results)
        
        except Exception as exc:
            error_msg = str(exc)
            
            # Rate limit error (429)
            if "429" in error_msg or "rate" in error_msg.lower():
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logger.warning(f"ArXiv rate limited. Retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    return f"[ArXiv Error: Rate limited after {max_retries} retries. Please try again later.]"
            
            # Other errors
            logger.error(f"ArXiv search failed: {error_msg}")
            return f"[ArXiv Error: {error_msg}]"
    
    return "[]"