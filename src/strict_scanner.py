import os
import json
from typing import List, Dict, Any
from pypdf import PdfReader
from docx import Document

class StrictDocumentScanner:
    def __init__(self, country_code: str):
        self.rules = self._load_json_rules(country_code)

    def _load_json_rules(self, country_code: str) -> Dict[str, Any]:
        file_path = f"database/{country_code}.json"
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "agency": "Global Regulatory Baseline",
            "required_keywords": ["Adverse Event Protocol"],
            "restricted_terms": ["guaranteed cure"]
        }

    def extract_text(self, file_bytes_or_path, file_type: str) -> List[str]:
        lines = []
        if file_type == "pdf":
            reader = PdfReader(file_bytes_or_path)
            for page in reader.pages:
                text = page.extract_text() or ""
                lines.extend(text.splitlines())
            
            # OCR Fallback for scanned PDFs
            if not "".join(lines).strip():
                try:
                    import pytesseract
                    from pdf2image import convert_from_bytes
                    images = convert_from_bytes(file_bytes_or_path.read())
                    for img in images:
                        ocr_text = pytesseract.image_to_string(img)
                        lines.extend(ocr_text.splitlines())
                except Exception:
                    pass

        elif file_type == "docx":
            doc = Document(file_bytes_or_path)
            for paragraph in doc.paragraphs:
                lines.append(paragraph.text)
        else:
            if isinstance(file_bytes_or_path, str):
                with open(file_bytes_or_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = [line.strip() for line in f.readlines()]
            else:
                lines = [line.decode('utf-8', errors='ignore').strip() for line in file_bytes_or_path.readlines()]

        return [line for line in lines if line.strip()]

    def scan_content(self, lines: List[str]) -> Dict[str, Any]:
        errors = []
        full_text = " ".join(lines).lower()

        for line_num, line_content in enumerate(lines, 1):
            for restricted in self.rules.get("restricted_terms", []):
                if restricted.lower() in line_content.lower():
                    errors.append({
                        "line": line_num,
                        "type": "FORBIDDEN_TERM",
                        "severity": "CRITICAL",
                        "text": line_content.strip(),
                        "reason": f"Prohibited phrasing for {self.rules['agency']}: '{restricted}'"
                    })

        for req in self.rules.get("required_keywords", []):
            if req.lower() not in full_text:
                errors.append({
                    "line": 0,
                    "type": "MISSING_REQUIREMENT",
                    "severity": "HIGH",
                    "text": f"Missing Mandate: '{req}'",
                    "reason": f"Required statutory parameter for {self.rules['agency']} is missing."
                })

        return {
            "agency": self.rules['agency'],
            "total_lines": len(lines),
            "total_errors": len(errors),
            "status": "APPROVED" if len(errors) == 0 else "REJECTED",
            "errors": errors
        }