import json
import time

from backend.core.llm import get_llm
from backend.core.logger import logger

llm = get_llm()


def planner_node(state):
    """Break down research query into specific tasks.
    
    Uses LLM to create 3-5 focused research subtasks from the main query.
    """
    query = state["query"]
    
    logger.info(f"Planning research tasks for query: {query}")
    start = time.time()

    prompt = f"""
You are a research planner.

Break the topic into 3-5 key research tasks.

Return ONLY JSON array with 3-5 items.

Topic:

{query}
"""

    result = llm.invoke(prompt)

    try:

        plan = json.loads(
            result.content
        )

    except:

        plan = [
            query
        ]
    
    elapsed = time.time() - start
    logger.info(f"Created {len(plan)} tasks in {elapsed:.2f}s")

    state["plan"] = plan

    return state