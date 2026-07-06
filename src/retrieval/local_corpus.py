"""
Local corpus retrieval via a FAISS vector index built from a curated document set.
"""


def build_index(documents: list[str], index_path: str) -> None:
    """
    Embed documents with sentence-transformers and persist a FAISS index.

    TODO: choose embedding model, chunking strategy, and index type (Flat vs IVF).
    """
    raise NotImplementedError


def search_local(query: str, index_path: str, k: int = 5) -> list[dict]:
    """
    Query the FAISS index and return the top-k matching chunks with scores.
    """
    raise NotImplementedError
