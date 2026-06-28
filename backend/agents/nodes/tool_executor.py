from backend.tools.calculator import (
    calculator
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

from backend.tools.tavily_tool import (
    search_tavily
)


def tool_executor_node(state):

    tool = state["selected_tool"]

    query = state["user_message"]

    if tool == "calculator":

        result = calculator(query)

    elif tool == "wikipedia":

        result = search_wikipedia(query)

    elif tool == "arxiv":

        result = search_arxiv(query)

    elif tool == "duckduckgo":

        result = search_duckduckgo(query)

    else:

        result = search_tavily(query)

    state["tool_result"] = result

    return state