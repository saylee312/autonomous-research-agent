from tavily import TavilyClient
from requests.exceptions import HTTPError

from backend.core.config import settings


client = TavilyClient(
    api_key=settings.TAVILY_API_KEY
)


def search_tavily(query):

    try:
        result = client.search(
            query=query,
            max_results=5
        )

        return str(result)

    except HTTPError as exc:
        response = getattr(exc, "response", None)
        if response is not None:
            return (
                f"Tavily search failed ({response.status_code}): "
                f"{response.text}"
            )
        return f"Tavily search failed: {str(exc)}"

    except Exception as exc:
        return f"Tavily search failed: {str(exc)}"
