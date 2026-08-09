import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class CertificateGenerator:
    """Generates a professional PDF Compliance Certificate in memory."""
    
    @staticmethod
    def create_pdf(agency_name: str, doc_name: str, total_lines: int) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        story = []
        
        styles = getSampleStyleSheet()
        
        # Title Style
        title_style = ParagraphStyle(
            'CertTitle',
            parent=styles['Heading1'],
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#0A2540"),
            alignment=1, # Center
            spaceAfter=20
        )
        
        subtitle_style = ParagraphStyle(
            'CertSub',
            parent=styles['Normal'],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#28A745"),
            alignment=1,
            spaceAfter=30
        )
        
        body_style = ParagraphStyle(
            'CertBody',
            parent=styles['Normal'],
            fontSize=11,
            leading=16,
            textColor=colors.HexColor("#333333"),
            spaceAfter=12
        )

        # Header Elements
        story.append(Paragraph("REGUAI COMPLIANCE VERIFICATION", title_style))
        story.append(Paragraph("OFFICIAL CERTIFICATE OF REGULATORY COMPLIANCE", subtitle_style))
        story.append(Spacer(1, 15))

        # Certificate Body Text
        cert_text = f"""
        This is to officially certify that the submitted regulatory dossier/document titled 
        <b>"{doc_name}"</b> ({total_lines} lines analyzed) has undergone full deterministic 
        automated compliance auditing against the statutory guidelines established by:
        <br/><br/>
        <font size="13" color="#0A2540"><b>Authority Agency: {agency_name}</b></font>
        <br/><br/>
        <b>Audit Status: PASSED (100% Compliant)</b><br/>
        No regulatory violations, restricted phrasing, or missing required statutory modules were detected during the automated audit scan.
        """
        story.append(Paragraph(cert_text, body_style))
        story.append(Spacer(1, 20))

        # Audit Summary Table
        data = [
            ["Verification Metric", "Result Status"],
            ["Target Regulatory Body", agency_name],
            ["Document Source File", doc_name],
            ["Critical Violations Found", "0 (Zero)"],
            ["Global Mandatory Deficiencies", "0 (Zero)"],
            ["Final Audit Verdict", "APPROVED / COMPLIANT"]
        ]

        t = Table(data, colWidths=[250, 250])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0A2540")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8F9FA")),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#DEE2E6")),
        ]))
        story.append(t)
        
        story.append(Spacer(1, 40))
        story.append(Paragraph("<i>Generated automatically by ReguAI Global Compliance Platform. Valid for pre-submission verification.</i>", ParagraphStyle('Footer', parent=styles['Italic'], fontSize=9, alignment=1, textColor=colors.gray)))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()