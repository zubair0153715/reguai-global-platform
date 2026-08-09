import streamlit as st
import os
from src.strict_scanner import StrictDocumentScanner
from src.certificate_generator import CertificateGenerator
from src.ai_fixer import RegulatoryAIFixer
from src.ectd_exporter import eCTDExporter

st.set_page_config(page_title="ReguAI - Global Regulatory Suite", page_icon="🛡️", layout="wide")

st.title("🛡️ ReguAI Global Regulatory Compliance Engine")
st.markdown("AI-Powered Multi-Jurisdiction Dossier Verification, Groq Auto-Fix, & eCTD Package Exporter")

# Sidebar
st.sidebar.title("Target Jurisdiction")

country_options = {
    "US_FDA": "🇺🇸 US FDA (United States)",
    "EU_EMA": "🇪🇺 EU EMA (European Union)",
    "SA_SFDA": "🇸🇦 SFDA (Saudi Arabia)",
    "UAE_MOHAP": "🇦🇪 MOHAP (United Arab Emirates)",
    "PK_DRAP": "🇵🇰 DRAP (Pakistan)"
}

selected_code = st.sidebar.selectbox("Select Authority", list(country_options.keys()), format_func=lambda x: country_options[x])

scanner = StrictDocumentScanner(selected_code)
st.sidebar.success(f"Active Engine: **{scanner.rules['agency']}**")

# Groq API Input
groq_key = st.sidebar.text_input("Groq API Key (For AI Auto-Fixer)", type="password")

# File Upload
uploaded_file = st.file_uploader("Upload Dossier or Medical Document (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    lines = scanner.extract_text(uploaded_file, file_ext)
    
    st.info(f"File Ingested: **{uploaded_file.name}** | Extracted Lines: **{len(lines)}**")
    
    results = scanner.scan_content(lines)
    
    # Scorecards
    col1, col2, col3 = st.columns(3)
    col1.metric("Compliance Status", results["status"], delta_color="normal" if results["status"]=="APPROVED" else "inverse")
    col2.metric("Total Compliance Errors", results["total_errors"])
    col3.metric("Authority Agency", results["agency"])
    
    st.divider()

    if results["status"] == "APPROVED":
        st.success("✅ PASSED: Document meets 100% regulatory requirements for " + results["agency"])
        st.balloons()
        
        c1, c2 = st.columns(2)
        with c1:
            pdf_bytes = CertificateGenerator.create_pdf(results["agency"], uploaded_file.name, len(lines))
            st.download_button("📥 Download PDF Compliance Certificate", data=pdf_bytes, file_name=f"Certificate_{selected_code}.pdf", mime="application/pdf")
        with c2:
            zip_bytes = eCTDExporter.create_ectd_zip(uploaded_file.name, "\n".join(lines), selected_code)
            st.download_button("📦 Export FDA/EMA eCTD Package (ZIP)", data=zip_bytes, file_name=f"eCTD_Package_{selected_code}.zip", mime="application/zip")
    else:
        st.error("❌ NON-COMPLIANT DOSSIER: Fix highlighted issues before official submission.")
        
        # AI Auto-Fix Button
        if groq_key:
            if st.button("🤖 Auto-Fix Violations with Groq AI"):
                fixer = RegulatoryAIFixer(api_key=groq_key)
                with st.spinner("AI is rewriting text into compliant phrasing..."):
                    fixed_text = fixer.auto_fix_text("\n".join(lines), results["agency"], results["errors"])
                    st.session_state["doc_text"] = fixed_text
                    st.rerun()

        st.subheader("⚠️ Regulatory Risk Highlights:")
        for idx, err in enumerate(results["errors"], 1):
            if err["line"] > 0:
                st.warning(f"**[{idx}] Line {err['line']} ({err['severity']})**: {err['reason']}")
                st.code(err["text"], language="text")
            else:
                st.error(f"**[{idx}] Global Deficiency ({err['severity']})**: {err['reason']}")

    # Interactive Editor
    st.divider()
    st.subheader("✏️ Live Onscreen Correction & Re-Validation Engine")
    
    doc_content = st.session_state.get("doc_text", "\n".join(lines))
    edited_text = st.text_area("Interactive Document Editor", value=doc_content, height=350)
    
    if st.button("Re-Scan Updated Document"):
        new_lines = [l.strip() for l in edited_text.splitlines() if l.strip()]
        re_results = scanner.scan_content(new_lines)
        
        if re_results["status"] == "APPROVED":
            st.success("🎉 VERIFIED: Document is 100% compliant with " + re_results["agency"])
            st.balloons()
            
            c1, c2 = st.columns(2)
            with c1:
                pdf_bytes = CertificateGenerator.create_pdf(re_results["agency"], uploaded_file.name, len(new_lines))
                st.download_button("📥 Download PDF Compliance Certificate", data=pdf_bytes, file_name=f"Certificate_{selected_code}.pdf", mime="application/pdf")
            with c2:
                zip_bytes = eCTDExporter.create_ectd_zip(uploaded_file.name, edited_text, selected_code)
                st.download_button("📦 Export FDA/EMA eCTD Package (ZIP)", data=zip_bytes, file_name=f"eCTD_Package_{selected_code}.zip", mime="application/zip")
        else:
            st.error(f"Remaining Errors: {re_results['total_errors']}")