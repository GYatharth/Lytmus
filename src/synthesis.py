"""
Synthesis engine: builds a citation-grounded answer from merged retrieval results.
"""


def synthesize_answer(query: str, retrieved_chunks: list[dict]) -> dict:
    """
    Generate a final answer with inline citations back to source chunks.

    Returns: {"answer": str, "claims": [{"text": str, "source_ids": [int]}]}

    TODO: prompt design for claim-level citation attribution.
    """
    raise NotImplementedError
