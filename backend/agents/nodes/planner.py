import json
import time

from backend.core.llm import get_llm

llm = get_llm()


def planner_node(state):

    query = state["query"]
    
    print(f"\n[TIMING] Planner: Breaking down query into tasks...")
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
    print(f"[TIMING] Planner created {len(plan)} tasks in {elapsed:.2f}s: {plan}")

    state["plan"] = plan

    return state