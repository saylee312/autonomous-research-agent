from backend.tools.tavily_tool import (
    search_tavily
)

TOOL_REGISTRY = {}

TOOL_REGISTRY["tavily"] = (
    search_tavily
)
