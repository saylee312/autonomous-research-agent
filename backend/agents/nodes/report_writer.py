from backend.core.llm import get_llm

llm = get_llm()


def report_writer_node(state):
    
    query = state.get("query", "Unknown topic")

    prompt = f"""
Create a professional research report about: {query}

Use the following synthesized content:

{state['synthesized_content']}

The report should be well-structured with:
- Title related to: {query}
- Executive Summary
- Main findings about: {query}
- Detailed sections
- Conclusion

Focus on answering questions about: {query}
"""

    result = llm.invoke(
        prompt
    )

    state["report"] = (
        result.content
    )

    return state