import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:3b"


def generate_answer(question, context):
    prompt = f"""
You are GenCodeX, an AI assistant that explains software repositories.

Answer the user's question using only the provided code context.

If the context does not contain enough information, say that clearly.

Keep the explanation clear and useful for a developer.

Code context:
{context}

User question:
{question}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]