# scripts/test_groq.py
"""
Groq smoke test — confirms your API key works and shows the raw
request/response shape before anything gets wrapped in LangChain.

Setup:
  1. Get a free API key at https://console.groq.com/keys
  2. Create a .env file in the project root with:
       GROQ_API_KEY=your_key_here
  3. pip install -r requirements.txt
  4. python scripts/test_groq.py
"""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "You are a concise research assistant.",
        },
        {
            "role": "user",
            "content": "In one sentence, what is retrieval-augmented generation?",
        },
    ],
    temperature=0,
    max_tokens=100,
)

print("--- Response text ---")
print(response.choices[0].message.content)

print("\n--- Token usage ---")
print(response.usage)