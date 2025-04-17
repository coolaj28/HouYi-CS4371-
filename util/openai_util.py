from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)

def completion_with_chatgpt(text: str, model: str = "gpt-4o") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content