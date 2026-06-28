"""Simple script to check tool outputs.
Run with: python backend/tools/tools_check.py
"""
from backend.tools.tavily_tool import search_tavily
from backend.tools.wikipedia_tool import search_wikipedia
from backend.tools.arxiv_tool import search_arxiv
from backend.tools.duckduckgo_tool import search_duckduckgo


def run_checks(query="todays weather"):
    print(f"Checking tools with query: {query}\n")

    try:
        print("Tavily result:\n", search_tavily(query), "\n")
    except Exception as e:
        print("Tavily error:", e)

    try:
        print("Wikipedia result:\n", search_wikipedia(query), "\n")
    except Exception as e:
        print("Wikipedia error:", e)

    try:
        print("ArXiv result:\n", search_arxiv(query), "\n")
    except Exception as e:
        print("ArXiv error:", e)

    try:
        print("DuckDuckGo result:\n", search_duckduckgo(query), "\n")
    except Exception as e:
        print("DuckDuckGo error:", e)


if __name__ == "__main__":
    run_checks()
