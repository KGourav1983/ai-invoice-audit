import json
import numpy as np

from embedding import embed

with open("po_store.json") as f:
    POs = json.load(f)

PO_EMBEDDINGS = []

for po in POs:
    for item in po["items"]:
        vector = embed(item["description"])

        PO_EMBEDDINGS.append({
            "po_id": po["po_id"],
            "supplier": po["supplier"],
            "item_id": item["item_id"],
            "description": item["description"],
            "qty": item["qty"],
            "unit_price": item["unit_price"],
            "embedding": vector
        })
