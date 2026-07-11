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