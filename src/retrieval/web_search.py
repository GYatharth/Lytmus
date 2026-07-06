"""
Web retrieval via Tavily API.
"""


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Run a live web search and return normalized results:
    [{"title": str, "url": str, "content": str}, ...]

    TODO: wire up Tavily client, handle rate limits / retries.
    """
    raise NotImplementedError
