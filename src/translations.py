TRANSLATIONS = {
    "EN": {
        "title": "🛡️ ReguAI Global Regulatory Enterprise Platform",
        "subtitle": "AI-Powered Multi-Jurisdiction Dossier Verification, Vector RAG Search, Groq Auto-Fix, & eCTD Exporter",
        "select_authority": "Select Authority",
        "upload_label": "Upload Dossier or Medical Document (.pdf, .docx, .txt)",
        "compliance_status": "Compliance Status",
        "total_errors": "Total Compliance Errors",
        "authority_agency": "Authority Agency",
        "doc_preview": "📄 Document Source Preview",
        "audit_insights": "🔍 Compliance Audit & RAG Citations",
        "auto_fix": "🤖 Auto-Fix Violations with Groq AI",
        "editor_title": "✏️ Live Onscreen Correction Engine",
        "rescan_btn": "Re-Scan Updated Document",
        "history_title": "📊 Private Workspace Audit Log",
        "upgrade_btn": "🚀 Upgrade Plan (Stripe)",
        "pricing_title": "💳 ReguAI SaaS Subscription Plans"
    },
    "AR": {
        "title": "🛡️ منصة ريغواي العالمية للتدقيق التنظيمي والامتثال",
        "subtitle": "التحقق من الملفات الدوائية بالذكاء الاصطناعي، والبحث المتجهي RAG، والتصحيح التلقائي، وتصدير eCTD",
        "select_authority": "اختر هيئة الدواء",
        "upload_label": "تحميل الملف الدوائي أو المستند الطبي (.pdf, .docx, .txt)",
        "compliance_status": "حالة الامتثال",
        "total_errors": "إجمالي المخالفات التنظيمية",
        "authority_agency": "الهيئة التنفيذية",
        "doc_preview": "📄 معاينة النص الأصلي للمستند",
        "audit_insights": "🔍 نتائج التدقيق ومراجع اللوائح",
        "auto_fix": "🤖 تصحيح الأخطاء تلقائياً باستخدام الذكاء الاصطناعي",
        "editor_title": "✏️ محرر التعديل الفوري وإعادة الفحص",
        "rescan_btn": "إعادة فحص النص المعدل",
        "history_title": "📊 سجل تدقيق مساحة العمل الخاصة",
        "upgrade_btn": "🚀 ترقية الاشتراك (Stripe)",
        "pricing_title": "💳 خطط اشتراك منصة ريغواي"
    }
}

def get_text(key: str, lang: str = "EN") -> str:
    return TRANSLATIONS.get(lang, TRANSLATIONS["EN"]).get(key, key)