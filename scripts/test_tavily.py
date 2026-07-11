# scripts/test_tavily.py
"""
Tavily smoke test — confirms your API key works and shows the raw
search response shape (built for LLM agents, cleaner than scraping
raw Google results yourself).

Setup:
  1. Get a free API key at https://tavily.com
  2. Add to your .env file:
       TAVILY_API_KEY=your_key_here
  3. pip install -r requirements.txt
  4. python scripts/test_tavily.py
"""

import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

response = client.search(
    query="latest advances in retrieval-augmented generation 2026",
    max_results=5,
)

print("--- Results ---")
for result in response["results"]:
    print(f"\nTitle: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Content snippet: {result['content'][:150]}...")