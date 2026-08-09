import streamlit as st
import os
from src.strict_scanner import StrictDocumentScanner
from src.certificate_generator import CertificateGenerator
from src.ai_fixer import RegulatoryAIFixer
from src.ectd_exporter import eCTDExporter
from src.rag_engine import RegulatoryRAGEngine
from database.supabase_db import register_user, authenticate_user, save_audit_log, get_user_audits

st.set_page_config(page_title="ReguAI - Global Regulatory Enterprise Suite", page_icon="🛡️", layout="wide")

# State Management
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None

# --- AUTHENTICATION PORTAL ---
if not st.session_state["authenticated"]:
    st.markdown("<h1 style='text-align: center; color: #38BDF8;'>🛡️ ReguAI Enterprise Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94A3B8;'>AI-Powered Dossier Validator with RBAC & Supabase Cloud Security</p>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        tab_login, tab_signup = st.tabs(["🔑 Enterprise Login", "📝 Register Account"])
        
        with tab_login:
            st.subheader("Workspace Access")
            l_user = st.text_input("Username", key="l_user", placeholder="e.g. admin")
            l_pass = st.text_input("Password", type="password", key="l_pass", placeholder="••••••••")
            
            if st.button("Log In to Dashboard", type="primary", use_container_width=True):
                is_valid, user_role = authenticate_user(l_user, l_pass)
                if is_valid:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = l_user.strip().lower()
                    st.session_state["role"] = user_role
                    st.success(f"✅ Welcome back! Logged in as [{user_role}]")
                    st.rerun()
                else:
                    st.error("❌ Invalid Username or Password.")
            
            st.caption("Default Demo Credentials: `admin` | Password: `pharma2026`")

        with tab_signup:
            st.subheader("Create Enterprise Account")
            s_user = st.text_input("Desired Username", key="s_user")
            s_pass = st.text_input("Desired Password", type="password", key="s_pass")
            s_confirm = st.text_input("Confirm Password", type="password", key="s_confirm")
            s_role = st.selectbox("Select Enterprise Role", ["Regulatory Editor", "QA Reviewer", "Admin"])
            
            if st.button("Register Account", use_container_width=True):
                if s_pass != s_confirm:
                    st.error("❌ Passwords do not match!")
                else:
                    success, msg = register_user(s_user, s_pass, s_role)
                    if success:
                        st.success("🎉 Account created! Logging in...")
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = s_user.strip().lower()
                        st.session_state["role"] = s_role
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

    st.stop()

# --- MAIN DASHBOARD (AUTHENTICATED & ROLE-AWARE) ---
rag = RegulatoryRAGEngine()
rag.seed_baseline_knowledge()

current_user = st.session_state['username']
current_role = st.session_state['role']

# Sidebar Controls & RBAC Indicator
st.sidebar.markdown(f"👤 User: **{current_user.upper()}**")
st.sidebar.info(f"🛡️ Active Role: **{current_role}**")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["role"] = None
    st.session_state.pop("doc_text", None)
    st.rerun()

st.sidebar.divider()
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

groq_key = st.sidebar.text_input("Groq API Key (For AI Auto-Fixer)", type="password")

# Main Header
st.title("🛡️ ReguAI Global Regulatory Enterprise Platform")
st.markdown(f"AI-Powered Dossier Verification | RAG Citations | Role: **{current_role}**")

# File Upload
uploaded_file = st.file_uploader("Upload Dossier or Medical Document (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    lines = scanner.extract_text(uploaded_file, file_ext)
    
    st.info(f"File Ingested: **{uploaded_file.name}** | Extracted Lines: **{len(lines)}**")
    
    results = scanner.scan_content(lines)
    
    # Save Audit Log with Signoff Status
    signoff = "APPROVED BY QA" if (results["status"] == "APPROVED" and current_role in ["QA Reviewer", "Admin"]) else "Pending Review"
    save_audit_log(current_user, uploaded_file.name, selected_code, results["status"], results["total_errors"], signoff)
    
    # Scorecards
    col1, col2, col3 = st.columns(3)
    col1.metric("Compliance Status", results["status"], delta_color="normal" if results["status"]=="APPROVED" else "inverse")
    col2.metric("Total Compliance Errors", results["total_errors"])
    col3.metric("Authority Agency", results["agency"])
    
    st.divider()

    # Split Screen
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("📄 Document Source Preview")
        st.text_area("Source Content View", value="\n".join(lines[:50]), height=400, disabled=True)

    with col_right:
        st.subheader("🔍 Compliance Audit & RAG Guideline Match")
        
        rag_context = rag.query_context("\n".join(lines[:5]))
        if rag_context:
            st.warning(f"📜 **Official Citation Match:** {rag_context[0]}")

        if results["status"] == "APPROVED":
            st.success("✅ PASSED: Document meets 100% regulatory requirements for " + results["agency"])
            st.balloons()
            
            c1, c2 = st.columns(2)
            with c1:
                pdf_bytes = CertificateGenerator.create_pdf(results["agency"], uploaded_file.name, len(lines))
                st.download_button("📥 PDF Compliance Certificate", data=pdf_bytes, file_name=f"Certificate_{selected_code}.pdf", mime="application/pdf")
            with c2:
                zip_bytes = eCTDExporter.create_ectd_zip(uploaded_file.name, "\n".join(lines), selected_code)
                st.download_button("📦 Export eCTD Package (ZIP)", data=zip_bytes, file_name=f"eCTD_Package_{selected_code}.zip", mime="application/zip")
        else:
            st.error("❌ NON-COMPLIANT DOSSIER")
            
            # RBAC Enforcement: Regulatory Editor & Admin can trigger AI Auto-Fix
            if current_role in ["Regulatory Editor", "Admin"]:
                if groq_key and st.button("🤖 Auto-Fix Violations with Groq AI"):
                    fixer = RegulatoryAIFixer(api_key=groq_key)
                    with st.spinner("AI is rewriting text into compliant phrasing..."):
                        fixed_text = fixer.auto_fix_text("\n".join(lines), results["agency"], results["errors"])
                        st.session_state["doc_text"] = fixed_text
                        st.rerun()

            for idx, err in enumerate(results["errors"], 1):
                if err["line"] > 0:
                    st.warning(f"**[{idx}] Line {err['line']} ({err['severity']})**: {err['reason']}")
                    st.code(err["text"], language="text")
                else:
                    st.error(f"**[{idx}] Global Deficiency ({err['severity']})**: {err['reason']}")

    # Interactive Editor (RBAC Protected)
    st.divider()
    if current_role in ["Regulatory Editor", "Admin"]:
        st.subheader("✏️ Live Onscreen Correction & Re-Validation Engine")
        doc_content = st.session_state.get("doc_text", "\n".join(lines))
        edited_text = st.text_area("Interactive Document Editor", value=doc_content, height=300)
        
        if st.button("Re-Scan Updated Document"):
            new_lines = [l.strip() for l in edited_text.splitlines() if l.strip()]
            re_results = scanner.scan_content(new_lines)
            
            if re_results["status"] == "APPROVED":
                st.success("🎉 VERIFIED: Document is 100% compliant with " + re_results["agency"])
                st.balloons()
            else:
                st.error(f"Remaining Errors: {re_results['total_errors']}")
    else:
        st.info("🔒 **QA Reviewer View Mode:** Document editing disabled for Reviewer role.")

# --- RBAC AUDIT TRAIL LOGS ---
user_history = get_user_audits(current_user, current_role)
if user_history:
    st.divider()
    st.subheader(f"📊 Enterprise Audit History ({'All Organization Audits' if current_role in ['Admin', 'QA Reviewer'] else 'Your Private Logs'})")
    st.dataframe(user_history, use_container_width=True)