from fastapi import FastAPI, UploadFile, File
import shutil, os

from ocr import extract_text_from_pdf
from extractor import extract_fields
from rules import run_validations
from risk import calculate_total_risk

from schemas import POMatchRequest
from po_match_agent import po_match
from explanation_agent import generate_explanation


app = FastAPI()

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/invoice/upload")
async def upload_invoice(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    raw_text = extract_text_from_pdf(file_path)

    # Step 2 pipeline
    from ai_parser import parse_invoice
    extracted_data = parse_invoice(raw_text)

    validation_results = run_validations(extracted_data)

    po_result = po_match({
        "supplier": extracted_data["supplier"],
        "line_items": extracted_data["line_items"]
    })

    risk_score, status = calculate_total_risk(
        validation_results,
        po_result
    )

    explanation = generate_explanation({
        "invoice_number": extracted_data["invoice_no"],
        "supplier": extracted_data["supplier"],
        "validations": validation_results,
        "po_matches": po_result,
        "risk_score": risk_score,
        "final_status": status
    })

    return {
        "filename": file.filename,
        "extracted_data": extracted_data,
        "validations": validation_results,
        "risk_score": risk_score,
        "po_matches": po_result,
        "final_status": status,
        "explanation": explanation
    }

@app.post("/po/match")
def match_po(req: POMatchRequest):
    
    results = po_match(req.dict())

    risk = 0

    for r in results:
        if r["status"] == "NO_PO_MATCH":
            risk += 40
        elif r["status"] == "MISMATCH":
            risk += 20

    status = (
        "AUTO_APPROVE"
        if risk < 20
        else "NEEDS_REVIEW"
        if risk < 50
        else "REJECT"
    )

    return {
        "po_matches": results,
        "po_risk_score": risk,
        "po_status": status
    }
