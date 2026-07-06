"""
Citation graph: shows how the papers cited in an answer relate to each
other (which cite each other, which are outliers) — only meaningful
because the corpus is structured research literature, not general web
pages. Rendered in the Streamlit UI alongside the flat citation list.
"""


def build_citation_graph(cited_papers: list[dict]) -> dict:
    """
    Returns a graph structure: {"nodes": [...], "edges": [...]} where edges
    represent citation relationships between the papers used in the answer.

    TODO: arXiv doesn't return citation links directly in its API response —
    consider Semantic Scholar API for citation data, keyed by arXiv ID.
    """
    raise NotImplementedError
