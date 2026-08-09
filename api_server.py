from fastapi import FastAPI, UploadFile, File, Form
from src.strict_scanner import StrictDocumentScanner
from src.ai_fixer import RegulatoryAIFixer
import shutil
import os

app = FastAPI(
    title="ReguAI Commercial REST API",
    description="Automated Regulatory Verification & Compliance Endpoints for Enterprise Integrations",
    version="3.0.0"
)

@app.get("/")
def health_check():
    return {"status": "online", "platform": "ReguAI Regulatory Compliance Engine"}

@app.post("/api/v1/scan")
async def scan_dossier(
    jurisdiction: str = Form("US_FDA"),
    file: UploadFile = File(...)
):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    scanner = StrictDocumentScanner(jurisdiction)
    file_ext = file.filename.split(".")[-1].lower()
    
    lines = scanner.extract_text(temp_path, file_ext)
    results = scanner.scan_content(lines)

    if os.path.exists(temp_path):
        os.remove(temp_path)

    return {
        "filename": file.filename,
        "jurisdiction": jurisdiction,
        "audit_results": results
    }