import streamlit as st
import os
from src.strict_scanner import StrictDocumentScanner
from src.certificate_generator import CertificateGenerator
from src.ai_fixer import RegulatoryAIFixer
from src.ectd_exporter import eCTDExporter
from src.rag_engine import RegulatoryRAGEngine
from src.translations import get_text
from database.supabase_db import register_user, authenticate_user, save_audit_log, get_user_audits
from database.stripe_manager import StripeSubscriptionManager

st.set_page_config(
    page_title="ReguAI - Global Regulatory Enterprise Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Variables
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None
if "tier" not in st.session_state:
    st.session_state["tier"] = "Free"
if "lang" not in st.session_state:
    st.session_state["lang"] = "EN"
if "scan_count" not in st.session_state:
    st.session_state["scan_count"] = 0

lang = st.session_state["lang"]

# Apply Custom CSS for RTL (Arabic) & Interface Lockdown
if lang == "AR":
    st.markdown("""
        <style>
        body, .stApp { direction: rtl; text-align: right; }
        .stMarkdown, .stText, p, h1, h2, h3 { text-align: right !important; }
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} .stDeployButton {display:none;}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} .stDeployButton {display:none;}
        </style>
    """, unsafe_allow_html=True)

# Custom Highlighting CSS
st.markdown("""
    <style>
    .error-highlight { background-color: rgba(239, 68, 68, 0.2); border-left: 4px solid #EF4444; padding: 8px; margin-bottom: 6px; border-radius: 4px; }
    .warning-highlight { background-color: rgba(245, 158, 11, 0.2); border-left: 4px solid #F59E0B; padding: 8px; margin-bottom: 6px; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- SECURE AUTHENTICATION PORTAL ---
if not st.session_state["authenticated"]:
    col_lang1, col_lang2 = st.columns([8, 2])
    with col_lang2:
        st.session_state["lang"] = st.selectbox("🌐 Language / اللغة", ["EN", "AR"], index=0 if lang=="EN" else 1)

    st.markdown("<h1 style='text-align: center; color: #38BDF8;'>🛡️ ReguAI Enterprise Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94A3B8;'>AI-Powered Multi-Jurisdiction Dossier Validator & Auto-Fixer</p>", unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        tab_login, tab_signup = st.tabs(["🔑 Member Login", "📝 Create Workspace"])
        
        with tab_login:
            st.subheader("Login to Enterprise Workspace")
            l_user = st.text_input("Username", key="l_user", placeholder="admin")
            l_pass = st.text_input("Password", type="password", key="l_pass", placeholder="••••••••")
            
            if st.button("Log In to Dashboard", type="primary", use_container_width=True):
                is_valid, user_role = authenticate_user(l_user, l_pass)
                if is_valid:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = l_user.strip().lower()
                    st.session_state["role"] = user_role
                    st.session_state["tier"] = "Enterprise" if user_role == "Admin" else "Free"
                    st.success("✅ Secure Connection Established!")
                    st.rerun()
                else:
                    st.error("❌ Invalid Username or Password.")
            st.caption("Default Demo: `admin` / `pharma2026`")

        with tab_signup:
            st.subheader("Register New Account")
            s_user = st.text_input("Desired Username", key="s_user")
            s_pass = st.text_input("Desired Password", type="password", key="s_pass")
            s_confirm = st.text_input("Confirm Password", type="password", key="s_confirm")
            s_role = st.selectbox("Account Scope", ["Regulatory Editor", "QA Reviewer"])
            
            if st.button("Create SaaS Workspace", use_container_width=True):
                if s_pass != s_confirm:
                    st.error("❌ Passwords do not match!")
                else:
                    success, msg = register_user(s_user, s_pass, s_role)
                    if success:
                        st.success("🎉 Account Created Successfully!")
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = s_user.strip().lower()
                        st.session_state["role"] = s_role
                        st.session_state["tier"] = "Free"
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

    st.stop()

# --- MAIN DASHBOARD (AUTHENTICATED) ---
rag = RegulatoryRAGEngine()
rag.seed_baseline_knowledge()

current_user = st.session_state['username']
current_role = st.session_state['role']
current_tier = st.session_state['tier']
tier_limits = StripeSubscriptionManager.get_tier_features(current_tier)

# Sidebar & Controls
st.sidebar.markdown(f"👤 Account: **{current_user.upper()}**")
st.sidebar.info(f"🛡️ Role: **{current_role}** | Plan: **[{current_tier}]**")

st.session_state["lang"] = st.sidebar.selectbox("🌐 UI Language", ["EN", "AR"], index=0 if lang=="EN" else 1)

if current_tier == "Free":
    st.sidebar.warning(f"⚡ Free Scans: {st.session_state['scan_count']}/3")
    if st.sidebar.button(get_text("upgrade_btn", lang)):
        st.session_state["show_pricing"] = True

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.rerun()

st.sidebar.divider()
st.sidebar.title(get_text("select_authority", lang))

country_options = {
    "US_FDA": "🇺🇸 US FDA (United States)",
    "EU_EMA": "🇪🇺 EU EMA (European Union)",
    "SA_SFDA": "🇸🇦 SFDA (Saudi Arabia)",
    "UAE_MOHAP": "🇦🇪 MOHAP (United Arab Emirates)",
    "PK_DRAP": "🇵🇰 DRAP (Pakistan)"
}

selected_code = st.sidebar.selectbox("Authority Agency", list(country_options.keys()), format_func=lambda x: country_options[x])
scanner = StrictDocumentScanner(selected_code)
st.sidebar.success(f"Active Engine: **{scanner.rules['agency']}**")

groq_key = st.sidebar.text_input("Groq API Key (For AI Auto-Fixer)", type="password", disabled=(not tier_limits["ai_autofix"]))

# --- PRICING & STRIPE MONETIZATION VIEW ---
if st.session_state.get("show_pricing", False):
    st.title(get_text("pricing_title", lang))
    
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("### Free Plan\n**$0 / mo**\n- 3 Document Scans / Month\n- Basic Validation Engine\n- PDF Compliance Certificate")
        st.button("Current Tier", disabled=True)
    with p2:
        st.markdown("### Pro Plan 🌟\n**$99 / mo**\n- **Unlimited** Document Scans\n- **Groq Llama-3 AI Auto-Fixer**\n- PDF Compliance Certificate\n- RAG Vector Citations")
        if st.button("Upgrade to Pro", type="primary"):
            st.session_state["tier"] = "Pro"
            st.session_state["show_pricing"] = False
            st.rerun()
    with p3:
        st.markdown("### Enterprise Plan 🏢\n**$499 / mo**\n- Everything in Pro\n- **eCTD Package Export (ZIP)**\n- **FastAPI Endpoints Access**\n- Multi-User Organization Audits")
        if st.button("Upgrade to Enterprise"):
            st.session_state["tier"] = "Enterprise"
            st.session_state["show_pricing"] = False
            st.rerun()
            
    if st.button("← Return to Workspace"):
        st.session_state["show_pricing"] = False
        st.rerun()
    st.stop()

# --- MAIN DASHBOARD BODY ---
st.title(get_text("title", lang))
st.markdown(get_text("subtitle", lang))

uploaded_file = st.file_uploader(get_text("upload_label", lang), type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    if current_tier == "Free" and st.session_state["scan_count"] >= 3:
        st.error("❌ Free Scan Limit Reached (3/3 Used). Upgrade to Pro or Enterprise for unlimited access.")
        st.stop()

    file_ext = uploaded_file.name.split(".")[-1].lower()
    lines = scanner.extract_text(uploaded_file, file_ext)
    
    st.session_state["scan_count"] += 1
    st.info(f"File Ingested: **{uploaded_file.name}** | Extracted Lines: **{len(lines)}**")
    
    results = scanner.scan_content(lines)
    
    signoff = "APPROVED BY QA" if (results["status"] == "APPROVED" and current_role in ["QA Reviewer", "Admin"]) else "Pending Review"
    save_audit_log(current_user, uploaded_file.name, selected_code, results["status"], results["total_errors"], signoff)
    
    # Scorecards
    col1, col2, col3 = st.columns(3)
    col1.metric(get_text("compliance_status", lang), results["status"], delta_color="normal" if results["status"]=="APPROVED" else "inverse")
    col2.metric(get_text("total_errors", lang), results["total_errors"])
    col3.metric(get_text("authority_agency", lang), results["agency"])
    
    st.divider()

    # Split Screen: In-Browser Document Annotator & Audit Engine
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader(get_text("doc_preview", lang))
        
        # In-Browser Annotated Document View
        st.caption("🔍 **Annotated Inspection (Non-compliant lines highlighted):**")
        error_lines_map = {err["line"]: err["reason"] for err in results["errors"] if err["line"] > 0}
        
        annotated_html = "<div style='height: 400px; overflow-y: scroll; border: 1px solid #334155; padding: 10px; border-radius: 8px; background-color: #0F172A;'>"
        for idx, line in enumerate(lines[:100], 1):
            if idx in error_lines_map:
                annotated_html += f"<div class='error-highlight'><strong>[Line {idx}] ⚠️ {line}</strong><br><small style='color: #F87171;'>Violation: {error_lines_map[idx]}</small></div>"
            else:
                annotated_html += f"<div style='padding: 2px 0; color: #CBD5E1;'><small style='color: #64748B;'>[{idx}]</small> {line}</div>"
        annotated_html += "</div>"
        
        st.markdown(annotated_html, unsafe_allow_html=True)

    with col_right:
        st.subheader(get_text("audit_insights", lang))
        
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
                if tier_limits["ectd_export"]:
                    zip_bytes = eCTDExporter.create_ectd_zip(uploaded_file.name, "\n".join(lines), selected_code)
                    st.download_button("📦 Export eCTD Package (ZIP)", data=zip_bytes, file_name=f"eCTD_Package_{selected_code}.zip", mime="application/zip")
                else:
                    st.info("🔒 eCTD Export requires Enterprise Plan.")
        else:
            st.error("❌ NON-COMPLIANT DOSSIER")
            
            if tier_limits["ai_autofix"] and current_role in ["Regulatory Editor", "Admin"]:
                if groq_key and st.button(get_text("auto_fix", lang)):
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

    # Onscreen Editor
    st.divider()
    if current_role in ["Regulatory Editor", "Admin"]:
        st.subheader(get_text("editor_title", lang))
        doc_content = st.session_state.get("doc_text", "\n".join(lines))
        edited_text = st.text_area("Interactive Document Editor", value=doc_content, height=250)
        
        if st.button(get_text("rescan_btn", lang)):
            new_lines = [l.strip() for l in edited_text.splitlines() if l.strip()]
            re_results = scanner.scan_content(new_lines)
            
            if re_results["status"] == "APPROVED":
                st.success("🎉 VERIFIED: Document is 100% compliant with " + re_results["agency"])
                st.balloons()
            else:
                st.error(f"Remaining Errors: {re_results['total_errors']}")

# Enterprise Audit History Log
user_history = get_user_audits(current_user, current_role)
if user_history:
    st.divider()
    st.subheader(get_text("history_title", lang))
    st.dataframe(user_history, use_container_width=True)