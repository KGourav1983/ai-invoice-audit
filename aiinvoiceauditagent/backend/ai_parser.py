import json
import os
from openai import OpenAI


# ======================
# OpenRouter Client
# ======================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY environment variable not set")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


# ======================
# Prompts
# ======================

SYSTEM_PROMPT = """
You are an invoice extraction agent.

Convert OCR invoice text into STRICT JSON ONLY matching exactly this schema:

{
  "invoice_no": "",
  "invoice_date": "",
  "supplier": "",
  "gst_id": "",
  "line_items":[
      {"description":"", "qty":0, "unit_price":0, "amount":0}
  ],
  "subtotal":0,
  "tax_amount":0,
  "total":0
}

Rules:
- RESPOND WITH JSON ONLY
- No markdown, no explanations, no surrounding text
- Do not leave any field empty (use "" or 0)
"""


# ======================
# Core Parser Function
# ======================

def parse_invoice(ocr_text: str):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": ocr_text},
        ],
        temperature=0,
        max_tokens=1000
    )

    raw_content = response.choices[0].message.content

    print("\n------ RAW MODEL OUTPUT ------\n")
    print(raw_content)
    print("\n------------------------------\n")

    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Model returned invalid JSON: {e}\n\nRAW OUTPUT:\n{raw_content}"
        )

    return data
