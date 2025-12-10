import re

def validate_gst(gst):
    if not gst:
        return False
    return bool(re.match(
        r"\d{2}[A-Z]{5}\d{4}[A-Z][A-Z\d]Z[A-Z\d]",
        gst
    ))

def validate_total(total):
    return isinstance(total, int) and total > 0

def validate_totals(data):

    items_sum = sum(
        item.get("amount",0)
        for item in data.get("line_items", [])
    )

    subtotal = data.get("subtotal", 0)
    tax      = data.get("tax_amount", 0)
    total    = data.get("total", 0)

    return {
        "line_total_matches": items_sum == subtotal,
        "final_total_matches": (subtotal + tax) == total
    }

def run_validations(data):

    line_items = data.get("line_items", [])
    subtotal   = data.get("subtotal", 0) or 0
    tax        = data.get("tax_amount", 0) or 0
    total      = data.get("total", 0) or 0

    # Sum all line item amounts
    calc_subtotal = sum(item.get("amount", 0) or 0 for item in line_items)

    results = {
        "line_total_matches": abs(calc_subtotal - subtotal) < 0.01,
        "final_total_matches": abs((subtotal + tax) - total) < 0.01,
        "gst_present": bool(data.get("gst_id"))
    }

    return results

