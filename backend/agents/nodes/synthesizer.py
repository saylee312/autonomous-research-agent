from backend.core.llm import get_llm

llm = get_llm()


def synthesizer_node(state):

    research = "\n".join(
        state["research_results"]
    )
    
    query = state.get("query", "Unknown topic")

    prompt = f"""
Synthesize the following research findings about: {query}

Remove duplicates.

Highlight important insights.

Focus on the topic: {query}

Research:

{research}
"""

    result = llm.invoke(
        prompt
    )

    state[
        "synthesized_content"
    ] = result.content

    return state