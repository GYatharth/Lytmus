"""
Builds the FAISS index from all fetched arXiv paper JSON files in data/.
Run this after fetch_arxiv.py has pulled all the categories you want.

Usage:
  python scripts/build_index.py
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.retrieval.local_corpus import build_index, load_papers  # noqa: E402

if __name__ == "__main__":
    papers = load_papers("data")
    print(f"Loaded {len(papers)} papers total from data/")

    if not papers:
        print("No papers found — run fetch_arxiv.py first.")
        sys.exit(1)

    build_index(papers)