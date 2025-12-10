def calculate_risk(results):

    score = 0

    if not results["line_total_matches"]:
        score += 25

    if not results["final_total_matches"]:
        score += 25

    if score < 20:
        status = "AUTO_APPROVE"
    elif score < 50:
        status = "NEEDS_REVIEW"
    else:
        status = "REJECT"

    return score, status
