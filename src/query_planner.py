"""
Query planner: decomposes a user's research question into sub-questions
that can be answered independently via web search and/or local corpus retrieval.
"""


def decompose_query(query: str) -> list[str]:
    """
    Break a complex or multi-part query into atomic sub-questions.

    TODO: implement via Groq-backed LLM call with a structured output schema
    (list[str]) instead of relying on free-text parsing.
    """
    raise NotImplementedError
