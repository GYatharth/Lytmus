"""
Pulls paper metadata + abstracts from arXiv to seed the local corpus.

arXiv's API is free, requires no auth, and returns Atom XML.
Docs: https://info.arxiv.org/help/api/user-manual.html

Suggested starting categories (adjust to taste):
  cs.CL - Computation and Language (NLP)
  cs.LG - Machine Learning
  cs.IR - Information Retrieval

Usage (once implemented):
  python scripts/fetch_arxiv.py --category cs.CL --max_results 200
"""

import argparse

ARXIV_API_URL = "http://export.arxiv.org/api/query"


def fetch_papers(category: str, max_results: int = 100) -> list[dict]:
    """
    Query the arXiv API for a given category and return a list of:
    [{"title": str, "abstract": str, "url": str, "published": str}, ...]

    TODO: build the query string, parse the Atom XML response
    (use `feedparser` or `xml.etree.ElementTree`), handle pagination
    if max_results > 100 (arXiv paginates at 100 per request).
    """
    raise NotImplementedError


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", default="cs.CL")
    parser.add_argument("--max_results", type=int, default=100)
    args = parser.parse_args()

    papers = fetch_papers(args.category, args.max_results)
    print(f"Fetched {len(papers)} papers from {args.category}")
