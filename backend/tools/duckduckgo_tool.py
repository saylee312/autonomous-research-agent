from ddgs import DDGS
import time


def search_duckduckgo(query: str, max_results: int = 3) -> str:
    """
    Search DuckDuckGo with error handling.
    
    Args:
        query: Search query string
        max_results: Maximum number of results (default: 3)
    
    Returns:
        String representation of results
    """
    
    try:
        # Handle dict input (defensive)
        if isinstance(query, dict):
            query = query.get("task", str(query))
        
        query = str(query).strip()
        if not query:
            return ""
        
        start = time.time()
        
        results = DDGS().text(
            query,
            max_results=max_results
        )
        
        elapsed = time.time() - start
        print(f"[PERF] DuckDuckGo search took {elapsed:.2f}s ({len(results) if results else 0} results)")
        
        return str(results) if results else ""
    
    except Exception as e:
        print(f"[ERROR] DuckDuckGo search failed: {str(e)}")
        return f"[DuckDuckGo Error: {str(e)}]"