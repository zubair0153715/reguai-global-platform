import os
import hashlib
import json
from datetime import datetime
from supabase import create_client, Client

# Default Cloud Credentials (Can be overridden via environment variables)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-supabase-url.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-supabase-anon-key")

DATA_FILE = "database/app_users.json"

def _load_local_data():
    os.makedirs("database", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        initial = {
            "users": {
                "admin": {
                    "hash": hashlib.sha256("pharma2026".encode()).hexdigest(),
                    "role": "Admin"
                }
            },
            "audits": {}
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(initial, f, indent=2)
        return initial
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"users": {}, "audits": {}}

def _save_local_data(data):
    os.makedirs("database", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.strip().encode()).hexdigest()

def register_user(username: str, password: str, role: str = "Regulatory Editor") -> tuple[bool, str]:
    username = username.strip().lower()
    password = password.strip()
    
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if not password or len(password) < 4:
        return False, "Password must be at least 4 characters long."

    data = _load_local_data()
    if username in data["users"]:
        return False, f"Username '{username}' already exists."

    data["users"][username] = {
        "hash": hash_password(password),
        "role": role
    }
    _save_local_data(data)
    return True, "Account successfully registered with assigned role!"

def authenticate_user(username: str, password: str) -> tuple[bool, str]:
    username = username.strip().lower()
    password = password.strip()
    
    data = _load_local_data()
    if username in data["users"]:
        user_info = data["users"][username]
        if user_info["hash"] == hash_password(password):
            return True, user_info.get("role", "Regulatory Editor")
    return False, ""

def save_audit_log(username: str, filename: str, jurisdiction: str, status: str, errors_count: int, reviewer_signoff: str = "Pending"):
    username = username.strip().lower()
    data = _load_local_data()
    
    if "audits" not in data:
        data["audits"] = {}
    if username not in data["audits"]:
        data["audits"][username] = []

    entry = {
        "Filename": filename,
        "Jurisdiction": jurisdiction,
        "Status": status,
        "Errors": errors_count,
        "SignoffStatus": reviewer_signoff,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data["audits"][username].insert(0, entry)
    _save_local_data(data)

def get_user_audits(username: str, role: str = "Regulatory Editor"):
    data = _load_local_data()
    audits_dict = data.get("audits", {})
    
    # QA Reviewers & Admins can view all organization audits
    if role in ["Admin", "QA Reviewer"]:
        all_logs = []
        for user_key, logs in audits_dict.items():
            for log in logs:
                item = log.copy()
                item["User"] = user_key.upper()
                all_logs.append(item)
        return all_logs
    
    # Standard Regulatory Editors see only their own private audits
    return audits_dict.get(username.strip().lower(), [])