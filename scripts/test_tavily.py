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