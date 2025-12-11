import base64
import os
from openai import OpenAI
import pypdfium2 as pdfium

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def extract_text_from_pdf(pdf_path: str) -> str:
    pdf = pdfium.PdfDocument(pdf_path)
    full_text = ""

    for i in range(len(pdf)):
        page = pdf[i]
        pil_image = page.render(scale=2).to_pil()
        
        # Convert to PNG bytes
        import io
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        img_bytes = buffer.getvalue()

        img_b64 = base64.b64encode(img_bytes).decode("utf-8")

        # Send page image to OpenRouter Vision model
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract all readable text from this invoice page."
                        },
                        {
                            "type": "image_url",
                            "image_url": f"data:image/png;base64,{img_b64}"
                        }
                    ]
                }
            ]
        )

        page_text = response.choices[0].message.content
        full_text += page_text + "\n\n"

    return full_text
