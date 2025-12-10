from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def embed(text: str):
    response = client.embeddings.create(
        model="openai/text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding
