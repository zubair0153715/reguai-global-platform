# 🛡️ ReguAI - Enterprise Global Regulatory Compliance Suite

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://reguai-global-platform-n4dvpwbpluphd9wnjwneue.streamlit.app/)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Regulatory Support](https://img.shields.io/badge/Jurisdictions-FDA%20%7C%20EMA%20%7C%20SFDA%20%7C%20MOHAP%20%7C%20DRAP-purple.svg)]()

> **Automated Multi-Jurisdiction Pharmaceutical Dossier Verification, Groq Llama-3 AI Auto-Fixer, and eCTD Package Exporter.**

**ReguAI** is an AI-powered regulatory technology (RegTech) platform designed for pharmaceutical manufacturers, regulatory affairs specialists, and clinical research organizations (CROs). It automates the verification of regulatory compliance dossiers (IND, NDA, 510(k), SmPC, and Labeling Leaflets) against statutory guidelines established by global regulatory authorities.

---

## 🚀 Live Demo

Access the active cloud deployment:  
👉 **[ReguAI Live Production Dashboard](https://reguai-global-platform-n4dvpwbpluphd9wnjwneue.streamlit.app/)**

---

## ✨ Key Features

- **🌐 Multi-Jurisdiction Regulatory Engine:**
  - 🇺🇸 **US FDA:** 21 CFR 312, eCTD Module 1, ISO 14971 Risk Management, CMC Batch Analysis.
  - 🇪🇺 **EU EMA:** Qualified Person (QP) Release, SmPC, EudraVigilance Safety Parameters.
  - 🇸🇦 **Saudi SFDA:** SFDA eCTD, Saudi Track & Trace (3DTron), Arabic PIL, Zone IVb Stability.
  - 🇦🇪 **UAE MOHAP / EDE:** Marketing Authorization, GCC Common Technical Document, Bilingual Packaging.
  - 🇵🇰 **Pakistan DRAP:** Form 5 Registration, GMP Certification, Zone IVb Stability Guidelines.

- **📄 Universal Document Ingestion & Parser:**
  - Native line-by-line deterministic extraction for **PDF**, **Microsoft Word (.docx)**, and **Plain Text (.txt)** formats.
  - OCR fallback integration for physical scanned clinical documents and lab certificates.

- **🤖 AI-Powered Compliance Auto-Fixer:**
  - Integrated with **Groq Llama-3 (70B)** API to automatically rewrite non-compliant sentences, remove forbidden phrasing (e.g., *"guaranteed cure"*, *"100% safe"*), and insert mandatory statutory modules.

- **📥 Automated Output Generation:**
  - **Official PDF Compliance Certificate:** Instant PDF report generation powered by ReportLab.
  - **eCTD Module 1-5 Package Exporter:** One-click ZIP exporter compiling ICH eCTD directory hierarchy and `index.xml` manifest files.

---

## 🛠️ Architecture & Tech Stack

- **Frontend & Interface:** Streamlit Engine
- **LLM / AI Orchestration:** Groq API (`llama-3.3-70b-versatile`)
- **Document Extractors:** `pypdf`, `python-docx`, `pytesseract`, `pdf2image`
- **PDF Engine:** `reportlab`
- **Rule Engine Structure:** Modular JSON Database (`database/*.json`)

---

## 💻 Local Installation & Setup

### Prerequisites
- Python 3.10+
- Git

### 1. Clone the Repository
```bash
git clone [https://github.com/zubair0153715/reguai-global-platform.git](https://github.com/zubair0153715/reguai-global-platform.git)
cd reguai-global-platform