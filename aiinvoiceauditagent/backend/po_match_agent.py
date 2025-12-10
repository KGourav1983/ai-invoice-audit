from embedding import embed
from matcher import find_best_po_match
from po_index import PO_EMBEDDINGS
import re

def clean_text(text):
    text = re.sub(r"\d+", "", text)             # remove digits
    text = re.sub(r"[^\w\s]", "", text)         # remove punctuation
    text = re.sub(r"\s+", " ", text)            # collapse spaces
    return text.strip().lower()


def po_match(invoice_data):

    matches = []

    for item in invoice_data["line_items"]:

        cleaned = clean_text(item["description"])
        inv_vector = embed(cleaned)

        po_line, similarity = find_best_po_match(
            invoice_item=item,
            invoice_vector=inv_vector,
            po_vectors=PO_EMBEDDINGS
        )

        if not po_line:
            matches.append({
                "invoice_item": item,
                "status": "NO_PO_MATCH",
                "similarity": similarity
            })
            continue

        issues = []

        if item["qty"] > po_line["qty"]:
            issues.append("QTY_EXCEEDS_PO")

        if item["unit_price"] > po_line["unit_price"]:
            issues.append("PRICE_EXCEEDS_PO")

        status = "MATCH" if not issues else "MISMATCH"

        matches.append({
            "invoice_item": item,
            "po_item": {
                "po_id": po_line["po_id"],
                "supplier": po_line["supplier"],
                "item_id": po_line["item_id"],
                "description": po_line["description"],
                "qty": po_line["qty"],
                "unit_price": po_line["unit_price"]
            },
            "status": status,
            "similarity": round(similarity, 3),
            "issues": issues
        })

    return matches
