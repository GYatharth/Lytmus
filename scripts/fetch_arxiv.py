"""
Pulls paper metadata + abstracts from arXiv to seed the local corpus.

arXiv's API is free, requires no auth, and returns Atom XML — we use
feedparser since it already knows how to parse Atom/RSS feeds, instead
of hand-rolling XML parsing.

Docs: https://info.arxiv.org/help/api/user-manual.html

Suggested starting categories:
  cs.CL - Computation and Language (NLP)
  cs.LG - Machine Learning
  cs.IR - Information Retrieval

Usage:
  python scripts/fetch_arxiv.py --category cs.CL --max_results 200
"""

import argparse
import json
import os
import time
import urllib.parse

import feedparser

ARXIV_API_URL = "http://export.arxiv.org/api/query"
BATCH_SIZE = 100  # arXiv paginates at 100 results per request


def fetch_papers(category: str, max_results: int = 100) -> list[dict]:
    """
    Query the arXiv API for a given category and return a list of:
    [{"title": str, "abstract": str, "url": str, "published": str}, ...]
    """
    papers = []
    start = 0

    while len(papers) < max_results:
        n = min(BATCH_SIZE, max_results - len(papers))
        params = {
            "search_query": f"cat:{category}",
            "start": start,
            "max_results": n,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        url = f"{ARXIV_API_URL}?{urllib.parse.urlencode(params)}"

        feed = feedparser.parse(url)

        if not feed.entries:
            # No more results available for this category
            break

        for entry in feed.entries:
            papers.append(
                {
                    "title": entry.title.replace("\n", " ").strip(),
                    "abstract": entry.summary.replace("\n", " ").strip(),
                    "url": entry.id,
                    "published": entry.published,
                }
            )

        start += n

        # arXiv asks API users to wait ~3 seconds between requests —
        # this isn't optional politeness, it's their documented rate limit
        time.sleep(3)

    return papers


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", default="cs.CL")
    parser.add_argument("--max_results", type=int, default=100)
    args = parser.parse_args()

    papers = fetch_papers(args.category, args.max_results)
    print(f"Fetched {len(papers)} papers from {args.category}")

    os.makedirs("data", exist_ok=True)
    output_path = f"data/arxiv_{args.category.replace('.', '_')}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2)

    print(f"Saved to {output_path}")