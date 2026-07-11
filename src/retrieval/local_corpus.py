"""
Local corpus retrieval via a FAISS vector index built from a curated document set.

Uses cosine similarity for search — implemented as inner product over
L2-normalized vectors (IndexFlatIP + normalize_L2), which is mathematically
equivalent to cosine similarity but avoids needing a separate distance type.
"""

import json
import os

import faiss
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

_model = None


def _get_model() -> SentenceTransformer:
    """
    Lazy-load the embedding model so importing this module doesn't trigger
    a model download until it's actually needed.
    """
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def load_papers(data_dir: str = "data") -> list[dict]:
    """
    Load and combine all fetched arXiv paper JSON files
    (data/arxiv_*.json) from data_dir into one list.

    Deduplicates by URL — a paper tagged with multiple arXiv categories
    (e.g. both cs.CL and cs.LG) would otherwise be pulled once per
    category file and end up duplicated in the corpus.
    """
    papers = []
    seen_urls = set()

    for filename in sorted(os.listdir(data_dir)):
        if filename.startswith("arxiv_") and filename.endswith(".json"):
            path = os.path.join(data_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                for paper in json.load(f):
                    if paper["url"] not in seen_urls:
                        seen_urls.add(paper["url"])
                        papers.append(paper)

    return papers


def build_index(
    papers: list[dict],
    index_path: str = "data/faiss_index.index",
    metadata_path: str = "data/faiss_metadata.json",
) -> None:
    """
    Embed each paper (title + abstract combined) and build a FAISS index.
    Saves both the index and a metadata file (so search results can be
    mapped back to the original paper info).
    """
    model = _get_model()

    texts = [f"{p['title']}. {p['abstract']}" for p in papers]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    faiss.write_index(index, index_path)

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2)

    print(f"Indexed {len(papers)} papers -> {index_path}")


def search_local(
    query: str,
    index_path: str = "data/faiss_index.index",
    metadata_path: str = "data/faiss_metadata.json",
    k: int = 5,
) -> list[dict]:
    """
    Query the FAISS index and return the top-k matching papers,
    each with a cosine similarity score attached.
    """
    model = _get_model()
    index = faiss.read_index(index_path)

    with open(metadata_path, "r", encoding="utf-8") as f:
        papers = json.load(f)

    query_vec = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_vec)

    scores, indices = index.search(query_vec, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        paper = papers[idx]
        results.append({**paper, "score": float(score)})

    return results