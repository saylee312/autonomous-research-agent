import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from backend.tools.tavily_tool import (
    search_tavily
)

from backend.tools.wikipedia_tool import (
    search_wikipedia
)

from backend.tools.arxiv_tool import (
    search_arxiv
)

from backend.tools.duckduckgo_tool import (
    search_duckduckgo
)


def researcher_node(state):

    findings = []
    
    print(f"\n[TIMING] Researcher: Starting research on {len(state['plan'])} tasks...")
    research_start = time.time()

    # Process tasks in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {}
        
        for task_idx, task in enumerate(state["plan"], 1):
            # Extract task query string
            task_query = task["task"] if isinstance(task, dict) else str(task)
            
            # Submit all 4 searches for this task
            future_tavily = executor.submit(search_tavily, task_query)
            future_wiki = executor.submit(search_wikipedia, task_query)
            future_arxiv = executor.submit(search_arxiv, task_query)
            future_ddg = executor.submit(search_duckduckgo, task_query)
            
            futures[future_tavily] = ("Tavily", task_idx, len(state["plan"]))
            futures[future_wiki] = ("Wikipedia", task_idx, len(state["plan"]))
            futures[future_arxiv] = ("ArXiv", task_idx, len(state["plan"]))
            futures[future_ddg] = ("DuckDuckGo", task_idx, len(state["plan"]))
        
        # Collect results as they complete
        for future in as_completed(futures):
            tool_name, task_idx, total = futures[future]
            try:
                result = future.result(timeout=10)
                if result:
                    findings.append(result)
            except Exception as e:
                findings.append(f"[{tool_name} Error: {str(e)}]")

    research_time = time.time() - research_start
    print(f"[TIMING] All research completed in {research_time:.2f}s ({len(findings)} results)")
    
    state["research_results"] = findings

    return state