from backend.core.llm import get_llm

llm = get_llm()


def response_generator_node(state):

    result = llm.invoke(
        f"""
Question:

{state['user_message']}

Tool Result:

{state['tool_result']}

Generate helpful answer.
"""
    )

    state["response"] = (
        result.content
    )

    return state