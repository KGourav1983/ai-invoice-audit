def calculate_total_risk(invoice_validations, po_matches):

    score = 0

    # ✅ Invoice rules
    if not invoice_validations["line_total_matches"]:
        score += 25

    if not invoice_validations["final_total_matches"]:
        score += 25

    if not invoice_validations["gst_present"]:
        score += 15

    # ✅ PO mismatches
    for r in po_matches:
        if r["status"] == "NO_PO_MATCH":
            score += 40
        elif r["status"] == "MISMATCH":
            score += 20

    # ✅ Final classification
    if score < 20:
        status = "AUTO_APPROVE"
    elif score < 50:
        status = "NEEDS_REVIEW"
    else:
        status = "REJECT"

    return score, status
