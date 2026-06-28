from backend.core.llm import get_llm

llm = get_llm()


def router_node(state):

    query = state["query"]

    prompt = f"""
Classify the query.

Routes:

chat
rag
research
tool

Return ONLY one route.

Query:

{query}
"""

    result = llm.invoke(prompt)

    state["route"] = (
        result.content
        .strip()
        .lower()
    )

    return state