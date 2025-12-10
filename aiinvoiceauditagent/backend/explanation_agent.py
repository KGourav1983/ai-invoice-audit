from openai import OpenAI
import os
import json

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

SYSTEM_PROMPT = """
You are a financial audit AI.

Explain invoice approval or rejection decisions in clear professional audit language.

Write:
- Short executive summary (2-3 lines)
- Bullet list of findings

Be factual. No speculation. Do not invent missing info.
"""

def generate_explanation(payload: dict):

    user_prompt = f"""
Explain this invoice decision:

{json.dumps(payload, indent=2)}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
        max_tokens=400
    )

    msg = response.choices[0].message

    # ✅ Handle OpenRouter / SDK differences safely
    if isinstance(msg.content, str) and msg.content.strip():
        return msg.content

    if isinstance(msg.content, list) and len(msg.content) > 0:
        return msg.content[0].get("text", "").strip()

    if hasattr(response.choices[0], "text"):
        return response.choices[0].text.strip()

    return "⚠️ AI explanation unavailable (empty model response)."
