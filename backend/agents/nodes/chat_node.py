from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from backend.core.llm import get_llm


llm = get_llm()


def chat_node(state):

    messages = []

    for msg in state["messages"]:

        if msg["role"] == "user":

            messages.append(
                HumanMessage(
                    content=msg["content"]
                )
            )

        elif msg["role"] == "assistant":

            messages.append(
                AIMessage(
                    content=msg["content"]
                )
            )

    messages.append(
        HumanMessage(
            content=state["user_message"]
        )
    )

    result = llm.invoke(
        messages
    )

    state["response"] = (
        result.content
    )

    return state