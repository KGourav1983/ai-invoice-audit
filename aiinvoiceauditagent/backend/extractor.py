import re

def extract_fields(text: str):

    def find(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    data = {
        "invoice_no": find(r"(INV[-\s]?\d+)"),
        "gst_id": find(r"\b(\d{2}[A-Z]{5}\d{4}[A-Z][A-Z\d]Z[A-Z\d])\b"),
        "tax_amount": find(r"\b(?:GST|TAX)[:\s₹]*([\d,]+)"),
        "total": find(r"Total[:\s₹]*([\d,]+)")
    }

    if data["tax_amount"]:
        data["tax_amount"] = int(data["tax_amount"].replace(",", ""))

    if data["total"]:
        data["total"] = int(data["total"].replace(",", ""))

    return data
